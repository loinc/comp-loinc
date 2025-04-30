"""All things dealing with taxonomies based on NLP approaches."""
import io
import json
import os
import pickle
import typing as t
from argparse import ArgumentParser
from datetime import date, datetime
from pathlib import Path

import jinja2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# noinspection PyProtectedMember
from sssom.parsers import _read_pandas_and_metadata, from_sssom_dataframe
from sssom.util import MappingSetDataFrame
from sssom.writers import write_table

from loinclib import Configuration

THIS_FILE_PATH = Path(os.path.abspath(__file__))
LOINCLIB_DIR = THIS_FILE_PATH.parent
SRC_DIR = LOINCLIB_DIR.parent
PROJECT_DIR = SRC_DIR.parent
# PROJECT_DIR = os.getcwd()
DANGLING_ANALYSIS_DIR = PROJECT_DIR / 'output/analysis/dangling'
DANGLING_CACHE_DIR = DANGLING_ANALYSIS_DIR / 'cache'
# todo: ideally not hard code. Best to solve via OO, i'm not sure
INPATH_DANGLING = DANGLING_ANALYSIS_DIR / 'dangling.tsv'
OUT_FILENAME = 'nlp-matches.sssom.tsv'
PROPERTY_ANALYSIS_OUTPATH = DANGLING_ANALYSIS_DIR / OUT_FILENAME.replace('.tsv', '_prop_analysis.tsv')
OUTPATH_HIST = DANGLING_ANALYSIS_DIR / 'confidence_histogram.png'
# todo: get this from config using standard pattern in codebase
# note: as of 2025/01/22 there are 62 Document terms in IN_PARTS_ALL not in IN_PARTS_CSV1 or IN_PARTS_CSV2
DEFAULT_CONFIG_PATH = PROJECT_DIR / 'comploinc_config.yaml'
CONFIG = Configuration(Path(os.path.dirname(str(DEFAULT_CONFIG_PATH))), Path(os.path.basename(DEFAULT_CONFIG_PATH)))
OUTDIR_CURATION = CONFIG.get_curation_dir_path()
OUTPATH = Path(OUTDIR_CURATION) / OUT_FILENAME
LOINC_RELEASE_DIR = CONFIG.get_loinc_release_path()
IN_PARTS_ALL = LOINC_RELEASE_DIR / 'AccessoryFiles' / 'PartFile' / 'Part.csv'
IN_PARTS_CSV1 = LOINC_RELEASE_DIR / 'AccessoryFiles' / 'PartFile' / 'LoincPartLink_Supplementary.csv'
IN_PARTS_CSV2 = LOINC_RELEASE_DIR / 'AccessoryFiles' / 'PartFile' / 'LoincPartLink_Primary.csv'
OUTPATH_STATS_DOCS = PROJECT_DIR / 'documentation' / 'stats-dangling.md'
PK = ['subject_id', 'object_id', 'subject_dangling', 'object_dangling']


# Inputs --------------------------------------------------------------------------------------------------------------
def parts_to_tsv(parts: t.List, outpath: Path = INPATH_DANGLING):
    """Save list of Part objects to TSV."""
    outdir = Path(os.path.dirname(outpath))
    if not outdir.exists():
        outdir.mkdir(parents=True)
    df = pd.DataFrame([{
        'PartNumber': p.part_number,
        'PartDisplayName': p.part_display,
        'PartTypeName': p.part_type,
        'is_search': p.is_search,
    } for p in parts])
    df.to_csv(outpath, sep='\t', index=False)


# Utils ---------------------------------------------------------------------------------------------------------------
def _get_display_id_map(df, label_field=['PartName', 'PartDisplayName'][0]) -> t.Dict[str, t.List[str]]:
    """Get map of all display names to part numbers. There are some duplciate display name values."""
    display_to_ids = df.groupby(label_field)['PartNumber'].unique().to_dict()
    return {name: list(parts) for name, parts in display_to_ids.items()}


