"""Analyze the set of 'class_' parts used for equivalent class defs in the supplemental model"""
from pathlib import Path

import pandas as pd
from pprint import pprint as pp

THIS_FILE = Path(__file__)
PROJ_DIR = THIS_FILE.parent.parent
INPATH = PROJ_DIR / 'equivalent_groups_defs.tsv'

df = pd.read_csv(INPATH, sep='\t')
df = df[df['property'] == 'class_'].sort_values('value')
counts = df['label'].value_counts().to_dict()
pp(counts)
