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

from comp_loinc.analysis.utils import CLASS_TYPES, bundle_inpaths, cli_add_inpath_args, _filter_classes, \
    _subclass_axioms_and_totals

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
    'variations': (('terms', ), ('terms', 'groups'), ('terms', 'groups', 'parts'))
}
# If need smaller, cand o: ![Title]({{ outpath }}){: width="600px"}
logger = logging.getLogger(__name__)
md_template = """
# Classification depth analysis 
This measures how deep into the hierarchy each class is. E.g. if the root of the hierarchy is TermA, and we have axioms
(TermC subClassOf TermB) and (TermB subClassOf TermA), then TermC is at depth 3, TermB is at depth 2, and TermA is at 
depth 1.

Dangling classes are not represented here.

{% for title, table_and_plot_path in figs_by_title.items() %}
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
        In a polyhierarchy, a class can occur at multiple depths and will be
        counted each time.
    """
    # logger.debug("Calculating depth counts for %d subclass pairs with filter %s", len(subclass_pairs), _filter)
    # Validation
    if _filter and any([x not in CLASS_TYPES for x in _filter]):
        raise ValueError(f"Filter must be one of {CLASS_TYPES}")

    # Remove owl:Thing as root if exists
    owl_thing_axioms = {x for x in subclass_pairs if x[1] == '<http://www.w3.org/2002/07/owl#Thing>'}
    subclass_pairs -= owl_thing_axioms

    # Build parent-child relationships
    children = defaultdict(set)
    parents = defaultdict(set)
    for child, parent in subclass_pairs:
        children[parent].add(child)
        parents[child].add(parent)

    # Find roots (classes with no parents)
    all_classes = set(children.keys()) | set(parents.keys())
    roots = all_classes - set(parents.keys())
    # logger.debug("Found %d root classes", len(roots))

    # Calculate depth using BFS
    # A class can have multiple depths if the ontology is a polyhierarchy.
    depths_raw_sets: Dict[str, Set[int]] = defaultdict(set)
    queue = deque([(root, 1) for root in roots])
    while queue:
        cls, depth = queue.popleft()
        if depth not in depths_raw_sets[cls]:
            depths_raw_sets[cls].add(depth)
            for child in children[cls]:
                queue.append((child, depth + 1))
    depths_raw: Dict[str, List[int]] = {
        cls: sorted(list(depths)) for cls, depths in depths_raw_sets.items()
    }
    # logger.debug("Calculated depths for %d classes", len(depths_raw))

    # Filter by class type inclusion
    depths_filtered: Dict[str, List[int]] = {}
    if _filter:
        filtered_classes = _filter_classes(all_classes, _filter)
        depths_filtered = {
            cls: depth for cls, depth in depths_raw.items() if cls in filtered_classes
        }
        # logger.debug("After filtering, %d classes remain", len(depths_filtered))
        logging.debug(f'    n classes: {len(all_classes)}')
        logging.debug(f'    remaining after filtering: {len(filtered_classes)}')

        # TODO: ensure that for (terms, groups, parts), filtered_classes is the same as all_classes. at least numbers
        #  OK: 0 in filtered classes. why? cuz LOINC and filter is 'terms' and axioms are parts
        if len(filtered_classes) != len(all_classes) and _filter == ('terms', 'groups', 'parts'):
            print()

        # TODO temp: how to handle multi-roots?
        # TODO: case 1: CompLOINC-Primary: {'<https://loinc.org/138875005>', '<https://loinc.org/LoincTerm>'}
        #  - which file does this appear in? CompLOINC-Primary
        #      <owl:Class rdf:about="https://loinc.org/138875005">
        #         <rdfs:subClassOf rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
        #         <rdfs:label>SCT   SNOMED CT Concept (SNOMED RT+CTV3)</rdfs:label>
        #     </owl:Class>

    # Roots: log for additonal analysis
    roots2 = {k for k, v in depths_filtered.items() if 1 in v}
    if roots != roots2:
        print()
    logging.debug(f'    n roots: {len(roots)}')
    if len(roots2) > 1:
        print()

    # Count classes at each depth
    depths = depths_filtered if depths_filtered else depths_raw
    depth_counts = defaultdict(int)
    for depth_list in depths.values():
        for depth in depth_list:
            depth_counts[depth] += 1
    depth_counts_list: List[Tuple[int, int]] = sorted(depth_counts.items())
    df = pd.DataFrame(depth_counts_list, columns=["depth", "n"])

    # logger.debug("Computed depth distribution: %s", depth_counts_list)
    return df