# Semantic matching ----------------------------------------------------------------------------------------------------
def _get_embeddings(text_list: t.List[str], cache_name: str, use_cache=True):
    """Get embeddings for a list of strings."""
    from sentence_transformers import SentenceTransformer

    # Try to load from cache first
    cache_file = f"embeddings_{cache_name}.pkl"
    cache_path = DANGLING_CACHE_DIR / cache_file
    if os.path.exists(cache_path) and use_cache:
        # print(f"Loading embeddings from cache: {cache_file}")
        with open(cache_path, 'rb') as f:
            return pickle.load(f)

    # If not in cache, generate embeddings
    print(f"Generating new embeddings ({cache_name}) for {len(text_list)} items...")
    t0 = datetime.now()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings: np.ndarray = model.encode(text_list)
    print(f"- completed in {datetime.now() - t0}")

    # Save to cache
    if not os.path.exists(DANGLING_CACHE_DIR):
        os.makedirs(DANGLING_CACHE_DIR)
    with open(cache_path, 'wb') as f:
        # noinspection PyTypeChecker false_positive
        pickle.dump(embeddings, f)
    return embeddings


# noinspection DuplicatedCode
def _update_curation_file__big_conf_diff_warn(new_df: pd.DataFrame, outpath: t.Union[Path, str] = OUTPATH):
    """Update curation file with new data while preserving curated records and tracking significant changes.

    But also:
    For a given record, if the similarity_score has significantly changed (which means that the confidence has changed
    by a relative + or - 20% between the two values; e.g. a 70% score in old_df changing to 84% in new_df would be 20%
    since 84/70 = 1.2), add a warnings column if it does not exist. Else, update what was there for that record in the
    old_df. the warnings column should be JSON. You should read that JSON and look for a key
    similarity_score_threshold_change, which contains an array. append some data to that array. if there is nothing
    there, you can insert some new json. The entry to add to the array is an object with the following keys:
    old_confidence, new_confidence, old_mapping_set_id, new_mapping_set_id, old_publication_date, new_publication_date}
    """
    # Incorporate curated data with new data
    with open(outpath, "r") as file:
        file_content = file.read()
    stream = io.StringIO(file_content)
    old_df, metadata = _read_pandas_and_metadata(stream, "\t")
    publication_date_old = metadata.get('publication_date', '')
    publication_date_old = publication_date_old.strftime('%Y-%m-%d') if \
        isinstance(publication_date_old, datetime) or isinstance(publication_date_old, date) \
        else publication_date_old
    publication_date_new = datetime.now().strftime('%Y-%m-%d')
    old_df = old_df.fillna('')

    # Create efficient merge key for lookups
    old_df['merge_key'] = old_df[PK].astype(str).agg('_'.join, axis=1)
    new_df['merge_key'] = new_df[PK].astype(str).agg('_'.join, axis=1)

    # Create dictionaries for fast lookups
    old_records = {row['merge_key']: row for _, row in old_df.iterrows()}
    new_records = {row['merge_key']: row for _, row in new_df.iterrows()}

    # Prepare result dataframe with proper columns
    all_columns = list(old_df.columns)
    if 'warnings' not in all_columns:
        all_columns.append('warnings')
    result_data = []

    # Process all old records
    for key, old_row in old_records.items():
        row_data = old_row.copy()

        # Set default warnings if not present
        if 'warnings' not in row_data or pd.isna(row_data['warnings']) or row_data['warnings'] == '':
            row_data['warnings'] = ''

        # Check if this record also exists in new data
        # TODO temp. though should order be flipped if bool cols flip?
        a1 = new_df = new_df[(new_df['subject_id'] == 'https://loinc.org/LP434027-1')
            & (new_df['object_id'] == 'https://loinc.org/LP34631-9')]  # 1
        if key in new_records:
            new_row = new_records[key]

            # Check for significant similarity score change
            old_score = float(old_row['similarity_score']) if old_row['similarity_score'] != '' else 0
            new_score = float(new_row['similarity_score']) if new_row['similarity_score'] != '' else 0

            if old_score > 0 and abs(new_score / old_score - 1) >= 0.2:
                # Handle warnings for significant change
                warnings_str = row_data['warnings']
                if warnings_str and warnings_str.strip():
                    try:
                        warnings_dict = json.loads(warnings_str)
                    except json.JSONDecodeError:
                        warnings_dict = {}
                else:
                    warnings_dict = {}

                if 'similarity_score_threshold_change' not in warnings_dict:
                    warnings_dict['similarity_score_threshold_change'] = []

                warnings_dict['similarity_score_threshold_change'].append({
                    "old_confidence": str(old_score),
                    "new_confidence": str(new_score),
                    "old_mapping_set_id": metadata['mapping_set_id'],
                    "old_publication_date": publication_date_old,
                    "new_publication_date": publication_date_new,
                })

                row_data['warnings'] = json.dumps(warnings_dict)

            # Update other fields from new data
            for col in new_df.columns:
                if col not in PK and col != 'warnings' and col != 'merge_key':
                    row_data[col] = new_row[col]

            # Mark this record as processed
            new_records.pop(key)

        result_data.append(row_data)

    # Add remaining new records
    for key, new_row in new_records.items():
        row_data = new_row.copy()
        if 'warnings' not in row_data or pd.isna(row_data['warnings']):
            row_data['warnings'] = ''
        result_data.append(row_data)

    # Convert to DataFrame and drop the temporary merge key
    result_df = pd.DataFrame(result_data)
    result_df = result_df.drop(columns=['merge_key'])

    # TODO temp
    a2 = result_df[result_df['warnings'] != '']
    a3 = result_df.sort_values(
        ['similarity_score', 'subject_id', 'object_id'], ascending=[False, True, True])
    a3 = a3[a3['object_id'] != '']

    # todo: why sub/obj dang keys swapped? https://loinc.org/LP434027-1 , https://loinc.org/LP34631-9
    a4 = result_df[(result_df['subject_id'] == 'https://loinc.org/LP434027-1') &
        (result_df['object_id'] == 'https://loinc.org/LP34631-9')]
    a4['sub_lab_len'] = a4['subject_id'].str.len()
    a4['obj_lab_len'] = a4['object_id'].str.len()

    keyz = ['https://loinc.org/LP34631-9', 'https://loinc.org/LP434027-1']
    a5 = result_df[(result_df['subject_id'].isin(keyz)) & (result_df['object_id'].isin(keyz))]

    # todo find all (21,900 / 45,845)
    dupes = result_df.copy()
    dupes['subject_id'] = dupes['subject_id'].str.replace('https://loinc.org/', '')
    dupes['object_id'] = dupes['object_id'].str.replace('https://loinc.org/', '')
    dupes = result_df[result_df.duplicated(subset=['subject_id', 'object_id'], keep=False)]
    dupes['sub_lab_len'] = dupes['subject_id'].str.len()
    dupes['obj_lab_len'] = dupes['object_id'].str.len()
    del dupes['predicate_id']
    del dupes['PartTypeName']
    del dupes['mapping_justification']
    del dupes['warnings']
    del dupes['curator_approved']

    _save_sssom(result_df, outpath)


