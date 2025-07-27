"""Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED.

Refs:
- https://claude.ai/chat/db6bb6d5-2ab5-4bc1-99cc-cffc9428fccd

todo's:
 - consider writing tables to TSV in addition to markdown. for easy ref / copying
 - can replace `tabulate` w/ `df.to_markdown(index=False, tablefmt="github")`. If so, remove package from poetry.
TODO: #1 Do I actually want a_minus_b or intersection? I thought I found that they were the same for my purposes, but
 now I'm not so sure.
"""

import os
import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
from tabulate import tabulate
from upsetplot import from_contents, UpSet

from comp_loinc.analysis.utils import bundle_inpaths_and_update_abs_paths, cli_add_inpath_args, \
    _subclass_axioms_and_totals, CLASS_TYPES, _filter_classes, _disaggregate_classes_from_class_list

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
MISSING_AXIOMS_PATH = PROJECT_ROOT / "output" / "tmp" / "missing_comploinc_axioms.tsv"
DESC = "Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."
DEFAULTS = {
    'loinc-path': 'output/tmp/subclass-rels-loinc-indirect-sc-axioms-included.tsv',
    'loinc-snomed-path': 'output/tmp/subclass-rels-loinc-snomed-indirect-sc-axioms-included.tsv',
    'comploinc-all-primary-path': \
'output/tmp/subclass-rels-comploinc-indirect-included-all-primary.tsv',
    'comploinc-all-supplementary-path': \
'output/tmp/subclass-rels-comploinc-indirect-included-all-supplementary.tsv',
    'comploinc-LOINC-primary-path': \
'output/tmp/subclass-rels-comploinc-indirect-included-LOINC-primary.tsv',
    'comploinc-LOINC-supplementary-path': \
'output/tmp/subclass-rels-comploinc-indirect-included-LOINC-supplementary.tsv',
    'comploinc-LOINCSNOMED-primary-path': \
        'output/tmp/subclass-rels-comploinc-indirect-included-LOINCSNOMED-primary.tsv',
    'comploinc-LOINCSNOMED-supplementary-path': \
        'output/tmp/subclass-rels-comploinc-indirect-included-LOINCSNOMED-supplementary.tsv',
    'outpath-md': 'documentation/subclass-analysis.md',
    'outdir-upset-plots': 'documentation',
    'class-types': ('terms',),
}
VARIATIONS: Dict[str, List[str]] = {
    'All sources, simple comparison': [
        'LOINC',
        'LOINC-SNOMED',
        'CompLOINC-all-Primary',
        'CompLOINC-all-Supplementary',
    ],
    'LOINC-specific enhancements': [
        'LOINC',
        'CompLOINC-LOINC-Primary',
        'CompLOINC-LOINC-Supplementary',
    ],
    'LOINC-SNOMED-specific enhancements': [
        'LOINC-SNOMED',
        'CompLOINC-LOINCSNOMED-Primary',
        'CompLOINC-LOINCSNOMED-Supplementary',
    ],
    'All sources, with CompLOINC disaggregations': [
        'LOINC',
        'LOINC-SNOMED',
        'CompLOINC-all-Primary',
        'CompLOINC-all-Supplementary',
        'CompLOINC-LOINC-Primary',
        'CompLOINC-LOINC-Supplementary',
        'CompLOINC-LOINCSNOMED-Primary',
        'CompLOINC-LOINCSNOMED-Supplementary',
    ],
}
logger = logging.getLogger(__name__)
md_template = """
# Subclass axiom analysis
This analysis shows set totals, intersections, and differences for subclass axioms in LOINC, CompLOINC, and
LOINC-SNOMED Ontology. This includes both direct and indirect axioms, "direct" meaning a direct parent/child
relationship, as opposed to "indirect", meaning a 2+ degree ancestor/descendant relationship.

## Data preparation
The only subclass axioms that were removed were those containing anonymous class expressions (bnodes) within
LOINC-SNOMED Ontology.

## Total subclass axioms
{{ tot_table }}

## Comparison: Upset plots
Horizontal bars represent the proportion of each terminology's subclass axioms relative to the total number of unique 
subclass axioms across all three resources. Vertical bars represent the proportion of subclass axioms belonging to 
specific combinations of terminology resources, with each column showing a distinct intersection pattern as indicated by
the connected dots below.

{% for variation in upset_variations %}
### {{ variation.title }}
{% for plot in variation.plots %}
![Upset plot]({{ plot.path }})
{% endfor %}

{{ variation.table }}

{% endfor %}

## Comparison: Merged tables
The following table only applies to the "All sources, simple comparison" variation. The other upset plot / intersection
analysis variations are not represented.

Cell formatting: (%intersection/a) / (n intersection) / (%intersection/b)

Where 'a' is the ontology represented by the row, and 'b' is the ontology represented by the column. 'n intersection' is
the total number of subclass axioms in the intersection of the two ontologies. '%intersection/' is the percentage of
subclass axioms in the intersection of the two ontologies, relative to the total number of subclass axioms in the
ontology.

{{ overlap_direct_merged_table }}

## Comparison: Individual tables
The following table only applies to the "All sources, simple comparison" variation. The other upset plot / intersection
analysis variations are not represented.

Meaning of table headers:

"a vs b": 'a' is the ontology on the left side of the comparison, and 'b' is the one on the right side.
- **tot a**: Total number of subclass axioms for ontology on left side of the comparison.
- **% (a-b)**: The percentage of "a - b" (the set difference of a and b) over the total number of axioms in a.
- **n (a-b)**: Total number of subclass axioms in the set difference of a and b.
- **intersection**: The length of the intersection
- **tot b**: Total number of subclass axioms for ontology on left side of the comparison.
- **n (b-a)**: Total number of subclass axioms in the set difference of b and a.
- **% (b-a)**: The percentage of "b - a" (the set difference of b and a) over the total number of axioms in b.

{% for ont_a in ontologies %}
### {{ ont_a }}
{% for ont_b in comparisons[ont_a] %}
#### vs {{ ont_b }}

{{ comparisons[ont_a][ont_b] }}

{% endfor %}
{% endfor %}
"""


