"""address part count discrepancies"""
from pathlib import Path

import pandas as pd

THIS_FILE_PATH = Path(__file__).resolve()
IN_PARTS_ALL = THIS_FILE_PATH.parent / 'loinc_release' / 'Loinc_2.80' / 'AccessoryFiles' / 'PartFile' / 'Part.csv'

queried_df = pd.read_csv("~/Desktop/queried-parts.tsv", sep="\t")
all_df = pd.read_csv(IN_PARTS_ALL, sep=",", low_memory=False)
all_parts = set(all_df['PartNumber'].unique())
queried_parts = set(queried_df['part'].unique())
print(f"All parts count: {len(all_parts)}")
print(f"Queried parts count: {len(queried_parts)}")

queried_not_in_all = queried_parts - all_parts
all_not_in_queried = all_parts - queried_parts

# TODO: is this because it's coming from the tree?
#  - query the tree
#  - ask them on slack why tree parts not in release

print()
