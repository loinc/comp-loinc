"""Analysis"""
PATH = '/Users/joeflack4/projects/comploinc/loinc_release/Loinc_2.80/AccessoryFiles/PartFile/LoincPartLink_Supplementary.csv'

import pandas as pd

df = pd.read_csv(PATH)
unique_combinations = df[['PartTypeName', 'Property']].drop_duplicates().sort_values(by='PartTypeName')
outpath = '~/Desktop/suppl.tsv'
# unique_combinations.to_csv(outpath, sep='\t', index=False)
unique_combinations['Property'] = (
    unique_combinations['Property'].str.replace('http://loinc.org/property/', '', regex=False))
print('PartTypeName|Property')
for _, row in unique_combinations.iterrows():
    print(f"{row['PartTypeName']} \t\t| {row['Property']}")