# noinspection DuplicatedCode
def semantic_similarity_update_curation_file(
    new_df: pd.DataFrame, outpath: t.Union[Path, str] = OUTPATH, warn_big_conf_diff=True, overwrite=False
):
    """Update curation file with new data while preserving existing records.

    If warn_big_conf_diff=True, routes to _update_curation_file__big_conf_diff_warn() instead.

    This simplified version:
    1. Keeps all records from old_df
    2. Adds new records from new_df
    3. Updates existing records with new data
    """
    # Save & return if this is the first time creating this file
    if not os.path.exists(outpath) or overwrite:
        _save_sssom(new_df, outpath)
        return

    # Else, incorporate curated data with new data
    if warn_big_conf_diff:
        return _update_curation_file__big_conf_diff_warn(new_df, outpath)

    old_df = pd.read_csv(outpath, sep='\t', comment='#').fillna('')

    # Create efficient merge key for lookups
    old_df['merge_key'] = old_df[PK].astype(str).agg('_'.join, axis=1)
    new_df['merge_key'] = new_df[PK].astype(str).agg('_'.join, axis=1)

    # Create dictionaries for fast lookups
    old_records = {row['merge_key']: row for _, row in old_df.iterrows()}
    new_records = {row['merge_key']: row for _, row in new_df.iterrows()}

    # Process all old records
    result_data = []
    for key, old_row in old_records.items():
        row_data = old_row.copy()

        # Check if this record also exists in new data
        if key in new_records:
            new_row = new_records[key]

            # Update fields from new data
            for col in new_df.columns:
                if col not in ['merge_key']:
                    row_data[col] = new_row[col]

            # Mark this record as processed
            new_records.pop(key)

        result_data.append(row_data)

    # Add remaining new records
    for key, new_row in new_records.items():
        result_data.append(new_row)

    # Convert to DataFrame and drop the temporary merge key
    result_df = pd.DataFrame(result_data)
    result_df = result_df.drop(columns=['merge_key'])

    _save_sssom(result_df, outpath)


