import pandas as pd
import json

def loincify(id):
    return f"loinc:{id}"

def generate_part_hierarchy(path_to_chem_hierarchy_file):
    hierarchy = pd.read_excel(path_to_chem_hierarchy_file, sheet_name="Hierarchy")
    node_id_to_part_id = {x.NODE_ID: x.FK_ID for x in hierarchy.itertuples()}

    def node_to_part(node_id):
        if node_id in node_id_to_part_id.keys():
            return node_id_to_part_id[node_id]
        else:
            print(node_id)
    hierarchy["parent_part_id"] = hierarchy['PARENT_ID'].apply(node_to_part)
    hierarchy.to_csv("../data/part_hierarchy.tsv", sep="\t")


def generate_part_type_lookup(path_to_loinc_part_file):
    part_data = pd.read_csv(path_to_loinc_part_file)
    part_type_lookup = {x.PartNumber: x.PartTypeName for x in part_data.itertuples()}
    with open("part_type_lookup.json", 'w') as ptl:
        json.dump(part_type_lookup, ptl)

# generate_part_hierarchy("../data/CHEM_HIERARCHY_LPL_DATA.xlsx")
# generate_part_type_lookup("../../../Loinc_2.72/AccessoryFiles/PartFile/Part.csv")