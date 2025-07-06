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
from collections import defaultdict, deque, OrderedDict
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple, Union

import pandas as pd
from jinja2 import Template
from matplotlib import pyplot as plt, colormaps
from matplotlib.colors import to_hex

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
APP_DATA_DIR = THIS_DIR / 'app_data'
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
    "outpath-counts-tsv": "output/tmp/depth-processing-counts.tsv",
}
# If need smaller, cand o: ![Title]({{ outpath }}){: width="600px"}
logger = logging.getLogger(__name__)
md_template = """# Classification depth analysis 
This measures how deep into the hierarchy each class is. E.g. if the root of the hierarchy is TermA, and we have axioms
(TermC subClassOf TermB) and (TermB subClassOf TermA), then TermC is at depth 3, TermB is at depth 2, and TermA is at 
depth 1.

## Web application: https://comp-loinc.onrender.com/
Can take ~5 minutes to load when asleep. Sleeps when unused for 15 minutes. Contains interactive variations of these 
plots.

## Polyhierarchies
**Impact on class depths**  
CompLOINC and the LOINC and LOINC-SNOMED representations are all polyhierarchies. This means that classes can appear 
multiple times. For this analysis, we have decided to include every occurrence of a class in the counts. For example, if
a class appears in 3 subtrees, once at depth 3, and in two subtrees at depth 2, this class will be tallied twice at 
depth 2, and once at depth 3. 

**Disaggregating major subtrees**  
CompLOINC and LOINC have more than 1 top-level branches (AKA subhierachies or subtrees).

| Terminology | Hierarchy name   | Root URI                        |
|-------------|------------------|---------------------------------|
| CompLOINC   | SNOMED-Inspired  | https://loinc.org/138875005     |
| CompLOINC   | LoincTerm        | https://loinc.org/LoincTerm     |
| CompLOINC   | CompLOINC Groups | http://comploinc/group          |
| CompLOINC   | LoincPart        | https://loinc.org/LoincPart     |
| LOINC       | LOINC Categories | https://loinc.org/LoincCategory |
| LOINC       | LOINC Groups     | https://loinc.org/LoincGroup    |
| LOINC       | LoincPart        | https://loinc.org/LoincPart     |

Note, by subtree:
- *SNOMED-Inspired*: This is inspired largely by the LOINC-SNOMED Ontology.
- *LoincTerm*: LOINC has no Term hierarchy. It has a part hierarchy in the tree browser (https://loinc.org/tree/), which 
has parts as leaves. CompLOINC has a term hierarchy based on inference, combining the part hierarchy from the tree 
browser with supplementary or primary part model definitions.
- *LoincPart*: Exists in the LOINC tree browser, but not the official LOINC release. CompLOINC includes it as an 
optional subtree, largely obtained.
- *LOINC Groups*: Part of the LOINC release. See more: https://loinc.org/groups/. Terms are grouped, and some groups 
have groups. Also just for this analysis, we have added a single, novel https://loinc.org/LoincGroup root as a parent of
the otherwise top level groups in the LOINC release.
- *LOINC Categories*: Part of  the LOINC release, but not as formal as LOINC groups. These categories have no URIs, just 
labels. They are parents only of groups, not terms. From https://loinc.org/groups/: 'Category: A short description that 
identifies the general purpose of the group, such as "Flowsheet", "Reportable microbiology" or "Document ontology 
grouped by role and subject matter domain".'
- *CompLOINC Groups*: CompLOINC has a novel grouping class hierarchy. It does not utilize LOINC groups or categories in 
the LOINC release. The top level class is "http://comploinc/group", followed by a major group branch for each "property 
axis" (that is, a single part property or combination thereof), e.g. "http://comploinc/group/component/". Then, groups 
which are defined via these properties descend from there. 

**Two sets of outputs**  
In many cases, the best way to use each of these is not to use the entire polyhierarchy, but individual major subtrees. 
As such, we have produced a set of "by hierarchy" outputs, where these major subtrees have been disaggregated. The other
set of outputs aggregates all of the subtrees together in its counts. 

## Class types
We consider the following 3 types of classes: terms, parts, and groups. There are 3 sets of outputs with respect to 
class types: terms only, terms+groups, and terms+groups+parts.

There are also different kinds of possible axioms in CompLOINC, LOINC, and LOINC-SNOMED Ontology, with respect to class 
types.  

Homogeneous
- term --> term
- part --> part
- group --> group

Heterogeneous
- term --> part
- part --> term
- term --> group
- group --> term
- part --> group
- group --> part 

For a given filter of class type, we discard any subclass axioms where either the parent or child is not included. So, 
for example if we are only looking at 'terms', we only consider the term-->term axioms. If we are looking at 
'terms+groups', we retain axioms for term-->term, group-->group, term-->group, and group-->term.

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

**Dangling subtrees**  
There is also the case where, as a result of filtering class types, there end up being dangling sub-trees. For example, 
it could be that somewhere in a hierarchy, there is a term-group axiom, which is the root of its own subtree. If we are 
filtering to show terms only, then this axiom gets removed, leaving its descendants (subtree) dangling. This subtree may
contain term-term axioms, which would otherwise be kept, but since they are part of a dangling subtree, they are 
removed. 

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

---

## Counts, by data processing stage
The following table shows details in regards to number of clases and subclass axioms at various sequential stages of 
data preparation. We start with the raw inputs queried by the ontology, including all class types. Then, a few transient 
grouping clases just for this analysis were added to LOINC and CompLOINC. Next, we filter out the classes types that are
not needed for one of the sub-analyses. The filter is some combination of terms, parts, and/or groups. Finally, we 
remove any dangling classes, as well as any dangling subtrees that were caused by the previous filtration step.  

{{ etl_counts_table }}

"""
ROOT_URI_LABEL_MAP = {
    '<https://loinc.org/138875005>': 'SNOMED-Inspired',
    '<https://loinc.org/LoincTerm>': 'LoincTerm',
    '<https://loinc.org/LoincCategory>': 'LOINC Categories',
    '<https://loinc.org/LoincGroup>': 'LOINC Groups',
    '<http://comploinc/group>': 'CompLOINC Groups',
    '<https://loinc.org/LoincPart>': 'LoincPart',
}


