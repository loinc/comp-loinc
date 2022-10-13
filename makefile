.PHONY: all all-force python-dependencies parts codes composed merge reason test


# Utils
python-dependencies:
	pip install --upgrade pip
	pip install -r requirements.txt

# Pipeline
## 1. Run: Build the part ontology from the intermediate Part Hierarchy files
data/output/owl_component_files/part_ontology.owl: python-dependencies
	python3 comp_loinc/build.py parts --schema-file ./model/schema/part_schema.yaml --part-directory ./data/part_files --output ./data/output/owl_component_files/part_ontology.owl
parts: data/output/owl_component_files

## 2. Run: Build the code classes from the intermediate Part Hierarchy files
data/output/owl_component_files/code_classes.owl: data/output/owl_component_files/part_ontology.owl
	python3 comp_loinc/build.py codes --schema-file ./model/schema/code_schema.yaml --part-directory ./data/part_files --output ./data/output/owl_component_files/code_classes.owl
codes: parts data/output/owl_component_files

## 3. Run: Build the composed class axioms for the reasoner to group classes (this is pretty bespoke, and hardcoded at the moment)
data/output/owl_component_files/composed_component_classes.owl: data/output/owl_component_files/code_classes.owl
	python3 comp_loinc/build.py composed --schema-file model/schema/grouping_classes_schema.yaml --composed-classes-data-file ./data/composed_classes_data.yaml --output data/output/composed_component_classes.owl
composed: codes data/output/composed_component_classes.owl

## 4. Run: Merge all of the owl files into single merged ontology
data/output/merged_loinc.owl: data/output/owl_component_files/composed_component_classes.owl
	python3 comp_loinc/build.py merge --owl-directory ./data/output/owl_component_files/ --output ./data/output/merged_loinc.owl
merge: composed data/output/merged_loinc.owl

## 5. Run: the reasoner using elk to create the composed code classes
data/output/merged_reasoned_loinc.owl: data/output/merged_loinc.owl
	python3 comp_loinc/build.py reason --merged-owl ./data/output/merged_loinc.owl --owl-reasoner elk --output ./data/output/merged_reasoned_loinc.owl
reason: merge data/output/merged_reasoned_loinc.owl

## all: Runs the whole pipeline (1-5). Running `reason` directly will do the same thing, as it depends on all the other steps.
all: data/output/merged_reasoned_loinc.owl
	python3 comp_loinc/build.py all
## all-force: Runs the pipeline, even if the end result `data/output/merged_reasoned_loinc.owl` already exists.
all-force:
	python3 comp_loinc/build.py all

# QC / test
test:
	python3 -m unittest discover -v
