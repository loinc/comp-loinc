"""Builds a representation of SNOMED in OWL functional syntax

todo: fix so no whitespace warnings. e.g.:
 WARN  LINE: 102963 Expected white space at pos: 16  LINE:
    SubClassOf(:421629003 ObjectIntersectionOf(:23217006 :373249005 ObjectSomeValuesFrom(:726542003 :764393008) ObjectSomeValuesFrom(:726542003 :765175006)))
 pos16 is right after SubClassOf( and before the :. I think this needs to be after all ( tags, and probably before all )
"""
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pandas as pd

from loinclib import Configuration

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
DESC = 'Builds a representation of SNOMED in OWL functional syntax.'
DEFAULT_OUTPATH = PROJECT_ROOT / 'output/analysis/snomed/snomed-unreasoned.ofn'
DEFAULT_CONFIG_PATH = PROJECT_ROOT / 'comploinc_config.yaml'
CONFIG = Configuration(Path(os.path.dirname(str(DEFAULT_CONFIG_PATH))), Path(os.path.basename(DEFAULT_CONFIG_PATH)))
DEFAULT_INPATH_OWL = CONFIG.get_snomed_owl_path()
DEFAULT_INPATH_LABELS = CONFIG.get_snomed_description_path()
# todo: Ideally I wanted to statically declare these header tags just in case in a future release, they don't appear
#  intermingled with the rest of the OWL expressions, but this requires doing set ops, and also parsing the prefix tags
#  to find the namespaces used.
# PREFIXES_MINIMUM_EXPECTED = {}
# PREFIX_IRI_BAK = "http://snomed.info/id/"
# ONTOLOGY_IRI_BAK = f"{PREFIX_IRI}ontology"


def _write(
    outpath: Union[Path, str], ontology_block_opener: str, prefixes_tags: List[str], axioms: List[str],
    label_triples: List[str]
) -> None:
    """Write to disk"""
    with open(outpath, 'w') as f:
        # Header
        for prefix in prefixes_tags:
            f.write(f"{prefix}\n")
        f.write(f"{ontology_block_opener}\n")

        # Axioms (mostly/all EquivalentClasses?)
        for axiom in axioms:
            f.write(f"    {axiom}\n")

        # Labels
        for label_triple in label_triples:
            f.write(f"    {label_triple}\n")

        # Footer: close the Ontology block
        f.write(")\n")


def _get_expressions(inpath_owl: Union[Path, str]) -> Tuple[str, List[str], List[str]]:
    """Get expressions from SNOMED release"""
    df = pd.read_csv(inpath_owl, sep='\t', dtype=str)
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

    return ontology_block_opener, prefixes_tags, axioms


def _get_labels(inpath: Union[Path, str]) -> List[str]:
    """Get labels from SNOMED release"""
    df = pd.read_csv(inpath, sep='\t', dtype=str)
    label_triples: List[str] = []
    # Remove special chars from labels
    #  - alternatively i could escape but we don't need full SNOMED label representation
    df['term'] = df['term'].str.replace(r'[^\w\s]', '', regex=True)
    # Get triples
    for row in df.itertuples():
        # can't use rdfs:label CURIE because : is the SNOMED prefix.
        # noinspection PyUnresolvedReferences false_positive_for_named_tuples
        label_triples.append(
            f'AnnotationAssertion(<http://www.w3.org/2000/01/rdf-schema#label> :{row.conceptId} "{row.term}")')
    return label_triples


def build_snomed(
    inpath_owl: Union[Path, str], inpath_labels: Union[Path, str], outpath: Union[Path, str], include_labels=True
) -> None:
    """Builds a representation of SNOMED in OWL functional syntax.

    Args:
        inpath_owl: Path to SNOMED release OWL expression file.
        outpath: Path to output file.
    """
    ontology_block_opener, prefixes_tags, axioms = _get_expressions(inpath_owl)
    label_triples = _get_labels(inpath_labels) if include_labels else []
    _write(outpath, ontology_block_opener, prefixes_tags, axioms, label_triples)


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Build SNOMED.', description=DESC)
    parser.add_argument(
        '-i', '--inpath-owl', required=False, type=str, default=DEFAULT_INPATH_OWL,
        help='Path to SNOMED release OWL expression file.')
    parser.add_argument(
        '-I', '--inpath-labels', required=False, type=str, default=DEFAULT_INPATH_LABELS,
        help='Path to SNOMED definition file for labels.')
    parser.add_argument(
        '-o', '--outpath', required=False, type=str, default=DEFAULT_OUTPATH, help='Outpath.')
    d: Dict = vars(parser.parse_args())
    return build_snomed(**d)


if __name__ == '__main__':
    cli()
