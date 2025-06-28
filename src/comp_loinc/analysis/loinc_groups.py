"""Create ROBOT TSV representation of the LOINC group hierarchy, including its grouping classes and linked terms"""
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
    "outpath": PROJECT_ROOT / "output/tmp/loinc-groups.robot.tsv",
}

HEADER = ["id", "parent_id", "label"]
SUBHEADER = ["ID", "SC %", "LABEL"]


def build_template(
    parent_group_path: Union[str, Path],
    group_path: Union[str, Path],
    outpath: Union[str, Path],
) -> None:
    """Create a ROBOT template TSV from LOINC group files."""
    parent_group_path = Path(parent_group_path)
    group_path = Path(group_path)
    outpath = Path(outpath)

    # Read CSVs
    df_parent = pd.read_csv(parent_group_path, dtype=str).fillna("")
    df_group = pd.read_csv(group_path, dtype=str).fillna("")

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

    df_out = pd.concat([parent_rows, group_rows], ignore_index=True)

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
        "--outpath",
        type=str,
        default=DEFAULTS["outpath"],
        help="Output path for ROBOT template TSV",
    )
    args = parser.parse_args()
    build_template(args.parent_group_path, args.group_path, args.outpath)


if __name__ == "__main__":
    cli()
