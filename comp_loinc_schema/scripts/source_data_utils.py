import pandas as pd
import json
from collections import defaultdict


def loincify(id):
    return f"loinc:{id}"


def generate_part_hierarchy(path_to_chem_hierarchy_file):
    hierarchy = pd.read_excel(path_to_chem_hierarchy_file, sheet_name="Hierarchy")
    node_id_to_part_id = {x.NODE_ID: x.FK_ID for x in hierarchy.itertuples()}

    def node_to_part(node_id):
        if node_id in node_id_to_part_id.keys():
            return node_id_to_part_id[node_id]
        else:
            print(f"No part id for node {node_id}")
    hierarchy["parent_part_id"] = hierarchy['PARENT_ID'].apply(node_to_part)
    return hierarchy


def generate_part_type_lookup(path_to_loinc_part_file):
    with open(path_to_loinc_part_file) as pf:
        part_data = json.load(pf)
    return part_data


def generate_label_map(hierarchy_data_df):
    return {x.FK_ID: x.PART for x in hierarchy_data_df[["FK_ID", "PART"]].drop_duplicates().itertuples()}


def generate_parent_relationships(hierarchy_data_df):
    d = defaultdict(list)
    for index, comp in enumerate(hierarchy_data_df.itertuples()):
        d[comp.FK_ID].append(comp.parent_part_id)
    return d
