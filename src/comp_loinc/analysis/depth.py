"""TODO

todo's
 disaggregate groups by type? e.g.:
  http://comploinc//group/component/LP...
  http://comploinc//group/system/LP...
"""
import os
from argparse import ArgumentParser
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

import pandas as pd
from matplotlib import pyplot as plt

# TODO
# from jinja2 import Template
# from tabulate import tabulate

from comp_loinc.analysis.utils import CLASS_TYPES, _filter_classes, _subclass_axioms_and_totals

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
DESC = ''  # TODO
ONTOLOGIES = ('LOINC', 'LOINC-SNOMED', 'CompLOINC')
# TODO: Narrative, etc. i guess just show the histogram? no table? render a link
# TODO: links below
# If need smaller, cand o: ![Title]({{ outpath }}){: width="600px"}
md_template = """
# Classifcation depth analysis 
narrative

![TODO: Title]({{ outpath_plot_n }})

![TODO: Title]({{ outpath_plot_pct }})
"""


def _depth_counts(subclass_pairs: Set[Tuple[str, str]], _filter: List[str] = None) -> pd.DataFrame:
    """TODO

    :param _filter: List of class types to filter by. If None, no filtering is applied.
    """
    if _filter and any([x not in CLASS_TYPES for x in _filter]):
        raise ValueError(f'Filter must be one of {CLASS_TYPES}')
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
    depths: Dict[str, int] = {}
    queue = deque([(root, 1) for root in roots])

    while queue:
        cls, depth = queue.popleft()
        if cls not in depths:
            depths[cls] = depth
            for child in children[cls]:
                queue.append((child, depth + 1))

    if _filter:
        filtered_classes = _filter_classes(all_classes, _filter)
        depths = {cls: depth for cls, depth in depths.items() if cls in filtered_classes}

    # Count classes at each depth
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


# TODO: convert path to absolute
# TODO: update title to include, ", {y_lab}"
def _save_plot(ont_depth_tables: Dict[str, pd.DataFrame], outpath_plot_n: Union[Path, str], y_lab='Number of Classes'):
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
    plt.savefig(PROJECT_ROOT / outpath_plot_n, dpi=300, bbox_inches='tight')


def _save_markdown(outpath_md: Union[Path, str], outpath_plot_n: Union[Path, str], outpath_plot_pct: Union[Path, str]):
    """TODO"""
    # TODO: use outpath_plots as-is; it's currently a rel path
    # TODO: convert md path to absolute
    outpath_md = PROJECT_ROOT / outpath_md
    print()


def analyze_class_depth(
    indir: Union[Path, str], outpath_md: Union[Path, str], outpath_plot_n: Union[Path, str],
    outpath_plot_pct: Union[Path, str]
):
    """TODO"""
    tots_df, ont_sets = _subclass_axioms_and_totals(indir)

    # TODO: modify the plot labels by which filter
    # TODO: modify file names by which filter
    #  - then update makefile/cli to include all variations, or just remove the png's, put a note about that in
    #  makefile, and add new cli param in both for just --outdir-plots
    for _filter in (['terms'], None):
        ont_depth_tables: Dict[str, pd.DataFrame] = {}
        for ont_name, axioms in ont_sets.items():
            print('processing ontology:', ont_name, 'with filter:', _filter)

            ont_depth_tables[ont_name] = _depth_counts(axioms, _filter)
        ont_pct_tables: Dict[str, pd.DataFrame] = _counts_to_pcts(ont_depth_tables)
        _save_plot(ont_depth_tables, outpath_plot_n)
        _save_plot(ont_pct_tables, outpath_plot_pct, '% of Classes')
        _save_markdown(outpath_md, outpath_plot_n, outpath_plot_pct)


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
        '-p', '--outpath-plot-n', required=True, type=str, help='Outpath for plot of number of classes.')
    parser.add_argument(
        '-P', '--outpath-plot-pct', required=True, type=str, help='Outpath for plot of class percents.')
    d: Dict = vars(parser.parse_args())
    return analyze_class_depth(**d)


if __name__ == '__main__':
    cli()
