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
    CL_GROUPING_CLASS_URI_STEMS, _disaggregate_classes_from_class_list,
    _get_parent_child_lookups, bundle_inpaths_and_update_abs_paths,
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

## CompLOINC representation
**Grouping class depths adjusted via synthetic "master grouping classes"**  
This particular analysis makes small modifications to the CompLOINC representation with respect to groups. In the 
CompLOINC .owl artefacts, there are many top-level grouping classes at the root of the ontology. These top level 
grouping classes come in various sets, one for each LOINC property or combination of properties used to construct the 
groups. For example, the grouping class http://comploinc/group/component/LP16066-0 falls under the "component" property 
axis, while the grouping class http://comploinc/group/component-system/LP7795-0-LP310005-6 falls under the 
"component+system" property (combination) axis. If these parts for these properties have no parents, then these grouping
classes will reside at the root of CompLOINC. However, for these classification depth analyses, we are comparing against 
other subtrees that have a single root, e.g. LoincPart or LoincTerm. Therefore, for the depths to be consistent along 
class types (terms, parts, groups), we have included "master grouping classes" just for this analysis. The top level for
all grouping clases is http://comploinc/group/ ("GRP"), and the children of this class are all of the roots of each 
property axis, e.g. http://comploinc/group/component/ ("GRP_CMP"), http://comploinc/group/component-system/ ("GRP_SYS"),
and so on.

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
    subclass_pairs: Set[Tuple[str, str]], ont_name: str, _filter: List[str] = None, group_groups=True,
    includes_angle_brackets=True
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Tuple[pd.DataFrame, pd.DataFrame]]]:
    """Provides a function to compute and analyze the hierarchical depth of classes based on their parent-child
    relationships, with an optional filter for specific class types.

    Args:
        subclass_pairs: A set of tuples where each tuple represents a child-parent relationship
         between classes.
        _filter: Optional list of strings specifying the class types to include in the filtering.
        group_groups: If True, will create a "GRP" master grouping class to group all "group by property" (e.g. GRP_CMP,
         GRP_SYS), and then all of the "CMP" and "SYS" grouping classes, etc, will also fall under their tree.

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

    # Get classes by type
    classes_by_type: Dict[str, Set]
    child_parents: Dict[str, Set[str]]
    parent_children: Dict[str, Set[str]]
    classes, classes_by_type, child_parents, parent_children = _parse_subclass_pairs(
        subclass_pairs, includes_angle_brackets)
    roots: Set[str] = classes - set(child_parents.keys())
    logging.debug(f"    n raw:")
    logging.debug(f"     - subclass pairs: {len(subclass_pairs):,}")
    logging.debug(f"     - classes: {len(classes):,}")
    logging.debug(f"     - roots: {len(roots):,}")

    # Group grouping classes
    if group_groups and 'groups' in _filter:
        if 'CompLOINC' in ont_name:
            classes, subclass_pairs, classes_by_type, child_parents, parent_children = \
                _add_synthetic_transient_groups_comploinc(subclass_pairs, classes_by_type, includes_angle_brackets)
        elif 'LOINC' == ont_name:
            classes, classes_by_type, child_parents, parent_children = _add_synthetic_transient_groups_loinc(
                subclass_pairs, child_parents, parent_children, includes_angle_brackets)
    roots = classes - set(child_parents.keys())
    logging.debug(f"    n after adding synthetic master grouping classes:")
    logging.debug(f"     - subclass pairs: {len(subclass_pairs):,}")
    logging.debug(f"     - classes: {len(classes):,}")
    logging.debug(f"     - roots: {len(roots):,}")

    # Preserve lookups prior to filtering to detect dangling roots later
    child_parents_before = child_parents

    # Filter by class types included in this analysis
    # TODO temp: before now, there are 4 roots. that's good. LoincPart will die later. but <http://comploinc/group>'
    #  needs to stay
    #  - prob prolly in this func
    classes_post_filter, subclass_pairs_post_filter, child_parents, parent_children = _filter_classes(
        subclass_pairs, _filter, classes_by_type)
    roots = classes_post_filter - set(child_parents.keys())
    logging.debug(f"    n after class type filtration:")
    logging.debug(f"     - subclass pairs: {len(subclass_pairs_post_filter):,}")
    logging.debug(f"     - classes : {len(classes_post_filter):,}")
    logging.debug(f"     - roots: {len(roots):,}")

    # TODO temp
    # TODO examine roots. there are lots of groups. but they lok like they have the pattern
    print('<http://comploinc/group>' in classes_post_filter)
    # only parts were filtered out. all start with LP, except 1 class: LoincPart
    # classes_filtered_out = classes - classes_post_filter  # mostly parts from what i can see
    # classes_filtered_out_non_parts = [x for x in classes_filtered_out if not x.startswith('<https://loinc.org/LP')]

    # Remove dangling subtrees: that became dangling due to filtering
    #  - This can happen e.g. because a term can have a part as a parent, and have a subtree of parts and/or terms.
    #    Filtering out parts will chop off its parent, leaving it and its descendants dangling.
    classes_post_filter, subclass_pairs_post_filter, child_parents, parent_children = _prune_dangling_subtrees(
        classes_post_filter,
        subclass_pairs_post_filter,
        child_parents,
        parent_children,
        child_parents_before,
    )

    # TODO temp
    print('<http://comploinc/group>' in classes_post_filter)
    grps_remain = [x for x in classes_post_filter if x.startswith('<http://comploinc/group>')]
    print('grps_remain', len(grps_remain))  # TODO: prob. only 1. so now it's dangling

    # Filter dangling nodes
    roots = set([x for x in roots if parent_children[x]])
    logging.debug(f"    n after pruning dangling subtrees & nodes:")
    logging.debug(f"     - subclass pairs: {len(subclass_pairs_post_filter):,}")
    logging.debug(f"     - classes: {len(classes_post_filter):,}")
    logging.debug(f"     - roots: {len(roots):,}")

    # TODO temp
    print('<http://comploinc/group>' in classes_post_filter)  # still true.

    # Calculate depth using BFS
    # A class can have multiple depths if the ontology is a polyhierarchy.
    depths_sets: Dict[str, Set[int]] = defaultdict(set)
    queue = deque([(root, 1) for root in roots])
    while queue:
        cls, depth = queue.popleft()
        if depth not in depths_sets[cls]:
            depths_sets[cls].add(depth)
            for child in parent_children[cls]:
                queue.append((child, depth + 1))
    depths: Dict[str, List[int]] = {  # type: ignore
        cls: sorted(list(depths)) for cls, depths in depths_sets.items()
    }

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

    # TODO: Handle polyhierarchy. disag roots. verify worked
    #  - write test?
    # Get counts by subtree / major hierarchy
    by_subtree: Dict[str, Tuple[pd.DataFrame, pd.DataFrame]] = {}
    if len(roots) > 1:
        for root in roots:
            nodes = _get_subtree_nodes(root, parent_children)
            df_depths_i = df_depths[df_depths['class'].isin(nodes)].copy()
            df_counts_i = df_depths_i.groupby('depth').size().reset_index(name='n')
            by_subtree[root] = (df_counts_i, df_depths_i)

    # TODO temp for analysis
    print('roots: ', roots)
    # noinspection PyUnusedLocal
    a_df_counts, a_df_depths, a_by_subtree = df_counts, df_depths, by_subtree
    # TODO temp
    for k in by_subtree:
        unique_class_types = set(by_subtree[k][1]['class_type'].unique())
        if unique_class_types != set(_filter):
            print(f'prolly OK. just wanna check filtering working everywhere. not all classes represented in all trees: {k}: {unique_class_types} | filter: {_filter}')
            # print()
    print('<http://comploinc/group>' in df_depths['class'].unique())  # False. Consistent (good) if its children removed

    # logger.debug("Computed depth distribution: %s", depth_counts_list)
    return df_counts, df_depths, by_subtree


def _get_subtree_nodes(root: str, parent_children: Dict[str, Set[str]]) -> Set[str]:
    """Get subtree of root (including root)"""
    seen, q = {root}, [root]
    while q:
        cur = q.pop()
        for ch in parent_children.get(cur, []):
            if ch not in seen:
                seen.add(ch)
                q.append(ch)
    return seen


def _prune_dangling_subtrees(
    classes_filtered: Set[str],
    filtered_pairs: Set[Tuple[str, str]],
    child_parents: Dict[str, Set[str]],
    parent_children: Dict[str, Set[str]],
    child_parents_before: Dict[str, Set[str]],
    # parent_children_before: Dict[str, Set[str]],
) -> Tuple[Set[str], Set[Tuple[str, str]], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Remove dangling subtrees introduced by filtering."""
    # Old way: was too restrictive for my taste here. This gets rid of dangling isolated nodes too, not just dangling
    # subtrees. We're getting rid of dangling isolated nodes further down.
    # https://claude.ai/chat/43ac6f3b-426b-434b-b44c-73bd67c96cca
    # roots_before = {
    #     c
    #     for c in classes_filtered
    #     if c not in child_parents_before and parent_children_before.get(c)
    # }
    #
    # roots_after = {
    #     c for c in classes_filtered if c not in child_parents and parent_children.get(c)
    # }
    roots_before: Set[str] = classes_filtered - set(child_parents_before.keys())
    roots_after: Set[str] = classes_filtered - set(child_parents.keys())
    dangling_roots = roots_after - roots_before
    if not dangling_roots:
        return classes_filtered, filtered_pairs, child_parents, parent_children

    to_remove = set(dangling_roots)
    queue = list(dangling_roots)
    while queue:
        cur = queue.pop()
        for ch in parent_children.get(cur, []):
            if ch in to_remove:
                continue
            remaining_parents = {
                p for p in child_parents.get(ch, set()) if p not in to_remove
            }
            if not remaining_parents:
                to_remove.add(ch)
                queue.append(ch)

    classes_filtered -= to_remove
    filtered_pairs = {
        (ch, par)
        for ch, par in filtered_pairs
        if ch not in to_remove and par not in to_remove
    }
    child_parents, parent_children = _get_parent_child_lookups(filtered_pairs)
    return classes_filtered, filtered_pairs, child_parents, parent_children


