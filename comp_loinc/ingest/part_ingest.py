"""Part ingest

# ## Example
# po = PartOntology("./model/schema/part_schema.yaml", "./local_data/part_files")
# po.generate_ontology()
# po.write_to_output('./data/output/owl_component_files/part_ontology.owl')
# # po.write_to_output('./local_data/part_ontology_files/part_ontology.owl')
"""
import pandas as pd
from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
import os
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from comp_loinc.ingest.source_data_utils import loincify
from comp_loinc.loinc_owl.part_schema import ComponentClass, SystemClass, PartClass, TimeClass, MethodClass, PropertyClass
# from scripts.source_data_utils import generate_part_hierarchy, generate_part_type_lookup, generate_label_map, generate_parent_relationships


def generate_class_params(part_data):
    params = {
        "id": loincify(part_data['PartNumber']),
        "part_number": part_data['PartNumber'],
        "label": part_data['PartName'],
        "part_type": part_data['PartType'],
    }
    parent_part_numbers = [loincify(x) for x in part_data['Parents'] if
                           loincify(x) != params['id']]
    if len(parent_part_numbers):
        params['subClassOf'] = parent_part_numbers
    else:
        params['subClassOf'] = "owl:Thing"
    return params

def generate_class(params):
    part = None
    if params['part_type'] == "TIME":
        part = TimeClass(**params)
    if params['part_type'] == "METHOD":
        part = MethodClass(**params)
    if params['part_type'] == "COMPONENT" or params['part_type'] == "CLASS":
        part = ComponentClass(**params)
    if params['part_type'] == "PROPERTY":
        part = PropertyClass(**params)
    if params['part_type'] == "SYSTEM":
        part = SystemClass(**params)
    return part


class PartOntology(object):
    """

    """
    def __init__(self, schema_path: str, part_file_directory_path: str, part_data_path: str):
        """

        :param schema_path:
        """
        self.sv = SchemaView(schema_path) # '../model/schema/part_schema.yaml'
        self.od = OWLDumper()
        self.part_classes = []
        self.part_file_directory_path = part_file_directory_path
        self.part_data_path = part_data_path
        self.all_parts_df = self.load_part_files()
        self.create_parent_nodes()
        self.parent_child_rels = []

    def load_part_files(self):
        part_file_dfs = []
        for part_file in os.listdir(self.part_file_directory_path):
            if ".tsv" in part_file.lower():
                part_file_dfs.append(pd.read_csv(f'{self.part_file_directory_path}/{part_file}', sep="\t"))
        return pd.concat(part_file_dfs)

    def create_parent_nodes(self):
        part_numbers = self.all_parts_df['ParentPartNumber'].tolist()
        part_data = pd.read_csv(self.part_data_path, sep="\t")
        parts_list = part_data[part_data['PartNumber'].isin(part_numbers)]
        for part in parts_list.itertuples():
            part_data = {
                "PartNumber": part.PartNumber,
                "PartName": part.PartName,
                "PartType": part.PartTypeName,
                "Parents": []
            }
            if part.PartTypeName == "COMPONENT":
                part_data['Parents'].append("LP432695-7")
            if part.PartTypeName == "SYSTEM":
                part_data['Parents'].append("LP76034-5")
            if part.PartTypeName == "METHOD":
                part_data['Parents'].append("LP432811-0")
            if part.PartTypeName == "PROPERTY":
                part_data['Parents'].append("LP432810-2")
            if part.PartTypeName == "TIME":
                part_data['Parents'].append("LP432812-8")
            params = generate_class_params(part_data)
            self.part_classes.append(generate_class(params))

    def generate_ontology(self):
        """
        :return:
        """
        part_groups = self.all_parts_df.groupby("ChildPartNumber")[['ChildPart', "ChildPartName", "ParentPartNumber"]]
        for pg in part_groups:
            part_number = pg[0]
            part_df = pg[1].reset_index()
            part_data = {
                "PartNumber": part_number,
                "PartName": pd.unique(part_df['ChildPart'])[0],
                "PartType": pd.unique(part_df['ChildPartName'])[0],
                "Parents": list(pd.unique(part_df['ParentPartNumber']))
            }
            for parent in part_data['Parents']:
                self.parent_child_rels.append({"child":part_number, "parent":parent})
            params = generate_class_params(part_data)
            self.part_classes.append(generate_class(params))
    def write_to_output(self, output_path):
        """

        :param output_path:
        :return:
        """
        pd.DataFrame(self.parent_child_rels).to_csv("parent_child.tsv", sep="\t")
        with open(output_path, 'w') as ccl_owl:  # ./data/output/owl_component_files/part_ontology.owl
            ccl_owl.write(self.od.dumps(self.part_classes, schema=self.sv.schema,))
