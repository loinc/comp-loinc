# CompLOINC
Computational LOINC (in OWL).

[![QC build and test](https://github.com/loinc/comp-loinc/actions/workflows/main.yaml/badge.svg)](https://github.com/loinc/comp-loinc/actions/workflows/main.yaml)

## Setup
### Prerequisities
1. Python 3.11

### Installation
1. Clone repo: `git clone https://github.com/loinc/comp-loinc.git`
2. Set up virtual environment & activate: `python -m venv venv` & `source venv/bin/activate`
3. Install [Poetry](https://python-poetry.org/): `pip install poetry`
4. Install dependencies: `poetry install`
5. Unzip downloaded inputs into the root directory of the repo.
  - a. Core developers: Download latest `*-build-sources.zip` from [Google Drive](
https://drive.google.com/drive/folders/1Ae5NX959S_CV60nbf9N_37Ao-wJzM0fh).
  - b. Everyone else: Download releases from each source:
    - [LOINC](https://loinc.org/downloads/)
    - [SNOMED](https://www.nlm.nih.gov/healthit/snomedct/us_edition.html)
    - [LOINC-SNOMED Ontology](https://loincsnomed.org/downloads)
    - [LOINC Tree](https://loinc.org/tree/)
      - From this app, select from the "Hierarchy" menu at the top of the page. There are 7 options. When you select an option, select 'Export'. Extract the CSVs in each zip, and put them into a single folder, using the following names: `class.csv`, `component.csv`, `document.csv`, `method.csv`, `panel.csv`, `system.csv`, `component_by_system.csv`.
    - General instructions: Ensure that these 4 sources are unzipped to the locations shown in [comploinc_config.yaml/](comploinc_config.yaml), or update the config to match your locations.

## Repository Structure
* [data/](data/) - Static input files that don't need to be downloaded.
* [logs/](logs/output) - Logs
* [owl-files/](owl-files/) - Place the default build output files in this directory and then open the comploinc.owl file in Protege to get what is considered to be the default content of CompLOINC (still WIP).
* [src/comp_loinc/](src/comp_loinc) - Uses a loinclib `networkx` graph to generate ontological outputs.
  * [builds/](src/comp_loinc/builds) -- LinkML schema
  * [datamodel/](src/comp_loinc/datamodel) - generated Python LinkML datamodel
  * [schema/](src/comp_loinc/schema) - LinkML source schema
  * [cli.py](src/comp_loinc/cli.py) - Command line interface
  * [loinc_builder_steps.py](src/comp_loinc/loinc_builder_steps.py) - LOINC builder steps
  * [module.py](src/comp_loinc/module.py) - Instantiates and processes builder modules.
  * [runtime.py](src/comp_loinc/runtime.py) - Manages the runtime environment. Allows sharing of data between modules.
  * [snomed_builder_steps.py](src/comp_loinc/snomed_builder_steps.py) - SNOMED builder steps
* [src/loinclib](src/loinclib) - Uses inputs from LOINC and other sources to create a `networkx` graph.
  * [config.py](src/loinclib/config.py) - Configuration
  * [graph.py](src/loinclib/graph.py) - `networkx` graph ops
  * [loinc_loader.py](src/loinclib/loinc_loader.py) - Loads LOINC release data
  * [loinc_schema.py](src/loinclib/loinc_schema.py) - Schema for LOINC
  * [loinc_snomed_loader.py](src/loinclib/loinc_snomed_loader.py) - Loads SNOMED-LOINC Ontology data
  * [loinc_snomed_schema.py](src/loinclib/loinc_snomed_schema.py) - Schema for SNOMED-LOINC Ontology
  * [loinc_tree_loader.py](src/loinclib/loinc_tree_loader.py) - Loads LOINC web app hierarchical data 
  * [loinc_tree_schema.py](src/loinclib/loinc_tree_schema.py) - Schema for LOINC web app hierarchical data
  * [snomed_loader.py](src/loinclib/snomed_loader.py) - Loads SNOMED release data
  * [snomed_schema_v2.py](src/loinclib/snomed_schema_v2.py) - Schema for SNOMED release data
* [tests/](test/) - Tests
* [comploinc_config.yaml/](comploinc_config.yaml) - Configuration (discussed further below)

## Usage
If you just want to run a build of default artefacts / options, use the command `comploinc build`.

### Command reference
`comploinc --help`:

Options:

| Arg usage            | Description                                                                                    |
|----------------------|------------------------------------------------------------------------------------------------|
| --work-dir PATH      | CompLOINC work directory, defaults to current work directory.  [default: (dynamic)]            |
| --config-file PATH   | Configuration file name. Defaults to "comploinc_config.yaml"  [default: comploinc_config.yaml] |
| -o, --out-dir PATH   | The output folder name. Defaults to "output". [default: output]                                |
| --install-completion | Install completion for the current shell.                                                      |
| --show-completion    | Show completion for the current shell, to copy it or customize the installation.               |

Commands:
* `build`: Performs a build from a build file as opposed to the "builder"...
* `builder` ...

### `build` 
Usage: `comploinc build [OPTIONS] [BUILD_NAME]`

Performs a build from a build file as opposed to the "builder" command which takes build steps.

Arguments:
* `[BUILD_NAME]`  The build name or a path to a build file. The "default" build will build all outputs. 
`[default: default]`

## Configuration
See: `comploinc_config.yaml`

If following the setup exactly, this configuration will not need to be modified.

## Troubleshooting
If there are errors related to `torch` while running CompLOINC or `nlp_taxonomification.py` specifically, try changing 
the `torch` version to 2.1.0 in `pyproject.toml`. 

## Curation
CompLOINC has some functionality to configure provide curator feedback on some of the inputs, which can be used to 
inform what content will or will not be included in the ontology.

**NLP on dangling parts: `nlp-matches.sssom.tsv`**
This file is the result of the semantic similarity process which matches dangling part terms (no parent or child)  
against those in the hierarchy to try and identify a good parent for them. For each dangling part, only the top match is
included. Confidence is shown in the `similarity_score` column.

File location & related files
- `/curation/nlp-matches.sssom.tsv`: Committed. To be used by curators and will be re-read during build time.
- `/output/analysis/dangling/`: Not committed. Has several files related to `/curation/nlp-matches.sssom.tsv`.

This file adheres to the [SSSOM standard](https://mapping-commons.github.io/sssom/). There are columns `subject_id`, 
`subject_label`, `object_id`, and `object_label`. The subjects are the dangling part t
erms, and the objects are the 
non-dangling part terms already in the hierarchy.

So where does curator input come into play? There is a `curator_approved` column. If the value of this is 
set to True (case insensitive) for a given row, the match will be included in the ontology. If it is set to False (case 
insensitive), the match will not be included. If it is empty, or some value other than true/false is present, then that 
column will be ignored and the setting for inclusion based on confidence threshold will be used. The default for this is
0.5, and can be configured in `comploinc_config.yaml`.

There are several columsn in `nlp-matches.sssom.tsv` that are not part of the SSSOM specification. `curator_approved` is
one of these, but there is also `PartTypeName`, representing the LOINC part type, and `subject_dangling` and 
`object_dangling`, which are boolean columns that indicate which of the subject or object for a given row is the 
dangling part and which is the part that is currently connected within the hierarchy.

## Statistics & analysis
### [Statistics page](documentation/stats.md)

### Analysis directory
This is created during when the pipeline is run, and contains the following:
```
/output/analysis
├── chebi-subsets/  # Various intermediary files which were used to create the ChEBI-inspired hierarchy.
└── dangling
    ├── cache/  # Cached word embeddings for dangling parts and hierarchical terms.
    ├── confidence_histogram.png
    ├── dangling.tsv  # The input file that generates nlp-matches.sssom.tsv. Shows all dangling part terms. 
    └── nlp-matches.sssom_prop_analysis.tsv  # nlp-matches.sssom.tsv but w/ more columns. Attempt to look at the confidence=1 cases and try to ascertain why they have same label by looking at their other properties 
```

This directory is not committed. `/output/analysis/dangling/` has several files related to `/curation/nlp-matches.sssom.tsv`. 


## Developer docs
<details><summary>Details</summary>

### Tests
#### Tests: prerequisites
1. [`robot`](https://robot.obolibrary.org/)
2. Files in `output/build-default/fast-run/`
  - Can populate via `comploinc --fast-run build default`

#### Tests: Running
`python -m unittest discover`

### Standard operating procedures (SOPs)
#### Setting up new/updated inputs/sources
1. Create a new `YYYY-MM-DD_comploinc-build-sources.zip` in the [Google Drive folder](
https://drive.google.com/drive/folders/1Ae5NX959S_CV60nbf9N_37Ao-wJzM0fh). Ensure it has the correct structure (folder 
names and files at the right paths).
2. Make the link public: In the Google Drive folder, right-click the file, select "Share", and click "Share."  At the 
bottom, under "General Access", click the left dropdown and select "Anyone with the link."  Click "Copy link".
3. Update `DL_LINK_ID` in GitHub: Go to the [page](https://github.com/loinc/comp-loinc/settings/secrets/actions/DL_LINK_ID) 
for updating it. Paste the link from the previous step into the box, and click "Update secret."

</details>
