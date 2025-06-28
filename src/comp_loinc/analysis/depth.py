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

from comp_loinc.analysis.utils import (
    CLASS_TYPES,
    _disaggregate_classes,
    bundle_inpaths_and_update_abs_paths,
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
    "labels-path": "output/tmp/labels-all-terminologies.tsv",
    "outpath-md": "documentation/analyses/class-depth/depth.md",
    "outdir-plots": "documentation/analyses/class-depth",
    "outpath-tsv": "output/tmp/depth-counts.tsv",
    # Non-CLI args
    "variations": (("terms",), ("terms", "groups"), ("terms", "groups", "parts")),
}
# If need smaller, cand o: ![Title]({{ outpath }}){: width="600px"}
logger = logging.getLogger(__name__)
md_template = """
# Classification depth analysis 
This measures how deep into the hierarchy each class is. E.g. if the root of the hierarchy is TermA, and we have axioms
(TermC subClassOf TermB) and (TermB subClassOf TermA), then TermC is at depth 3, TermB is at depth 2, and TermA is at 
depth 1.

**Dangling classes** 
Dangling classes are not represented here in this class depth analysis.

*Ramifications for LOINC*
Note that this results in LOINC showing that it has 0 terms at any depths, as LOINC has no term hierarchy. The only 
hierarchies that exist in LOINC are a shallow grouping hierarchy (represented by CSVs in `AccessoryFiles/GroupFile/` in 
the LOINC release, and the part hierarchy, which is not represented in the release, but only exists in the LOINC tree 
browser (https://loinc.org/tree/). Regarding parts, there are also a large number of those that are dangling even after 
when considering all of the tree browser hierarchies, and those as well are not represented here. 

*Ramifications for CompLOINC*
The only dangling classes in CompLOINC are dangling parts from the LOINC release, specifically the ones which CompLOINC 
was not able to find matches. Those classes are not represented here.

{% for title, table_and_plot_path in figs_by_title.items() %}
{% set table, plot_path = table_and_plot_path %}
## {{ title }}
![{{ title }}]({{ plot_path }})

{{ table }}

{% endfor %}
"""