def _add_synthetic_transient_groups_loinc(
    subclass_pairs: Set[Tuple[str, str]], child_parents: Dict[str, Set[str]],
    parent_children: Dict[str, Set[str]], includes_angle_brackets=True,
) -> Tuple[Set[str], Dict[str, Set], Dict[str, Set], Dict[str, Set]]:
    """Add transient groups (just for this analysis) to LOINC"""
    cat_uri = 'https://loinc.org/LoincCategory'
    grp_uri = 'https://loinc.org/LoincGroup'
    cat_uri = f'<{cat_uri}>' if includes_angle_brackets else cat_uri
    grp_uri = f'<{grp_uri}>' if includes_angle_brackets else grp_uri
    classes = set(parent_children.keys()) | set(child_parents.keys())
    roots = classes - set(child_parents.keys())
    subclass_pairs_group_groups: Set[Tuple[str, str]] = set()
    for root in roots:
        if 'loinc.org/category/' in root:
            subclass_pairs_group_groups.add((root, cat_uri))
        elif 'loinc.org/LG' in root:
            subclass_pairs_group_groups.add((root, grp_uri))
        # else: Should just be 1 case left over: LoincPart, which is already a proper root
    subclass_pairs = subclass_pairs.union(subclass_pairs_group_groups)
    classes, classes_by_type, child_parents, parent_children = _parse_subclass_pairs(
        subclass_pairs, includes_angle_brackets)
    return classes, classes_by_type, child_parents, parent_children


