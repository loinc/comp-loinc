"""Analyze classification depth

todo's
 if including, disaggregate groups by type? e.g.:
  http://comploinc//group/component/LP...
  http://comploinc//group/system/LP...
"""

import os
import logging
from argparse import ArgumentParser
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

import pandas as pd
from jinja2 import Template
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

# from jinja2 import Template
# from tabulate import tabulate

from comp_loinc.analysis.utils import (
    CLASS_TYPES,
    bundle_inpaths,
    cli_add_inpath_args,
    _filter_classes,
    _subclass_axioms_and_totals,
)

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
DESC = "Analyze classification depth."
DEFAULTS = {
    # CLI args
    "loinc-path": "output/tmp/subclass-rels-loinc.tsv",
    "loinc-snomed-path": "output/tmp/subclass-rels-loinc-snomed.tsv",
    "comploinc-primary-path": "output/tmp/subclass-rels-comploinc-primary.tsv",
    "comploinc-supplementary-path": "output/tmp/subclass-rels-comploinc-supplementary.tsv",
    "outpath-md": "documentation/analyses/class-depth/depth.md",
    "outdir-plots": "documentation/analyses/class-depth",
    # Non-CLI args
    "variations": (["terms"], ["terms", "groups"], ["terms", "groups", "parts"]),
}
# If need smaller, cand o: ![Title]({{ outpath }}){: width="600px"}
md_template = """
# Classifcation depth analysis 
This measures how deep into the hierarchy each class is. E.g. if the root of the hierarchy is TermA, and we have axioms
(TermC subClassOf TermB) and (TermB subClassOf TermA), then TermC is at depth 3, TermB is at depth 2, and TermA is at 
depth 1.

{% title, table_and_plot_path in figs_by_title.items() %}
{% set table, plot_path = table_and_plot_path %}
## {{ title }}
![{{ title }}]({{ plot_path }})

{{ table }}

{% endfor %}
"""


def _depth_counts(
    subclass_pairs: Set[Tuple[str, str]], _filter: List[str] = None
) -> pd.DataFrame:
    """Provides a function to compute and analyze the hierarchical depth of classes based on their parent-child
    relationships, with an optional filter for specific class types.

    Args:
        subclass_pairs: A set of tuples where each tuple represents a child-parent relationship
            between classes.
        _filter: Optional list of strings specifying the class types to include in the filtering.

    Raises:
        ValueError: Raised when one or more values in `_filter` do not belong to the acceptable
            `CLASS_TYPES`.

    Returns:
        pd.DataFrame: A pandas DataFrame containing two columns:
            - 'depth': Represents the depth level within the class hierarchy.
            - 'n': Represents the count of classes at the corresponding depth.
    """
    logger.debug(
        "Calculating depth counts for %d subclass pairs with filter %s",
        len(subclass_pairs),
        _filter,
    )
    if _filter and any([x not in CLASS_TYPES for x in _filter]):
        raise ValueError(f"Filter must be one of {CLASS_TYPES}")
    # Build parent-child relationships
    children = defaultdict(set)
    parents = defaultdict(set)

    for child, parent in subclass_pairs:
        children[parent].add(child)
        parents[child].add(parent)

    # Find roots (classes with no parents)
    all_classes = set(children.keys()) | set(parents.keys())
    roots = all_classes - set(parents.keys())
    logger.debug("Found %d root classes", len(roots))

    # Calculate depth using BFS
    depths: Dict[str, int] = {}
    queue = deque([(root, 1) for root in roots])

    while queue:
        cls, depth = queue.popleft()
        if cls not in depths:
            depths[cls] = depth
            for child in children[cls]:
                queue.append((child, depth + 1))
    logger.debug("Calculated depths for %d classes", len(depths))

    if _filter:
        filtered_classes = _filter_classes(all_classes, _filter)
        # TODO: ensure that for [terms, groups, parts], filtered classes is the same as all classes. at least numbers
        depths = {
            cls: depth for cls, depth in depths.items() if cls in filtered_classes
        }  # TODO: check if the root is owl:thing, or loincTerm etc. and maybe update narrative w/ that info
        logger.debug("After filtering, %d classes remain", len(depths))

    # Count classes at each depth
    depth_counts = defaultdict(int)
    for depth in depths.values():
        depth_counts[depth] += 1
    depth_counts_list: List[Tuple[int, int]] = sorted(depth_counts.items())
    logger.debug("Computed depth distribution: %s", depth_counts_list)

    return pd.DataFrame(depth_counts_list, columns=["depth", "n"])


