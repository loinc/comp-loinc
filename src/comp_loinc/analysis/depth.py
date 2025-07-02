"""Analyze classification depth

todo's
 if including, disaggregate groups by type? e.g.:
  http://comploinc//group/component/LP...
  http://comploinc//group/system/LP...
 inner bar stacking: IDK if this is possible, but it'd be great to have a separate bar for each source, and then the
 source bars are actually stacked, depending on class type. To do this, I'd need to pass classes_by_type as well to the
 plot function.
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
    # Non-CLI args
    "variations": (("terms",), ("terms", "groups"), ("terms", "groups", "parts")),
    "outpath-tsv-pattern": "output/tmp/depth-by-class-{}.tsv",
}
# If need smaller, cand o: ![Title]({{ outpath }}){: width="600px"}
logger = logging.getLogger(__name__)
md_template = """# Classification depth analysis 
This measures how deep into the hierarchy each class is. E.g. if the root of the hierarchy is TermA, and we have axioms
(TermC subClassOf TermB) and (TermB subClassOf TermA), then TermC is at depth 3, TermB is at depth 2, and TermA is at 
depth 1.

## Polyhierarchies and their effect on counts
CompLOINC and the LOINC and LOINC-SNOMED representations are all polyhierarchies. This means that classes can appear 
multiple times. For this analysis, we have decided to include every occurrence of a class in the counts. For example, if
a class appears in 3 subtrees, once at depth 3, and in two subtrees at depth 2, this class will be tallied twice at 
depth 2, and once at depth 3. 

## Dangling classes  
Dangling classes are not represented here in this class depth analysis.

**Ramifications for CompLOINC**  
The only dangling classes in CompLOINC are dangling parts from the LOINC release, specifically the ones which CompLOINC 
was not able to find matches. Those classes are not represented here.