def _log_counts(
    stage: str,
    pairs: Set[Tuple[str, str]],
    classes_set: Set[str],
    roots_set: Set[str],
    ont_name: str,
    filter_str: str,
) -> List[Dict[str, Union[str, int]]]:
    """Log counts for a processing stage and return rows for a dataframe."""

    stage_to_label = {
        "1: raw_input": "raw",
        "2: post_new_groupings": "after adding synthetic master grouping classes",
        "3: post_filters": "after class type filtration",
        "4: post_pruning": "after pruning dangling subtrees & nodes",
    }
    label = stage_to_label.get(stage, stage)
    logging.debug(f"    n {label}:")
    logging.debug(f"     - subclass pairs: {len(pairs):,}")
    logging.debug(f"     - classes: {len(classes_set):,}")
    logging.debug(f"     - roots: {len(roots_set):,}")

    rows = [
        {
            "filter": filter_str,
            "terminology": ont_name,
            "stage": stage,
            "metric": "subclass pairs",
            "value": len(pairs),
        },
        {
            "filter": filter_str,
            "terminology": ont_name,
            "stage": stage,
            "metric": "classes",
            "value": len(classes_set),
        },
        {
            "filter": filter_str,
            "terminology": ont_name,
            "stage": stage,
            "metric": "roots",
            "value": len(roots_set),
        },
    ]

    return rows