def _counts_to_pcts(
    ont_depth_tables: Dict[str, pd.DataFrame],
) -> Dict[str, pd.DataFrame]:
    """Convert counts to percentages"""
    ont_pct_tables: Dict[str, pd.DataFrame] = {}
    for ont_name, df in ont_depth_tables.items():
        df["%"] = (df["n"] / df["n"].sum()) * 100
        ont_pct_tables[ont_name] = df[["depth", "%"]]
        logger.debug("Converted counts to percentages for %s", ont_name)
    return ont_pct_tables


def _get_stat_label(stat: str) -> str:
    """Generate a label for outputs from stat type"""
    stat_str = (
        "Number" if stat == "totals" else "%" if stat == "percentages" else "Measure"
    )
    return f"{stat_str} of classes)"


def _save_plot(
    ont_depth_tables: Dict[str, pd.DataFrame],
    outdir: Union[Path, str],
    _filter: List[str],
    stat: str,
) -> Tuple[pd.DataFrame, Path]:
    """Saves a plot representing the class depth distribution based on the provided ontology depth tables.

    This function processes multiple ontology depth tables, aggregates them into a consistent format, and
    creates a stacked bar chart representing the class depth distribution. The resulting plot is saved
    to the specified output directory.

    Parameters:
        ont_depth_tables (Dict[str, pd.DataFrame]): A dictionary where the keys are ontology names and
            the values are pandas DataFrames containing depth information. Each DataFrame must have at
            least two columns, where the first column represents depths and the second represents counts.
        outdir (Union[Path, str]): The directory path where the generated plot will be saved.
        _filter: Shows which CLASS_TYPES are represented in the data. 1+ of ['terms', 'groups', 'parts'].
        stat: The statistic to use for the plot. 1+ of ['totals', 'percentages'].
    """
    if stat not in ("totals", "percentages"):
        raise ValueError(f'`stat` arg must be either "totals" or "percentages".')
    logger.debug("Saving plot for stat %s with filter %s", stat, _filter)
    # Labels and paths
    class_types_str = f'{", ".join(_filter)}'
    y_lab = _get_stat_label(stat)
    outpath = outdir / f'plot-class-depth_{"-".join(_filter)}_{stat}.png'

    # Data prep
    data_for_plot = {}
    for name, df in ont_depth_tables.items():
        cols = list(df.columns)
        # Create a series with depth as index and n as values
        data_for_plot[name] = df.set_index(cols[0])[cols[1]]
    merged = pd.DataFrame(data_for_plot).fillna(0)

    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    merged.plot(kind="bar", stacked=False, ax=ax)
    ax.set_xlabel("Depth")
    ax.set_ylabel(y_lab)
    ax.set_title(f"Class depth distribution ({class_types_str})")
    ax.legend(title="Terminology")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300, bbox_inches="tight")
    logger.debug("Saved plot to %s", outpath)

    return merged, outpath


