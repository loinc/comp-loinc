"""Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED.

Refs:
- https://claude.ai/chat/db6bb6d5-2ab5-4bc1-99cc-cffc9428fccd

todo's:
 - consider writing tables to TSV in addition to markdown. for easy ref / copying
TODO: #1 Do I actually want a_minus_b or intersection? I thought I found that they were the same for my purposes, but
 now I'm not so sure.
"""

import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Set, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
from tabulate import tabulate
from upsetplot import from_contents, UpSet

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
ONTO_DIR = PROJECT_ROOT / "src" / "ontology"
MISSING_AXIOMS_PATH = PROJECT_ROOT / "output" / "tmp" / "missing_comploinc_axioms.tsv"
DESC = "Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."
ONTOLOGIES = ("LOINC", "LOINC-SNOMED", "CompLOINC")
md_template = """
# Subclass axiom analysis
This analysis shows set totals, intersections, and differences for direct subclass axioms in LOINC, CompLOINC, and 
LOINC-SNOMED Ontology. "Direct" means a direct parent/child relationship, as opposed to "indirect", meaning 2+ degree 
ancestor relationship.  

## Total subclass axioms
{{ tot_table }}

## Comparison: Upset plot
![Upset plot](upset.png)

In this upset plot, we observe both CompLOINC's large count of subclass axioms, and its nearly full inclusion of 
subclass axioms from sources. In the upset plot, horizontal bars represent the proportion of each terminology's subclass
axioms relative to the total number of unique subclass axioms across all three resources. Vertical bars represent the 
proportion of subclass axioms belonging to specific combinations of terminology resources, with each column showing a 
distinct intersection pattern as indicated by the connected dots below.

## Comparison: Merged table
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


def _read(
    indir: Union[Path, str]
) -> Tuple[pd.DataFrame, Dict[str, Set[Tuple[str, str]]]]:
    """Read & return transformed inputs"""
    ont_paths = {
        k: PROJECT_ROOT / indir / f"subclass-rels-{k.lower()}.tsv" for k in ONTOLOGIES
    }
    ont_sets: Dict[str, Set[Tuple[str, str]]] = {}
    ont_dfs = {}

    # Totals
    tots_rows = []
    for ont, path in ont_paths.items():
        df = pd.read_csv(path, sep="\t")
        ont_dfs[ont] = df
        tots_rows.append({"": ont, "n": f"{len(df):,}"})
        ont_sets[ont] = set(zip(df["?child"], df["?parent"]))
    tots_df = pd.DataFrame(tots_rows)
    return tots_df, ont_sets


def _make_tables(
    tots_df: pd.DataFrame,
    ont_sets: Dict[str, Set[Tuple[str, str]]],
    outpath: Union[Path, str],
):
    """Calculate and save tables"""
    # Overlap/comparison: merged table
    overlap_direct_merged_rows = []
    for row_ont in ONTOLOGIES:
        overlap_row = {"": row_ont}
        row_set = ont_sets[row_ont]
        for col_ont in ONTOLOGIES:
            col_set = ont_sets[col_ont]
            if row_ont == col_ont:
                overlap_row[col_ont] = "-"
            else:
                # noinspection DuplicatedCode
                intersection = row_set.intersection(col_set)
                # Calculate percentages
                pct_row_in_col = (
                    len(intersection) / len(row_set) * 100 if len(row_set) > 0 else 0
                )
                pct_col_in_row = (
                    len(intersection) / len(col_set) * 100 if len(col_set) > 0 else 0
                )
                overlap_row[col_ont] = (
                    f"{pct_row_in_col:.1f}% / {len(intersection):,} / {pct_col_in_row:.1f}%"
                )
        overlap_direct_merged_rows.append(overlap_row)
    overlap_direct_merged_df = pd.DataFrame(overlap_direct_merged_rows)

    # Overlap/comparison: individual tables
    comparison_tables = {}
    for ont_a in ONTOLOGIES:
        comparison_tables[ont_a] = {}
        set_a = ont_sets[ont_a]
        for ont_b in ONTOLOGIES:
            if ont_a == ont_b:
                continue  # Skip self-comparison
            set_b = ont_sets[ont_b]
            # Calculate differences and intersection
            a_minus_b = set_a.difference(set_b)
            b_minus_a = set_b.difference(set_a)
            # noinspection DuplicatedCode
            intersection = set_a.intersection(set_b)
            # TODO: #1 Do I actually want a_minus_b or intersection? I thought I found that they were the same for my
            #  purposes, but now I'm not so sure.
            # Calculate percentages
            pct_a_minus_b = len(a_minus_b) / len(set_a) * 100 if len(set_a) > 0 else 0
            pct_b_minus_a = len(b_minus_a) / len(set_b) * 100 if len(set_b) > 0 else 0

            # Create comparison dataframe
            comparison_df = pd.DataFrame(
                [
                    {
                        "% (a-b)": f"{pct_a_minus_b:.1f}%",
                        "n (a-b)": len(a_minus_b),
                        "tot a": len(set_a),
                        "intersection": len(intersection),
                        "tot b": len(set_b),
                        "n (b-a)": len(b_minus_a),
                        "% (b-a)": f"{pct_b_minus_a:.1f}%",
                    }
                ]
            )
            comparison_tables[ont_a][ont_b] = comparison_df

    # Render & save
    template = Template(md_template)
    tots_table = tabulate(tots_df, headers="keys", tablefmt="pipe", showindex=False)
    rendered_comparisons = {}
    for ont_a in comparison_tables:
        rendered_comparisons[ont_a] = {}
        for ont_b in comparison_tables[ont_a]:
            rendered_comparisons[ont_a][ont_b] = tabulate(
                comparison_tables[ont_a][ont_b],
                headers="keys",
                tablefmt="pipe",
                showindex=False,
            )
    overlap_direct_merged_table = tabulate(
        overlap_direct_merged_df, headers="keys", tablefmt="pipe", showindex=False
    )
    markdown_output = template.render(
        tot_table=tots_table,
        ontologies=ONTOLOGIES,
        comparisons=rendered_comparisons,
        overlap_direct_merged_table=overlap_direct_merged_table,
    )
    with open(outpath, "w") as f:
        f.write(markdown_output)


def _interrogate_missing_axioms(ont_sets: Dict[str, Set[Tuple[str, str]]]):
    """Analyze and save information about missing axioms in each data source.

    Args:
        ont_sets: Dictionary mapping ontology names to sets of subclass axioms
    """
    print("Interrogating non-inclusion of axioms in CompLOINC and its sources.")
    all_elements = set()
    for s in ont_sets.values():
        all_elements.update(s)
    print(f"- Total unique elements across all sets: {len(all_elements)}")

    # Find elements not in CompLOINC
    if "CompLOINC" in ont_sets:
        missing_from_comploinc = all_elements - ont_sets["CompLOINC"]
        print(
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

        print("\n- Missing elements by source combinations:")
        for sources, count in sorted(
            source_combinations.items(), key=lambda x: x[1], reverse=True
        ):
            print(f" - {', '.join(sources)}: {count} elements")

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
            print("Could not save missing axioms to tmp directory; doesn't exist.")


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
    indir: Union[Path, str],
    outpath_md: Union[Path, str],
    outpath_upset_plot: Union[Path, str],
):
    """Analysis for totals and overlap of subclass axioms / relationships between LOINC, CompLOINC, and LOINC-SNOMED."""
    outpath_md = PROJECT_ROOT / outpath_md
    outpath_upset_plot = PROJECT_ROOT / outpath_upset_plot
    tots_df, ont_sets = _read(indir)
    _make_tables(tots_df, ont_sets, outpath_md)
    _make_upset_plot(ont_sets, outpath_upset_plot)
    _interrogate_missing_axioms(ont_sets)


def cli():
    """Command line interface."""
    parser = ArgumentParser(prog="Subclass axiom analysis.", description=DESC)
    parser.add_argument(
        "-i",
        "--indir",
        required=True,
        type=str,
        help="Path to directory containing expected inputs: subclass-rels-*.tsv, where * are: "
        + ", ".join([x.lower() for x in ONTOLOGIES]),
    )
    parser.add_argument(
        "-m",
        "--outpath-md",
        required=True,
        type=str,
        help="Outpath for markdown file containing results.",
    )
    parser.add_argument(
        "-u",
        "--outpath-upset-plot",
        required=True,
        type=str,
        help="Outpath for upset plot.",
    )
    d: Dict = vars(parser.parse_args())
    return subclass_rel_analysis(**d)


if __name__ == "__main__":
    cli()
