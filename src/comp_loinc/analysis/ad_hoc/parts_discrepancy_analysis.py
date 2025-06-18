"""Analyze part count discrepancies between the release and the tree browser

Prerequisites:
- Needs `output/tmp/cl-parts.tsv`, which you can get by running `make output/tmp/cl-parts.tsv`.
"""
import os
from pathlib import Path
from typing import Set, Tuple

import pandas as pd

PROJ_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
LOINC_RELEASE_DIR = PROJ_DIR / 'loinc_release' / 'Loinc_2.80'
PART_DIR = LOINC_RELEASE_DIR / 'AccessoryFiles' / 'PartFile'
IN_PARTS_RELEASE = PART_DIR / 'Part.csv'
LINKS_PRIMARY_PATH = PART_DIR / 'LoincPartLink_Primary.csv'
LINKS_SUPPL_PATH = PART_DIR / 'LoincPartLink_Supplementary.csv'
TREE_DIR_PATH = PROJ_DIR / 'loinc_trees' / '2.80'
CL_QUERIED_PATH = PROJ_DIR / 'output' / 'tmp' / 'cl-parts.tsv'
# DANGLING_PATH = PROJ_DIR / 'curation' / 'nlp-matches.sssom.tsv'  # issues with non-matches removing IDs
DANGLING_PATH = PROJ_DIR / 'output' / 'analysis' / 'dangling' / 'dangling.tsv'


def get_tree_parts(keep_only_component_and_sys=False) -> Set:
    """Get all tree browser parts"""
    tree_all = set()
    comp_and_sys = ('component.csv', 'system.csv', 'component_by_system.csv')
    for file in os.listdir(TREE_DIR_PATH):
        if file.endswith(".csv"):
            if keep_only_component_and_sys and file not in comp_and_sys:
                continue
            df_i = pd.read_csv(TREE_DIR_PATH / file)
            parts_i = set(df_i['Code'].unique())
            tree_all = tree_all.union(parts_i)
    return tree_all


def check_exclusion_from_tree_browser(check_inclusion: Set, verbose=True):
    """Checks to see what parts not in tree browser"""
    for file in os.listdir(TREE_DIR_PATH):
        if file.endswith(".csv"):
            df_i = pd.read_csv(TREE_DIR_PATH / file)
            parts_i = set(df_i['Code'].unique())
            missing_i = parts_i - check_inclusion
            if verbose:
                print(f" - {file}: {len(missing_i)}")


def check_inclusion_in_tree_browser(check_inclusion: Set, verbose=True) -> Tuple[Set, Set]:
    """Checks to see what parts in tree browser"""
    missing = check_inclusion
    included = set()
    for file in os.listdir(TREE_DIR_PATH):
        if file.endswith(".csv"):
            df_i = pd.read_csv(TREE_DIR_PATH / file)
            parts_i = set(df_i['Code'].unique())
            intersection = check_inclusion.intersection(parts_i)
            included = included.union(intersection)
            if verbose:
                print(f" - {file}: {len(intersection)}")
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
tree_parts: Set = get_tree_parts()
print("n parts in CL (CompLOINC):", len(cl_parts))
print('n parts in tree browser:', len(tree_parts))
print("n parts in LOINC release (Part.csv):", len(release_parts))

print()
cl_not_in_release = cl_parts - release_parts  # n=43,445
cl_in_trees, cl_not_in_trees = check_inclusion_in_tree_browser(cl_not_in_release, verbose=False)
print('n parts in CL not in LOINC release:', len(cl_not_in_release))
print('n parts in CL not in tree browser:', len(cl_not_in_trees))

tree_not_in_cl = tree_parts - cl_parts
print('n parts in tree browser not in CL:', len(tree_not_in_cl))
print('- by tree:')
check_exclusion_from_tree_browser(cl_parts)

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
# todo: it would be better to finish this code using curation TSV, because it is persistent, unlike dangling TSV
#  which only shows things that exist in current release. Obsolete if we implement:
#  https://github.com/loinc/comp-loinc/issues/181
# dang_df = dang_df['']
# for col in ['subject_id', 'object_id']:
#     dang_df[col] = dang_df[col].str.replace('https://loinc.org/', '')
#
# dang_parts1 = set(dang_df[dang_df['subject_dangling'] == True]['subject_id'].unique())
# dang_parts2 = set(dang_df[dang_df['object_dangling'] == True]['object_id'].unique())
# dang_parts = dang_parts1.union(dang_parts2)
# dang_parts.remove('')
print('n dangling parts: ', len(dang_parts))
dangling_in_trees, dangling_not_in_trees = check_inclusion_in_tree_browser(dang_parts, verbose=False)
dangling_not_in_release = dang_parts - release_parts
dangling_in_release = dang_parts.intersection(release_parts)  # unused
print('n dangling parts not in tree browser:', len(dangling_not_in_trees))
print('n dangling parts not in release:', len(dangling_not_in_release))
dangling_not_in_either = dangling_not_in_release.intersection(dangling_not_in_trees)
print('- of these, which are also not in tree browser:', len(dangling_not_in_either))
if dangling_not_in_either:
    print('  - I guess these are from older version of release? They are probably not being added to CompLOINC because '
          'they probably have low confidence. But not sure. See: https://github.com/loinc/comp-loinc/issues/181')

print()
print('n dangling parts in each tree browser tree: ')
check_inclusion_in_tree_browser(dang_parts)

print()
print('3. Look into part/term linking --------------------')
# I thought that Steve was supposed to do this: "verify: 100% non-release parts are unlinked to terms"
# but he didn't get back about it. So I went and checked, and I saw that this wasn't the case.
# But I actually checked on Slack (https://comploincworkspace.slack.com/archives/C07FD85066L/p1745954688099209?thread_
# ts=1745185166.474269&cid=C07FD85066L) and he actually said this:
# > The other thing could be that unless a part is directly linked to a LOINC it won't be in the file.  So parts further
# up the tree for grouping are not included.  I'll have to check to verify.
# So either he never said that thing about "100%" and I misunderstood it, or he said it elsewhere, perhaps verbally at
# the all hands meeting.
# Probably best to just pause the analysis here.
df_p = pd.read_csv(LINKS_PRIMARY_PATH, sep=",", low_memory=False)
df_s = pd.read_csv(LINKS_SUPPL_PATH, sep=",", low_memory=False)
release_parts_linked_p = set(df_p['PartNumber'].unique())  # 60,656
print('n parts in release linked to primary: ', len(release_parts_linked_p))
release_parts_linked_s = set(df_s['PartNumber'].unique())  # 64,431
print('n parts in release linked to supplementary: ', len(release_parts_linked_s))
tree_parts_with_p_links = tree_parts.intersection(release_parts_linked_p)  # 30,637
print('tree parts with primary links: ', len(tree_parts_with_p_links))
tree_parts_with_s_links = tree_parts.intersection(release_parts_linked_s)  # 35,951
print('tree parts with supplementary links: ', len(tree_parts_with_s_links))
# todo: Where I left off: look at he 'n' in comments above. can follow up to print this, but it might be more intersting
#  to see which file has which links.

print()