# TODO:
# todo: does this way of iteration work?
# {% title, table_and_plot_path in figs_by_title.items() %}
# {% set table, plot_path = table_and_plot_path %}
# todo: ensure that the dfs look good
# todo: convert the df to tabulated string using 'tabulate' package?
def _save_markdown(
    tables_n_plots_by_filter_and_stat: Dict[Tuple[str, str], Tuple[pd.DataFrame, Path]],
    outpath: Union[Path, str],
    template: str = md_template,
):
    """Save results to markdown"""
    logger.debug("Saving markdown to %s", outpath)
    figs_by_title: Dict[str, Tuple[str, str]] = {}

    for (
        filter_and_stat,
        table_and_plot_path,
    ) in tables_n_plots_by_filter_and_stat.items():
        # Construct title
        _filter, stat = filter_and_stat
        stat_label: str = _get_stat_label(stat)
        class_types_str = f'{", ".join(_filter)}'
        title = f"{stat_label} ({class_types_str})"

        # Convert formats
        df, plot_path = table_and_plot_path
        plot_path = str(plot_path)
        table_str = df.to_markdown(index=False, tablefmt="orgtbl")
        figs_by_title[title] = (table_str, plot_path)
    logger.debug("Markdown will contain %d sections", len(figs_by_title))

    # Render template
    template_obj = Template(template)
    rendered_markdown = template_obj.render(figs_by_title=figs_by_title)

    # Write to file
    outpath = Path(outpath)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(rendered_markdown)
    logger.debug("Wrote markdown to %s", outpath)


def analyze_class_depth(
    loinc_path: Union[Path, str],
    loinc_snomed_path: Union[Path, str],
    comploinc_primary_path: Union[Path, str],
    comploinc_supplementary_path: Union[Path, str],
    outpath_md: Union[Path, str],
    outdir_plots: Union[Path, str],
    variations=DEFAULTS["variations"],
    dont_convert_paths_to_abs=False,
):
    """Analyze classification depth"""
    logger.debug("Starting analysis")
    # Resolve paths
    terminologies: Dict[str, Path]
    terminologies, outpath_md, outdir_plots = bundle_inpaths(
        loinc_path,
        loinc_snomed_path,
        comploinc_primary_path,
        comploinc_supplementary_path,
        dont_convert_paths_to_abs,
        outpath_md,
        outdir_plots,
    )
    logger.debug("Resolved input paths: %s", terminologies)
    if not os.path.exists(outdir_plots):
        os.makedirs(outdir_plots)

    # todo: do I want 2 sets of outputs, 1 per part model? maybe not
    # for mdl in ('primary', 'supplementary'):

    # Get sets of axioms by ontology and grand total and by ontology set
    ont_sets: Dict[str, Set[Tuple[str, str]]]
    tots_df, ont_sets = _subclass_axioms_and_totals(terminologies)
    logger.debug("Loaded subclass axioms for %d ontologies", len(ont_sets))

    # Derive depths & save
    tables_n_plots_by_filter_and_stat: Dict[
        Tuple[str, str], Tuple[pd.DataFrame, Path]
    ] = {}
    for _filter in variations:
        ont_depth_tables: Dict[str, pd.DataFrame] = {}
        for ont_name, axioms in ont_sets.items():
            logger.debug("Processing ontology %s with filter %s", ont_name, _filter)
            ont_depth_tables[ont_name] = _depth_counts(axioms, _filter)
            ont_depth_pct_tables: Dict[str, pd.DataFrame] = _counts_to_pcts(
                ont_depth_tables
            )
            for stat, data in {
                "totals": ont_depth_tables,
                "percentages": ont_depth_pct_tables,
            }.items():
                df, plot_outpath = _save_plot(data, outdir_plots, _filter, stat)
                tables_n_plots_by_filter_and_stat[(ont_name, _filter)] = (
                    df,
                    plot_outpath,
                )
                logger.debug(
                    "Generated plot %s for ontology %s", plot_outpath, ont_name
                )
    _save_markdown(tables_n_plots_by_filter_and_stat, outpath_md)
    logger.debug("Analysis complete")


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog="Classification depth.", description=DESC)
    cli_add_inpath_args(parser, DEFAULTS)
    parser.add_argument(
        "-M",
        "--outpath-md",
        type=str,
        default=DEFAULTS["outpath-md"],
        help="Outpath for markdown file containing results.",
    )
    parser.add_argument(
        "-P",
        "--outdir-plots",
        type=str,
        default=DEFAULTS["outdir-plots"],
        help="Outdir for plots: (number/% of classes) x (types of classes included).",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.DEBUG))
    d: Dict = vars(args)
    d.pop("log_level", None)
    return analyze_class_depth(**d)


if __name__ == "__main__":
    cli()
