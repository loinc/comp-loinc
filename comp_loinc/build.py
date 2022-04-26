import typer
from ingest.part_ingest import PartOntology
from ingest.code_ingest import CodeIngest
from pprint import pprint
import json

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

if __name__ == "__main__":
    app()