"""TODO
"""
import os
from argparse import ArgumentParser
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

import pandas as pd
from matplotlib import pyplot as plt

# TODO
# import matplotlib.pyplot as plt
# import pandas as pd
# from jinja2 import Template
# from tabulate import tabulate
# from upsetplot import from_contents, UpSet

from comp_loinc.analysis.utils import _subclass_axioms_and_totals

# TODO: cull vars i don't need
THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
ONTO_DIR = PROJECT_ROOT / 'src' / 'ontology'
MISSING_AXIOMS_PATH = PROJECT_ROOT / 'output' / 'tmp' / 'missing_comploinc_axioms.tsv'
# TODO
DESC = ''
ONTOLOGIES = ('LOINC', 'LOINC-SNOMED', 'CompLOINC')
# TODO: Narrative, etc. i guess just show the histogram? no table? render a link
md_template = """
# Classifcation depth analysis 
narrative

{{ path }}
"""


def _depth_counts(subclass_pairs: Set[Tuple[str, str]]) -> pd.DataFrame:
    """TODO"""
    # Build parent-child relationships
    children = defaultdict(set)
    parents = defaultdict(set)

    for child, parent in subclass_pairs:
        children[parent].add(child)
        parents[child].add(parent)

    # Find roots (classes with no parents)
    all_classes = set(children.keys()) | set(parents.keys())
    roots = all_classes - set(parents.keys())

    # Calculate depth using BFS
    depths = {}
    queue = deque([(root, 1) for root in roots])

    while queue:
        cls, depth = queue.popleft()
        if cls not in depths:
            depths[cls] = depth
            for child in children[cls]:
                queue.append((child, depth + 1))

    # Count classes at each depth
    # TODO: what is the resulting data type?
    depth_counts = defaultdict(int)
    for depth in depths.values():
        depth_counts[depth] += 1
    depth_counts_list: List[Tuple[int, int]] = sorted(depth_counts.items())

    return pd.DataFrame(depth_counts_list, columns=['depth', 'n'])


def _counts_to_pcts(ont_depth_tables: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """TODO"""
    ont_pct_tables: Dict[str, pd.DataFrame] = {}
    for ont_name, df in ont_depth_tables.items():
        df['%'] = (df['n'] / df['n'].sum()) * 100
        ont_pct_tables[ont_name] = df[['depth', '%']]
    return ont_pct_tables


def _save_markdown(outpath_md: Union[Path, str], outpath_plot: Union[Path, str]):
    """TODO"""
    # TODO: use outpath_plot as-is; it's currently a rel path
    # TODO: convert md path to absolute
    outpath_md = PROJECT_ROOT / outpath_md
    print()


# TODO: convert path to absolute
# TODO: update title to include, ", {y_lab}"
def _save_plot(ont_depth_tables: Dict[str, pd.DataFrame], outpath_plot: Union[Path, str], y_lab='Number of Classes'):
    """Create a stacked histogram of class depths across multiple ontologies.

    Args:
        ont_depth_tables: dict with ontology names as keys and dataframes as values
                     Each dataframe should have 'depth' and 'n' columns
    """
    # First, let's convert all dataframes to a consistent format
    data_for_plot = {}

    for name, df in ont_depth_tables.items():
        cols = list(df.columns)
        # Create a series with depth as index and n as values
        data_for_plot[name] = df.set_index(cols[0])[cols[1]]

    # Create a new dataframe from all the series
    merged = pd.DataFrame(data_for_plot).fillna(0)

    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    merged.plot(kind='bar', stacked=True, ax=ax)

    ax.set_xlabel('Depth')
    ax.set_ylabel(y_lab)
    ax.set_title('Class Depth Distribution')
    ax.legend(title='Terminology')

    plt.tight_layout()
    plt.savefig(PROJECT_ROOT / outpath_plot, dpi=300, bbox_inches='tight')


def analyze_class_depth(indir: Union[Path, str], outpath_md: Union[Path, str], outpath_plot: Union[Path, str]):
    """TODO"""
    tots_df, ont_sets = _subclass_axioms_and_totals(indir)
    ont_depth_tables: Dict[str, pd.DataFrame] = {}
    for ont_name, axioms in ont_sets.items():
        ont_depth_tables[ont_name] = _depth_counts(axioms)
    ont_pct_tables: Dict[str, pd.DataFrame] = _counts_to_pcts(ont_depth_tables)
    _save_plot(ont_depth_tables, outpath_plot)
    # todo: better to parameterize this outpath
    _save_plot(ont_pct_tables, outpath_plot.replace('.png', '-percents.png'), '% of Classes')
    _save_markdown(outpath_md, outpath_plot)


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Classification depth.', description=DESC)
    parser.add_argument(
        '-i', '--indir', required=True, type=str,
        help='Path to directory containing expected inputs: subclass-rels-*.tsv, where * are: '
             + ', '.join([x.lower() for x in ONTOLOGIES]))
    parser.add_argument(
        '-m', '--outpath-md', required=True, type=str, help='Outpath for markdown file containing results.')
    parser.add_argument(
        '-u', '--outpath-plot', required=True, type=str, help='Outpath for plot.')
    d: Dict = vars(parser.parse_args())
    return analyze_class_depth(**d)


if __name__ == '__main__':
    cli()