def _depth_counts(
    subclass_pairs: Set[Tuple[str, str]],
    ont_name: str,
    _filter: Iterable[str] = None,
    group_groups=True,
    rename_subtree_roots=True,
    includes_angle_brackets=True,
) -> Tuple[
    pd.DataFrame,
    pd.DataFrame,
    Dict[str, Tuple[pd.DataFrame, pd.DataFrame]],
    pd.DataFrame,
]:
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
        Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Tuple[pd.DataFrame, pd.DataFrame]], pd.DataFrame]:
            - The first DataFrame contains two columns:
                * ``depth``: The depth level within the class hierarchy.
                * ``n``: The count of classes at the corresponding depth.
            - The second DataFrame contains a row for each class-depth pair with
              the columns ``class`` and ``depth``. In a polyhierarchy a class can
              occur at multiple depths and will be returned multiple times.
            - The final DataFrame summarises counts of subclass pairs, classes,
              and roots at key processing stages.
    """
    # logger.debug("Calculating depth counts for %d subclass pairs with filter %s", len(subclass_pairs), _filter)
    # Validation
    if _filter and any([x not in CLASS_TYPES for x in _filter]):
        raise ValueError(f"Filter must be one of {CLASS_TYPES}")

    filter_str = ", ".join(_filter) if _filter else ""
    etl_counts_rows: List[Dict[str, Union[str, int]]] = []

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
    etl_counts_rows.extend(
        _log_counts(
            "1: raw_input",
            subclass_pairs,
            classes,
            roots,
            ont_name,
            filter_str,
        )
    )

    # Group grouping classes
    if group_groups and 'groups' in _filter:
        if 'CompLOINC' in ont_name:
            classes, subclass_pairs, classes_by_type, child_parents, parent_children = \
                _add_synthetic_transient_groups_comploinc(subclass_pairs, classes_by_type, includes_angle_brackets)
        elif 'LOINC' == ont_name:
            classes, subclass_pairs, classes_by_type, child_parents, parent_children = \
                _add_synthetic_transient_groups_loinc(
                    subclass_pairs, child_parents, parent_children, includes_angle_brackets)
    roots = classes - set(child_parents.keys())
    etl_counts_rows.extend(
        _log_counts(
            "2: post_new_groupings",
            subclass_pairs,
            classes,
            roots,
            ont_name,
            filter_str,
        )
    )

    # Preserve lookups prior to filtering to detect dangling roots later
    child_parents_before = child_parents

    # Filter by class types included in this analysis
    classes_post_filter, subclass_pairs_post_filter, child_parents, parent_children = _filter_classes(
        subclass_pairs, _filter, classes_by_type)
    roots = classes_post_filter - set(child_parents.keys())
    etl_counts_rows.extend(
        _log_counts(
            "3: post_filters",
            subclass_pairs_post_filter,
            classes_post_filter,
            roots,
            ont_name,
            filter_str,
        )
    )

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
    # Remove dangling nodes
    roots = set([x for x in roots if parent_children[x]])
    etl_counts_rows.extend(
        _log_counts(
            "4: post_pruning",
            subclass_pairs_post_filter,
            classes_post_filter,
            roots,
            ont_name,
            filter_str,
        )
    )

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

    # Get counts by subtree / major hierarchy
    by_subtree: Dict[str, Tuple[pd.DataFrame, pd.DataFrame]] = {}
    if len(roots) > 1:
        for root in roots:
            nodes = _get_subtree_nodes(root, parent_children)
            df_depths_i = df_depths[df_depths['class'].isin(nodes)].copy()
            df_counts_i = df_depths_i.groupby('depth').size().reset_index(name='n')
            by_subtree[root] = (df_counts_i, df_depths_i)
    # elif len(roots) == 1:
        # by_subtree[list(roots)[0]] = (df_counts, df_depths)
    else:
        by_subtree['hierarchy'] = (df_counts, df_depths)

    if rename_subtree_roots:
        by_subtree = {ROOT_URI_LABEL_MAP.get(k, k): v for k, v in by_subtree.items()}
        # Not most elegant solution. Mainly for plotting later. Disambiguate from same/similar tree in CompLOINC.

    # logger.debug("Computed depth distribution: %s", depth_counts_list)
    return df_counts, df_depths, by_subtree, pd.DataFrame(etl_counts_rows)


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
    classes_post_filter: Set[str],
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
    roots_before: Set[str] = classes_post_filter - set(child_parents_before.keys())
    roots_after: Set[str] = classes_post_filter - set(child_parents.keys())
    dangling_roots = roots_after - roots_before
    if not dangling_roots:
        return classes_post_filter, filtered_pairs, child_parents, parent_children

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

    classes_post_filter -= to_remove
    filtered_pairs = {
        (ch, par)
        for ch, par in filtered_pairs
        if ch not in to_remove and par not in to_remove
    }
    child_parents, parent_children = _get_parent_child_lookups(filtered_pairs)
    return classes_post_filter, filtered_pairs, child_parents, parent_children


def _add_synthetic_transient_groups_loinc(
    subclass_pairs: Set[Tuple[str, str]], child_parents: Dict[str, Set[str]],
    parent_children: Dict[str, Set[str]], includes_angle_brackets=True,
) -> Tuple[Set[str], Set[Tuple[str, str]], Dict[str, Set], Dict[str, Set], Dict[str, Set]]:
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
    subclass_pairs2 = subclass_pairs.union(subclass_pairs_group_groups)
    classes, classes_by_type, child_parents, parent_children = _parse_subclass_pairs(
        subclass_pairs2, includes_angle_brackets)
    return classes, subclass_pairs2, classes_by_type, child_parents, parent_children


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
    subclass_pairs2 = subclass_pairs.union(subclass_pairs_group_groups)
    # todo: mutate like this, or make alt versions so we can compare before/after easily?
    classes, classes_by_type, child_parents, parent_children = _parse_subclass_pairs(
        subclass_pairs2, includes_angle_brackets)
    return classes, subclass_pairs2, classes_by_type, child_parents, parent_children


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
    """Get colors for bars.

    When columns contain ``"ONT - SUBTREE"`` style labels, each subtree will get
    a different shade of the ontology's base colour. Otherwise the base colour is
    used directly.
    """

    default_color = "#6D8196"  # slate grey
    columns = df.columns.tolist()
    colors: List[str] = []

    # For "merged" variations
    base_colours = {
        "LOINC": "#d62728",  # medium/deep red
        "LOINC-SNOMED": "#2ca02c",  # medium green
        "CompLOINC-Primary": "#1f77b4",  # mid-tone blue
        "CompLOINC-Supplementary": "#1f38b4",  # dark blue
        # "CompLOINC-Supplementary": "#ff7f0e",  # orange
    }
    # For "by hierarchy" variations
    cmaps = {
        "LOINC": colormaps.get_cmap("Reds"),
        "LOINC-SNOMED": colormaps.get_cmap("Greens"),
        "CompLOINC-Primary": colormaps.get_cmap("Blues"),
        "CompLOINC-Supplementary": colormaps.get_cmap("Purples"),
    }

    # Group columns by ontology
    ont_to_cols: Dict[str, List[str]] = defaultdict(list)
    for col in columns:
        ont = col.split(" - ")[0]
        ont_to_cols[ont].append(col)

    # Generate colours
    col_colour_map: Dict[str, str] = {}
    for ont, cols in ont_to_cols.items():
        n = len(cols)
        if n == 1:
            colour = base_colours.get(ont, default_color)
            col_colour_map[cols[0]] = colour
            continue

        cmap = cmaps.get(ont, colormaps.get_cmap("Greys"))
        for i, col in enumerate(cols):
            # Spread shades between set ranges so they remain distinguishable. LOINC shades were previously too extreme
            # in brightness variation, so we constrain the range for it alone.
            start, end = (0.3, 0.9) if ont != "LOINC" else (0.6, 1)
            frac = start + ((end - start) * (i / max(n - 1, 1)))
            col_colour_map[col] = to_hex(cmap(frac))

    for col in columns:
        colors.append(col_colour_map.get(col, default_color))

    return colors


def _save_plot(
    ont_depth_tables: Dict[str, pd.DataFrame],
    outdir: Union[Path, str],
    _filter: Iterable[str],
    stat: str,
    disaggregated_subtrees: bool = False,
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
        disaggregated_subtrees: Set to True if the data/plot is not just 1 set of measures / bar per terminology, but
         per major hierarchy. This will change labels and optimize rendering.

    todo: For 'by hierarchy' change plot & lagend to be "TERMINOLOGY: SUBTREE" rather than "TERMINOLOGY - SUBTREE"
    """
    if stat not in ("totals", "percentages"):
        raise ValueError(f'`stat` arg must be either "totals" or "percentages".')
    # logger.debug("Saving plot for stat %s with filter %s", stat, _filter)
    # Labels and paths
    class_types_str = f'{", ".join(_filter)}'
    y_lab = _get_stat_label(stat)
    suffix = "_by-hierarchy" if disaggregated_subtrees else ""
    outpath = outdir / f'plot-class-depth{suffix}_{"-".join(_filter)}_{stat}.png'

    # Data prep
    data_for_plot = {}
    for name, df in ont_depth_tables.items():
        cols = list(df.columns)
        # Create a series with depth as index and n as values
        data_for_plot[name] = df.set_index(cols[0])[cols[1]]
    merged = pd.DataFrame(data_for_plot).fillna(0)
    merged.index.name = "Depth"

    # Ensure deterministic column ordering.
    term_order = [
        "LOINC",
        "LOINC-SNOMED",
        "CompLOINC-Primary",
        "CompLOINC-Supplementary",
    ]

    def _sort_key(col: str):
        if disaggregated_subtrees:
            ont, subtree = col.split(" - ", 1)
        else:
            ont, subtree = col, ""
        try:
            ont_idx = term_order.index(ont)
        except ValueError:
            ont_idx = len(term_order)
        return (ont_idx, subtree.lower())

    merged = merged[sorted(merged.columns, key=_sort_key)]

    # Create bar chart
    bars_direction_map = {'vertical': 'bar', 'horizontal': 'barh'}
    bars_direction = 'horizontal' if disaggregated_subtrees else 'vertical'
    fig_height = 15 if disaggregated_subtrees else 6
    fig, ax = plt.subplots(figsize=(10, fig_height))
    bar_width = 1 if disaggregated_subtrees else 0.8
    merged.plot(
        kind=bars_direction_map[bars_direction], stacked=False, ax=ax, color=_get_plot_colors(merged), width=bar_width)
    if disaggregated_subtrees:  # unsure why, but when bar direction is horizontal, changes to descending. this fixes it
        ax.invert_yaxis()
    ax.set_xlabel("Depth")
    ax.set_ylabel(y_lab)
    title_extra = ", by hierarchy" if disaggregated_subtrees else ""
    ax.set_title(f"Class depth distribution{title_extra} ({class_types_str})")
    if disaggregated_subtrees:
        # Can also lower a little more if overlaps w/ any bars; add: `bbox_to_anchor=(0.98, 0.4)`
        ax.legend(title="Terminology - Subtree", loc='center right')
    else:
        ax.legend(title="Terminology")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300, bbox_inches="tight")

    # Save a TSV of plot data. Used by web app.
    tsv_path = APP_DATA_DIR / f"plot-class-depth{suffix}_{'-'.join(_filter)}_{stat}.tsv"
    merged.to_csv(tsv_path, sep="\t")

    return merged, os.path.basename(outpath)