def _add_synthetic_transient_groups_comploinc(
    subclass_pairs: Set[Tuple[str, str]], classes_by_type: Dict[str, Set], includes_angle_brackets=True
) -> Tuple[Set[str], Set[Tuple[str, str]], Dict[str, Set], Dict[str, Set], Dict[str, Set]]:
    """Add transient groups (just for this analysis) to CompLOINC

    Eventually we may do this in core CompLOINC, by adding these as actual classes. If so, we should remove this code,
    or easily deactivate it by setting the flag to false.
    E.g. "CMP_SYS" (component-system)
    Examples: http://comploinc//group/component-system/LP7795-0-LP310005-6 http://comploinc//group/component/LP16066-0
    """
    child_parents: Dict[str, Set[str]]
    parent_children: Dict[str, Set[str]]
    master_group_uri = 'http://comploinc/group'
    master_group_uri = f'<{master_group_uri}>' if includes_angle_brackets else master_group_uri
    subclass_pairs_group_groups: Set[Tuple[str, str]] = set()
    grouping_classes_by_prop: Dict[str, List[str]] = defaultdict(list)  # e.g. {"component": [URI_1, ..., URI_N]}
    for uri in classes_by_type["groups"]:
        fixed_uri = uri.replace('//', '/')  # as of 2025/07/02, there is a bug: http://comploinc//group/...
        property_axis = fixed_uri.split('/')[-2]  # e.g. "component-system" or "component"
        grouping_classes_by_prop[property_axis].append(uri)
    prop_axis_uris: List[str] = []
    for prop_axis, uris in grouping_classes_by_prop.items():
        # prop_axis_uri: e.g. http://comploinc/group/component-system
        prop_axis_uri = CL_GROUPING_CLASS_URI_STEMS[1] + '/' + prop_axis
        prop_axis_uri = f'<{prop_axis_uri}>' if includes_angle_brackets else prop_axis_uri
        prop_axis_uris.append(prop_axis_uri)
        subclass_pairs_group_groups |= {(uri, prop_axis_uri) for uri in uris}
    for prop_axis_uri in prop_axis_uris:
        subclass_pairs_group_groups.add((prop_axis_uri, master_group_uri))
    subclass_pairs = subclass_pairs.union(subclass_pairs_group_groups)
    # todo: mutate like this, or make alt versions so we can compare before/after easily?
    classes, classes_by_type, child_parents, parent_children = _parse_subclass_pairs(
        subclass_pairs, includes_angle_brackets)
    return classes, subclass_pairs, classes_by_type, child_parents, parent_children


