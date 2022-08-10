# CompLOINC LinkML

Setup:
python 3.9.7
pip install -r requirements.txt

# Required Loinc Files
- data/part_files/CHEM_HIERARCHY_REVISED.TSV
- data/part_files/METHOD_CHEM_HIERARCHY.TSV
- data/part_files/PROPERTY_CHEM_HIERARCHY.TSV
- data/part_files/SYSTEM_CHEM_HIERARCHY.TSV
- data/part_files/TIME_CHEM_HIERARCHY.TSV


# Build the part ontology from the intermediate Part Hierarchy files
python comp_loinc/build.py parts  ./model/schema/part_schema.yaml ./local_data/part_files ./data/output/owl_files/part_ontology.owl

# Build the code classes from the intermediate Part Hierarchy files
python comp_loinc/build.py codes  ./model/schema/code_schema.yaml ./local_data/part_files ./data/output/owl_files/part_ontology.owl

# Build the composed class axioms for the reasoner to group classes (this is pretty bespoke, and hardcoded at the moment)
python comp_loinc/build.py composed model/schema/grouping_classes_schema.yaml data/composed_classes_data.yaml data/output/composed_component_classes.owl

# Merge all of the owl files into single merged ontology
python comp_loinc/build.py merge data/output/ data/output/merged_loinc.owl

# Run the reasoner using elk to create the composed code classes
python comp_loinc/build.py reason data/output/ merged_loinc.owl elk merged_reasponed_loinc.owl

# Open the merged and reasoned owl file in protege for viewing
data/output/merged_reasponed_loinc.owl