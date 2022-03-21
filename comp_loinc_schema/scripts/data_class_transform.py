import pandas as pd
from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview

from loinc_owl.part_schema import ComponentClass, LoincCodeOntology
from linkml_runtime.dumpers import json_dumper


component_system_hierarchy = pd.read_excel('../data/CHEM_HIERARCHY_LPL_DATA.xlsx', sheet_name="Hierarchy").astype(str)
supplement_names = pd.read_csv('../data/LoincPartLink_Primary.csv')
class_data = []

merged = pd.merge(how='left', left=component_system_hierarchy, left_on='FK_ID', right=supplement_names, right_on='PartNumber')
component_i = merged.loc[(merged["PartTypeName"] == "COMPONENT"), ['PARENT_ID', 'PartNumber', 'PartName']].drop_duplicates().astype(str)
component = component_i.groupby(['PartName', 'PartNumber'])['PARENT_ID'].apply(' '.join).reset_index()
system = merged[merged['PartTypeName'] == 'SYSTEM']


def get_parent_code(parent_node_id, dataframe):
    parent_code = dataframe.loc[dataframe["NODE_ID"] == parent_node_id, 'FK_ID']
    return parent_code.values[0]


def loincify(id):
    return f"loinc:{id}"


component_classes = []
# sv = package_schemaview('comp_loinc_schema.part_schema')
sv = SchemaView('../model/schema/part_schema.yaml')
od = OWLDumper()


for index, comp in enumerate(component.itertuples()):
    if index < 15:
        parents_list = [loincify(get_parent_code(x, component_system_hierarchy)) for x in comp.PARENT_ID.split()]
        component_class = ComponentClass(id=loincify(comp.PartNumber), subClassOf=parents_list, label=comp.PartName)
        component_classes.append(component_class)
with open("../data/output/component_classes.owl", 'w') as ccl_owl:
    ccl_owl.write(od.dumps(component_classes, schema=sv.schema))
loinc_ontology_class = LoincCodeOntology(component_class_set=component_classes)
#
# with open("../data/output/component_classes.json", 'w') as ccl_json:
#     ccl_json.write(json_dumper.dumps(loinc_ontology_class))
#     # joined = ',\n'.join([json_dumper.dumps(x) for x in component_classes])
#     # ccl_json.write(f"[\n{joined}\n]")



