# Update

The documentation below no longer reflects the current implemenation. It might still work but there is a parallel
implementation in the works that is not documented yet. In the meantime, please reach out for guidance if you're
attempting to use this tooling on your own. There is additional setup that needs to be performed manually after cloning the repository. Some of this setup is already documented in the readme at `data/loinc_release/README.md`, and it should be up-to-date at the time this was written.

# CompLOINC LinkML

Computable OWL Formalization of LOINC

## Website

## Repository Structure

* [comp-loinc/](comp-loinc/) - Python package for this project
    * [data/](data/) - LOINC Input data and output OWL Files
        * [code_files/](data/code_files) - LOINC Code Files
        * [part_files/](data/part_files) - LOINC Part Files
        * [output/](data/output) - OWL Output Files
            * [owl_component_files/](data/output/owl_component_files) - OWL Component Files
            * [merged_loinc.owl](data/output/merged_loinc.owl) - Merged OWL File
            * [merged_reasoned_loinc.owl](data/output/merged_reasoned_loinc.owl) - Merged and Reasoned OWL File
    * [project/](project/) - project files (do not edit these)
    * [src/](src/) - source files (edit these)
        * [comp_loinc](src/comp_loinc)
            * [schema](src/comp_loinc/schema) -- LinkML schema
            * [datamodel](src/comp_loinc/datamodel) -- generated Python datamodel
            * [cli](src/comp_loinc/cli) -- command line interface
            * [ingest](src/comp_loinc/ingest) -- ingest code
            * [mapping](src/comp_loinc/mapping) -- mapping code for extracting mappings from the loin fhir server
            * [ROBOT](src/comp_loinc/ROBOT) -- ROBOT tools for OWL Operations
    * [tests/](tests/) - Python tests

## Developer Documentation

<details>
Use the `make` command to generate project artefacts:

* `make all`: make everything
* `make deploy`: deploys site

</details>

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).

## Prerequisities

1. Python 3.9.7+
2. Required LOINC Files
   For now, these files
   are [downloadable from GoogleDrive](https://drive.google.com/drive/u/0/folders/1SjDFYs1ocbpovGlAZDKuRVcTDoNztHOc).
   They need to be put in these locations:

- `data/part_files/ComponentTree.tsv`
- `data/code_files/LOINC.csv`
- `data/code_files/LoincPartlink_Primary.csv`

## Setup

1. Clone this repository.
2. install poetry
3. run poetry install

## Usage

Commands 1.1 - 1.5 are meant to be run sequentially.

Alternatively, you can run all of them at once using default values by running `python src/comp_loinc/cli/main.py all`.

Help text can be run via `python src/comp_loinc/cli/main.py --help`. You can see help text for a specific command,
including
information about its parameters, by running `python src/comp_loinc/cli/main.py COMMAND_NAME --help`.

### 1.0. `loinc_release`: Download the latest LOINC release files and put them in the correct locations. Zip LoincRelease needs to be in the data/loinc_release directory.

`python src/comp_loinc/main.py  loinc_release`

### 1.1. `parts`: Build the part ontology from the intermediate Part Hierarchy files

`python src/comp_loinc/main.py parts --schema-file src/comp_loinc/schema/part_schema.yaml --part-directory data/part_files --output data/output/owl_component_files/part_ontology.owl`

### 1.2. `codes`: Build the code classes from the intermediate Part Hierarchy files

`python src/comp_loinc/main.py  codes --schema-file src/comp_loinc/schema/code_schema.yaml --code-directory data/code_files --output data/output/owl_component_files/code_classes.owl`

### 1.3. `composed`: Build the composed class axioms for the reasoner to group classes (this is pretty bespoke, and hardcoded at the moment)

`python src/comp_loinc/main.py  composed --schema-file src/comp_loinc/schema/grouping_classes_schema.yaml --composed-classes-data-file data/composed_classes_data.yaml --output data/output/owl_component_files/composed_component_classes.owl`

### 1.4. `map`: Get Mappings from the LOINC FHIR Server and use SSSOM to convert to OWL (Requires LOINC FHIR Server credentials)

`python src/comp_loinc/main.py  map --username username --password password --output loinc2chebi.owl`

### 1.5. `merge`: Merge all owl files into single merged ontology

`python src/comp_loinc/main.py  merge --owl-directory data/output/owl_component_files/ --output data/output/merged_loinc.owl`

### 1.6. `reason`: Run the reasoner using elk to create the composed code classes

`python src/comp_loinc/main.py reason --output latest/comp_loinc.owl`

### 2. Open the merged and reasoned owl file in Protégé for viewing

Open `data/output/merged_reasoned_loinc.owl`
