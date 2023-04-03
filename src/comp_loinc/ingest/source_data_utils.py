import pandas as pd
import json
from collections import defaultdict
import os
import sys


def counter(i, total_i):
    sys.stdout.write('\r')
    sys.stdout.write(f"{i}/{total_i}")
    sys.stdout.flush()

def loincify(id):
    """
    adds the loinc: prefix to loinc part and code numbers
    :param id:
    :return: string
    """
    return f"loinc:{id}"


class PartHierarchy(object):
    """
    Generates the child parent hierarchy lookup from hierarchy excel doc
    """
    def __init__(self, path_to_hierarchy_xlsx):
        self.hierarchy = pd.read_excel(path_to_hierarchy_xlsx, sheet_name="Hierarchy")
        self.generate_part_hierarchy()
        self.parent_relationships = self.generate_parent_relationships()

    def generate_part_hierarchy(self):
        """
        return a dataframe from the node id based hierarchy with added parent id that has the part identifier
        :param path_to_chem_hierarchy_file:
        :return: Pandas Dataframe
        """
        node_id_to_part_id = {
            x.NODE_ID: x.FK_ID for x in self.hierarchy.itertuples()
        }

        def node_to_part(node_id):
            if node_id in node_id_to_part_id.keys():
                return node_id_to_part_id[node_id]
            else:
                print(f"No part id for node {node_id}")
        self.hierarchy["parent_part_id"] = self.hierarchy['PARENT_ID'].apply(node_to_part)

    def generate_parent_relationships(self):
        d = defaultdict(list)
        for index, comp in enumerate(self.hierarchy.itertuples()):
            d[comp.FK_ID].append(comp.parent_part_id)
        return d

    def generate_label_map(self):
        return {
            x.FK_ID: x.PART for x in self.hierarchy[["FK_ID", "PART"]].drop_duplicates().itertuples()
        }


class PartLookups(object):
    """
    Generates  part type lookup dictionaries from the Part.csv file (too big to push to git)
    """
    def __init__(self, part_primary_file_path, part_supplementarty_file_path):
        self.part_primary_file_path = part_primary_file_path
        self.part_supplementarty_file_path = part_supplementarty_file_path
        self.part_file = self.combine_part_files_to_df()

    def combine_part_files_to_df(self):
        return pd.concat([pd.read_csv(self.part_primary_file_path), pd.read_csv(self.part_supplementarty_file_path)])

    def generate_part_type_lookup(self):
        """
        generates a dictionary of {part number : part type}
        :return: dict
        """
        return dict(zip(self.part_file['PartNumber'].tolist(),self.part_file['PartTypeName']))

    def generate_part_name_lookup(self):
        """
        generates a dictionary of {part number: part name}
        :return: dict
        """
        return dict(zip(self.part_file['PartNumber'].tolist(), self.part_file['PartName']))