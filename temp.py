"""address part count discrepancies"""
import os
from pathlib import Path

import pandas as pd

THIS_FILE_PATH = Path(__file__).resolve()
IN_PARTS_ALL = THIS_FILE_PATH.parent / 'loinc_release' / 'Loinc_2.80' / 'AccessoryFiles' / 'PartFile' / 'Part.csv'
TREE_DIR_PATH = THIS_FILE_PATH.parent / 'loinc_trees' / '2.80'

queried_df = pd.read_csv("~/Desktop/queried-parts.tsv", sep="\t")
all_df = pd.read_csv(IN_PARTS_ALL, sep=",", low_memory=False)
all_parts = set(all_df['PartNumber'].unique())
queried_parts = set(queried_df['part'].unique())
print(f"n parts in LOINC release (Part.csv): {len(all_parts)}")
print(f"n parts in CL (CompLOINC): {len(queried_parts)}")

print()
print('n parts in CL not in LOINC release: ', len(queried_parts - all_parts))

queried_not_in_all = queried_parts - all_parts  # n=43,445
# all_not_in_queried = all_parts - queried_parts  # n=0

# TODO: is this because it's coming from the tree?
#  - query the tree
#  - ask them on slack why tree parts not in release
queried_not_in_trees = queried_not_in_all
all_tree_browser_parts = set()
print()
print('n CL parts found in LOINC tree browser: ')
for file in os.listdir(TREE_DIR_PATH):
    if file.endswith(".csv"):
        df = pd.read_csv(TREE_DIR_PATH / file)
        parts_i = set(df['Code'].unique())
        all_tree_browser_parts = all_tree_browser_parts.union(parts_i)
        interesection = queried_not_in_all.intersection(parts_i)
        print(f" - {file}: {len(interesection)}")
        still_missing = queried_not_in_trees - parts_i
        queried_not_in_trees = queried_not_in_trees - still_missing

print()
print('n parts in tree browser: ', len(all_tree_browser_parts))
print('n CL parts still unaccounted for: ', len(queried_not_in_trees))
print('n parts in tree browser not in release: ', len(all_tree_browser_parts - all_parts))

print()
