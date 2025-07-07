"""Builds a representation of SNOMED in OWL functional syntax"""
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Union

import pandas as pd

from loinclib import Configuration

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
DESC = 'Builds a representation of SNOMED in OWL functional syntax.'
DEFAULT_OUTPATH = PROJECT_ROOT / 'analysis/snomed/snomed-unreasoned.ofn'
DEFAULT_CONFIG_PATH = PROJECT_ROOT / 'comploinc_config.yaml'
CONFIG = Configuration(Path(os.path.dirname(str(DEFAULT_CONFIG_PATH))), Path(os.path.basename(DEFAULT_CONFIG_PATH)))
DEFAULT_INPATH = CONFIG.get_snomed_owl_path()
# todo: Ideally I wanted to statically declare these header tags just in case in a future release, they don't appear
#  intermingled with the rest of the OWL expressions, but this requires doing set ops, and also parsing the prefix tags
#  to find the namespaces used.
# PREFIXES_MINIMUM_EXPECTED = {}
# PREFIX_IRI_BAK = "http://snomed.info/id/"
# ONTOLOGY_IRI_BAK = f"{PREFIX_IRI}ontology"

def build_snomed(inpath: Union[Path, str], outpath: Union[Path, str]) -> None:
    """Builds a representation of SNOMED in OWL functional syntax.

    Args:
        inpath: Path to SNOMED release OWL expression file.
        outpath: Path to output file.
    """
    df = pd.read_csv(inpath, sep='\t', dtype=str)
    expressions: List[str] = df['owlExpression'].dropna().tolist()
    axioms: List[str] = []
    prefixes_tags: List[str] = []
    ontology_block_opener = None

    # Extract the ontology tag, prefixes, and axioms
    for exp in expressions:
        if exp.startswith('Ontology'):
            ontology_block_opener = exp[:-1] if exp.endswith(')') else exp
        elif exp.startswith('Prefix'):
            prefixes_tags.append(exp)
        else:
            axioms.append(exp)

    # Validate
    if any([not x for x in [ontology_block_opener, prefixes_tags]]):
        raise ValueError("Ontology IRI or prefixes are missing from the input data.")

    # Write
    with open(outpath, 'w') as f:
        # Header
        for prefix in prefixes_tags:
            f.write(f"{prefix}\n")
        f.write(f"{ontology_block_opener}\n")

        # Write each EquivalentClasses axiom (one per line, indent for readability)
        for axiom in axioms:
            f.write(f"    {axiom}\n")

        # Footer: close the Ontology block
        f.write(")\n")


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Build SNOMED.', description=DESC)
    parser.add_argument(
        '-i', '--inpath', required=False, type=str, default=DEFAULT_INPATH,
        help='Path to SNOMED release OWL expression file.')
    parser.add_argument(
        '-o', '--outpath', required=False, type=str, default=DEFAULT_OUTPATH,
        help='Outpath.')
    d: Dict = vars(parser.parse_args())
    return build_snomed(**d)


if __name__ == '__main__':
    cli()
