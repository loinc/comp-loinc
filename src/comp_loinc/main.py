"""CLI

Resources
- CLI type system docs (typer is a higher leve wrapper around click): https://click.palletsprojects.com/en/8.1.x/api/

TODO's (major)
  -

todo's (minor)
  1. Path resolution / graceful exiting: If path of a file/dir doesn't exist, should exit gracefully early on. I left
  exists=False for each `typer.Option` as a reminder. I would use `exists=True`, but `typer` has a relative path bug.
  2. help text: Consider changing/adding docstring param descriptions to `typer.Option(help=<description>)`.
"""
import logging
import os
import pathlib
import subprocess
import time
import typing
from os.path import dirname

import typer
from typing_extensions import Annotated

import comp_loinc
import loinclib
from comp_loinc.ingest.code_ingest import CodeIngest
from comp_loinc.ingest.load_loinc_release import LoadLoincRelease
# try:
from comp_loinc.ingest.part_ingest import PartOntology
from comp_loinc.mapping.fhir_concept_map_ingest import ChebiFhirIngest

# except ModuleNotFoundError:
#     from comp_loinc.ingest.part_ingest import PartOntology
#     from comp_loinc.ingest.code_ingest import CodeIngest
#     from comp_loinc.mapping.fhir_concept_map_ingest import ChebiFhirIngest
#     from comp_loinc.ingest.load_loinc_release import LoadLoincRelease


app = typer.Typer(help='CompLOINC. A tool for creating an OWL version of LOINC.')

PROJECT_DIR = pathlib.Path(dirname(dirname(dirname(__file__))))
LOINC_DIR = PROJECT_DIR / 'data' / 'loinc_release' / 'extracted'

SRC_DIR = os.path.join(PROJECT_DIR, 'src', 'comp_loinc')
SCHEMA_DIR = os.path.join(PROJECT_DIR, 'src', 'comp_loinc', 'schema')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
ROBOT_BIN_PATH = os.path.join(PROJECT_DIR, 'src', 'comp_loinc', 'ROBOT', 'robot')

DEFAULTS = {
    'schema_file.parts': os.path.join(SRC_DIR, 'schema', 'part_schema.yaml'),
    'schema_file.codes': os.path.join(SRC_DIR, 'schema', 'code_schema.yaml'),
    'schema_file.composed': os.path.join(SRC_DIR, 'schema', 'grouping_classes_schema.yaml'),
    'part_directory': os.path.join(DATA_DIR, 'part_files'),
    'code_directory': os.path.join(DATA_DIR, 'code_files'),
    'release_directory': os.path.join(DATA_DIR, 'loinc_release'),
    'code_file': os.path.join(SRC_DIR, 'schema', 'code_schema.yaml'),
    'composed_classes_data_file': os.path.join(DATA_DIR, 'composed_classes_data.yaml'),
    'owl_reasoner': 'elk',

    # output
    'output.parts': os.path.join(DATA_DIR, 'output', 'owl_component_files', 'part_ontology.owl'),
    'output.codes': os.path.join(DATA_DIR, 'output', 'owl_component_files', 'code_classes.owl'),
    'output.composed': os.path.join(DATA_DIR, 'output', 'owl_component_files', 'composed_component_classes.owl'),
    'output.map': os.path.join(DATA_DIR, 'output', 'sssom_mapping_files', 'loinc2chebi_sssom.tsv'),
    'output.merge': os.path.join(DATA_DIR, 'output', 'merged_loinc.owl'),
    'output.reason': os.path.join(DATA_DIR, 'output', 'merged_reasoned_loinc.owl'),
    'owl_directory': os.path.join(DATA_DIR, 'output', 'owl_component_files'),
    # 'merged_owl': os.path.join(DATA_DIR, 'output', 'merged_loinc.owl'),
}

release: typing.Optional[loinclib.LoincRelease] = None
generator: typing.Optional[comp_loinc.Generator] = None

def get_latest_loinc_release():
    loinc_release = None
    loinc_releases_path = pathlib.Path(__file__).parent / '..' / '..' / 'data' / 'loinc_release'
    loinc_releases_path = loinc_releases_path.resolve()
    for d in reversed(sorted(list(loinc_releases_path.glob('*')))):
        if pathlib.Path.is_dir(d):
            loinc_release = d
            break
    return loinc_release


def get_latest_trees():
    loinc_trees = None
    loinc_path = get_latest_loinc_release()
    if loinc_path:
        for d in reversed(sorted(list((loinc_path / 'trees' ).glob('*')))):
            if pathlib.Path.is_dir(d):
                loinc_trees = d
                break
    return loinc_trees

def get_loinc_version():
    release_path = get_latest_loinc_release()
    if release_path:
        return release_path.name


