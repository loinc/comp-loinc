"""Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."""
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Union

HERE = Path(os.path.abspath(os.path.dirname(__file__)))
SRC_DIR = HERE.parent
PROJECT_ROOT = SRC_DIR.parent
ONTO_DIR = PROJECT_ROOT / 'src' / 'ontology'
DESC = 'Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED.'
ONTOLOGIES = ('loinc', 'loinc-snomed', 'comploinc')

# TODO: side effects: also write individual TSVs?
# TODO: TSVs and then use that jinja table plugin (look at mondo-ingest reqs)
def subclass_rel_analysis(indir: Union[Path, str], outpath: Union[Path, str]):
    """TODO"""
    print()


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Subclass axiom analysis.', description=DESC)
    parser.add_argument(
        '-i', '--indir', required=True, type=str,
        help='Path to directory containing expected inputs: subclass-rels-*.tsv, where * are: ' + ', '.join(ONTOLOGIES))
    parser.add_argument(
        '-o', '--outpath', required=True, type=str, help='Outpath for markdown file containing results.')
    d: Dict = vars(parser.parse_args())
    return subclass_rel_analysis(**d)


if __name__ == '__main__':
    cli()