def _counts_to_pcts(
    ont_depth_tables: Dict[str, pd.DataFrame],
) -> Dict[str, pd.DataFrame]:
    """Convert counts to percentages"""
    ont_pct_tables: Dict[str, pd.DataFrame] = {}
    for ont_name, df in ont_depth_tables.items():
        df["%"] = (df["n"] / df["n"].sum()) * 100
        ont_pct_tables[ont_name] = df[["depth", "%"]]
        # logger.debug("Converted counts to percentages for %s", ont_name)
    return ont_pct_tables


def _get_stat_label(stat: str) -> str:
    """Generate a label for outputs from stat type"""
    stat_str = 'Number' if stat == "totals" else "%" if stat == 'percentages' else 'Measure'
    return f'{stat_str} of classes'


def _save_plot(
    ont_depth_tables: Dict[str, pd.DataFrame], outdir: Union[Path, str], _filter: List[str], stat: str,
) -> Tuple[pd.DataFrame, str]:
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
    # logger.debug("Saving plot for stat %s with filter %s", stat, _filter)
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
    # logger.debug("Saved plot to %s", outpath)

    return merged, os.path.basename(outpath)


def _save_markdown(
    tables_n_plots_by_filter_and_stat: Dict[Tuple[Tuple[str], str], Tuple[pd.DataFrame, str]],
    outpath: Union[Path, str], template: str = md_template,
):
    """Save results to markdown

    :param tables_n_plots_by_filter_and_stat: keys are [(_filter, stat)], and values are (df, plot_filename).
     The df is a pandas dataframe that was used to create the plot. stat is one of ['totals', 'percentages']. _filter is
     one of class variations, e.g. ('terms', ), ('terms', 'groups'), or ('terms', 'groups', 'parts').
    """
    # logger.debug("Saving markdown to %s", outpath)
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
    # logger.debug("Markdown will contain %d sections", len(figs_by_title))

    # Render template
    template_obj = Template(template)
    rendered_markdown = template_obj.render(figs_by_title=figs_by_title)

    # Write to file
    outpath = Path(outpath)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(rendered_markdown)
    # logger.debug("Wrote markdown to %s", outpath)


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
    # Resolve paths
    terminologies: Dict[str, Path]
    terminologies, outpath_md, outdir_plots = bundle_inpaths(
        loinc_path, loinc_snomed_path, comploinc_primary_path, comploinc_supplementary_path, dont_convert_paths_to_abs,
        outpath_md, outdir_plots)
    if not os.path.exists(outdir_plots):
        os.makedirs(outdir_plots)

    # todo: do I want 2 sets of outputs, 1 per part model? maybe not
    # for mdl in ('primary', 'supplementary'):

    # Get sets of axioms by ontology and grand total and by ontology set
    ont_sets: Dict[str, Set[Tuple[str, str]]]
    tots_df, ont_sets = _subclass_axioms_and_totals(terminologies)
    # logger.debug("Loaded subclass axioms for %d ontologies", len(ont_sets))

    # Derive depths & save
    logger.debug("Running class depth analysis.\n\nLog format:\nINCLUDED_CLASSES\n - TERMINOLOGY\n")
    tables_n_plots_by_filter_and_stat: Dict[Tuple[Tuple[str], str], Tuple[pd.DataFrame, str]] = {}
    for _filter in variations:
        logger.debug(" " + ", ".join(_filter))
        ont_depth_tables: Dict[str, pd.DataFrame] = {}
        ont_depth_pct_tables: Dict[str, pd.DataFrame] = {}
        for ont_name, axioms in ont_sets.items():
            logger.debug("  - " + ont_name)
            ont_depth_tables[ont_name] = _depth_counts(axioms, _filter)
            ont_depth_pct_tables = _counts_to_pcts(ont_depth_tables)
        for stat, data in {'totals': ont_depth_tables, 'percentages': ont_depth_pct_tables}.items():
            df, plot_filename = _save_plot(data, outdir_plots, _filter, stat)
            tables_n_plots_by_filter_and_stat[(_filter, stat)] = (df, plot_filename)
    _save_markdown(tables_n_plots_by_filter_and_stat, outpath_md)


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
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.DEBUG))
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    d: Dict = vars(args)
    del d['log_level']
    return analyze_class_depth(**d)


if __name__ == "__main__":
    cli()
