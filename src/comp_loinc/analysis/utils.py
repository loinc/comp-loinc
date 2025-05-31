"""Utilities

todo: curies package could be useful here
"""
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

import pandas as pd

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
ONTOLOGIES = ('LOINC', 'LOINC-SNOMED', 'CompLOINC')
CLASS_TYPES = ('terms', 'groups', 'parts')


def _disaggregate_classes(classes: Set, includes_angle_brackets=True, verbose=False) -> Dict[str, Set]:
    """Disaggregate classes by type"""
    b = '<' if includes_angle_brackets else ''
    classes_by_type: Dict[str, Set] = {'terms': set(), 'groups': set(), 'parts': set(), 'other': set()}
    if '<https://loinc.org/LoincPart>' in classes:
        classes_by_type['parts'].add('<https://loinc.org/LoincPart>')
        classes.remove('<https://loinc.org/LoincPart>')
    for cls in classes:
        if cls.startswith(f'{b}http://comploinc//group/'):
            classes_by_type['groups'].add(cls)
        elif cls.startswith(f'{b}https://loinc.org/'):
            if cls.startswith(f'{b}https://loinc.org/LP'):
                classes_by_type['parts'].add(cls)
            elif cls.startswith(f'{b}https://loinc.org/LG'):  # LOINC groups, e.g. LG10324-8
                classes_by_type['groups'].add(cls)
            else:
                classes_by_type['terms'].add(cls)
        else:
            classes_by_type['other'].add(cls)

    if verbose:
        for k, v in classes_by_type.items():
            if v:
                print(f'{k}: {len(v)}')

    return classes_by_type


def _filter_classes(classes: Set, _filter: List[str], includes_angle_brackets=True) -> Set:
    """Flter classes by type

    :param: includes_angle_brackets: Leave True if URI looks like <http://www.w3.org/2002/07/owl#Thing>"""
    if any([x not in CLASS_TYPES for x in _filter]):
        raise ValueError(f'Filter must be one of {CLASS_TYPES}')
    # Disaggregate
    classes_by_type: Dict[str, Set] = _disaggregate_classes(classes, includes_angle_brackets)
    # Filter
    filtered_classes = set()
    for cls_type in _filter:
        filtered_classes |= classes_by_type.get(cls_type, set())
    return filtered_classes


# todo?: incomplete & unused. Not sure if this will be useful for anything
def _disaggregate_axiom_sets(ont_sets: Dict[str, Set[Tuple[str, str]]]) -> Dict[str, Dict[str, Set[Tuple[str, str]]]]:
    """Disaggregate by type (groups, terms, parts)

    todo: If useful, disaggregate 'other' by term-part, part-term, term-group, group-term, part-group, and group-part,
     though some of these groups should not happen.
    todo: also disag by group type, e.g.   http://comploinc//group/component/LP..., http://comploinc//group/system/LP...
    """
    ont_sets_by_type: Dict[str, Dict[str, Set[Tuple[str, str]]]] = {}
    for ont_name, axioms in ont_sets.items():
        ont_sets_by_type[ont_name] = {'term-term': set(), 'group-group': set(), 'part-part': set(), 'other': set()}
        for child, parent in axioms:
            # Todo: this is plaaceholder code
            if child.startswith('http://loinc.org/'):
                if parent.startswith('http://loinc.org/'):
                    ont_sets_by_type[ont_name]['terms'].add((child, parent))
                elif parent.startswith('http://loinc.org/group/'):
                    ont_sets_by_type[ont_name]['groups'].add((child, parent))
                elif parent.startswith('http://loinc.org/part/'):
                    ont_sets_by_type[ont_name]['parts'].add((child, parent))
                else:
                    ont_sets_by_type[ont_name]['other'].add((child, parent))
            else:
                ont_sets_by_type[ont_name]['other'].add((child, parent))
    return ont_sets_by_type


def _subclass_axioms_and_totals(indir: Union[Path, str]) -> Tuple[pd.DataFrame, Dict[str, Set[Tuple[str, str]]]]:
    """Read & return transformed inputs"""
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

    return tots_df, ont_sets
