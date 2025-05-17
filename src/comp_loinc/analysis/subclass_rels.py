"""Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED.

Refs:
- https://claude.ai/chat/db6bb6d5-2ab5-4bc1-99cc-cffc9428fccd
"""
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Set, Tuple, Union

import pandas as pd
from jinja2 import Template
from tabulate import tabulate

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
ONTO_DIR = PROJECT_ROOT / 'src' / 'ontology'
DESC = 'Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED.'
ONTOLOGIES = ('LOINC', 'LOINC-SNOMED', 'CompLOINC')
# TODO have the template explain what these tables mean
md_template = """# Subclass axiom analysis

## Subclass axioms: totals
{{ tot_table }}

## Subclass axioms: overlap
Formatting: (%a in b) / (% intersection) / (%b in a)
Where 'a' is the ontology represented by the row, and 'b' is the ontology represented by the column.

{{ overlap_direct_table }}
"""

# TODO: side effects: also write individual TSVs?
def subclass_rel_analysis(indir: Union[Path, str], outpath: Union[Path, str]):
    """Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."""
    outpath = PROJECT_ROOT / outpath
    ont_paths = {k: PROJECT_ROOT / indir / f'subclass-rels-{k.lower()}.tsv' for k in ONTOLOGIES}
    ont_sets: Dict[str, Set[Tuple[str, str]]] = {}
    ont_dfs = {}

    # Totals
    tots_rows = []
    for ont, path in ont_paths.items():
        df = pd.read_csv(path, sep='\t')
        ont_dfs[ont] = df
        tots_rows.append({'': ont, 'n': f'{len(df):,}'})
        ont_sets[ont] = set(zip(df["?child"], df["?parent"]))
    tots_df = pd.DataFrame(tots_rows)

    # Direct subclass axiom overlap
    overlap_direct_rows = []
    for row_ont in ONTOLOGIES:
        overlap_row = {'': row_ont}
        row_set = ont_sets[row_ont]
        for col_ont in ONTOLOGIES:
            col_set = ont_sets[col_ont]
            if row_ont == col_ont:
                overlap_row[col_ont] = "-"
            else:
                intersection = row_set.intersection(col_set)

                # Calculate percentages
                pct_row_in_col = len(intersection) / len(row_set) * 100 if len(row_set) > 0 else 0
                pct_col_in_row = len(intersection) / len(col_set) * 100 if len(col_set) > 0 else 0
                # TODO temp
                a_col_ont = col_ont
                a_row_ont = row_ont
                a_col_set = col_set
                a_row_set = row_set
                a1 = row_set.difference(col_set)
                a2 = col_set.difference(row_set)

                overlap_row[col_ont] = f"{pct_row_in_col:.1f}% / {len(intersection):,} / {pct_col_in_row:.1f}%"
        overlap_direct_rows.append(overlap_row)
    overlap_direct_df = pd.DataFrame(overlap_direct_rows)

    # Render & save
    template = Template(md_template)
    tots_table = tabulate(tots_df, headers='keys', tablefmt='pipe', showindex=False)
    overlap_direct_table = tabulate(overlap_direct_df, headers='keys', tablefmt='pipe', showindex=False)
    markdown_output = template.render(tot_table=tots_table, overlap_direct_table=overlap_direct_table)
    with open(outpath, 'w') as f:
        f.write(markdown_output)
    print()


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Subclass axiom analysis.', description=DESC)
    parser.add_argument(
        '-i', '--indir', required=True, type=str,
        help='Path to directory containing expected inputs: subclass-rels-*.tsv, where * are: '
             + ', '.join([x.lower() for x in ONTOLOGIES]))
    parser.add_argument(
        '-o', '--outpath', required=True, type=str, help='Outpath for markdown file containing results.')
    d: Dict = vars(parser.parse_args())
    return subclass_rel_analysis(**d)


if __name__ == '__main__':
    cli()
