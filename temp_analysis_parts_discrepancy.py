"""address part count discrepancies"""
import os
from pathlib import Path
from typing import Set, Tuple

import pandas as pd

PROJ_DIR = Path(__file__).resolve().parent
IN_PARTS_RELEASE = PROJ_DIR / 'loinc_release' / 'Loinc_2.80' / 'AccessoryFiles' / 'PartFile' / 'Part.csv'
TREE_DIR_PATH = PROJ_DIR / 'loinc_trees' / '2.80'
CL_QUERIED_PATH = PROJ_DIR / 'cl-parts.tsv'
# DANGLING_PATH = PROJ_DIR / 'curation' / 'nlp-matches.sssom.tsv'  # issues with non-matches removing IDs
DANGLING_PATH = PROJ_DIR / 'output' / 'analysis' / 'dangling' / 'dangling.tsv'


def get_tree_parts() -> Set:
    """Get all tree browser parts"""
    tree_all = set()
    for file in os.listdir(TREE_DIR_PATH):
        if file.endswith(".csv"):
            df_i = pd.read_csv(TREE_DIR_PATH / file)
            parts_i = set(df_i['Code'].unique())
            tree_all = tree_all.union(parts_i)
    return tree_all


def check_inclusion_in_tree_browser(check_inclusion: Set, verbose=True) -> Tuple[Set, Set]:
    """Checks to see what parts in tree browser"""
    missing = check_inclusion
    included = set()
    for file in os.listdir(TREE_DIR_PATH):
        if file.endswith(".csv"):
            df_i = pd.read_csv(TREE_DIR_PATH / file)
            parts_i = set(df_i['Code'].unique())
            interesection = check_inclusion.intersection(parts_i)
            included = included.union(interesection)
            if verbose:
                print(f" - {file}: {len(interesection)}")
            missing = missing - parts_i
    return included, missing


# Get sets of parts
# - need to run sparql to generate this if needing updated list
cl_df = pd.read_csv(CL_QUERIED_PATH, sep="\t")
cl_df['?term'] = cl_df['?term'].str.replace('<https://loinc.org/', '')
cl_df['?term'] = cl_df['?term'].str.replace('>', '')
release_df = pd.read_csv(IN_PARTS_RELEASE, sep=",", low_memory=False)
release_parts = set(release_df['PartNumber'].unique())
cl_parts = set(cl_df['?term'].unique())

print()
print()
print('1. Cross-checking CompLOINC, Release, & Tree browser --------------------')
tree_parts = get_tree_parts()
print("n parts in CL (CompLOINC):", len(cl_parts))
print('n parts in tree browser:', len(tree_parts))
print("n parts in LOINC release (Part.csv):", len(release_parts))

print()
cl_not_in_release = cl_parts - release_parts  # n=43,445
cl_in_trees, cl_not_in_trees = check_inclusion_in_tree_browser(cl_not_in_release, verbose=False)
print('n parts in CL not in LOINC release:', len(cl_not_in_release))
print('n parts in CL not in tree browser:', len(cl_not_in_trees))

print()
print('n CL parts in each tree browser tree: ')
check_inclusion_in_tree_browser(cl_not_in_release)
print()

in_tree_not_in_release = tree_parts - release_parts
in_release_not_in_tree = release_parts - tree_parts
print('n parts in tree browser not in release:', len(in_tree_not_in_release))
print('n parts in release not in tree browser:', len(in_release_not_in_tree))  # TODO: should be 0

print()
print('2. Cross-checking dangling --------------------')
# todo: cross-check against curation TSV (sub where is dangling, obj where is dangling)
# todo: also: see how many of these are from component by system
dang_df = pd.read_csv(DANGLING_PATH, sep="\t", comment="#").fillna('')
dang_parts = set(dang_df['PartNumber'])
print('n dangling parts: ', len(dang_parts))
dangling_in_trees, dangling_not_in_trees = check_inclusion_in_tree_browser(dang_parts, verbose=False)
dangling_not_in_release = dang_parts - release_parts
dangling_in_release = dang_parts.intersection(release_parts)  # unused
print('n dangling parts not in tree browser:', len(dangling_not_in_trees))
print('n dangling parts not in release:', len(dangling_not_in_release))
dangling_not_in_either = dangling_not_in_release.intersection(dangling_not_in_trees)
print('- of these, which are also not in tree browser:', len(dangling_not_in_either))
if dangling_not_in_either:
    print('  - I guess these are from older version of release?')
# # this part only useful for curation tsv
# dang_df = dang_df['']
# for col in ['subject_id', 'object_id']:
#     dang_df[col] = dang_df[col].str.replace('https://loinc.org/', '')
#
# dang_parts1 = set(dang_df[dang_df['subject_dangling'] == True]['subject_id'].unique())
# dang_parts2 = set(dang_df[dang_df['object_dangling'] == True]['object_id'].unique())
# dang_parts = dang_parts1.union(dang_parts2)
# dang_parts.remove('')

print()
print('n dangling parts in each tree browser tree: ')
check_inclusion_in_tree_browser(dang_parts)  # TODO nums dont make sense? do they now after fixing?

print()
# TODO: do something similar that I did above. see workflowy
# TODO: how many dangling parts NOT in tree browser parts
# TODO: how many dangling in release VS not
#  - how many do we lose if we get rid of tee browser