def _write_markdown(
    lens_by_ont: Dict[str, str], ont_sets: Dict[str, Set[Tuple[str, str]]], outpath: Union[Path, str], 
    upset_variations_data: List[Dict]
    ):
    """Calculate and save tables

    todo: logic is similar for each for loop, iterating over ont_sets.items() 2x. Should we abstract?
    """
    # Process upset variations data - convert table DataFrames to markdown
    for variation_data in upset_variations_data:
        if variation_data['table'] is not None:
            variation_data['table'] = tabulate(variation_data['table'], headers='keys', tablefmt='pipe', showindex=False)
    # Create DF from tots
    tots_df = pd.DataFrame(list(lens_by_ont.items()), columns=['Terminology', 'n'])

    # Overlap/comparison: merged table
    overlap_direct_merged_rows = []
    for row_ont_name, row_axioms in ont_sets.items():
        overlap_row = {'': row_ont_name}
        for col_ont_name, col_axioms in ont_sets.items():
            if row_ont_name == col_ont_name:
                overlap_row[col_ont_name] = "-"
            else:
                # noinspection DuplicatedCode
                intersection = row_axioms.intersection(col_axioms)
                # Calculate percentages
                pct_row_in_col = len(intersection) / len(row_axioms) * 100 if len(row_axioms) > 0 else 0
                pct_col_in_row = len(intersection) / len(col_axioms) * 100 if len(col_axioms) > 0 else 0
                overlap_row[col_ont_name] = f"{pct_row_in_col:.1f}% / {len(intersection):,} / {pct_col_in_row:.1f}%"
        overlap_direct_merged_rows.append(overlap_row)
    overlap_direct_merged_df = pd.DataFrame(overlap_direct_merged_rows)

    # Overlap/comparison: individual tables
    comparison_tables = {}
    for ont_a_name, axioms_a in ont_sets.items():
        comparison_tables[ont_a_name] = {}
        for ont_b_name, axioms_b in ont_sets.items():
            if ont_a_name == ont_b_name:
                continue  # Skip self-comparison
            # Calculate differences and intersection
            a_minus_b = axioms_a.difference(axioms_b)
            b_minus_a = axioms_b.difference(axioms_a)
            # noinspection DuplicatedCode
            intersection = axioms_a.intersection(axioms_b)
            # TODO: #1 Do I actually want a_minus_b or intersection? I thought I found that they were the same for my
            #  purposes, but now I'm not so sure.
            # Calculate percentages
            pct_a_minus_b = len(a_minus_b) / len(axioms_a) * 100 if len(axioms_a) > 0 else 0
            pct_b_minus_a = len(b_minus_a) / len(axioms_b) * 100 if len(axioms_b) > 0 else 0

            # Create comparison dataframe
            comparison_df = pd.DataFrame([{
                '% (a-b)': f"{pct_a_minus_b:.1f}%",
                'n (a-b)': len(a_minus_b),
                'tot a': len(axioms_a),
                'intersection': len(intersection),
                'tot b': len(axioms_b),
                'n (b-a)': len(b_minus_a),
                '% (b-a)': f"{pct_b_minus_a:.1f}%",
            }])
            comparison_tables[ont_a_name][ont_b_name] = comparison_df

    # Render & save
    template = Template(md_template)
    tots_table = tabulate(tots_df, headers="keys", tablefmt="pipe", showindex=False)
    rendered_comparisons = {}
    for ont_a_name in comparison_tables:
        rendered_comparisons[ont_a_name] = {}
        for ont_b_name in comparison_tables[ont_a_name]:
            rendered_comparisons[ont_a_name][ont_b_name] = tabulate(
                comparison_tables[ont_a_name][ont_b_name], headers='keys', tablefmt='pipe', showindex=False)
    overlap_direct_merged_table = tabulate(overlap_direct_merged_df, headers='keys', tablefmt='pipe', showindex=False)
    markdown_output = template.render(
        tot_table=tots_table, ontologies=list(ont_sets.keys()), comparisons=rendered_comparisons,
        overlap_direct_merged_table=overlap_direct_merged_table, upset_variations=upset_variations_data)
    with open(outpath, 'w') as f:
        f.write(markdown_output)


