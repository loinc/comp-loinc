import pandas as pd
from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview

from loinc_owl.part_schema import ComponentClass, LoincCodeOntology
from linkml_runtime.dumpers import json_dumper
import json

# component_system_hierarchy = pd.read_excel('../data/CHEM_HIERARCHY_LPL_DATA.xlsx', sheet_name="Hierarchy").astype(str)
# supplement_names = pd.read_csv('../data/LoincPartLink_Primary.csv')
# class_data = []
#
# merged = pd.merge(how='left', left=component_system_hierarchy, left_on='FK_ID', right=supplement_names, right_on='PartNumber')
# component_i = merged.loc[(merged["PartTypeName"] == "COMPONENT"), ['PARENT_ID', 'PartNumber', 'PartName']].drop_duplicates().astype(str)
# component = component_i.groupby(['PartName', 'PartNumber'])['PARENT_ID'].apply(' '.join).reset_index()
# system = merged[merged['PartTypeName'] == 'SYSTEM']


def get_parent_code(parent_node_id, dataframe):
    parent_code = dataframe.loc[dataframe["NODE_ID"] == parent_node_id, 'FK_ID']
    return parent_code.values[0]


def loincify(id):
    return f"loinc:{id}"
with open ("../data/part_type_lookup.json", 'r') as ptl:
    part_type_lookup = json.load(ptl)
component = pd.read_csv('../data/part_hierarchy.tsv', sep="\t")
label_map = {x.FK_ID: x.PART for x in component[["FK_ID", "PART"]].drop_duplicates().itertuples()}
component_classes = []
# sv = package_schemaview('comp_loinc_schema.part_schema')
sv = SchemaView('../model/schema/part_schema.yaml')
od = OWLDumper()

from collections import defaultdict
d = defaultdict(list)
for index, comp in enumerate(component.itertuples()):
    d[comp.FK_ID].append(comp.parent_part_id)

for part, parents in d.items():
    parents_list = [loincify(x) for x in parents]
    description = "No Part Type"
    if part in part_type_lookup.keys():
        description = part_type_lookup[part]
    component_class = ComponentClass(id=loincify(part), subClassOf=parents_list, label=label_map[part], description=description)
    component_classes.append(component_class)
with open("../data/output/component_classes.owl", 'w') as ccl_owl:
    ccl_owl.write(od.dumps(component_classes, schema=sv.schema))
loinc_ontology_class = LoincCodeOntology(component_class_set=component_classes)

with open("../data/output/component_classes.json", 'w') as ccl_json:
    ccl_json.write(json_dumper.dumps(loinc_ontology_class))
    joined = ',\n'.join([json_dumper.dumps(x) for x in component_classes])
    ccl_json.write(f"[\n{joined}\n]")

#
#
