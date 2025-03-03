"""All things dealing with taxonomies based on NLP approaches."""
import os
import pickle
import typing as t
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sssom.parsers import from_sssom_dataframe
from sssom.util import MappingSetDataFrame
from sssom.writers import write_table

from loinclib import Configuration

THIS_FILE_PATH = Path(os.path.abspath(__file__))
LOINCLIB_DIR = THIS_FILE_PATH.parent
SRC_DIR = LOINCLIB_DIR.parent
PROJECT_DIR = SRC_DIR.parent
# PROJECT_DIR = os.getcwd()
DANGLING_DIR = PROJECT_DIR / 'output/analysis/dangling'
DANGLING_CACHE_DIR = DANGLING_DIR / 'cache'
# todo: ideally not hard code. Best to solve via OO, i'm not sure
INPATH_DANGLING = DANGLING_DIR / 'dangling.tsv'
OUT_FILENAME = 'nlp-matches.sssom.tsv'
# todo: not DRY. This is also defined in LoincTreeSource.nlp_tree
OUTPATH_ANALYSIS_MATCHES = DANGLING_DIR / OUT_FILENAME
OUTPATH_HIST = DANGLING_DIR / 'confidence_histogram.png'
# todo: get this from config using standard pattern in codebase
# note: as of 2025/01/22 there are 62 Document terms in IN_PARTS_ALL not in IN_PARTS_CSV1 or IN_PARTS_CSV2
IN_PARTS_ALL = PROJECT_DIR / 'loinc_release/Loinc_2.78/AccessoryFiles/PartFile/Part.csv'
IN_PARTS_CSV1 = PROJECT_DIR / 'loinc_release/Loinc_2.78/AccessoryFiles/PartFile/LoincPartLink_Supplementary.csv'
IN_PARTS_CSV2 = PROJECT_DIR / 'loinc_release/Loinc_2.78/AccessoryFiles/PartFile/LoincPartLink_Primary.csv'
DEFAULT_CONFIG_PATH = PROJECT_DIR / 'comploinc_config.yaml'

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
def get_embeddings(text_list: t.List[str], cache_name: str, use_cache=True):
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