def _interrogate_missing_axioms(
    ont_sets: Dict[str, Set[Tuple[str, str]]], outpath: Union[Path, str] = MISSING_AXIOMS_PATH
):
    """Analyze and save information about missing axioms in each data source.

    Args:
        ont_sets: Dictionary mapping ontology names to sets of subclass axioms
    """
    logger.debug("Interrogating non-inclusion of axioms in CompLOINC and its sources.")
    all_elements = set()
    for s in ont_sets.values():
        all_elements.update(s)
    logger.debug(f"- Total unique elements across all sets: {len(all_elements)}")

    # Find elements not in CompLOINC
    if "CompLOINC" in ont_sets:
        missing_from_comploinc = all_elements - ont_sets["CompLOINC"]
        logger.debug(
            f"- Elements missing from CompLOINC: "
            f"{len(missing_from_comploinc)} ({len(missing_from_comploinc) / len(all_elements) * 100:.2f}%)"
        )

        # Find where these missing elements exist
        missing_elements_source = {}
        for missing in missing_from_comploinc:
            sources = []
            for ont_name, elements in ont_sets.items():
                if missing in elements:
                    sources.append(ont_name)
            missing_elements_source[missing] = sources

        # Count by source combinations
        source_combinations = {}
        for sources in missing_elements_source.values():
            key = tuple(sorted(sources))
            source_combinations[key] = source_combinations.get(key, 0) + 1

        logger.debug("\n- Missing elements by source combinations:")
        for sources, count in sorted(source_combinations.items(), key=lambda x: x[1], reverse=True):
            logger.debug(f" - {', '.join(sources)}: {count} elements")

        rows = []
        for axiom, sources in missing_elements_source.items():
            rows.append(
                {
                    "child": axiom[0],
                    "parent": axiom[1],
                    "in_loinc": "LOINC" in sources,
                    "in_loinc-snomed": "LOINC-SNOMED" in sources,
                }
            )
        missing_df = pd.DataFrame(rows)
        try:
            missing_df.to_csv(outpath, index=False, sep="\t")
        except FileNotFoundError:
            logger.debug("Could not save missing axioms to tmp directory; doesn't exist.")