def _find_best_matches(
    terms_dangling: t.List[str], terms_hier: t.List[str], part_type: str,
    label_field=['PartName', 'PartDisplayName'][0], use_cache=False, batch_size=30_000
) -> pd.DataFrame:
    """Find best matches between two sets of strings using embeddings.

    FYI: Introduced batch size for fear of high memory usage. But not an issue, especially when splitting by part_type.
    batch_size 30k is about equal to the total number of dangling terms. This could become useful if we start to match
    terms against each other even when they have not been classified as in the same part_type.
    """
    from sklearn.metrics.pairwise import cosine_similarity

    if not terms_hier:
        return pd.DataFrame([{
            f'{label_field}_dangling': term,
            f'{label_field}_hierarchical': None,
            'confidence': 0
        } for term in terms_dangling])

    # Embed hierarchical terms
    embeds_hier = _get_embeddings(terms_hier, f'{part_type}_hierarchical', use_cache)

    # Process matches in chunks
    best_matches = []
    for i in range(0, len(terms_dangling), batch_size):
        terms_dangling_i = terms_dangling[i:i + batch_size]
        embeds_dangling_i = _get_embeddings(terms_dangling_i, f'{part_type}_dangling_{i}', use_cache)
        # - Calculate all similarities
        similarities_i = cosine_similarity(embeds_dangling_i, embeds_hier)
        # - Find best matches
        for j, term in enumerate(terms_dangling_i):
            best_match_idx = np.argmax(similarities_i[j])
            confidence = similarities_i[j][best_match_idx]
            best_matches.append({
                f'{label_field}_dangling': term,
                f'{label_field}_hierarchical': terms_hier[best_match_idx],
                'confidence': confidence
            })
    return pd.DataFrame(best_matches)