def _parse_subclass_pairs(
    pairs: Set[Tuple[str, str]], includes_angle_brackets=True
) -> Tuple[Set[str], Dict[str, Set], Dict[str, Set], Dict[str, Set]]:
    """Get parents, children, and type disaggregation lookups"""
    # Build parent-child relationships
    child_parents, parent_children = _get_parent_child_lookups(pairs)

    # Get all classes on both sides of all subclass axioms
    classes = set(parent_children.keys()) | set(child_parents.keys())

    # Group classes by class type
    classes_by_type: Dict[str, Set] = _disaggregate_classes_from_class_list(classes, includes_angle_brackets)
    return classes, classes_by_type, child_parents, parent_children


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
        Tuple[bool, Tuple[str], str], Tuple[pd.DataFrame, str]
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
        disag_filter_stat,
        table_and_plot_path,
    ) in tables_n_plots_by_filter_and_stat.items():
        # Construct title
        disaggregate_roots, _filter, stat = disag_filter_stat
        # TODO: use disaggregate_roots
        # TODO temp: skip it for now
        if disaggregate_roots:
            continue

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


def _save_depths_tsvs(dfs: List[pd.DataFrame], labels_path: Union[Path, str], outpath_pattern: Union[Path, str]):
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
            logger.warning(f"Labels file not found: {labels_path}. Couldn't add labels to 'Classes by depth' TSVs")
    else:
        logger.warning(
            f"'Classes by depth' TSVs empty because no variation was processed which includes all "
            f"class types: {str(CLASS_TYPES)}"
        )
    # df_depths_all.to_csv(outpath_tsv, sep="\t", index=False)  # opting not to save because ~>200mb
    # todo: would be nice maybe to have these variations in the makefile target, but idk
    for terminology, group_df in df_depths_all.groupby('terminology'):
        del group_df['terminology']
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
):
    """Analyze classification depth"""
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

    # Get sets of axioms by ontology and grand total and by ontology set
    ont_sets: Dict[str, Set[Tuple[str, str]]]
    tots_df, ont_sets = _subclass_axioms_and_totals(terminologies)
    # logger.debug("Loaded subclass axioms for %d ontologies", len(ont_sets))

    # Derive depths & save
    logger.debug(
        "Running class depth analysis.\n\nLog format:\nINCLUDED_CLASSES\n - TERMINOLOGY\n"
    )
    tables_n_plots_by_filter_and_stat: Dict[
        Tuple[bool, Tuple[str], str], Tuple[pd.DataFrame, str]
    ] = {}
    depth_by_class_dfs: List[pd.DataFrame] = []

    # TODO temp
    variations = (('terms', 'groups'), )
    ont_sets = {k: v for k, v in ont_sets.items() if k == 'CompLOINC-Primary'}

    for _filter in variations:
        logger.debug(" " + ", ".join(_filter))
        ont_depth_tables: Dict[str, pd.DataFrame] = {}
        ont_depth_pct_tables: Dict[str, pd.DataFrame] = {}
        # - get data for tables and plots
        for ont_name, axioms in ont_sets.items():
            logger.debug(f"  - {ont_name}")
            # TODO use by_subtree
            #  - note if only 1 root, by_subtree will be {}
            counts_df, depth_by_class_df, by_subtree = _depth_counts(
                axioms, ont_name, _filter
            )  # main data processing func
            ont_depth_tables[ont_name] = counts_df
            if tuple(_filter) == tuple(CLASS_TYPES):
                depth_by_class_df.insert(0, "terminology", ont_name)
                depth_by_class_dfs.append(depth_by_class_df)
            ont_depth_pct_tables = _counts_to_pcts(ont_depth_tables)
        # - plots
        # TODO: temp. figure out what to do w/ this. maybe make a separate tables_n_plots_by_filter_and_stat for whether
        #  we're going over disaggregated stuff or not, idk
        disag_tf = True
        for stat, data in {
            "totals": ont_depth_tables,
            "percentages": ont_depth_pct_tables,
        }.items():
            # TODO: use disaggregate_roots
            df, plot_filename = _save_plot(data, outdir_plots, _filter, stat)
            # TODO: use disaggregate_roots
            df2: pd.DataFrame = _reformat_table(df, stat)
            tables_n_plots_by_filter_and_stat[(disag_tf, _filter, stat)] = (df2, plot_filename)

    # Save
    # TODO: update to also show a "by root" section
    #  - wiltables_n_plots_by_filter_and_stat now has a disaggregate_roots T/F key at start of tuple
    _save_markdown(tables_n_plots_by_filter_and_stat, outpath_md)
    # todo: also output TSVs for when disaggregate by roots, too?
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
