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


class PartOntology(object):
    """

    """
    def __init__(self, schema_path: str, part_file_directory_path: str):
        """

        :param schema_path:
        """
        self.sv = SchemaView(schema_path) # '../model/schema/part_schema.yaml'
        self.od = OWLDumper()
        self.part_classes = []
        self.part_file_directory_path = part_file_directory_path
        self.all_parts_df = self.load_part_files()

    def load_part_files(self):
        part_file_dfs = []
        for part_file in os.listdir(self.part_file_directory_path):
            part_file_dfs.append(pd.read_csv(f'{self.part_file_directory_path}/{part_file}', sep="\t"))
        return pd.concat(part_file_dfs)

    def generate_ontology(self):
        """

        :return:
        """
        part_groups = self.all_parts_df.groupby("ChildPartNumber")[['ChildPart', "ChildPartName", "ParentPartNumber"]]
        for pg in part_groups:
            params = {
                "id": loincify(pg[0]),
                "part_number": pg[0]
            }
            part_attributes = pg[1].reset_index()
            params['label'] = list(set(part_attributes['ChildPart'].tolist()))[0]
            params['part_type'] = list(set(part_attributes['ChildPartName'].tolist()))[0]
            parent_part_numbers = [loincify(x) for x in list(set(part_attributes['ParentPartNumber'].tolist())) if loincify(x) != params['id']]
            if len(parent_part_numbers):
                params['subClassOf'] = parent_part_numbers
            else:
                params['subClassOf'] = "owl:Thing"

            if params['part_type'] == "TIME":
                part = TimeClass(**params)
                self.part_classes.append(part)
            if params['part_type'] == "METHOD":
                part = MethodClass(**params)
                self.part_classes.append(part)
            if params['part_type'] == "COMPONENT" or params['part_type'] == "CLASS":
                part = ComponentClass(**params)
                self.part_classes.append(part)
            if params['part_type'] == "PROPERTY":
                part = PropertyClass(**params)
                self.part_classes.append(part)
            if params['part_type'] == "SYSTEM":
                part = SystemClass(**params)
                self.part_classes.append(part)

    def write_to_output(self, output_path):
        """

        :param output_path:
        :return:
        """
        with open(output_path, 'w') as ccl_owl:  # ./data/output/owl_component_files/part_ontology.owl
            ccl_owl.write(self.od.dumps(self.part_classes, schema=self.sv.schema,))