def _save_sssom(
    df: pd.DataFrame, outpath: t.Union[Path, str] = OUTPATH
):
    """Save matches to SSSOM

    todo: consider saving the metadata as a separate yaml file
    """
    # Fix mapping precision
    #  Otheriwse, some show up with precision >1. Digits >5 causes issue.
    #  Can't do this with SSSOM, so convert col: matches_df.to_csv(outpath, sep='\t', index=False, float_format='%.5f')
    df['similarity_score'] = pd.to_numeric(df['similarity_score'], errors='coerce')
    df['similarity_score'] = df['similarity_score'].round(5).astype(str)
    if 'curator_approved' not in df.columns:
        df['curator_approved'] = ''

    # Set metadata
    msdf: MappingSetDataFrame = from_sssom_dataframe(df, prefix_map={
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'COMPLOINC_PROP': 'https://comploinc-props#',
    }, meta={
        'mapping_tool': 'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2',
        # todo: Getting dynamically would be great, but not easy. This version number was true by looking at poetry.lock
        #  on 2025/02/22, but won't always be true.
        'mapping_tool_version': '3.4.1',
        'similarity_measure': 'https://www.wikidata.org/wiki/Q1784941',
        'publication_date': datetime.now().strftime('%Y-%m-%d'),  # custom field
        'extension_definitions': [  # https://mapping-commons.github.io/sssom/spec-model/#non-standard-slots
            {
                'slot_name': 'publication_date',
                'property': 'COMPLOINC_PROP:publication_date',
                # 'type_hint': 'xsd:date',  # http://www.w3.org/2001/XMLSchema#date
                'type_hint': 'http://www.w3.org/2001/XMLSchema#date',
            },
            {
                'slot_name': 'PartTypeName',
                'property': 'COMPLOINC_PROP:PartTypeName',
                'type_hint': 'http://www.w3.org/2001/XMLSchema#string',
            },
            {
                'slot_name': 'curator_approved',
                'property': 'COMPLOINC_PROP:curator_approved',
                'type_hint': 'http://www.w3.org/2001/XMLSchema#bool',
            },
            {
                'slot_name': 'subject_dangling',
                'property': 'COMPLOINC_PROP:subject_dangling',
                'type_hint': 'http://www.w3.org/2001/XMLSchema#bool',
            },
            {
                'slot_name': 'object_dangling',
                'property': 'COMPLOINC_PROP:object_dangling',
                'type_hint': 'http://www.w3.org/2001/XMLSchema#bool',
            },
        ],
    })

    # Post-SSSOM initialization updates
    df2 = msdf.df
    # - Add back extension slots (not sure why these are getting removed)
    # todo: Support for non-standard slots (“extensions”) #583 (https://github.com/mapping-commons/sssom-py/issues/583)
    #  - when addressed, this section no longer needed
    # todo: I think this will be correct, as the sorting should be the same, but it would be good to check, or add a
    #  more robust way here to ensure that the PartTypeName is correct.
    for col in ['PartTypeName', 'subject_dangling', 'object_dangling', 'curator_approved']:
        df2[col] = df[col].values
    df2 = df2[['subject_id', 'predicate_id', 'object_id', 'subject_label', 'object_label', 'PartTypeName',
        'mapping_justification', 'similarity_score', 'subject_dangling', 'object_dangling', 'curator_approved']]
    # - Update non-match rows
    #   Update to make it clearer that these rows are not bugged, but represent non-matches. Note that this is
    #   technically not valid SSSOM.
    # todo: should I move this logic above, before the SSSOM is created?
    mask = df2['object_label'] == ''
    df2_matches = df2[~mask].copy()
    df2_na = df2[mask].copy()
    df2_na['non_match'] = True
    df2_matches['non_match'] = False
    cols = ['predicate_id', 'object_id', 'object_label', 'mapping_justification', 'similarity_score', 'object_dangling']
    for col in cols:
        df2_na[col] = ''
    df2_na['curator_approved'] = False
    # - Add back sorting
    df3 = pd.concat([df2_matches, df2_na]).sort_values(
        ['non_match', 'similarity_score', 'subject_id', 'object_id'], ascending=[True, False, True, True])
    del df3['non_match']

    # Save
    msdf.df = df3
    with open(outpath, 'w') as f:
        write_table(msdf, f)


def semantic_similarity_gen_stats(outpath: t.Union[Path, str] = OUTPATH_STATS_DOCS):
    """Generate statistics about dangling part terms

    todo: show additional stats?
     n/pct deprecated? (dangling & non)
     totals for which match determined to be subclass? (dangling or non-dangling)
     n curator_approved = True, False, or nan?
     disaggregate by PartTypeName?
     n/pct dangling not >= threshold?
    """
    template_string = """
### Dangling part terms
These are parts that do not fall in the hierarchy in LOINC, but for which CompLOINC attempts to incorporate.

Similarity threshold: {{ similarity_threshold }}

| Part | n | Percentage |
|----------|-------|------------|
| All parts | {{ n_all }} | 100% |
| Non-dangling | {{ n_non_dangling }} | {{ pct_non_dangling }}% |
| Dangling | {{ n_dangling }} | {{ pct_dangling }}% |
| (Dangling >= threshold) / dangling | {{ n_over_threshold }} | {{ pct_over_threshold_over_dangling }}% |
| (Dangling >= threshold) / all | {{ n_over_threshold }} | {{ pct_over_threshold_over_all }}% |
    """
    # Read data
    df_all = pd.read_csv(IN_PARTS_ALL)
    df_dangling_in = pd.read_csv(INPATH_DANGLING, sep='\t')
    df_dangling_out = pd.read_csv(OUTPATH, sep='\t', comment='#')
    # Calculations & rendering
    similarity_threshold: float = CONFIG.config['loinc_nlp_tree']['similarity_threshold']
    n_all = len(df_all)
    n_dangling = len(df_dangling_in)
    n_non_dangling = n_all - n_dangling
    n_over_threshold = len(df_dangling_out[df_dangling_out['similarity_score'] >= similarity_threshold])
    template = jinja2.Template(template_string)
    output = template.render(
        similarity_threshold=similarity_threshold,
        n_all=n_all,
        n_dangling=n_dangling,
        n_non_dangling=n_non_dangling,
        n_over_threshold=n_over_threshold,
        pct_dangling=f'{n_dangling / n_all * 100:.1f}',
        pct_non_dangling=f'{n_non_dangling / n_all * 100:.1f}',
        pct_over_threshold_over_dangling=f'{n_over_threshold / n_dangling * 100:.1f}',
        pct_over_threshold_over_all=f'{n_over_threshold / n_all * 100:.1f}')
    # Save
    with open(outpath, "w") as f:
        f.write(output)


