"""Create ROBOT TSV representation of the LOINC group hierarchy, including its grouping classes and linked terms

Example subclass axioms:
CHILD_ID,PARENT_ID
LG10030-1,LG100-4
LG10030-1,https://loinc.org/category/flowsheet-laboratory
26970-4,LG10030-1
"""
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Union

import pandas as pd

from loinclib import Configuration

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "comploinc_config.yaml"
CONFIG = Configuration(
    Path(os.path.dirname(str(DEFAULT_CONFIG_PATH))),
    Path(os.path.basename(DEFAULT_CONFIG_PATH)),
)

# Paths relative to the LOINC release
LOINC_RELEASE_PATH = CONFIG.get_loinc_release_path()
DEFAULTS = {
    "parent-group-path": str(
        LOINC_RELEASE_PATH / "AccessoryFiles" / "GroupFile" / "ParentGroup.csv"
    ),
    "group-path": str(
        LOINC_RELEASE_PATH / "AccessoryFiles" / "GroupFile" / "Group.csv"
    ),
    "group-loinc-terms-path": str(
        LOINC_RELEASE_PATH / "AccessoryFiles" / "GroupFile" / "GroupLoincTerms.csv"
    ),
    "outpath": PROJECT_ROOT / "output/tmp/loinc-groups.robot.tsv",
}

HEADER = ["id", "parent_id", "label"]
SUBHEADER = ["ID", "SC %", "LABEL"]


def build_template(
    parent_group_path: Union[str, Path],
    group_path: Union[str, Path],
    group_loinc_terms_path: Union[str, Path],
    outpath: Union[str, Path],
) -> None:
    """Create a ROBOT template TSV from LOINC group files."""
    parent_group_path = Path(parent_group_path)
    group_path = Path(group_path)
    group_loinc_terms_path = Path(group_loinc_terms_path)
    outpath = Path(outpath)

    # Read CSVs
    df_parent = pd.read_csv(parent_group_path, dtype=str).fillna("")
    df_group = pd.read_csv(group_path, dtype=str).fillna("")
    df_terms = pd.read_csv(group_loinc_terms_path, dtype=str).fillna("")

    # Process ParentGroup.csv
    parent_rows = pd.DataFrame(
        {
            "id": "https://loinc.org/" + df_parent["ParentGroupId"],
            "parent_id": "",
            "label": df_parent["ParentGroup"],
        }
    )

    # Process Group.csv
    group_rows = pd.DataFrame(
        {
            "id": "https://loinc.org/" + df_group["GroupId"],
            "parent_id": "https://loinc.org/" + df_group["ParentGroupId"],
            "label": df_group["Group"],
        }
    )

    # Process GroupLoincTerms.csv for term-to-group axioms
    term_rows = pd.DataFrame(
        {
            "id": "https://loinc.org/" + df_terms["LoincNumber"],
            "parent_id": "https://loinc.org/" + df_terms["GroupId"],
            "label": "",
        }
    )

    # Category URIs
    def _category_uri(cat: str) -> str:
        import re

        slug = re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")
        return "https://loinc.org/category/" + slug

    df_terms["CategoryURI"] = df_terms["Category"].apply(_category_uri)

    # GroupId -> Category axioms
    group_category_rows = pd.DataFrame(
        {
            "id": "https://loinc.org/" + df_terms["GroupId"],
            "parent_id": df_terms["CategoryURI"],
            "label": "",
        }
    ).drop_duplicates()

    # Category class rows
    categories = df_terms[["Category", "CategoryURI"]].drop_duplicates()
    category_rows = pd.DataFrame(
        {
            "id": categories["CategoryURI"],
            "parent_id": "",
            "label": categories["Category"],
        }
    )

    df_out = pd.concat(
        [parent_rows, group_rows, term_rows, group_category_rows, category_rows],
        ignore_index=True,
    )

    # Write output with ROBOT template headers
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\t".join(HEADER) + "\n")
        f.write("\t".join(SUBHEADER) + "\n")
        df_out.to_csv(f, sep="\t", header=False, index=False)


def cli() -> None:
    """Command line interface."""
    parser = ArgumentParser(prog="LOINC groups to template")
    parser.add_argument(
        "--parent-group-path",
        type=str,
        default=DEFAULTS["parent-group-path"],
        help="Path to ParentGroup.csv",
    )
    parser.add_argument(
        "--group-path",
        type=str,
        default=DEFAULTS["group-path"],
        help="Path to Group.csv",
    )
    parser.add_argument(
        "--group-loinc-terms-path",
        type=str,
        default=DEFAULTS["group-loinc-terms-path"],
        help="Path to GroupLoincTerms.csv",
    )
    parser.add_argument(
        "--outpath",
        type=str,
        default=DEFAULTS["outpath"],
        help="Output path for ROBOT template TSV",
    )
    args = parser.parse_args()
    build_template(
        args.parent_group_path,
        args.group_path,
        args.group_loinc_terms_path,
        args.outpath,
    )


if __name__ == "__main__":
    cli()
