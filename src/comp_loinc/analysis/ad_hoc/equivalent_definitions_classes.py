"""Analyze the set of 'class_' parts used for equivalent class defs in the supplemental model"""
from pathlib import Path

import pandas as pd

THIS_FILE = Path(__file__)
PROJ_DIR = THIS_FILE.parent.parent.parent.parent.parent
INDIR = PROJ_DIR / 'output' / 'analysis' / 'equivalent_def_collisions'
INPATH = PROJ_DIR / 'equivalent_groups_defs.tsv'
INPATH_PRIMARY = PROJ_DIR / 'equivalent_groups_defs_primary.tsv'
OUTPATH = INDIR / 'stats.tsv'

# Iterate over specific file patterns in INDIR and save aggregated counts to a TSV
#  - single TSV, where each model x (include indirect?) shows up. 1 col for each of those dimensions
def run():
    """Run analysis for class_ properties and aggregate results"""
    output_rows = []
    for file in [x for x in INDIR.glob("primary-*--defs.tsv")] + [x for x in INDIR.glob("supplementary-*--defs.tsv")]:
        model = 'primary' if 'primary' in file.name else 'supplementary'
        inferred_included = 'inferred_included' in file.name
        df = pd.read_csv(file, sep='\t')
        df2 = df[df['property'] == 'class_']
        counts = dict(df2['label'].value_counts())
        if not counts:
            counts = {
                'n/a': max(df['group_num']),
            }
        for label, count in counts.items():
            output_rows.append({
                'model': model,
                'inferred_included': inferred_included,
                'class_hierarchy_label': label,
                'count': count
            })
    output_df = pd.DataFrame(output_rows)
    output_df.to_csv(OUTPATH, sep='\t', index=False)


if __name__ == '__main__':
    run()