def semantic_similarity_df(
    label_field=['PartName', 'PartDisplayName'][0], use_cached_embeddings=False,
    inpath_dangling: t.Union[Path, str] = INPATH_DANGLING, inpath_all: t.Union[Path, str] = IN_PARTS_ALL,
    filter_deprecated=True
) -> pd.DataFrame:
    """Creates a dataframe showing semantic similarity confidence between danging and non-dangling terms."""
    # Data load & prep
    df_all = pd.read_csv(inpath_all).fillna('')
    df_dangling = pd.read_csv(inpath_dangling, sep='\t')\
        .rename(columns={'PartDisplayName': 'PartDisplayName_dangling'}).fillna('')
    # - filter deprecated
    if filter_deprecated:
        deprecated: t.Set[str] = set(df_all[df_all['Status'] == 'DEPRECATED']['PartNumber'])
        df_all = df_all[~df_all['PartNumber'].isin(deprecated)]
        df_dangling = df_dangling[~df_dangling['PartNumber'].isin(deprecated)]
    # - replace df_dangling PartDisplayName w/ lookup of PartName in df_all
    if label_field == 'PartName':
        df_dangling = df_dangling.merge(df_all[['PartNumber', 'PartName']], on='PartNumber', how='left')
    df_hier = df_all[~df_all['PartNumber'].isin(df_dangling['PartNumber'])]

    # Iterate matching, by type
    dfs_matches = []
    dfs_no_matching_types = []
    for part_type, df_dangling_i in df_dangling.groupby('PartTypeName'):
        # todo: .fillna('') should not be necessary here, I would think, as it is done above.
        #  Why  getting nan if I don't do this?
        df_hier_i = df_hier[df_hier['PartTypeName'] == part_type]
        df_dangling_i, df_hier_i = df_dangling_i.fillna(''), df_hier_i.fillna('')
        display_ids_dangling: t.Dict[str, t.List[str]] = _get_display_id_map(df_dangling_i, label_field)
        display_ids_hier: t.Dict[str, t.List[str]] = _get_display_id_map(df_hier_i, label_field)
        df_matches_i: pd.DataFrame = _find_best_matches(
            df_dangling_i[label_field].tolist(), df_hier_i[label_field].tolist(), str(part_type),
            label_field, use_cached_embeddings)
        df_matches_i['PartNumber_dangling'] = df_matches_i[f'{label_field}_dangling'].map(display_ids_dangling)
        df_matches_i['PartNumber_hierarchical'] = df_matches_i[f'{label_field}_hierarchical'].map(display_ids_hier)
        df_matches_i = df_matches_i.explode('PartNumber_dangling')
        df_matches_i = df_matches_i.explode('PartNumber_hierarchical')
        df_matches_i['PartTypeName'] = part_type
        if df_hier_i.empty:
            dfs_no_matching_types.append(df_matches_i)
        else:
            dfs_matches.append(df_matches_i)

    df_matches = pd.concat(dfs_matches)[[f'{label_field}_hierarchical', f'{label_field}_dangling', 'confidence',
        'PartTypeName', 'PartNumber_hierarchical', 'PartNumber_dangling']]
    df_matches = pd.concat([df_matches] + dfs_no_matching_types)
    df_matches['URL_hierarchical'] = df_matches['PartNumber_hierarchical'].apply(
        lambda x: f'https://loinc.org/{x}' if x else '')
    df_matches['URL_dangling'] = df_matches['PartNumber_dangling'].apply(lambda x: f'https://loinc.org/{x}')

    # Determine sublcass direction by string length
    df_matches = df_matches.rename(columns={
        'URL_dangling': 'subject_id',
        'URL_hierarchical': 'object_id',
        'PartName_dangling': 'subject_label',
        'PartName_hierarchical': 'object_label',
    })
    df_matches['subject_dangling'] = True
    df_matches['object_dangling'] = False
    mask = df_matches['subject_label'].str.len() < df_matches['object_label'].str.len()
    df_matches_no_swap = df_matches[mask]
    df_matches_swap = df_matches[~mask]
    # todo: refactor this block; somewhat inefficient and confusing
    if len(df_matches_swap) > 0:
        # Swap col vals
        df_matches_swap[['subject_label', 'object_label']] = df_matches_swap[['object_label', 'subject_label']].values
        df_matches_swap[['subject_id', 'object_id']] = df_matches_swap[['object_id', 'subject_id']].values
        df_matches_swap[['subject_dangling', 'object_dangling']] = df_matches_swap[
            ['object_dangling', 'subject_dangling']].values  # same as sub_dangling=False, obj_dangling=True
        # Disallow cases where swapping would result in multiple (dangling) parents for non-dangling
        # - Filter single parent
        sub_counts = df_matches_swap['subject_id'].value_counts()
        df_matches_swap_true = df_matches_swap[df_matches_swap['subject_id'].map(sub_counts) == 1]
        if len(df_matches_swap_true) > 0:
            # - Revert changs made to the multiparent swap rows
            df_matches_no_swap2 = df_matches_swap[df_matches_swap['subject_id'].map(sub_counts) > 1]
            df_matches_no_swap2[['subject_label', 'object_label']] = (
                df_matches_no_swap2[['object_label', 'subject_label']].values)
            df_matches_no_swap2[['subject_id', 'object_id']] = df_matches_no_swap2[['object_id', 'subject_id']].values
            df_matches_no_swap2[['subject_dangling', 'object_dangling']] = df_matches_no_swap2[
                ['object_dangling', 'subject_dangling']].values  # same as sub_dangling=False, obj_dangling=True
            # Update the original dataframe with the swapped values
            df_matches = pd.concat([df_matches_no_swap, df_matches_no_swap2, df_matches_swap_true])

    # Convert to SSSOM
    # - Commenetd out alternative to undefined slot PartTypeName, which is now preferred
    # df_matches['other'] = df_matches['PartTypeName'].apply(lambda x: f'PartTypeName={x}')
    df_matches['curator_approved'] = ''
    df_matches['predicate_id'] = 'rdfs:subClassOf'
    df_matches['mapping_justification'] = 'semapv:SemanticSimilarityThresholdMatching'
    df_matches = df_matches.drop_duplicates().rename(columns={'confidence': 'similarity_score'})[
        ['subject_id', 'predicate_id', 'object_id', 'subject_label', 'object_label', 'PartTypeName',
        'mapping_justification', 'similarity_score', 'subject_dangling', 'object_dangling', 'curator_approved']]\
        .sort_values(['similarity_score', 'subject_id', 'object_id'], ascending=[False, True, True])
    return df_matches


