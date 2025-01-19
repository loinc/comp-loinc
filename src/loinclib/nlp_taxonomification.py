"""All things dealing with taxonomies based on NLP approaches."""
import os
import pickle
import typing as t
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.comp_loinc.groups.property_use import Part

DANGLING_DIR = os.getcwd() / Path('output/analysis/dangling')
DANGLING_CACHE_DIR = DANGLING_DIR / 'cache'
# todo: ideally not hard code. Best to solve via OO, i'm not sure
INPATH_DANGLING = DANGLING_DIR / 'dangling.tsv'
OUTPATH_MATCHES = DANGLING_DIR / 'matches.tsv'
OUTPATH_HIST = DANGLING_DIR / 'confidence_histogram.png'
# todo: get this from config using standard pattern in codebase
INPATH_ALL = os.getcwd() / Path('loinc_release/Loinc_2.78/AccessoryFiles/PartFile/Part.csv')


# Inputs --------------------------------------------------------------------------------------------------------------
def parts_to_tsv(parts: t.List[Part], outpath: Path):
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
def _get_display_id_map(df) -> t.Dict[str, t.List[str]]:
    """Get map of all display names to part numbers. There are some duplciate display name values."""
    display_to_ids = df.groupby('PartDisplayName')['PartNumber'].unique().to_dict()
    return {name: list(parts) for name, parts in display_to_ids.items()}


# Semantic matching ----------------------------------------------------------------------------------------------------
def get_embeddings(text_list: t.List[str], cache_name: str, use_cache=True):
    """Get embeddings for a list of strings."""
    # Try to load from cache first
    cache_file = f"embeddings_{cache_name}.pkl"
    cache_path = DANGLING_CACHE_DIR / cache_file
    if os.path.exists(cache_path) and use_cache:
        # print(f"Loading embeddings from cache: {cache_file}")
        with open(cache_file, 'rb') as f:
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
    terms_dangling: t.List[str], terms_hier: t.List[str], part_type: str, use_cache=True, batch_size=30_000
) -> pd.DataFrame:
    """Find best matches between two sets of strings using embeddings.

    FYI: Introduced batch size for fear of high memory usage. But not an issue, especially when splitting by part_type.
    batch_size 30k is about equal to the total number of dangling terms. This could become useful if we start to match
    terms against each other even when they have not been classified as in the same part_type.
    """
    if not terms_hier:
        return pd.DataFrame([{
            'PartDisplayName_dangling': term,
            'PartDisplayName_hierarchical': None,
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
                'PartDisplayName_dangling': term,
                'PartDisplayName_hierarchical': terms_hier[best_match_idx],
                'confidence': confidence
            })
    return pd.DataFrame(best_matches)


def semantic_similarity_df(
    use_cached_df=True, use_cached_embeddings=True, outpath: t.Union[Path, str] = OUTPATH_MATCHES
) -> pd.DataFrame:
    """Creates a dataframe showing semantic similarity confidence between danging and non-dangling terms."""
    if os.path.exists(outpath) and use_cached_df:
        print(f"Using cached matches from {outpath}")
        return pd.read_csv(outpath, sep='\t')

    # Data load & prep
    df_dangling = pd.read_csv(INPATH_DANGLING, sep='\t')
    df_all = pd.read_csv(INPATH_ALL)
    # - filter
    df_hier = df_all[~df_all['PartNumber'].isin(df_dangling['PartNumber'])]

    # Iter, by type
    dfs_matches = []
    dfs_no_matching_types = []
    for part_type, df_dangling_i in df_dangling.groupby('PartTypeName'):
        df_hier_i = df_hier[df_hier['PartTypeName'] == part_type]
        display_ids_dangling: t.Dict[str, t.List[str]] = _get_display_id_map(df_dangling_i)
        display_ids_hier: t.Dict[str, t.List[str]] = _get_display_id_map(df_hier_i)
        df_matches_i: pd.DataFrame = find_best_matches(
            df_dangling_i['PartDisplayName'].tolist(), df_hier_i['PartDisplayName'].tolist(), str(part_type),
            use_cached_embeddings)
        df_matches_i['PartNumber_dangling'] = df_matches_i['PartDisplayName_dangling'].map(display_ids_dangling)
        df_matches_i['PartNumber_hierarchical'] = df_matches_i['PartDisplayName_hierarchical'].map(display_ids_hier)
        df_matches_i = df_matches_i.explode('PartNumber_dangling')
        df_matches_i = df_matches_i.explode('PartNumber_hierarchical')
        df_matches_i['PartTypeName'] = part_type
        if df_hier_i.empty:
            dfs_no_matching_types.append(df_matches_i)
        else:
            dfs_matches.append(df_matches_i)

    df_matches = pd.concat(dfs_matches)[['PartDisplayName_hierarchical', 'PartDisplayName_dangling', 'confidence',
        'PartTypeName', 'PartNumber_hierarchical', 'PartNumber_dangling']].sort_values('confidence', ascending=False)
    df_matches = pd.concat([df_matches] + dfs_no_matching_types)
    df_matches['URL_hierarchical'] = df_matches['PartNumber_hierarchical'].apply(
        lambda x: f'https://loinc.org/{x}' if x else '')
    df_matches['URL_dangling'] = df_matches['PartNumber_dangling'].apply(lambda x: f'https://loinc.org/{x}')
    df_matches = df_matches.drop_duplicates()
    df_matches.to_csv(outpath, sep='\t', index=False, float_format='%.6f')
    return df_matches


# noinspection PyUnusedLocal
def semantic_similarity_hierarchy_owl(df: pd.DataFrame):
    """Create OWL hierarchy based on previously computed semantic similarity.
    TODO: Next, .owl w/ subclassing on matches"""
    print()


def semantic_similarity_graphs(df: pd.DataFrame, outpath: t.Union[Path, str] = OUTPATH_HIST):
    """Create graphs based on previously computed semantic similarity."""
    plt.rcParams.update({'font.size': 14})
    plt.rcParams['axes.titlesize'] = 16

    # Create bins for the histogram
    bins = [-float('inf'), 0.50, 0.60, 0.70, 0.80, 0.90, 0.99, 1.0]
    labels = ['<0.50', '0.50-0.59', '0.60-0.69', '0.70-0.79', '0.80-0.89', '0.90-0.99', '1.0']

    # Create the histogram using pd.cut to bin the values
    confidence_counts = pd.cut(df['confidence'], bins=bins, labels=labels, right=True).value_counts().sort_index()

    # Create the bar plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(confidence_counts)), confidence_counts.values)
    plt.xticks(range(len(confidence_counts)), confidence_counts.index, rotation=45)

    # Add value labels on top of each bar with larger font
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{int(height)}',
                 ha='center', va='bottom',
                 fontsize=12)

    plt.title('Distribution of Confidence Scores', pad=20)
    plt.xlabel('Confidence Range', labelpad=10)
    plt.ylabel('Number of Entries', labelpad=10)
    plt.tight_layout()  # Adjust layout to prevent label cutoff

    plt.savefig(outpath, dpi=300, bbox_inches='tight')


