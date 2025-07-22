"""Builds a representation of SNOMED RF2 (Release Format 2) modules in OWL functional syntax

RF2: See more: https://support.nlm.nih.gov/kbArticle/?pn=KA-04047

todo: fix so no whitespace warnings. e.g.:
 WARN  LINE: 102963 Expected white space at pos: 16  LINE:
    SubClassOf(:421629003 ObjectIntersectionOf(:23217006 :373249005 ObjectSomeValuesFrom(:726542003 :764393008) ObjectSomeValuesFrom(:726542003 :765175006)))
 pos16 is right after SubClassOf( and before the :. I think this needs to be after all ( tags, and probably before all )
"""

import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd

from loinclib import Configuration

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
DESC = (
    "Builds a representation of SNOMED RF2 modules in OWL functional syntax.\n"
    "If no args are passed, will convert all RF2 modules registered in the DEFAULTS config."
)

# Module name constants
SNOMED_MODULE_NAME = "snomed"
LOINC_SNOMED_MODULE_NAME = "loinc-snomed"

# todo: Ideally I wanted to statically declare these header tags just in case in a future release, they don't appear
#  intermingled with the rest of the OWL expressions, but this requires doing set ops, and also parsing the prefix tags
#  to find the namespaces used.
# PREFIXES_MINIMUM_EXPECTED = {}
# PREFIX_IRI_BAK = "http://snomed.info/id/"
# ONTOLOGY_IRI_BAK = f"{PREFIX_IRI}ontology"
CONFIG_PATH = PROJECT_ROOT / "comploinc_config.yaml"
CONFIG = Configuration(
    Path(os.path.dirname(str(CONFIG_PATH))), Path(os.path.basename(str(CONFIG_PATH)))
)
DEFAULT_ONTOLOGY_BLOCK_OPENER = "Ontology(<http://snomed.info/sct/900000000000207008>"
DEFAULT_PREFIXES_TAGS = [
    "Prefix(owl:=<http://www.w3.org/2002/07/owl#>)",
    "Prefix(xml:=<http://www.w3.org/XML/1998/namespace>)",
    "Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)",
    "Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)",
    "Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)",
    "Prefix(:=<http://snomed.info/id/>)",
]
DEFAULTS: Dict[str, Dict[str, Union[Path, str]]] = {
    SNOMED_MODULE_NAME: {
        "inpath_owl": CONFIG.get_snomed_owl_path(),
        "inpath_labels": CONFIG.get_snomed_description_path(),
        "outpath": PROJECT_ROOT / "output/analysis/snomed/snomed-unreasoned.ofn",
    },
    LOINC_SNOMED_MODULE_NAME: {
        "inpath_owl": CONFIG.get_loinc_snomed_owl_path(),
        "inpath_labels": CONFIG.get_loinc_snomed_description_path(),
        "outpath": PROJECT_ROOT
        / "output/analysis/loinc-snomed/loinc-snomed-module.ofn",
    },
}


def _write(
    outpath: Union[Path, str],
    ontology_block_opener: str,
    prefixes_tags: List[str],
    axioms: List[str],
    label_triples: List[str],
) -> None:
    """Write to disk"""
    outdir = os.path.dirname(outpath)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    with open(outpath, "w") as f:
        # Header
        for prefix in prefixes_tags:
            f.write(f"{prefix}\n")
        f.write(f"{ontology_block_opener}\n")

        # Axioms (mostly/all EquivalentClasses?)
        for axiom in axioms:
            f.write(f"    {axiom}\n")

        # Labels
        for label_triple in label_triples:
            f.write(f"    {label_triple}\n")

        # Footer: close the Ontology block
        f.write(")\n")


def _get_expressions(inpath_owl: Union[Path, str]) -> Tuple[str, List[str], List[str]]:
    """Get expressions from SNOMED release"""
    df = pd.read_csv(inpath_owl, sep="\t", dtype=str)
    expressions: List[str] = df["owlExpression"].dropna().tolist()
    axioms: List[str] = []
    prefixes_tags: List[str] = []
    ontology_block_opener = None

    # Extract the ontology tag, prefixes, and axioms
    for exp in expressions:
        if exp.startswith("Ontology"):
            ontology_block_opener = exp[:-1] if exp.endswith(")") else exp
        elif exp.startswith("Prefix"):
            prefixes_tags.append(exp)
        else:
            axioms.append(exp)

    # Missing data
    if any([not x for x in [ontology_block_opener, prefixes_tags]]):
        ontology_block_opener, prefixes_tags = (
            _borrow_ontology_block_opener_and_prefixes_from_snomed()
        )
        # raise ValueError("Ontology IRI or prefixes are missing from the input data.")

    return ontology_block_opener, prefixes_tags, axioms