def semantic_similarity_graphs(df: pd.DataFrame, outpath: t.Union[Path, str] = OUTPATH_HIST):
    """Create graphs based on previously computed semantic similarity."""
    plt.rcParams.update({'font.size': 14})
    plt.rcParams['axes.titlesize'] = 16

    # Create bins for the histogram
    bins = [-float('inf'), 0.50, 0.60, 0.70, 0.80, 0.90, 0.99, 1.0]
    labels = ['<0.50', '0.50-0.59', '0.60-0.69', '0.70-0.79', '0.80-0.89', '0.90-0.99', '1.0']

    # Create the histogram using pd.cut to bin the values
    df['similarity_score'] = df['similarity_score'].astype(float)
    confidence_counts = pd.cut(df['similarity_score'], bins=bins, labels=labels, right=True).value_counts().sort_index()

    # Create the bar plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(confidence_counts)), confidence_counts.values)
    plt.xticks(range(len(confidence_counts)), confidence_counts.index, rotation=45)

    # Add value labels on top of each bar with larger font
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom', fontsize=12)

    plt.title('Distribution of Confidence Scores', pad=20)
    plt.xlabel('Confidence Range', labelpad=10)
    plt.ylabel('Number of Entries', labelpad=10)
    plt.tight_layout()  # Adjust layout to prevent label cutoff

    plt.savefig(outpath, dpi=300, bbox_inches='tight')


