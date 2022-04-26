import pandas as pd
from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview

from pathlib import Path
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
        self.lpl = pd.read_excel(code_file_path, sheet_name="LPL") #'../data/CHEM_HIERARCHY_LPL_DATA.xlsx'
        self.sv = SchemaView(schema_path) # '../model/schema/code_schema.yaml'
        self.od = OWLDumper()

    def generate_codes(self):
        for index, code in enumerate(self.lpl.itertuples()):
            if code.NAME == "COMPONENT":
                code_class = LoincCodeClass(
                    id=loincify(code.LOINC_NUM),
                    label=code.LONG_COMMON_NAME,
                    has_component=loincify(code.PART_NUM)
                )
                self.code_classes.append(code_class)
            if code.NAME == "SYSTEM":
                code_class = LoincCodeClass(
                    id=loincify(code.LOINC_NUM),
                    label=code.LONG_COMMON_NAME,
                    has_system=loincify(code.PART_NUM))
                self.code_classes.append(code_class)

    def write_output_to_file(self, output_path):
        #"../../data/output/code_classes.owl"
        with open(output_path, 'w') as ccl_owl:
            ccl_owl.write(self.od.dumps(self.code_classes, schema=self.sv.schema))
        # loinc_ontology_class = LoincCodeOntology(code_class_set=code_classes)

        # with open("../data/output/code_classes.json", 'w') as ccl_json:
        #     ccl_json.write(json_dumper.dumps(loinc_ontology_class))