def _save_markdown(
    tables_n_plots_by_filter_and_stat: Dict[
        Tuple[bool, Iterable[str], str], Tuple[pd.DataFrame, str]
    ],
    outpath: Union[Path, str],
    etl_counts_df: pd.DataFrame = None,
    template: str = md_template,
):
    """Save results to markdown

    :param tables_n_plots_by_filter_and_stat: Keys are ``(disaggregate_roots, filter, stat)`` and values are
        ``(df, plot_filename)``. ``stat`` is one of ``['totals', 'percentages']`` and ``filter`` is one of the class
        type variations, e.g. ``('terms',)`` or ``('terms', 'groups')``.
    :param etl_counts_df: DataFrame summarising processing counts to render.

    Results are rendered in the following order:
    filter variation -> merged/by hierarchy -> counts/percentages.
    """
    # logger.debug("Saving markdown to %s", outpath)
    figs_by_title: "OrderedDict[str, Tuple[str, str]]" = OrderedDict()

    # Determine ordering of filters based on insertion order
    filter_order: List[Iterable[str]] = []
    for disagg, filt, _ in tables_n_plots_by_filter_and_stat.keys():
        if filt not in filter_order:
            filter_order.append(filt)

    # Build ordered sections: per filter -> aggregated/by hierarchy -> stat
    for filt in filter_order:
        for disagg in (False, True):
            for stat in ("totals", "percentages"):
                key = (disagg, filt, stat)
                if key not in tables_n_plots_by_filter_and_stat:
                    continue
                df, plot_path = tables_n_plots_by_filter_and_stat[key]
                stat_label: str = _get_stat_label(stat)
                class_types_str = ", ".join(filt)
                title = f"{stat_label} ({class_types_str})"
                if disagg:
                    title += ", by hierarchy"

                plot_path = str(plot_path)
                table_str = df.to_markdown(tablefmt="github")
                figs_by_title[title] = (table_str, plot_path)
    # logger.debug("Markdown will contain %d sections", len(figs_by_title))
    # Render template
    etl_counts_table = ""
    if etl_counts_df is not None and not etl_counts_df.empty:
        etl_counts_table = etl_counts_df.to_markdown(tablefmt="github", index=False)

    template_obj = Template(template)
    rendered_markdown = template_obj.render(
        figs_by_title=figs_by_title,
        etl_counts_table=etl_counts_table,
    )

    # Write to file
    outpath = Path(outpath)  # TODO check etl counts if has data
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
    loinc_path: Union[Path, str] = DEFAULTS["loinc-path"],
    loinc_snomed_path: Union[Path, str] = DEFAULTS["loinc-snomed-path"],
    comploinc_primary_path: Union[Path, str] = DEFAULTS["comploinc-primary-path"],
    comploinc_supplementary_path: Union[Path, str] = DEFAULTS["comploinc-supplementary-path"],
    labels_path: Union[Path, str] = DEFAULTS["labels-path"],
    outpath_md: Union[Path, str] = DEFAULTS["outpath-md"],
    outdir_plots: Union[Path, str] = DEFAULTS["outdir-plots"],
    outpath_counts_tsv: Union[Path, str] = DEFAULTS["outpath-counts-tsv"],
    # Non CLI args
    outpath_tsv_pattern: Union[Path, str] = DEFAULTS["outpath-tsv-pattern"],
    variations: Iterable[Iterable[str]] = DEFAULTS["variations"],
    dont_convert_paths_to_abs: bool = False,
):
    """Analyze classification depth"""
    # Resolve paths
    terminologies: Dict[str, Path]
    terminologies, outpath_md, outpath_tsv_pattern, outdir_plots, labels_path, outpath_counts_tsv = (
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
            outpath_counts_tsv,
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
        Tuple[bool, Iterable[str], str], Tuple[pd.DataFrame, str]
    ] = {}
    depth_by_class_dfs: List[pd.DataFrame] = []  # for TSVs
    etl_stage_count_dfs: List[pd.DataFrame] = []

    # TODO temp
    # variations = [('terms', 'groups', 'parts'), ]
    # ont_sets = {k: v for k, v in ont_sets.items() if k == 'CompLOINC-Primary'}

    for _filter in variations:
        logger.debug(" " + ", ".join(_filter))
        ont_depth_tables: Dict[str, pd.DataFrame] = {}
        ont_depth_tables_by_subtree: Dict[str, pd.DataFrame] = {}
        ont_depth_pct_tables: Dict[str, pd.DataFrame] = {}
        ont_depth_pct_tables_by_subtree: Dict[str, pd.DataFrame] = {}
        # - get data for tables and plots
        for ont_name, axioms in ont_sets.items():
            logger.debug(f"  - {ont_name}")
            counts_df, depth_by_class_df, by_subtree, etl_counts_df = _depth_counts(
                axioms, ont_name, _filter
            )  # main data processing func
            # Main outputs: plots & tables
            ont_depth_tables[ont_name] = counts_df
            for subtree_name, (counts_sub, _) in by_subtree.items():
                key = f"{ont_name} - {subtree_name}" if subtree_name != 'hierarchy'\
                    else ont_name  # improves labels if just 1 root
                ont_depth_tables_by_subtree[key] = counts_sub
            ont_depth_pct_tables = _counts_to_pcts(ont_depth_tables)
            ont_depth_pct_tables_by_subtree = _counts_to_pcts(ont_depth_tables_by_subtree)
            # TSV outputs
            if tuple(_filter) == tuple(CLASS_TYPES):
                depth_by_class_df.insert(0, "terminology", ont_name)
                depth_by_class_dfs.append(depth_by_class_df)
            etl_stage_count_dfs.append(etl_counts_df)
        # - plots
        # Create plots and tables for both aggregate and per-subtree views
        for stat, data, disag in [
            ("totals", ont_depth_tables, False),
            ("percentages", ont_depth_pct_tables, False),
            ("totals", ont_depth_tables_by_subtree, True),
            ("percentages", ont_depth_pct_tables_by_subtree, True),
        ]:
            df, plot_filename = _save_plot(
                data, outdir_plots, _filter, stat, disaggregated_subtrees=disag
            )
            df2: pd.DataFrame = _reformat_table(df, stat)
            tables_n_plots_by_filter_and_stat[(disag, _filter, stat)] = (
                df2,
                plot_filename,
            )

    # Save
    # - Data processing stage counts
    etl_counts_df_all = pd.concat(etl_stage_count_dfs, ignore_index=True)
    etl_counts_df_all.to_csv(outpath_counts_tsv, sep="\t", index=False)  # redundant
    # - Markdown
    _save_markdown(tables_n_plots_by_filter_and_stat, outpath_md, etl_counts_df_all)  # TODO temp: etl df empty?
    # todo: also output TSVs for when disaggregate by roots, too?
    # - Depths TSVs
    _save_depths_tsvs(depth_by_class_dfs, labels_path, outpath_tsv_pattern)  # for manual analysis / troubleshooting


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
        "-c",
        "--outpath-counts-tsv",
        type=str,
        default=DEFAULTS["outpath-counts-tsv"],
        help="Path to TSV of processing stage counts.",
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