def find_best_matches(
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
    embeds_hier = get_embeddings(terms_hier, f'{part_type}_hierarchical', use_cache)

    # Process matches in chunks
    best_matches = []
    for i in range(0, len(terms_dangling), batch_size):
        terms_dangling_i = terms_dangling[i:i + batch_size]
        embeds_dangling_i = get_embeddings(terms_dangling_i, f'{part_type}_dangling_{i}', use_cache)
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


def semantic_similarity_df(
    label_field=['PartName', 'PartDisplayName'][0], use_cached_embeddings=False,
    inpath_dangling: t.Union[Path, str] = INPATH_DANGLING, inpath_all: t.Union[Path, str] = IN_PARTS_ALL
) -> pd.DataFrame:
    """Creates a dataframe showing semantic similarity confidence between danging and non-dangling terms."""
    # Data load & prep
    df_all = pd.read_csv(inpath_all)
    df_dangling = pd.read_csv(inpath_dangling, sep='\t').rename(columns={'PartDisplayName': 'PartDisplayName_dangling'})
    if label_field == 'PartName':  # replace df_dangling PartDisplayName w/ lookup of PartName in df_all
        df_dangling = df_dangling.merge(df_all[['PartNumber', 'PartName']], on='PartNumber', how='left')
    # - filter
    df_hier = df_all[~df_all['PartNumber'].isin(df_dangling['PartNumber'])]

    # Iter, by type
    dfs_matches = []
    dfs_no_matching_types = []
    for part_type, df_dangling_i in df_dangling.groupby('PartTypeName'):
        df_hier_i = df_hier[df_hier['PartTypeName'] == part_type]
        display_ids_dangling: t.Dict[str, t.List[str]] = _get_display_id_map(df_dangling_i, label_field)
        display_ids_hier: t.Dict[str, t.List[str]] = _get_display_id_map(df_hier_i, label_field)
        df_matches_i: pd.DataFrame = find_best_matches(
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

    # Convert to SSSOM
    # - Commenetd out alternative to undefined slot PartTypeName, which is now preferred
    # df_matches['other'] = df_matches['PartTypeName'].apply(lambda x: f'PartTypeName={x}')
    df_matches['curator_approved'] = ''
    df_matches['predicate_id'] = 'rdfs:subClassOf'
    df_matches['mapping_justification'] = 'semapv:SemanticSimilarityThresholdMatching'
    df_matches = df_matches.drop_duplicates().rename(columns={
        'URL_dangling': 'subject_id',
        'URL_hierarchical': 'object_id',
        'PartName_dangling': 'subject_label',
        'PartName_hierarchical': 'object_label',
        'confidence': 'similarity_score'
    })[['subject_id', 'predicate_id', 'object_id', 'subject_label', 'object_label', 'PartTypeName',
        'mapping_justification', 'similarity_score', 'curator_approved']].sort_values(
        ['similarity_score', 'subject_id', 'object_id'], ascending=[False, True, True])
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

    df.to_csv(str(OUTPATH_ANALYSIS_MATCHES).replace('.tsv', '_prop_analysis.tsv'), sep='\t', index=False)


def _save_sssom(
    df: pd.DataFrame, outpath_tree: t.Union[Path, str] = OUTPATH_ANALYSIS_MATCHES,
    outpath_analysis: t.Union[Path, str] = OUTPATH_ANALYSIS_MATCHES
):
    """Save matches to SSSOM

    Params outpath and outpath2 differences are explained in semantic_similarity().
    todo: consider saving the metadata as a separate yaml file
    """
    # Fix mapping precision
    #  Otheriwse, some show up with precision >1. Digits >5 causes issue.
    #  Can't do this with SSSOM, so convert col: matches_df.to_csv(outpath, sep='\t', index=False, float_format='%.5f')
    df['similarity_score'] = df['similarity_score'].round(5).astype(str)

    # Set metadata
    msdf: MappingSetDataFrame = from_sssom_dataframe(df, prefix_map={
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    }, meta={
        'mapping_tool': 'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2',
        # todo: Getting dynamically would be great, but not easy. This version number was true by looking at poetry.lock
        #  on 2025/02/22, but won't always be true.
        'mapping_tool_version': '3.4.1',
        # todo: make this a defined slot https://mapping-commons.github.io/sssom/spec-model/#non-standard-slots
        'similarity_measure': 'https://www.wikidata.org/wiki/Q1784941',
        # todo: Ideally, the 'curator_approved' and 'PartTypeName' columns would also have a defined extension
    })
    # Add back sorting
    msdf.df = msdf.df.sort_values(['similarity_score', 'subject_id', 'object_id'], ascending=[False, True, True])
    # Add back undefined cols
    msdf.df['curator_approved'] = ''
    # todo: I think this will be correct, as the sorting should be the same, but it would be good to check, or add a
    #  more robust way here to ensure that the PartTypeName is correct.
    msdf.df['PartTypeName'] = df['PartTypeName'].values
    msdf.df = msdf.df[['subject_id', 'predicate_id', 'object_id', 'subject_label', 'object_label', 'PartTypeName',
        'mapping_justification', 'similarity_score', 'curator_approved']]

    # Save
    with open(outpath_analysis, 'w') as f:
        write_table(msdf, f)
    with open(outpath_tree, 'w') as f:
        write_table(msdf, f)


def semantic_similarity(
    outpath_tree: t.Union[Path, str], use_display_name=False, use_cached_df=False, use_cached_embeddings=False,
    outpath_analysis: t.Union[Path, str] = OUTPATH_ANALYSIS_MATCHES,
):
    """Creates an .owl where dangling terms are inserted under most likely parents based on semantic similarity.

    :param outpath_tree: This is to place the resulting matches file in the tree browser files dir for easier loading.
    :param outpath_analysis: This is a mostly redundant path, used to save the dangling matches with the other related
    analytical files, for easy access.
    the top of the file."""
    label_field = 'PartDisplayName' if use_display_name else 'PartName'
    matches_df: pd.DataFrame = semantic_similarity_df(label_field, use_cached_embeddings) \
        if not (os.path.exists(outpath_analysis) and use_cached_df) \
        else pd.read_csv(outpath_analysis, sep="\t", comment="#")
    _save_sssom(matches_df, outpath_tree, outpath_analysis)
    semantic_similarity_further_analyses(matches_df)
    semantic_similarity_graphs(matches_df)


def main(
    use_display_name=False, use_cached_ss_df=False, use_cached_ss_embeddings=False,
    config_path: t.Union[Path, str] = DEFAULT_CONFIG_PATH
):
    """Run everything here. Assumes inputs already present."""
    config = Configuration(Path(os.path.dirname(str(config_path))), Path(os.path.basename(config_path)))
    outpath_tree_format = config.get_loinc_trees_path() / OUT_FILENAME
    semantic_similarity(outpath_tree_format, use_display_name, use_cached_ss_df, use_cached_ss_embeddings)


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
        '-f', '--config-path', required=False, default=DEFAULT_CONFIG_PATH, help='Path to CompLOINC config.')
    main(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()