def semantic_similarity_further_analyses(df: pd.DataFrame):
    """Additional analyses"""
    # 1. Prop analysis: Look at conf=1's; Can we ascertain why they have same label by looking at their other props?
    parts_csv1 = os.getcwd() / Path('loinc_release/Loinc_2.78/AccessoryFiles/PartFile/LoincPartLink_Supplementary.csv')
    parts_csv2 = os.getcwd() / Path('loinc_release/Loinc_2.78/AccessoryFiles/PartFile/LoincPartLink_Primary.csv')
    parts_df = pd.concat([pd.read_csv(parts_csv1), pd.read_csv(parts_csv2)])[['PartNumber', 'LinkTypeName', 'Property']]
    # parts_df = parts_df[parts_df['Property'] == 'http://loinc.org/property/search']  # could be another useful field

    parts_grouped = parts_df.groupby('PartNumber')['LinkTypeName'].agg(lambda x: '|'.join(sorted(set(x)))).reset_index()
    hierarchical_merge = df.merge(parts_grouped, left_on='PartNumber_hierarchical', right_on='PartNumber', how='left')
    df['LinkType_hierarchical'] = hierarchical_merge['LinkTypeName']
    dangling_merge = df.merge(parts_grouped, left_on='PartNumber_dangling', right_on='PartNumber', how='left')
    df['LinkType_dangling'] = dangling_merge['LinkTypeName']

    df.to_csv(str(OUTPATH_MATCHES).replace('.tsv', '_prop_analysis.tsv'), sep='\t', index=False)


def semantic_similarity(use_cached_df=True, use_cached_embeddings=True):
    """Creates an .owl where dangling terms are inserted under most likely parents based on semantic similarity."""
    df: pd.DataFrame = semantic_similarity_df(use_cached_df, use_cached_embeddings)
    semantic_similarity_further_analyses(df)
    semantic_similarity_graphs(df)
    semantic_similarity_hierarchy_owl(df)


def main(use_cached_ss_df=True, use_cached_ss_embeddings=True):
    """Run everything here. Assumes inputs already present."""
    semantic_similarity(use_cached_ss_df, use_cached_ss_embeddings)


if __name__ == '__main__':
    main(use_cached_ss_df=True)