def _borrow_ontology_block_opener_and_prefixes_from_snomed(
    inpath_owl: Union[Path, str] = DEFAULTS[SNOMED_MODULE_NAME]["inpath_owl"]
) -> Tuple[str, List[str]]:
    """SNOMED modules don't typically have these tags, so we borrow from SNOMED proper."""
    # Grab from registered local module
    try:
        ontology_block_opener, prefixes_tags, axioms = _get_expressions(inpath_owl)
    except FileNotFoundError as e:
        # If the SNOMED OWL file is not found, fall back to static defaults
        print(
            f"Warning: SNOMED OWL file not found at {inpath_owl}. Using static defaults. Error: {e}"
        )
        ontology_block_opener, prefixes_tags = (
            DEFAULT_ONTOLOGY_BLOCK_OPENER,
            DEFAULT_PREFIXES_TAGS,
        )
    except pd.errors.EmptyDataError as e:
        # If the file exists but is empty or has no valid data
        print(
            f"Warning: SNOMED OWL file at {inpath_owl} is empty or invalid. Using static defaults. Error: {e}"
        )
        ontology_block_opener, prefixes_tags = (
            DEFAULT_ONTOLOGY_BLOCK_OPENER,
            DEFAULT_PREFIXES_TAGS,
        )
    except Exception as e:
        # Catch any other unexpected errors during file processing
        print(
            f"Warning: Failed to parse SNOMED OWL file at {inpath_owl}. Using static defaults. Error: {e}"
        )
        ontology_block_opener, prefixes_tags = (
            DEFAULT_ONTOLOGY_BLOCK_OPENER,
            DEFAULT_PREFIXES_TAGS,
        )

    return ontology_block_opener, prefixes_tags


def _get_labels(inpath: Union[Path, str]) -> List[str]:
    """Get labels from SNOMED release"""
    df = pd.read_csv(inpath, sep="\t", dtype=str)
    label_triples: List[str] = []
    # Remove special chars from labels
    #  - alternatively i could escape but we don't need full SNOMED label representation
    df["term"] = df["term"].str.replace(r"[^\w\s]", "", regex=True)
    # Get triples
    for row in df.itertuples():
        # can't use rdfs:label CURIE because : is the SNOMED prefix.
        # noinspection PyUnresolvedReferences false_positive_for_named_tuples
        label_triples.append(
            f'AnnotationAssertion(<http://www.w3.org/2000/01/rdf-schema#label> :{row.conceptId} "{row.term}")'
        )
    return label_triples


def build_snomed(
    inpath_owl: Union[Path, str],
    inpath_labels: Union[Path, str],
    outpath: Union[Path, str],
    include_labels: bool = True,
) -> None:
    """Builds a representation of a SNOMED module in OWL functional syntax.

    Args:
        inpath_owl: Path to SNOMED module release OWL expression file.
        outpath: Path to output file.
    """
    ontology_block_opener, prefixes_tags, axioms = _get_expressions(inpath_owl)
    label_triples = _get_labels(inpath_labels) if include_labels else []
    _write(outpath, ontology_block_opener, prefixes_tags, axioms, label_triples)


def _validate_module_name(module: str) -> None:
    """Validate that the module name exists in DEFAULTS."""
    if module not in DEFAULTS:
        raise ValueError(
            f"Module '{module}' not found in DEFAULTS. Available modules: {list(DEFAULTS.keys())}"
        )


def _resolve_config_arguments(args_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve configuration arguments, handling module-based defaults and user overrides."""
    # Handle module-based defaults
    module = args_dict.get("by_module_name")
    if module:
        _validate_module_name(module)
        # Start with module defaults
        config_defaults = DEFAULTS[module]
        # Override defaults with any user-supplied values
        args_dict["inpath_owl"] = args_dict.get("inpath_owl") or config_defaults.get(
            "inpath_owl"
        )
        args_dict["inpath_labels"] = args_dict.get(
            "inpath_labels"
        ) or config_defaults.get("inpath_labels")
        args_dict["outpath"] = args_dict.get("outpath") or config_defaults.get(
            "outpath"
        )

    # Remove module name from args before passing to build function
    if "by_module_name" in args_dict:
        del args_dict["by_module_name"]

    return args_dict


def _run_all_modules() -> None:
    """Run build_snomed for all modules in DEFAULTS."""
    for module_config in DEFAULTS.values():
        build_snomed(**module_config)


def _create_argument_parser() -> ArgumentParser:
    """Create and configure the argument parser."""
    parser = ArgumentParser(prog="Build SNOMED.", description=DESC)
    # a. Choose explicit paths
    parser.add_argument(
        "-i",
        "--inpath-owl",
        required=False,
        type=str,
        help="Path to SNOMED release OWL expression file.",
    )
    parser.add_argument(
        "-I",
        "--inpath-labels",
        required=False,
        type=str,
        help="Path to SNOMED definition file for labels.",
    )
    parser.add_argument("-o", "--outpath", required=False, type=str, help="Outpath.")
    # b. Choose defaults in config by module name
    parser.add_argument(
        "-m",
        "--by-module-name",
        required=False,
        type=str,
        help="If specified, then will consult the "
        "DEFAULTS config and use the supplied args. If you pass this with other args, the values in the DEFAULTS will "
        "be replaced by what you pass.",
    )
    return parser


def cli() -> Optional[None]:
    """Command line interface."""
    parser = _create_argument_parser()
    args_dict: Dict = vars(parser.parse_args())

    # If no arguments provided, run all modules
    if set(args_dict.values()) == {None}:
        _run_all_modules()
        return

    # Resolve configuration and run specific module
    resolved_args = _resolve_config_arguments(args_dict)
    return build_snomed(**resolved_args)


if __name__ == "__main__":
    cli()
