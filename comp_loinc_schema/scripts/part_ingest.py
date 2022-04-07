import pandas as pd
from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview
from source_data_utils import loincify
from loinc_owl.part_schema import ComponentClass, SystemClass, PartClass
from loinc_owl.set_schema import LoincCodeOntology
from linkml_runtime.dumpers import json_dumper
from scripts.source_data_utils import generate_part_hierarchy, generate_part_type_lookup, generate_label_map, generate_parent_relationships
import json

sv = SchemaView('../model/schema/part_schema.yaml')
od = OWLDumper()


def get_parent_code(parent_node_id, dataframe):
    """
    finds the code of the parent based on the node id of the existing LOINC Part Hierarchy
    :param parent_node_id:
    :param dataframe:
    :return: loinc code
    """
    parent_code = dataframe.loc[dataframe["NODE_ID"] == parent_node_id, 'FK_ID']
    return parent_code.values[0]


part_type_lookup = generate_part_type_lookup("../data/part_type_lookup.json")
part_hierarchy_data = generate_part_hierarchy("../data/CHEM_HIERARCHY_LPL_DATA.xlsx")
label_map = generate_label_map(part_hierarchy_data)
part_parents = generate_parent_relationships(part_hierarchy_data)

part_root = PartClass(id="loinc:LP000001", label="Part", subClassOf=["owl:Thing"])
component_root = ComponentClass(id="loinc:LP000002", label="Component", subClassOf=["loinc:LP000001"])
system_root = ComponentClass(id="loinc:LP000003", label="System", subClassOf=["loinc:LP000001"])
part_classes = [part_root, component_root, system_root]

for part, parents in part_parents.items():
    parents_list = [loincify(x) for x in parents]
    part_type = "PART"
    superclass = False
    if part in part_type_lookup.keys():
        part_type = part_type_lookup[part]
    if len(parents) == 1 and parents[0] == part:
        superclass = True
    if part_type == "PART":
        if superclass:
            parents_list.append(part_root.id)
        part_class = PartClass(id=loincify(part), subClassOf=parents_list, label=label_map[part])
        part_classes.append(part_class)
    if part_type == "COMPONENT":
        if superclass:
            parents_list.append(component_root.id)
        component_class = ComponentClass(id=loincify(part), subClassOf=parents_list, label=label_map[part])
        part_classes.append(component_class)
    if part_type == "SYSTEM":
        if superclass:
            parents_list.append(system_root.id)
        system_class = SystemClass(id=loincify(part), subClassOf=parents_list, label=label_map[part])
        part_classes.append(system_class)
with open("../data/output/part_classes.owl", 'w') as ccl_owl:
    ccl_owl.write(od.dumps(part_classes, schema=sv.schema))