**Ramifications for LOINC representation**  
Note that this results in LOINC showing that it has 0 terms at any depths, as LOINC has no term hierarchy. The only 
hierarchies that exist in LOINC are a shallow grouping hierarchy (represented by CSVs in `AccessoryFiles/GroupFile/` in 
the LOINC release, and the part hierarchy, which is not represented in the release, but only exists in the LOINC tree 
browser (https://loinc.org/tree/). Regarding parts, there are also a large number of those that are dangling even after 
when considering all of the tree browser hierarchies, and those as well are not represented here. 

## LOINC representation
LOINC itself does not have an `.owl` representaiton, but for this analysis we constructed one. The following are some 
caveats about the representation, by class type.

**Terms**  
LOINC defines no term-term subclass relationships. It only defines term-group relationships. Therefore, for the analyses 
where we consider only terms, the term-group subclass axioms are intentionally dropped, resulting in no axioms at all, 
and therefore rendering LOINC to show 0 classes at any depth.  

**Parts**  
Some variations of the outputs include part classes. The LOINC release does not establish part-part subclass 
relationships. These relationships are obtained by exports from the LOINC tree browser: https://loinc.org/tree/.

**Groups**  
Some variations of the outputs include parts group classes. While the LOINC release does not have term-term or part-part
subclass axioms, it does have such "axioms" for group-group and term-group. `Group.csv`: Defines relationships between 
groups and parent groups. `GroupLoincTerms.csv`: Defines relationships between terms (`LoincNumber` column) and groups 
(`GroupId` column). Also defines relationships between categories (`Category` column) and groups/terms. For this 
analysis, we consider categories to be just another kind of group. This results in our representation of LOINC groups 
being a polyhierarchy, as terms and groups can fall under other groups, but also can fall under categories. Thus, such 
terms and groups will be counted multiple times in the depths counts. 

More information about LOINC groups can be found here: https://loinc.org/groups/

---

{% for title, table_and_plot_path in figs_by_title.items() %}
{% set table, plot_path = table_and_plot_path %}
## {{ title }}
![{{ title }}]({{ plot_path }})

{{ table }}

{% endfor %}
"""


def _depth_counts(
    subclass_pairs: Set[Tuple[str, str]],
    _filter: List[str] = None,
    by_root: bool = False,
) -> Tuple[Union[pd.DataFrame, Dict[str, pd.DataFrame]], pd.DataFrame]:
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
        Tuple[pd.DataFrame | Dict[str, pd.DataFrame], pd.DataFrame]:
            - The first element is either a DataFrame containing ``depth``/``n``
              or a dictionary mapping each root to such a DataFrame when
              ``by_root`` is ``True``.
            - The second DataFrame contains a row for each class-depth pair with
              the columns ``class`` and ``depth``. In a polyhierarchy a class can
              occur at multiple depths and will be returned multiple times. When
              ``by_root`` is ``True`` this DataFrame also contains a ``root``
              column.
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

    # Get all classes on both sides of all subclass axioms
    classes_all = set(children.keys()) | set(parents.keys())
    logging.debug(f"    n classes: {len(classes_all):,}")

    # Filter, by axiom types for thi sanalysis
    classes_by_type: Dict[str, Set] = _disaggregate_classes(classes_all)
    classes_filtered = _filter_classes(_filter, classes_by_type)
    logging.debug(f"    n after class type filtration: {len(classes_filtered):,}")

    # Find roots (classes with no parents)
    roots = classes_filtered - set(parents.keys())
    logging.debug(f"    n roots: {len(roots):,}")

    # # TODO temp
    # for root in roots:
    #     print(root)

    # Calculate depth using BFS
    # A class can have multiple depths if the ontology is a polyhierarchy.
    if by_root:
        depths_sets_by_root: Dict[str, Dict[str, Set[int]]] = defaultdict(
            lambda: defaultdict(set)
        )
        queue = deque([(root, 1, root) for root in roots])
        while queue:
            cls, depth, root_id = queue.popleft()
            if depth not in depths_sets_by_root[root_id][cls]:
                depths_sets_by_root[root_id][cls].add(depth)
                for child in children[cls]:
                    queue.append((child, depth + 1, root_id))
        depths_by_root: Dict[str, Dict[str, List[int]]] = {}
        for r, dsets in depths_sets_by_root.items():
            depths_by_root[r] = {cls: sorted(list(ds)) for cls, ds in dsets.items()}
    else:
        depths_sets: Dict[str, Set[int]] = defaultdict(set)
        queue = deque([(root, 1) for root in roots])
        while queue:
            cls, depth = queue.popleft()
            if depth not in depths_sets[cls]:
                depths_sets[cls].add(depth)
                for child in children[cls]:
                    queue.append((child, depth + 1))
        depths: Dict[str, List[int]] = {
            cls: sorted(list(depths)) for cls, depths in depths_sets.items()
        }

    # Count classes at each depth
    # - Create reverse lookup: class_id -> class_type
    class_to_type = {}
    for class_type, class_set in classes_by_type.items():
        for class_id in class_set:
            class_to_type[class_id] = class_type
    # - Get counts
    if by_root:
        counts_by_root: Dict[str, pd.DataFrame] = {}
        depths_rows = []
        for root_id, depth_map in depths_by_root.items():
            depth_counts = defaultdict(int)
            for cls_id, depth_list in depth_map.items():
                class_type: str = class_to_type.get(cls_id, "unknown")
                for depth in depth_list:
                    depth_counts[depth] += 1
                    depths_rows.append(
                        {
                            "root": root_id,
                            "class_type": class_type,
                            "class": cls_id,
                            "depth": depth,
                        }
                    )
            depth_counts_list = sorted(depth_counts.items())
            counts_by_root[root_id] = pd.DataFrame(
                depth_counts_list, columns=["depth", "n"]
            )
        df_depths = pd.DataFrame(depths_rows)
        return counts_by_root, df_depths
    else:
        depth_counts = defaultdict(int)
        depths_rows = []
        for cls_id, depth_list in depths.items():
            class_type: str = class_to_type.get(cls_id, "unknown")
            for depth in depth_list:
                depth_counts[depth] += 1
                depths_rows.append(
                    {"class_type": class_type, "class": cls_id, "depth": depth}
                )
        depth_counts_list = sorted(depth_counts.items())
        df_counts = pd.DataFrame(depth_counts_list, columns=["depth", "n"])
        df_depths = pd.DataFrame(depths_rows)
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


def _save_depths_tsvs(
    dfs: List[pd.DataFrame],
    labels_path: Union[Path, str],
    outpath_pattern: Union[Path, str],
):
    """Save depths TSVs."""
    # todo: this combining into one df is no longer needed
    df_depths_all = pd.DataFrame()
    if dfs:
        df_depths_all = pd.concat(dfs, ignore_index=True)
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
            logger.warning(
                f"Labels file not found: {labels_path}. Couldn't add labels to 'Classes by depth' TSVs"
            )
    else:
        logger.warning(
            f"'Classes by depth' TSVs empty because no variation was processed which includes all "
            f"class types: {str(CLASS_TYPES)}"
        )
    # df_depths_all.to_csv(outpath_tsv, sep="\t", index=False)  # opting not to save because ~>200mb
    # todo: would be nice maybe to have these variations in the makefile target, but idk
    for terminology, group_df in df_depths_all.groupby("terminology"):
        del group_df["terminology"]
        group_df.to_csv(str(outpath_pattern).format(terminology), sep="\t", index=False)


def analyze_class_depth(
    # CLI args
    loinc_path: Union[Path, str],
    loinc_snomed_path: Union[Path, str],
    comploinc_primary_path: Union[Path, str],
    comploinc_supplementary_path: Union[Path, str],
    labels_path: Union[Path, str],
    outpath_md: Union[Path, str],
    outdir_plots: Union[Path, str],
    # Non CLI args
    outpath_tsv_pattern: Union[Path, str] = DEFAULTS["outpath-tsv-pattern"],
    variations=DEFAULTS["variations"],
    dont_convert_paths_to_abs=False,
    by_root: bool = False,
):
    """Analyze classification depth

    If ``by_root`` is ``True`` the results are split by each root of every
    terminology, producing a column per root rather than per terminology.
    """
    # Resolve paths
    terminologies: Dict[str, Path]
    terminologies, outpath_md, outpath_tsv_pattern, outdir_plots, labels_path = (
        bundle_inpaths_and_update_abs_paths(
            # Inpaths to bundle into `terminologies`
            loinc_path,
            loinc_snomed_path,
            comploinc_primary_path,
            comploinc_supplementary_path,
            dont_convert_paths_to_abs,
            # Path varibales to update
            outpath_md,
            outpath_tsv_pattern,
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
    depth_by_class_dfs: List[pd.DataFrame] = []
    for _filter in variations:
        logger.debug(" " + ", ".join(_filter))
        ont_depth_tables: Dict[str, pd.DataFrame] = {}
        ont_depth_pct_tables: Dict[str, pd.DataFrame] = {}
        # - get data for tables and plots
        for ont_name, axioms in ont_sets.items():
            logger.debug("  - " + ont_name)
            counts_res, depth_by_class_df = _depth_counts(
                axioms, _filter, by_root=by_root
            )  # main data processing func
            if by_root:
                assert isinstance(counts_res, dict)
                for root_uri, cdf in counts_res.items():
                    key = f"{ont_name}__{root_uri.strip('<>')}"
                    ont_depth_tables[key] = cdf
            else:
                assert not isinstance(counts_res, dict)
                ont_depth_tables[ont_name] = counts_res
            if tuple(_filter) == tuple(CLASS_TYPES):
                depth_by_class_df.insert(0, "terminology", ont_name)
                depth_by_class_dfs.append(depth_by_class_df)
            ont_depth_pct_tables = _counts_to_pcts(ont_depth_tables)
        # - plots
        for stat, data in {
            "totals": ont_depth_tables,
            "percentages": ont_depth_pct_tables,
        }.items():
            df, plot_filename = _save_plot(data, outdir_plots, _filter, stat)
            df2: pd.DataFrame = _reformat_table(df, stat)
            tables_n_plots_by_filter_and_stat[(_filter, stat)] = (df2, plot_filename)

    # Save
    _save_markdown(tables_n_plots_by_filter_and_stat, outpath_md)
    _save_depths_tsvs(depth_by_class_dfs, labels_path, outpath_tsv_pattern)


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
    parser.add_argument(
        "--by-root",
        action="store_true",
        help="Split results by terminology root instead of by terminology.",
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
