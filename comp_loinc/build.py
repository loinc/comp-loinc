"""CLI

TODO's
  1. Flesh out documentation for each param for each command.
  2. Change args from positional to named, e.g.: https://typer.tiangolo.com/tutorial/parameter-types/number/
    i. if i can't make them required, then i can raise an err if any are missing
"""
import os
import subprocess

import typer

try:
    from comp_loinc.ingest.part_ingest import PartOntology
    from comp_loinc.ingest.code_ingest import CodeIngest
except ModuleNotFoundError:
    from ingest.part_ingest import PartOntology
    from ingest.code_ingest import CodeIngest


app = typer.Typer(help='CompLOINC. A tool for creating an OWL version of LOINC.')


@app.command(name='parts')
def build_part_ontology(
        schema_file: str,
        part_primary_file: str,
        part_supplementary_file: str,
        hierarchy_file: str,
        output: str):
    """Build part ontology.
    :param schema_file: Path to...
    :param part_primary_file: Path to...
    :param part_supplementary_file: Path to...
    :param hierarchy_file: Path to...
    :param output: Path where output will be saved."""
    po = PartOntology(schema_path=schema_file)
    po.generate_part_type_lookup(loinc_primary_part_file=part_primary_file,
                                 loinc_supplement_part_file=part_supplementary_file)
    po.generate_part_hierarchy_lookup(chem_hierarchy_file=hierarchy_file)
    po.generate_ontology()
    po.write_to_output(output_path=output)


@app.command(name='codes')
def build_codes(
        schema_file: str,
        code_file: str,
        output: str):
    """Build codes.
    :param schema_file: Path to...
    :param code_file: Path to...
    :param output: Path where output will be saved."""
    cp = CodeIngest(schema_path=schema_file, code_file_path=code_file)
    cp.generate_codes()
    cp.write_output_to_file(output_path=output)


@app.command(name='composed')
def build_composed_classes(
        schema_file: str,
        composed_classes_data_file: str,
        output: str):
    """Build composed classes.
    :param schema_file: Path to...
    :param composed_classes_data_file: Path to...
    :param output: Path where output will be saved."""
    # TODO: this is just calling a linkml owl cli, should be written as code
    subprocess.call(["linkml-data2owl", "-s", schema_file, composed_classes_data_file, "-o", output])


@app.command(name="merge")
def merge_owl(
        owl_directory: str,
        output: str):
    """Merge owl.
    :param owl_directory: Path to directory where `.owl` files are stored.
    :param output: Path where output will be saved."""
    files = [f'{owl_directory}{x}' for x in os.listdir(owl_directory) if ".owl" in x]
    subprocess.call(["./robot", "merge", "-i"] + " -i ".join(files).split() + ['-o', output])


@app.command(name="reason")
def reason_owl(
        owl_directory: str,
        merged_owl: str,
        owl_reasoner: str,
        output: str):
    """Reason owl.
    :param owl_directory: Path to directory where `.owl` files are stored.
    :param merged_owl: Name of OWL file...
    :param owl_reasoner: The n ame of the OWL reasoner to use.
    :param output: Path where output will be saved."""
    call_list = [
        "./robot", "reason", "-r", owl_reasoner, '-i', f"{owl_directory}{merged_owl}", '-o', f"{owl_directory}{output}"]
    subprocess.call(call_list)


if __name__ == "__main__":
    app()
