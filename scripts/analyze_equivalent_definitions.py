"""Analyze equivalent definitions in CompLOINC.

This script groups terms that share identical OWL equivalence definitions.  It
produces two TSV files:

1. ``equivalent_groups.tsv`` – a row for each property/value pair in a group of
   terms that share the same definition.  This file replicates the previous
   behaviour of the script.
2. ``labels.tsv`` – a simple mapping of ``group_num`` to the labels of the terms
   in that group.
"""

import argparse
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


OWL = '{http://www.w3.org/2002/07/owl#}'
RDF = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
RDFS = '{http://www.w3.org/2000/01/rdf-schema#}'
THIS_FILE = Path(__file__)
PROJ_DIR = THIS_FILE.parent.parent
INPATH = PROJ_DIR / 'output/build-default/merged-and-reasoned/canonical/comploinc-merged-reasoned-all-supplementary.owl'
OUTPATH = PROJ_DIR / 'equivalent_groups.tsv'
LABELS_OUTPATH = PROJ_DIR / 'labels.tsv'


def extract_pairs(intersection: ET.Element) -> List[Tuple[str, str]]:
    """todo"""
    pairs = []
    for restriction in intersection.findall(f'{OWL}Restriction'):
        prop_elem = restriction.find(f'{OWL}onProperty')
        val_elem = restriction.find(f'{OWL}someValuesFrom')
        if prop_elem is None or val_elem is None:
            continue
        prop_uri = prop_elem.attrib.get(f'{RDF}resource')
        val_uri = val_elem.attrib.get(f'{RDF}resource')
        if not prop_uri or not val_uri:
            continue
        prop = prop_uri.rsplit('/', 1)[-1]
        val = val_uri.rsplit('/', 1)[-1]
        pairs.append((prop, val))
    return pairs


def parse_file(path: str) -> Tuple[Dict[Tuple[Tuple[str, str], ...], List[str]], Dict[str, str]]:
    """Parse the OWL file and group terms by their equivalence definitions.

    Returns a mapping of property/value pairs to a list of terms (``groups``) and
    a mapping from term identifier to its ``rdfs:label`` (``labels``).
    """

    tree = ET.parse(path)
    root = tree.getroot()

    groups: Dict[Tuple[Tuple[str, str], ...], List[str]] = defaultdict(list)
    labels: Dict[str, str] = {}

    for cls in root.findall(f'.//{OWL}Class'):
        term_uri = cls.get(f'{RDF}about') or cls.get(f'{RDF}ID')
        if not term_uri:
            continue
        term = term_uri.rsplit('/', 1)[-1]

        label_elem = cls.find(f'{RDFS}label')
        if label_elem is not None and label_elem.text:
            labels[term] = label_elem.text.strip()

        eq_elem = cls.find(f'{OWL}equivalentClass')
        if eq_elem is None:
            continue
        anon_class = eq_elem.find(f'{OWL}Class')
        if anon_class is None:
            continue
        intersection = anon_class.find(f'{OWL}intersectionOf')
        if intersection is None:
            continue
        pairs = extract_pairs(intersection)
        if not pairs:
            continue
        key = tuple(sorted(pairs))
        groups[key].append(term)

    return groups, labels


def generate_rows(groups: Dict[Tuple[Tuple[str, str], ...], List[str]]):
    """Generate rows for the TSV outputs.

    Returns a list of rows for ``equivalent_groups.tsv`` and a mapping from
    ``group_num`` to the list of terms in that group for use when writing the
    labels file.
    """

    rows = []
    group_terms: Dict[int, List[str]] = {}
    group_num = 0

    for key, terms in groups.items():
        if len(terms) < 2:
            continue
        group_num += 1
        sorted_terms = sorted(terms)
        term_str = '|'.join(sorted_terms)
        for prop, val in key:
            rows.append((group_num, prop, val, term_str))
        group_terms[group_num] = sorted_terms

    return rows, group_terms


def main():
    """CLI entry point."""

    parser = argparse.ArgumentParser(
        description='Group LOINC terms by equivalent class definitions.'
    )
    parser.add_argument(
        '-i', '--inpath',
        help='Path to comploinc-merged-reasoned-all-supplementary.owl',
        default=INPATH,
    )
    parser.add_argument('-o', '--outpath', default=OUTPATH, help='Output TSV file')
    parser.add_argument(
        '-l', '--labels',
        dest='labels_out',
        default=LABELS_OUTPATH,
        help='Output TSV file containing labels for each term',
    )
    args = parser.parse_args()

    groups, labels = parse_file(args.inpath)
    rows, group_terms = generate_rows(groups)

    with open(args.outpath, 'w', encoding='utf-8') as f:
        f.write('group_num\tproperty\tvalue\tterms\n')
        for g, p, v, t in rows:
            f.write(f"{g}\t{p}\t{v}\t{t}\n")

    with open(args.labels_out, 'w', encoding='utf-8') as f:
        f.write('group_num\tterm\tlabel\n')
        for g, terms in group_terms.items():
            for term in terms:
                f.write(f"{g}\t{term}\t{labels.get(term, '')}\n")


if __name__ == '__main__':
    main()
