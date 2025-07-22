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
from typing import Dict, Set, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
from tabulate import tabulate
from upsetplot import from_contents, UpSet

logger = logging.getLogger(__name__)

from comp_loinc.analysis.utils import bundle_inpaths_and_update_abs_paths, cli_add_inpath_args, \
    _subclass_axioms_and_totals

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
MISSING_AXIOMS_PATH = PROJECT_ROOT / "output" / "tmp" / "missing_comploinc_axioms.tsv"
DESC = "Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."
DEFAULTS = {
    'loinc-path': 'output/tmp/subclass-rels-loinc-indirect-sc-axioms-included.tsv',
    'loinc-snomed-path': 'subclass-rels-loinc-snomed-indirect-sc-axioms-included.tsv',
    'comploinc-primary-path': 'output/tmp/subclass-rels-comploinc-indirect-included-primary.tsv',
    'comploinc-supplementary-path': 'output/tmp/subclass-rels-comploinc-indirect-included-supplementary.tsv',
    'outpath-md': 'documentation/analyses/class-depth/depth.md',
    'outpath-upset-plot': 'documentation/analyses/class-depth',
}
md_template = """
# Subclass axiom analysis
This analysis shows set totals, intersections, and differences for direct subclass axioms in LOINC, CompLOINC, and 
LOINC-SNOMED Ontology. "Direct" means a direct parent/child relationship, as opposed to "indirect", meaning 2+ degree 
ancestor relationship.  

## Data preparation
The only subclass axioms that were removed were those containing anyonymous class expressions (bnodes) within 
LOINC-SNOMED Ontology.

## Total subclass axioms
{{ tot_table }}

## Comparison: Upset plots
In this upset plot, we observe both CompLOINC's large count of subclass axioms, and its nearly full inclusion of 
subclass axioms from sources. In the upset plot, horizontal bars represent the proportion of each terminology's subclass
axioms relative to the total number of unique subclass axioms across all three resources. Vertical bars represent the 
proportion of subclass axioms belonging to specific combinations of terminology resources, with each column showing a 
distinct intersection pattern as indicated by the connected dots below.

![Upset plot](upset.png)

## Comparison: Merged tables
Cell formatting: (%intersection/a) / (n intersection) / (%intersection/b)

Where 'a' is the ontology represented by the row, and 'b' is the ontology represented by the column. 'n intersection' is 
the total number of subclass axioms in the intersection of the two ontologies. '%intersection/' is the percentage of 
subclass axioms in the intersection of the two ontologies, relative to the total number of subclass axioms in the 
ontology. 

{{ overlap_direct_merged_table }}

## Comparison: Individual tables
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


def _make_tables(tots_df: pd.DataFrame, ont_sets: Dict[str, Set[Tuple[str, str]]], outpath: Union[Path, str]):
    """Calculate and save tables

    todo: logic is similar for each for loop, iterating over ont_sets.items() 2x. Should we abstract?
    """
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
        overlap_direct_merged_table=overlap_direct_merged_table)
    with open(outpath, 'w') as f:
        f.write(markdown_output)


def _interrogate_missing_axioms(ont_sets: Dict[str, Set[Tuple[str, str]]]):
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
            missing_df.to_csv(MISSING_AXIOMS_PATH, index=False, sep="\t")
        except FileNotFoundError:
            logger.debug("Could not save missing axioms to tmp directory; doesn't exist.")


def _make_upset_plot(
    ont_sets: Dict[str, Set[Tuple[str, str]]], outpath: Union[Path, str]
):
    """Make upset plot showing relationships between ontology subclass axioms.

    Args:
        ont_sets: Dictionary mapping ontology names to sets of subclass axioms
        outpath: Path to save the resulting plot
    """
    # Convert sets to a dictionary format for upsetplot
    data = {}
    for ont_name, axiom_set in ont_sets.items():
        # Convert tuples to strings for easier handling
        data[ont_name] = {f"{parent}>{child}" for parent, child in axiom_set}

    # Generate the upset data structure
    upset_data = from_contents(data)

    # Create the plot
    fig = plt.figure(figsize=(12, 8))
    # fig = plt.figure(figsize=(12, 8), constrained_layout=True)  # alternative layout; doesn't seem any different
    upset = UpSet(upset_data, sort_by="cardinality", show_percentages=True)
    upset.plot(fig=fig)
    # Add title and adjust layout
    # plt.suptitle("Ontology Subclass Axiom Overlap", fontsize=16)
    # plt.tight_layout()  # alternative to .subplots_adjust(). looked bad and gave warning: This figure includes Axes
    # that are not compatible with tight_layout, so results might be incorrect.
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    # Save
    plt.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close()


def subclass_rel_analysis(
    loinc_path: Union[Path, str], loinc_snomed_path: Union[Path, str], comploinc_primary_path: Union[Path, str],
    comploinc_supplementary_path: Union[Path, str], outpath_md: Union[Path, str], outpath_upset_plot: Union[Path, str],
    dont_convert_paths_to_abs=False
):
    """Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."""
    terminologies: Dict[str, Path]
    terminologies, outpath_md, outdir_plots = bundle_inpaths_and_update_abs_paths(
        loinc_path, loinc_snomed_path, comploinc_primary_path, comploinc_supplementary_path, dont_convert_paths_to_abs,
        outpath_md, outpath_upset_plot)

    # todo: do I want 2 sets of outputs, 1 per part model? maybe not
    # for mdl in ('primary', 'supplementary'):

    tots_df, ont_sets = _subclass_axioms_and_totals(terminologies)
    _make_tables(tots_df, ont_sets, outpath_md)
    _make_upset_plot(ont_sets, outpath_upset_plot)
    _interrogate_missing_axioms(ont_sets)


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog='Subclass axiom analysis.', description=DESC)
    cli_add_inpath_args(parser, DEFAULTS)
    parser.add_argument(
        '-m', '--outpath-md', type=str, default=DEFAULTS['outpath-md'],
        help='Outpath for markdown file containing results.')
    parser.add_argument(
        '-u', '--outpath-upset-plot', type=str, default=DEFAULTS['outpath-upset-plot'],
        help='Outpath for upset plot.')
    parser.add_argument(
        '--log-level', type=str, default='DEBUG',
        help='Logging level (e.g. DEBUG, INFO).')
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.DEBUG))
    d: Dict = vars(args)
    d.pop('log_level', None)
    return subclass_rel_analysis(**d)


if __name__ == "__main__":
    cli()
