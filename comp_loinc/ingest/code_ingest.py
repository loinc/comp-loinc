"""Code ingest

# ## Example
# lcc = CodeIngest("./model/schema/code_schema.yaml", "./data/part_files")
# lcc.write_output_to_file("./data/output/owl_component_files/code_classes.owl")
"""
import pandas as pd
from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
# from linkml_runtime.utils.introspection import package_schemaview

from pathlib import Path
import os
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
from comp_loinc.ingest.source_data_utils import loincify
from comp_loinc.loinc_owl.code_schema import LoincCodeClass
# from comp_loinc.loinc_owl.set_schema import LoincCodeOntology
# from linkml_runtime.dumpers import json_dumper
# import json


class CodeIngest(object):
    def __init__(self, schema_path, code_file_path):
        self.code_file_path = code_file_path
        self.code_dataframe = self.process_code_files()
        self.group_map = self.group_by_code()
        self.sv = SchemaView(schema_path) # '../model/schema/code_schema.yaml'
        self.od = OWLDumper()
        self.code_classes = []
        self.generate_codes()

    def process_code_files(self):
        code_dfs = []
        for file in os.listdir(self.code_file_path):
            code_dfs.append(pd.read_csv(f"{self.code_file_path}/{file}", sep="\t"))
        return pd.concat(code_dfs)

    def group_by_code(self):
        group_map = {}
        groups = self.code_dataframe.groupby(['LoincNumber', 'LoincFormalName'])
        for group, data in groups:
            group_map[group[0]] = {
                "name": group[1],
                "parts": list(zip(data['ChildPartNumber'], data['ChildPartName']))
            }
        return group_map

    def generate_codes(self):
        def part_type_to_predicate(part_type):
            part_pred_map = {
                "TIME": "has_time",
                "PROPERTY": "has_property",
                "METHOD": "has_method",
                "COMPONENT": "has_component",
                "SYSTEM": "has_system"
            }
            return part_pred_map[part_type]
        for loinc_number, data in self.group_map.items():
            params = {
                "id": loincify(loinc_number),
                "label": data['name'],
                "subClassOf": loincify("lc0000001")
            }
            for pnum, ptype in data['parts']:
                params[part_type_to_predicate(ptype)] = loincify(pnum)
            code_class = LoincCodeClass(**params)
            self.code_classes.append(code_class)

    def write_output_to_file(self, output_path):
        #"../../data/output/code_classes.owl"
        with open(output_path, 'w') as ccl_owl:
            ccl_owl.write(self.od.dumps(self.code_classes, schema=self.sv.schema))
        # loinc_ontology_class = LoincCodeOntology(code_class_set=code_classes)

        # with open("../data/output/code_classes.json", 'w') as ccl_json:
        #     ccl_json.write(json_dumper.dumps(loinc_ontology_class))
