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
        part_file: str,
        hierarchy_file: str,
        output: str):
    po = PartOntology(schema_path=schema_file)
    po.generate_part_type_lookup(loinc_part_file=part_file)
    po.generate_part_hierarchy_lookup(chem_hierarchy_file=hierarchy_file)
    po.generate_ontology()
    po.write_to_output(output_path=output)


@app.command(name='codes')
def build_codes(
        schema_file: str,
        code_file: str,
        output: str):
    cp = CodeIngest(schema_path=schema_file, code_file_path=code_file)
    cp.generate_codes()
    cp.write_output_to_file(output_path=output)

@app.command(name="merge")
def merge_owl(
        owl_directory: str,
        output: str):
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