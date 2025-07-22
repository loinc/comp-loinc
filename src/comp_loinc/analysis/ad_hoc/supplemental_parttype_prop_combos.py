"""Check all of the different properties and their part types

Result:
PartTypeName|Property
ADJUSTMENT 		| adjustment
CHALLENGE 		| search
CHALLENGE 		| challenge
CLASS 		| category
CLASS 		| CLASS
COMPONENT 		| analyte
COMPONENT 		| analyte-core
COMPONENT 		| search
COUNT 		| count
DIVISOR 		| analyte-divisor
GENE 		| analyte-gene
METHOD 		| search
METHOD 		| METHOD_TYP
NUMERATOR 		| analyte-numerator
PROPERTY 		| PROPERTY
SCALE 		| SCALE_TYP
SUFFIX 		| analyte-suffix
SUFFIX 		| analyte-divisor-suffix
SUPER SYSTEM 		| super-system
SUPER SYSTEM 		| search
SYSTEM 		| system-core
SYSTEM 		| search
TIME 		| time-core
TIME MODIFIER 		| time-modifier
"""
from pathlib import Path

import pandas as pd

PROJ_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
# todo: get from config
PATH = PROJ_DIR / 'sources/loinc/Loinc_2.80/AccessoryFiles/PartFile/LoincPartLink_Supplementary.csv'


df = pd.read_csv(PATH)
unique_combinations = df[['PartTypeName', 'Property']].drop_duplicates().sort_values(by='PartTypeName')
outpath = '~/Desktop/suppl.tsv'
# unique_combinations.to_csv(outpath, sep='\t', index=False)
unique_combinations['Property'] = (
    unique_combinations['Property'].str.replace('http://loinc.org/property/', '', regex=False))
print('PartTypeName|Property')
for _, row in unique_combinations.iterrows():
    print(f"{row['PartTypeName']} \t\t| {row['Property']}")