@app.callback()
def comp_loinc_main(loinc_dir: Annotated[pathlib.Path, typer.Option()] = get_latest_loinc_release(),
                    trees_date: Annotated[str, typer.Option()] = get_latest_trees(),
                    loinc_version: Annotated[str, typer.Option()] = get_loinc_version(),
                    out_dir: Annotated[pathlib.Path, typer.Option()] = PROJECT_DIR / 'data' / 'loinc_owl',
                    log_level: Annotated[str, typer.Option()] = 'WARN',
                    owl_output: Annotated[bool, typer.Option()] = True,
                    rdf_output: Annotated[bool, typer.Option()] = True
                    ):
    logging.basicConfig(filename=PROJECT_DIR / 'logs' / f'log_{time.strftime("%Y%m%d-%H%M%S")}.txt',
                        encoding='utf-8',
                        level=logging.getLevelName(log_level.upper())
                        )

    global release, generator
    release = loinclib.LoincRelease(loinc_dir, loinc_version, loinc_dir / 'trees' / trees_date)
    generator = comp_loinc.Generator(loinc_release=release,
                                     schema_directory=pathlib.Path(SCHEMA_DIR),
                                     output_directory=out_dir,
                                     owl_output=owl_output,
                                     rdf_output=rdf_output
                                     )


@app.command()
def generate_all():
    print(f'Building all')
    loincs_list()
    loincs_primary_defs()
    loincs_supplementary_defs()
    chebi_part_equivalence()
    # TODO: SE: broken
    # parts_group_chem_eq()
    loincs_comp_has_slash()
    parts_list()
    parts_trees()


@app.command()
def loincs_list():
    release.load_LoincTable_Loinc_csv()
    generator.generate_loincs_list()
    generator.save_outputs()


@app.command()
def loincs_primary_defs():
    print(f'Building loinc-primary-defs.owl')
    release.load_AccessoryFiles_PartFile_LoincPartLink_Primary_csv()
    generator.generate_loincs_primary_defs()
    generator.save_outputs()


@app.command()
def loincs_supplementary_defs():
    print(f'Building loinc-primary-defs.owl')
    release.load_AccessoryFiles_PartFile_LoincPartLink_Supplementary_csv()
    generator.generate_loincs_supplementary_defs()
    generator.save_outputs()


@app.command()
def loincs_comp_has_slash():
    print(f'Building loincs with slash in component')
    release.load_LoincTable_Loinc_csv()
    generator.generate_group_component_has_slash()
    generator.save_outputs()


@app.command()
def parts_list():
    release.load_AccessoryFiles_PartFile_Part_csv()
    print("Generating parts ontology", flush=True)
    generator.generate_parts_list()
    generator.save_outputs()


@app.command()
def parts_trees():
    release.load_AccessoryFiles_PartFile_Part_csv()
    release.load_all_trees()
    generator.generate_parts_trees()
    generator.save_outputs()


@app.command()
def parts_group_chem_eq():
    raise NotImplemented('parts_group_chem_eq is broken for now. Do not use.')
    release.load_AccessoryFiles_PartFile_Part_csv()
    release.load_all_trees()
    generator.generate_parts_group_chem_equivalences()
    generator.save_outputs()


@app.command()
def chebi_part_equivalence():
    release.load_AccessoryFiles_PartFile_PartRelatedCodeMapping_csv()
    generator.generate_chebi_mappings()
    generator.save_outputs()


############################


@app.command(name='load_release')
def load_release():
    """Load LOINC release into local data directory.

    A specific LOINC verions's *.zip file should be manually downloaded and placed in the data/loinc_release before
    invoking this command.
    """
    l = LoadLoincRelease(DEFAULTS['release_directory'])


@app.command(name='parts-older')
def build_part_ontology(
        schema_file: Annotated[str, typer.Option(resolve_path=True, exists=False)] = DEFAULTS['schema_file.parts'],
        part_directory: Annotated[str, typer.Option(resolve_path=True, exists=False)] = DEFAULTS['part_directory'],
        output: Annotated[str, typer.Option(resolve_path=True, writable=True)] = DEFAULTS['output.parts']
):
    """Build ontology for LOINC term parts. Part 1/5 of the pipeline.

    :param schema_file: str to LinkML `.yaml` file that defines data model for LOINC term 'parts', which are
    essentially subcomponents of LOINC terms.
    :param part_directory: str to directory containing TSV files which define the entire LOINC hierarchy of terms and
    their subcomponent parts.
    :param output: str where output will be saved.

    # Example
    po = PartOntology("./model/schema/part_schema.yaml", "./local_data/part_files")
    po.generate_ontology()
    po.write_to_output('./data/output/owl_component_files/part_ontology.owl')
    """
    po = PartOntology(str(schema_file), str(part_directory))
    po.generate_ontology()
    po.write_to_output(output)


@app.command(name='parts2')
def build_part2_ontology():
    print("building parts 2")
    generator.generate_parts_ontology(add_childless=True)


