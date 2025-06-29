"""Utilities

todo: curies package could be useful here
"""
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

import pandas as pd

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
CLASS_TYPES = ('terms', 'groups', 'parts')


def _disaggregate_classes(classes: Set, includes_angle_brackets=True, verbose=False) -> Dict[str, Set]:
    """Disaggregate classes by type"""
    b = '<' if includes_angle_brackets else ''
    classes_by_type: Dict[str, Set] = {'terms': set(), 'groups': set(), 'parts': set(), 'other': set()}
    # Parse roots
    # todo: Any other root types in LOINC, CompLOINC, or LOINC-SNOMED Ontology?
    #  - perhaps if we add roots like GRP_SYS, etc, if they have a different URL pattenr, will need to parse them here.
    # Note: No such "https://loinc.org/LoincGroup" exists.
    for root_uri, root_type in (('<https://loinc.org/LoincTerm>', 'terms'), ('<https://loinc.org/LoincPart>', 'parts')):
        if root_uri in classes:
            classes_by_type[root_type].add(root_uri)
            classes.remove(root_uri)

    # Parse non-roots
    for cls in classes:
        if cls.startswith(f'{b}http://comploinc//group/'):
            classes_by_type['groups'].add(cls)
        elif cls.startswith(f'{b}https://loinc.org/'):
            if cls.startswith(f'{b}https://loinc.org/category/'):  # LOINC "categories", e.g. "Document groups"
                classes_by_type['groups'].add(cls)
            elif cls.startswith(f'{b}https://loinc.org/LG'):  # LOINC groups, e.g. LG10324-8
                classes_by_type['groups'].add(cls)
            elif cls.startswith(f'{b}https://loinc.org/LP'):
                classes_by_type['parts'].add(cls)
            else:
                classes_by_type['terms'].add(cls)
        else:
            classes_by_type['other'].add(cls)

    if len(classes_by_type['other']) > 0:
        raise ValueError(f'Found n unexpected classes: {len(classes_by_type["other"])}. Check that '
            f'_disaggregate_classes() is aware of all prefixes for terms, groups, and parts in CompLOINC, LOINC-SNOMED '
            f'Ontology, and LOINC.')

    if verbose:
        for k, v in classes_by_type.items():
            if v:
                print(f'{k}: {len(v)}')

    return classes_by_type


def _filter_classes(
    _filter: List[str], classes_by_type: Dict[str, Set] = None, classes: Set = None, includes_angle_brackets=True
) -> Set:
    """Flter classes by type

    :param: includes_angle_brackets: Leave True if URI looks like <http://www.w3.org/2002/07/owl#Thing>"""
    if any([x not in CLASS_TYPES for x in _filter]):
        raise ValueError(f'Filter must be one of {CLASS_TYPES}')
    # Disaggregate
    if not classes_by_type:
        if not classes:
            raise ValueError('Must pass classes_by_type or classes')
        classes_by_type: Dict[str, Set] = _disaggregate_classes(classes, includes_angle_brackets)
    # Filter
    filtered_classes = set()
    for cls_type in _filter:
        filtered_classes |= classes_by_type.get(cls_type, set())
    return filtered_classes


def bundle_inpaths_and_update_abs_paths(
    loinc_path: Union[Path, str], loinc_snomed_path: Union[Path, str], comploinc_primary_path: Union[Path, str],
    comploinc_supplementary_path: Union[Path, str], dont_convert_paths_to_abs=False, *args
):  # -> Tuple[Dict[str, Path], ...]  # would keep this typedef, but it trips up PyCharm
    """Bundle inpath arguments into dict, adding titles as dict keys. Also can update relative paths to absolute"""
    terminologies: Dict[str, Path] = {
        'LOINC': loinc_path,
        'LOINC-SNOMED': loinc_snomed_path,
        'CompLOINC-Primary': comploinc_primary_path,
        'CompLOINC-Supplementary': comploinc_supplementary_path,
    }
    if not dont_convert_paths_to_abs:
        terminologies = {k: PROJECT_ROOT / Path(v) for k, v in terminologies.items()}
        processed_args = tuple(PROJECT_ROOT / Path(arg) for arg in args)
    else:
        processed_args = args
    return terminologies, *processed_args


def cli_add_inpath_args(parser: ArgumentParser, defaults: Dict[str, str]):
    """Add some common CLI args"""
    parser.add_argument(
        '-l', '--loinc-path', type=str, default=defaults.get('loinc-path'),
        help='Path to TSV containing subclass axioms / relationships for LOINC.')
    parser.add_argument(
        '-L', '--loinc-snomed-path', type=str, default=defaults.get('loinc-snomed-path'),
        help='Path to TSV containing subclass axioms / relationships for LOINC-SNOMED Ontology.')
    parser.add_argument(
        '-p', '--comploinc-primary-path', type=str, default=defaults.get('comploinc-primary-path'),
        help='Path to TSV containing subclass axioms / relationships for CompLOINC (variation using the primary part '
             'model).')
    parser.add_argument(
        '-s', '--comploinc-supplementary-path', type=str,
        default=defaults.get('comploinc-supplementary-path'),
        help='Path to TSV containing subclass axioms / relationships for CompLOINC (variation using the supplementary '
             'part model).')
    parser.add_argument(
        '-r', '--dont-convert-paths-to-abs', required=False, action='store_true',
        help='Set this flag if the all the paths you are passing absolute paths, rather than relative paths, relative'
             ' to the root of the repository. All paths should be one or the other.')
    return parser


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


def _subclass_axioms_and_totals(
    terminologies: Dict[str, Union[Path, str]]
) -> Tuple[pd.DataFrame, Dict[str, Set[Tuple[str, str]]]]:
    """Get sets of axioms by ontology/terminology and grand total and by ontology set

    :params terminologies: Dictionary of ontology paths to files
    :returns tots_df: Grand total number of subclass axioms, by ontolgoy
    :returns ont_sets: Sets of axioms by ontology, with URIs surrounded by angle brackets ('<URI>').
    """
    sets: Dict[str, Set[Tuple[str, str]]] = {}
    dfs = {}

    # Totals
    tots_rows = []
    for ont, path in terminologies.items():
        df = pd.read_csv(path, sep='\t')
        dfs[ont] = df
        tots_rows.append({'': ont, 'n': f'{len(df):,}'})
        sets[ont] = set(zip(df["?child"], df["?parent"]))
    tots_df = pd.DataFrame(tots_rows)

    return tots_df, sets
