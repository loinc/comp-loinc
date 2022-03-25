import pandas as pd
from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview
from source_data_utils import loincify
from loinc_owl.code_schema import LoincCodeClass
from loinc_owl.set_schema import LoincCodeOntology
from linkml_runtime.dumpers import json_dumper
import json

lpl = pd.read_excel('../data/CHEM_HIERARCHY_LPL_DATA.xlsx', sheet_name="LPL")
sv = SchemaView('../model/schema/code_schema.yaml')
od = OWLDumper()

code_classes = []
for index, code in enumerate(lpl.itertuples()):
    if index < 10:
        if code.NAME == "COMPONENT":
            code_class = LoincCodeClass(
                id=loincify(code.LOINC_NUM),
                label=code.LONG_COMMON_NAME,
                has_component=loincify(code.PART_NUM))
            code_classes.append(code_class)
        if code.NAME == "SYSTEM":
            code_class = LoincCodeClass(
                id=loincify(code.LOINC_NUM),
                label=code.LONG_COMMON_NAME,
                has_system=loincify(code.PART_NUM))
            code_classes.append(code_class)
with open("../data/output/code_classes.owl", 'w') as ccl_owl:
    ccl_owl.write(od.dumps(code_classes, schema=sv.schema))
loinc_ontology_class = LoincCodeOntology(code_class_set=code_classes)

with open("../data/output/code_classes.json", 'w') as ccl_json:
    ccl_json.write(json_dumper.dumps(loinc_ontology_class))
    # joined = ',\n'.join([json_dumper.dumps(x) for x in code_classes])
    # ccl_json.write(f"[\n{joined}\n]")
