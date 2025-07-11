"""TODO"""
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Union

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
DESC = 'TODO'  # TODO
DEFAULT_OUTPATH = PROJECT_ROOT / ''  # TODO
DEFAULT_INPATH = ''  # TODO

def build_snomed(inpath: Union[Path, str], outpath: Union[Path, str]) -> None:
    """TODO"""
    pass

def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Build SNOMED-LOINC Ontology.', description=DESC)
    parser.add_argument(
        '-i', '--inpath', required=False, type=str, default=DEFAULT_INPATH, help='Inpath.')  # TODO
    parser.add_argument(
        '-o', '--outpath', required=False, type=str, default=DEFAULT_OUTPATH, help='Outpath.')
    d: Dict = vars(parser.parse_args())
    return build_snomed(**d)


if __name__ == '__main__':
    cli()
