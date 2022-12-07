# CompLOINC LinkML

## Prerequisities
1. Python 3.9.7+
2. Required LOINC Files
For now, these files are [downloadable from GoogleDrive](https://drive.google.com/drive/u/0/folders/1SjDFYs1ocbpovGlAZDKuRVcTDoNztHOc). They need to be put in these locations:
- `data/part_files/CHEM_HIERARCHY_REVISED.TSV`
- `data/part_files/METHOD_CHEM_HIERARCHY.TSV`
- `data/part_files/PROPERTY_CHEM_HIERARCHY.TSV`
- `data/part_files/SYSTEM_CHEM_HIERARCHY.TSV`
- `data/part_files/TIME_CHEM_HIERARCHY.TSV`

## Setup
1. Clone this repository.
2. From repo directory, run: `pip install -r requirements.txt`

## Usage
Commands 1.1 - 1.5 are meant to be run sequentially.

Alternatively, you can run all of them at once using default values by running `python comp_loinc/build.py all`.

Help text can be run via `python comp_loinc/build.py --help`. You can see help text for a specific command, including 
information about its parameters, by running `python comp_loinc/build.py COMMAND_NAME --help`.

### 1.1. `parts`: Build the part ontology from the intermediate Part Hierarchy files
`python comp_loinc/build.py parts --schema-file ./model/schema/part_schema.yaml --part-directory ./data/part_files --output ./data/output/owl_component_files/part_ontology.owl --part-data ./data/part_data/part_data.tsv`

### 1.2. `codes`: Build the code classes from the intermediate Part Hierarchy files
`python comp_loinc/build.py codes --schema-file ./model/schema/code_schema.yaml --part-directory ./data/part_files --output ./data/output/owl_component_files/code_classes.owl`

### 1.3. `composed`: Build the composed class axioms for the reasoner to group classes (this is pretty bespoke, and hardcoded at the moment)
`python comp_loinc/build.py composed --schema-file model/schema/grouping_classes_schema.yaml --composed-classes-data-file data/composed_classes_data.yaml --output data/output/owl_component_files/composed_component_classes.owl`

### 1.4. `merge`: Merge all of the owl files into single merged ontology
`python comp_loinc/build.py merge --owl-directory data/output/owl_component_files/ --output data/output/merged_loinc.owl`

### 1.5. `reason`: Run the reasoner using elk to create the composed code classes
`python comp_loinc/build.py reason --merged-owl data/output/merged_loinc.owl --owl-reasoner elk --output data/output/merged_reasoned_loinc.owl`

### 2. Open the merged and reasoned owl file in Protégé for viewing
Open `data/output/merged_reasoned_loinc.owl`