def semantic_similarity_further_analyses(df: pd.DataFrame):
    """Additional analyses"""
    df['PartNumber_hierarchical'] = df['object_id'].str.extract(r'loinc.org/(\w+)')
    df['PartNumber_dangling'] = df['subject_id'].str.extract(r'loinc.org/(\w+)')

    # Prop analysis: Look at conf=1's; Can we ascertain why they have same label by looking at their other props?
    parts_df = pd.concat([
        pd.read_csv(IN_PARTS_CSV1), pd.read_csv(IN_PARTS_CSV2)])[['PartNumber', 'LinkTypeName', 'Property']]
    # parts_df = parts_df[parts_df['Property'] == 'http://loinc.org/property/search']  # could be another useful field

    # Merge
    parts_grouped = parts_df.groupby('PartNumber')['LinkTypeName'].agg(lambda x: '|'.join(sorted(set(x)))).reset_index()
    hierarchical_merge = df.merge(parts_grouped, left_on='PartNumber_hierarchical', right_on='PartNumber', how='left')
    df['LinkType_hierarchical'] = hierarchical_merge['LinkTypeName']
    dangling_merge = df.merge(parts_grouped, left_on='PartNumber_dangling', right_on='PartNumber', how='left')
    df['LinkType_dangling'] = dangling_merge['LinkTypeName']
    df.to_csv(PROPERTY_ANALYSIS_OUTPATH, sep='\t', index=False)


def semantic_similarity(
    use_display_name=False, use_cached_df=False, use_cached_embeddings=False,
    outpath: t.Union[Path, str] = OUTPATH,
):
    """Creates an .owl where dangling terms are inserted under most likely parents based on semantic similarity."""
    label_field = 'PartDisplayName' if use_display_name else 'PartName'
    matches_df: pd.DataFrame = semantic_similarity_df(label_field, use_cached_embeddings) \
        if not (os.path.exists(outpath) and use_cached_df) \
        else pd.read_csv(outpath, sep="\t", comment="#")
    semantic_similarity_update_curation_file(matches_df, outpath)
    semantic_similarity_further_analyses(matches_df)
    semantic_similarity_graphs(matches_df)


def main(use_display_name=False, use_cached_ss_df=False, use_cached_ss_embeddings=False):
    """Run everything here. Assumes inputs already present."""
    semantic_similarity(use_display_name, use_cached_ss_df, use_cached_ss_embeddings)


def cli():
    """Command line interface."""
    parser = ArgumentParser(
        prog='nlp-taxonomification',
        description='Do semantic similarity to identify subclass candidates for dangling parts.')
    parser.add_argument(
        '-d', '--use-display-name', required=False, action='store_true',
        help='Use fuller label field "PartDisplayName" rather than the unique, canonical "PartName".')
    parser.add_argument(
        '-c', '--use-cached-ss-df',  required=False, action='store_true',
        help='Use cached semantic similarity results dataframe?')
    parser.add_argument(
        '-C', '--use-cached-ss-embeddings', required=False, action='store_true',
        help='Use cached semantic similarity embeddings for LOINC labels?')
    parser.add_argument(
        '-s', '--stats-only', required=False, action='store_true',
        help='If this flag is present, will create a markdown file with statistics about dangling parts. If not '
             'present, no such statistics will be generated.')
    args: t.Dict = vars(parser.parse_args())
    if args['stats_only']:
        return semantic_similarity_gen_stats()
    del args['stats_only']
    main(**args)


if __name__ == '__main__':
    cli()