def _make_upset_plot(
    ont_sets: Dict[str, Set[Tuple[str, str]]], outpath: Union[Path, str], variation_name: Optional[str] = None
):
    """Make upset plot showing relationships between ontology subclass axioms.

    Args:
        ont_sets: Dictionary mapping ontology names to sets of subclass axioms
        outpath: Path to save the resulting plot
        
    Returns:
        Dict containing title, plot paths, and table data
    """
    # Convert sets to a dictionary format for upsetplot
    data = {}
    for ont_name, axiom_set in ont_sets.items():
        # Convert tuples to strings for easier handling
        data[ont_name] = {f"{parent}>{child}" for parent, child in axiom_set}

    # Generate the upset data structure
    upset_data = from_contents(data)
    
    def _create_table_from_upset_data(upset_data, max_rank=None):
        """Create a table representation of upset data."""
        # Get counts for each intersection pattern
        intersection_counts = upset_data.groupby(level=list(range(len(upset_data.index.names)))).size()
        
        # Sort by count (descending)
        sorted_counts = intersection_counts.sort_values(ascending=False)
        if max_rank:
            sorted_counts = sorted_counts.head(max_rank)
            
        table_rows = []
        for index, count in sorted_counts.items():
            # Create intersection pattern string
            if isinstance(index, tuple):
                # Each boolean in the tuple indicates set membership
                involved_sets = []
                for i, is_member in enumerate(index):
                    if is_member:
                        ont_name = upset_data.index.names[i]
                        involved_sets.append(ont_name)
            else:
                involved_sets = [str(index)]
            
            # Create intersection pattern like "Set1 ∩ Set2"
            intersection_pattern = " ∩ ".join(involved_sets) if len(involved_sets) > 1 else (involved_sets[0] if involved_sets else "Unknown")
            
            # Calculate percentage of total unique elements
            total_unique = len(set().union(*data.values()))
            percentage = (count / total_unique) * 100 if total_unique > 0 else 0
            
            table_rows.append({
                'Intersection': intersection_pattern,
                'Count': f"{count:,}",
                'Percentage': f"{percentage:.1f}%"
            })
        
        return pd.DataFrame(table_rows)
    
    # Check if we have more than 10 intersections
    
    outpath_obj = Path(outpath)
    result = {'title': '', 'plots': [], 'table': None}
    
    # Ideally do this dynamically. num_intersections did not work, as the DF is a list of all axioms
    num_bars = len(upset_data.index.unique())
    if num_bars > 10:
        # Save untruncated version first
        untruncated_outpath = Path(str(outpath_obj).replace('.png', '-untruncated.png'))
        
        # Create untruncated plot
        fig = plt.figure(figsize=(12, 8))
        title = f"SC axioms: {variation_name}" if variation_name else "SubClass Axiom intersections"
        fig.suptitle(title, fontsize=16)
        upset = UpSet(upset_data, sort_by="cardinality", show_percentages=True)
        upset.plot(fig=fig)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.savefig(untruncated_outpath, dpi=300, bbox_inches="tight")
        plt.close()
        
        # Create truncated version with max 10 bars
        fig = plt.figure(figsize=(12, 8))
        truncated_title = f"SC axioms: {variation_name}, top 10" if variation_name else "SubClass Axiom intersections, top 10"
        fig.suptitle(truncated_title, fontsize=16)
        upset = UpSet(upset_data, sort_by="cardinality", show_percentages=True, max_subset_rank=10)
        upset.plot(fig=fig)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.savefig(outpath, dpi=300, bbox_inches="tight")
        plt.close()
        
        # Set result data - use truncated version as primary
        result['title'] = truncated_title
        result['plots'] = [
            {'path': outpath_obj.name, 'type': 'truncated'},
            {'path': untruncated_outpath.name, 'type': 'untruncated'}
        ]
        result['table'] = _create_table_from_upset_data(upset_data, max_rank=10)
    else:
        # <= 10 intersections, save normally
        fig = plt.figure(figsize=(12, 8))
        title = f"SC axioms: {variation_name}" if variation_name else "SubClass Axiom intersections"
        fig.suptitle(title, fontsize=16)
        upset = UpSet(upset_data, sort_by="cardinality", show_percentages=True)
        upset.plot(fig=fig)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        plt.savefig(outpath, dpi=300, bbox_inches="tight")
        plt.close()
        
        # Set result data
        result['title'] = title
        result['plots'] = [{'path': outpath_obj.name, 'type': 'normal'}]
        result['table'] = _create_table_from_upset_data(upset_data)
    
    return result


