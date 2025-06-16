import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Dict, List, Tuple

OWL = '{http://www.w3.org/2002/07/owl#}'
RDF = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'


def extract_pairs(intersection: ET.Element) -> List[Tuple[str, str]]:
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


def parse_file(path: str) -> Dict[Tuple[Tuple[str, str], ...], List[str]]:
    tree = ET.parse(path)
    root = tree.getroot()
    groups: Dict[Tuple[Tuple[str, str], ...], List[str]] = defaultdict(list)
    for cls in root.findall(f'.//{OWL}Class'):
        term_uri = cls.get(f'{RDF}about') or cls.get(f'{RDF}ID')
        if not term_uri:
            continue
        term = term_uri.rsplit('/', 1)[-1]
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
    return groups


def generate_rows(groups: Dict[Tuple[Tuple[str, str], ...], List[str]]):
    rows = []
    group_num = 0
    for key, terms in groups.items():
        if len(terms) < 2:
            continue
        group_num += 1
        term_str = '|'.join(sorted(terms))
        for prop, val in key:
            rows.append((group_num, prop, val, term_str))
    return rows


def main():
    parser = argparse.ArgumentParser(description='Group LOINC terms by equivalent class definitions.')
    parser.add_argument('owl_file', help='Path to comploinc-merged-reasoned-all-supplementary.owl')
    parser.add_argument('-o', '--output', default='equivalent_groups.tsv', help='Output TSV file')
    args = parser.parse_args()

    groups = parse_file(args.owl_file)
    rows = generate_rows(groups)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('group_num\tproperty\tvalue\tterms\n')
        for g, p, v, t in rows:
            f.write(f"{g}\t{p}\t{v}\t{t}\n")


if __name__ == '__main__':
    main()
