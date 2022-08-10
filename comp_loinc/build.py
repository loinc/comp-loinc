import typer
from typing import List
from ingest.part_ingest import PartOntology
from ingest.code_ingest import CodeIngest
import os
import subprocess

app = typer.Typer()

@app.command(name='parts')
def build_part_ontology(
        schema_file: str,
        part_directory: str,
        output: str):
    """
    TODO: REfactor this to use the new simplified part_ingest.py
    :param schema_file:
    :param part_directory:
    :param output:
    :return:
    """
    ## Example
    # po = PartOntology("./model/schema/part_schema.yaml", "./local_data/part_files")
    # po.generate_ontology()
    # po.write_to_output('./data/output/owl_files/part_ontology.owl')
    po = PartOntology(schema_file, part_directory)
    po.generate_ontology()
    po.write_to_output(output)


@app.command(name='codes')
def build_codes(
        schema_file: str,
        part_directory: str,
        output: str):
    """
    TODO: Refactor this to use the new simplified code_ingest.py
    :param schema_file:
    :param part_directory:
    :param output:
    :return:
    """
    ## Example
    # lcc = CodeIngest("./model/schema/code_schema.yaml", "./data/part_files")
    # lcc.write_output_to_file("./data/output/owl_files/code_classes.owl")
    lcc = CodeIngest(schema_file, part_directory)
    lcc.write_output_to_file(output)


@app.command(name='composed')
def build_composed_classes(
        schema_file: str,
        composed_classes_data_file: str,
        output: str):
    """
    todo: this is just calling a linkml owl cli, should be written as code with python
    :param schema_file:
    :param code_file:
    :param output:
    :return:
    """
    subprocess.call(["linkml-data2owl", "-s", schema_file, composed_classes_data_file, "-o", output])

@app.command(name="merge")
def merge_owl(
        owl_directory: str,
        output: str):
    # TODO: Consider removing the files created from this point on each time this code executes e.g. any file with 'merge_*'
    files = [f'{owl_directory}{x}' for x in os.listdir(owl_directory) if ".owl" in x]
    subprocess.call(["./robot", "merge", "-i"] + " -i ".join(files).split() + ['-o', output])

@app.command(name="reason")
def reason_owl(
        owl_directory: str,
        merged_owl: str,
        owl_reasoner: str,
        output: str):
    call_list = ["./robot", "reason", "-r", owl_reasoner, '-i', f"{owl_directory}{merged_owl}", '-o', f"{owl_directory}{output}"]
    subprocess.call(call_list)


if __name__ == "__main__":
    app()