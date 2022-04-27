# CompLOINC LinkML

Setup:
python 3.9.7
pip install -r requirements.txt

# Required Loinc Files
- stored in comp_loinc/local_data because they are too big to push to git. (should eventually be programattically pulled)
- local/data/CHEM_HIERARCHY_LPL_DATA.xlsx
- local_data/LoincPartLink_Primary.csv
- local_data/LoincPartLink_Supplementary.csv



# Build the part ontology the downloaded LOINC part source tabular data and the intermediate CHEM_HIERARCHY_LPL_DATA.xlsx file
python comp_loinc/build.py parts  ./model/schema/part_schema.yaml ./local_data/LoincPartLink_Primary.csv ./local_data/LoincPartLink_Supplementary.csv ./local_data/CHEM_HIERARCHY_LPL_DATA.xlsx ./data/output/part_classes.owl

# Build the code classes with linked parts from  the intermediate CHEM_HIERARCHY_LPL_DATA.xlsx file
python comp_loinc/build.py codes ./model/schema/code_schema.yaml ./local_data/CHEM_HIERARCHY_LPL_DATA.xlsx ./data/output/code_classes_cli.owl

# Build the composed class axioms for the reasoner to group classes (this is pretty bespoke, and hardcoded at the moment)
python comp_loinc/build.py composed model/schema/grouping_classes_schema.yaml data/composed_classes_data.yaml data/output/composed_component_classes.owl

# Merge all of the owl files into single merged ontology
python comp_loinc/build.py merge data/output/ data/output/merged_loinc.owl

# Run the reasoner using elk to create the composed code classes
python comp_loinc/build.py reason data/output/ merged_loinc.owl elk merged_reasponed_loinc.owl

# Open the merged and reasoned owl file in protege for viewing
data/output/merged_reasponed_loinc.owl