def _depth_counts(
    subclass_pairs: Set[Tuple[str, str]], _filter: List[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
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
        Tuple[pd.DataFrame, pd.DataFrame]:
            - The first DataFrame contains two columns:
                * ``depth``: The depth level within the class hierarchy.
                * ``n``: The count of classes at the corresponding depth.
            - The second DataFrame contains a row for each class-depth pair with
              the columns ``class`` and ``depth``. In a polyhierarchy a class can
              occur at multiple depths and will be returned multiple times.
    """
    # logger.debug("Calculating depth counts for %d subclass pairs with filter %s", len(subclass_pairs), _filter)
    # Validation
    if _filter and any([x not in CLASS_TYPES for x in _filter]):
        raise ValueError(f"Filter must be one of {CLASS_TYPES}")

    # Remove owl:Thing as root if exists
    owl_thing_axioms = {
        x for x in subclass_pairs if x[1] == "<http://www.w3.org/2002/07/owl#Thing>"
    }
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
    logging.debug(f"    n roots: {len(roots):,}")

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
    depths_raw: Dict[str, List[int]] = {  # type: ignore
        cls: sorted(list(depths)) for cls, depths in depths_raw_sets.items()
    }
    # logger.debug("Calculated depths for %d classes", len(depths_raw))

    # Filter by class type inclusion
    depths: Dict[str, List[int]] = depths_raw
    classes_by_type: Dict[str, Set] = _disaggregate_classes(all_classes)
    if _filter:
        filtered_classes = _filter_classes(_filter, classes_by_type)
        depths_filtered: Dict[str, List[int]] = {
            cls: depth for cls, depth in depths_raw.items() if cls in filtered_classes
        }
        depths = depths_filtered
        # logger.debug("After filtering, %d classes remain", len(depths_filtered))
        logging.debug(f"    n classes: {len(all_classes):,}")
        logging.debug(f"    n after class type filtration: {len(filtered_classes):,}")

        # TODO: ensure that for (terms, groups, parts), filtered_classes is the same as all_classes. at least numbers
        #  OK: 0 in filtered classes. why? cuz LOINC and filter is 'terms' and axioms are parts
        if len(filtered_classes) != len(all_classes) and _filter == (
            "terms",
            "groups",
            "parts",
        ):
            # TODO: Why do filtered classes have LoincPArt but AllClasses do not?
            diff1 = all_classes - filtered_classes
            diff2 = filtered_classes - all_classes
            print(diff1)
            print(diff2)
            print()

    # Count classes at each depth
    # - Create reverse lookup: class_id -> class_type
    class_to_type = {}
    for class_type, class_set in classes_by_type.items():
        for class_id in class_set:
            class_to_type[class_id] = class_type
    # - Get counts
    depth_counts = defaultdict(int)
    depths_rows = []
    for cls_id, depth_list in depths.items():
        class_type: str = class_to_type.get(
            cls_id, "unknown"
        )  # fallback for missing classes
        for depth in depth_list:
            depth_counts[depth] += 1
            depths_rows.append(
                {"class_type": class_type, "class": cls_id, "depth": depth}
            )
    depth_counts_list: List[Tuple[int, int]] = sorted(depth_counts.items())
    df_counts = pd.DataFrame(depth_counts_list, columns=["depth", "n"])
    df_depths = pd.DataFrame(depths_rows)

    # logger.debug("Computed depth distribution: %s", depth_counts_list)
    return df_counts, df_depths


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
    stat_str = (
        "Number" if stat == "totals" else "%" if stat == "percentages" else "Measure"
    )
    return f"{stat_str} of classes"


def _get_plot_colors(df: pd.DataFrame) -> List[str]:
    """Get colors for bars"""
    default_color = "#6D8196"  # slate grey
    columns = df.columns.tolist()
    colors = []
    for col in columns:
        if col.startswith("CompLOINC"):
            if col == "CompLOINC-Primary":
                colors.append("#1f77b4")  # dark blue
            if col == "CompLOINC-Supplementary":
                colors.append("#aec7e8")  # light blue
            else:
                colors.append(default_color)  # todo: variations if rendering subtrees
        # Let matplotlib handle other colors automatically ( didn't work)
        # else:
        #     colors.append(None)
        # Alternative: Manually
        elif col == "LOINC":
            colors.append("#d62728")  # red
        elif col == "LOINC-SNOMED":
            colors.append("#2ca02c")  # green
        else:
            colors.append(default_color)
    return colors


def _save_plot(
    ont_depth_tables: Dict[str, pd.DataFrame],
    outdir: Union[Path, str],
    _filter: List[str],
    stat: str,
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
    merged.plot(kind="bar", stacked=False, ax=ax, color=_get_plot_colors(merged))
    ax.set_xlabel("Depth")
    ax.set_ylabel(y_lab)
    ax.set_title(f"Class depth distribution ({class_types_str})")
    ax.legend(title="Terminology")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300, bbox_inches="tight")
    # logger.debug("Saved plot to %s", outpath)

    return merged, os.path.basename(outpath)


def _save_markdown(
    tables_n_plots_by_filter_and_stat: Dict[
        Tuple[Tuple[str], str], Tuple[pd.DataFrame, str]
    ],
    outpath: Union[Path, str],
    template: str = md_template,
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
        table_str = df.to_markdown(tablefmt="github")
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


def _reformat_table(df: pd.DataFrame, stat: str, set_index_name=False) -> pd.DataFrame:
    """Convert the dataframe from a version that is good for plotting, to one that is good for a table."""
    df2 = df.copy()
    # Format numbers
    if stat == "totals":
        df2 = df2.applymap(lambda x: int(x) if pd.notna(x) else x)  # integers
    elif stat == "percentages":
        df2 = df2.applymap(
            lambda x: f"{float(x):.2g}" if pd.notna(x) else x
        )  # 2 significant figures
    else:
        raise ValueError(f"Unknown stat {stat}")
    # Set index name
    if set_index_name:
        df2.index.name = "Depth"
    return df2


def analyze_class_depth(
    loinc_path: Union[Path, str],
    loinc_snomed_path: Union[Path, str],
    comploinc_primary_path: Union[Path, str],
    comploinc_supplementary_path: Union[Path, str],
    labels_path: Union[Path, str],
    outpath_md: Union[Path, str],
    outpath_tsv: Union[Path, str],
    outdir_plots: Union[Path, str],
    variations=DEFAULTS["variations"],
    dont_convert_paths_to_abs=False,
):
    """Analyze classification depth"""
    # Resolve paths
    terminologies: Dict[str, Path]
    terminologies, outpath_md, outpath_tsv, outdir_plots, labels_path = (
        bundle_inpaths_and_update_abs_paths(
            loinc_path,
            loinc_snomed_path,
            comploinc_primary_path,
            comploinc_supplementary_path,
            dont_convert_paths_to_abs,
            outpath_md,
            outpath_tsv,
            outdir_plots,
            labels_path,
        )
    )
    if not os.path.exists(outdir_plots):
        os.makedirs(outdir_plots)

    # todo: do I want 2 sets of outputs, 1 per part model? maybe not
    # for mdl in ('primary', 'supplementary'):

    # Get sets of axioms by ontology and grand total and by ontology set
    ont_sets: Dict[str, Set[Tuple[str, str]]]
    tots_df, ont_sets = _subclass_axioms_and_totals(terminologies)
    # logger.debug("Loaded subclass axioms for %d ontologies", len(ont_sets))

    # Derive depths & save
    logger.debug(
        "Running class depth analysis.\n\nLog format:\nINCLUDED_CLASSES\n - TERMINOLOGY\n"
    )
    tables_n_plots_by_filter_and_stat: Dict[
        Tuple[Tuple[str], str], Tuple[pd.DataFrame, str]
    ] = {}
    depth_detail_frames: List[pd.DataFrame] = []
    for _filter in variations:
        logger.debug(" " + ", ".join(_filter))
        ont_depth_tables: Dict[str, pd.DataFrame] = {}
        ont_depth_pct_tables: Dict[str, pd.DataFrame] = {}
        # - get data for tables and plots
        for ont_name, axioms in ont_sets.items():
            logger.debug("  - " + ont_name)
            counts_df, detail_df = _depth_counts(
                axioms, _filter
            )  # main data processing func
            ont_depth_tables[ont_name] = counts_df
            if tuple(_filter) == tuple(CLASS_TYPES):
                detail_df.insert(0, "terminology", ont_name)
                depth_detail_frames.append(detail_df)
            ont_depth_pct_tables = _counts_to_pcts(ont_depth_tables)
        # - plots
        for stat, data in {
            "totals": ont_depth_tables,
            "percentages": ont_depth_pct_tables,
        }.items():
            df, plot_filename = _save_plot(data, outdir_plots, _filter, stat)
            df2: pd.DataFrame = _reformat_table(df, stat)
            tables_n_plots_by_filter_and_stat[(_filter, stat)] = (df2, plot_filename)

    # Save markdown
    _save_markdown(tables_n_plots_by_filter_and_stat, outpath_md)
    # Save depths TSV
    df_depths_all = pd.DataFrame()
    if depth_detail_frames:
        df_depths_all = pd.concat(depth_detail_frames, ignore_index=True)
        df_depths_all.sort_values(
            ["terminology", "depth", "class_type", "class"], inplace=True
        )
        # Add labels
        try:
            labels_df = pd.read_csv(labels_path, sep="\t")
            label_map = {
                f"<{cls}>" if not str(cls).startswith("<") else str(cls): lbl
                for cls, lbl in zip(labels_df.iloc[:, 0], labels_df.iloc[:, 1])
            }
            df_depths_all["label"] = df_depths_all["class"].map(label_map)
        except FileNotFoundError:
            logger.warning(f"Labels file not found: {labels_path}")
        except Exception as e:
            logger.warning(f"Could not add labels: {e}")
    else:
        logger.warning(
            f"{os.path.basename(outpath_tsv)} empty because no variation was processed which includes all "
            f"class types: {str(CLASS_TYPES)}"
        )
    df_depths_all.to_csv(outpath_tsv, sep="\t", index=False)


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
        "-T",
        "--outpath-tsv",
        type=str,
        default=DEFAULTS["outpath-tsv"],
        help="Outpath for TSV containing class depths.",
    )
    parser.add_argument(
        "-b",
        "--labels-path",
        type=str,
        default=DEFAULTS["labels-path"],
        help="TSV file mapping classes to labels.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.DEBUG),
        format="%(message)s",
    )
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    d: Dict = vars(args)
    del d["log_level"]
    return analyze_class_depth(**d)


if __name__ == "__main__":
    cli()