def subclass_rel_analysis(
    loinc_path: Union[Path, str],
    loinc_snomed_path: Union[Path, str],
    comploinc_all_primary_path: Union[Path, str],
    comploinc_all_supplementary_path: Union[Path, str],
    comploinc_LOINC_primary_path: Union[Path, str],
    comploinc_LOINC_supplementary_path: Union[Path, str],
    comploinc_LOINCSNOMED_primary_path: Union[Path, str],
    comploinc_LOINCSNOMED_supplementary_path: Union[Path, str],
    outpath_md: Union[Path, str],
    outdir_upset_plots: Union[Path, str],
    class_types: Tuple[str, ...] = DEFAULTS['class-types'],
    dont_convert_paths_to_abs=False,
    variations: Dict[str, List[str]] = VARIATIONS,
):
    """Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."""
    terminologies: Dict[str, Path]
    lens_by_ont: Dict[str, str] = {}
    ont_sets_list: List[Dict[str, Set[Tuple[str, str]]]] = []
    upset_variations_data: List[Dict] = []
    
    for variation_name, terminology_inclusions in variations.items():
        variation_filename_stem = variation_name.replace(',', '').replace(' ', '-').lower()
        # Calculate intermediate vars
        terminologies, outpath_md, outdir_upset_plots = bundle_inpaths_and_update_abs_paths(
            loinc_path, loinc_snomed_path,
            comploinc_all_primary_path,
            comploinc_all_supplementary_path,
            comploinc_LOINC_primary_path,
            comploinc_LOINC_supplementary_path,
            comploinc_LOINCSNOMED_primary_path,
            comploinc_LOINCSNOMED_supplementary_path,
            terminology_inclusions, dont_convert_paths_to_abs, outpath_md, outdir_upset_plots)

        # Core calculations - load raw axioms first
        ont_sets_raw, lens_by_ont_raw = _subclass_axioms_and_totals(terminologies)
        
        # Apply class type filtering
        ont_sets = {}
        lens_by_ont_i = {}
        for ont_name, axioms in ont_sets_raw.items():
            # Apply string replacement to both elements of tuples
            # todo: Hacky. Ideally, we would update CompLOINC to use the latter prefix URI, which is used by SNOMED &
            #  LOINC-SNOMED Ontology.
            axioms = {
                (x[0].replace("http://snomed.info/sct/", "http://snomed.info/id/"),
                 x[1].replace("http://snomed.info/sct/", "http://snomed.info/id/"))
                for x in axioms
            }
            
            # Remove owl:Thing as root if exists
            owl_thing_axioms = {
                x for x in axioms if x[1] == "<http://www.w3.org/2002/07/owl#Thing>"
            }
            axioms = axioms - owl_thing_axioms
            
            # Get all classes from axioms
            all_classes = set()
            for child, parent in axioms:
                all_classes.add(child)
                all_classes.add(parent)
            
            # Disaggregate classes by type
            classes_by_type = _disaggregate_classes_from_class_list(all_classes, includes_angle_brackets=True)
            
            # Filter axioms by class types
            filtered_classes, filtered_axioms, _, _ = _filter_classes(axioms, class_types, classes_by_type)
            
            ont_sets[ont_name] = filtered_axioms
            lens_by_ont_i[ont_name] = f'{len(filtered_axioms):,}'
        
        ont_sets_list.append(ont_sets)
        for ont, lens in lens_by_ont_i.items():
            lens_by_ont[ont] = lens

        # Plots
        outpath_upset_plot = outdir_upset_plots / f'upset-plot_{variation_filename_stem}.png'
        plot_data = _make_upset_plot(ont_sets, outpath_upset_plot, variation_name)
        upset_variations_data.append(plot_data)

        # Missing axioms analysis: for ad hoc troubleshooting
        missing_axioms_outpath = str(MISSING_AXIOMS_PATH).replace('.tsv', f'_{variation_filename_stem}.tsv')
        _interrogate_missing_axioms(ont_sets, missing_axioms_outpath)

    # todo: include other (non-simple, non-[0]) variations? (later)
    _write_markdown(lens_by_ont, ont_sets_list[0], outpath_md, upset_variations_data)


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Subclass axiom analysis.', description=DESC)
    cli_add_inpath_args(parser, DEFAULTS, use_only_2_comploinc_variations=False)
    parser.add_argument(
        '-m', '--outpath-md', type=str, default=DEFAULTS['outpath-md'],
        help='Outpath for markdown file containing results.')
    parser.add_argument(
        '-u', '--outdir-upset-plots', type=str, default=DEFAULTS['outdir-upset-plots'],
        help='Output directory for upset plots.')
    parser.add_argument(
        '--class-types', type=str, nargs='+', default=DEFAULTS['class-types'],
        choices=CLASS_TYPES, help='Class types to include in analysis. One or more of: terms, groups, parts.')
    parser.add_argument(
        '--log-level', type=str, default='INFO',
        help='Logging level (e.g. DEBUG, INFO).')
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.DEBUG))
    d: Dict = vars(args)
    d.pop('log_level', None)
    # Convert class_types list to tuple
    d['class_types'] = tuple(d['class_types'])
    return subclass_rel_analysis(**d)


if __name__ == "__main__":
    cli()