@app.command(name='codes')
def build_codes(
        schema_file: Annotated[str, typer.Option(resolve_path=True, exists=False)] = DEFAULTS['schema_file.codes'],
        code_directory: Annotated[str, typer.Option(resolve_path=True, exists=False)] = DEFAULTS['code_directory'],
        output: Annotated[str, typer.Option(resolve_path=True, writable=True)] = DEFAULTS['output.codes']
):
    """Build ontology for LOINC codes.  Part 2/5 of the pipeline.

    :param schema_file: str to LinkML `.yaml` file that defines data model for LOINC terms, which are identified by
    LOINC codes.
    :param code_directory: str to directory containing TSV files which define the entire LOINC hierarchy of terms and
    their subcomponent parts.
    :param output: str where output will be saved.

    # Example
    lcc = CodeIngest("./model/schema/code_schema.yaml", "./data/part_files")
    lcc.write_output_to_file("./data/output/owl_component_files/code_classes.owl")
    """
    lcc = CodeIngest(str(schema_file), str(code_directory))
    lcc.write_output_to_file(output)


@app.command(name='composed')
def build_composed_classes(
        schema_file: Annotated[str, typer.Option(resolve_path=True, exists=False)] = DEFAULTS['schema_file.composed'],
        composed_classes_data_file: Annotated[str, typer.Option(resolve_path=True, exists=False)] = DEFAULTS[
            'composed_classes_data_file'],
        output: Annotated[str, typer.Option(resolve_path=True, writable=True)] = DEFAULTS['output.composed']
):
    """Build composed classes ontology.  Part 3/5 of the pipeline.

    :param schema_file: str to LinkML `.yaml` file that defines data model for "grouping classes" of LOINC terms, that 
    is, classes that group sets of LOINC terms into specific categories.
    :param composed_classes_data_file: str to `.yaml` file which lists LOINC composed classes. These are lower-level,
    more granular groupings of classes, and their are a greater number of them than the grouping classes in the
    `schema_file`.
    :param output: str where output will be saved.

    todo: this is just calling a linkml owl cli, should be written as code with python code
    """
    subprocess.call(["linkml-data2owl", "-s", schema_file, composed_classes_data_file, "-o", output])


@app.command(name='map')
def build_mappings(
        username: Annotated[str, typer.Option()] = None,
        password: Annotated[str, typer.Option()] = None,
        output: Annotated[str, typer.Option(resolve_path=True, writable=True)] = DEFAULTS['output.map']
):
    """Build mappings ontology.  Part 3/5 of the pipeline.

    :param password: str to password for LOINC API.
    :param username: str to username for LOINC API.
    :param output: str where output will be saved."""

    chebi_fhir = ChebiFhirIngest(pwd=password, user=username, output=output)
    chebi_fhir.get_fhir_chebi_mappings()


@app.command(name="merge")
def merge_owl(
        owl_directory: Annotated[str, typer.Option(resolve_path=True, exists=False)] = DEFAULTS['owl_directory'],
        output: Annotated[str, typer.Option(resolve_path=True, writable=True)] = DEFAULTS['output.merge']
):
    """Merge all OWL ontology files into a single ontology. Part 4/5 of the pipeline.

    :param owl_directory: str to directory where unmerged `.owl` files are stored.
    :param output: str where output will be saved.

    TODO: Consider removing the files created from this point each time this code executes e.g. any file with 'merge_*'
    """
    files = [os.path.join(owl_directory, str(x)) for x in os.listdir(owl_directory) if ".owl" in str(x)]
    subprocess.call([ROBOT_BIN_PATH, "merge", "-i"] + " -i ".join(files).split() + ['-o', output])


@app.command(name="reason")
def reason_owl(
        merged_owl: Annotated[str, typer.Option()] = DEFAULTS['output.merge'],
        owl_reasoner: Annotated[str, typer.Option()] = DEFAULTS['owl_reasoner'],
        output: Annotated[str, typer.Option(resolve_path=True, writable=True)] = DEFAULTS['output.reason']
):
    """Add computational reasoning to the merged ontology. Creates a new, reasoned ontology. Part 5/5 of the pipeline.

    :param merged_owl: Name of the merged OWL file created from the `merge` command.
    :param owl_reasoner: The name of the OWL reasoner to use.
    :param output: str where output will be saved."""
    call_list = [ROBOT_BIN_PATH, "reason", "-r", owl_reasoner, '-i', f"{merged_owl}", '-o', f"{output}"]
    subprocess.call(call_list)


@app.command(name="all")
def run_all():
    """Runs the whole pipeline.

    Uses default values for all steps. For something more custom, it is recommended to run the steps 1 at a time."""

    load_release()
    print("Loaded release")
    build_part_ontology()
    print("Built parts")
    build_codes()
    print("Built codes")
    build_composed_classes()
    print("Built composed")
    build_mappings()
    print("Built mappings")
    merge_owl()
    print("Built merged")
    reason_owl()
    print("Built reasoned")





if __name__ == "__main__":
    app()
