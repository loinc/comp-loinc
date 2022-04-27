from linkml_owl.owl_dumper import OWLDumper
from linkml_runtime import SchemaView

from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from comp_loinc.ingest.source_data_utils import loincify
from comp_loinc.loinc_owl.part_schema import ComponentClass, SystemClass, PartClass
# from scripts.source_data_utils import generate_part_hierarchy, generate_part_type_lookup, generate_label_map, generate_parent_relationships
from comp_loinc.ingest.source_data_utils import PartHierarchy, PartLookups



class PartOntology(object):
    """

    """
    def __init__(self, schema_path):
        """

        :param schema_path:
        """
        self.sv = SchemaView(schema_path) # '../model/schema/part_schema.yaml'
        self.od = OWLDumper()
        self.part_type_lookup = None
        self.part_parents_lookup = None
        self.part_name_lookup = {}

        """
        Hardcoded high level Part classes that don't exist in LOINC yet
        """
        self.part_root = PartClass(id="loinc:LP000001", label="Part", subClassOf=["owl:Thing"])
        self.component_root = ComponentClass(id="loinc:LP000002", label="Component", subClassOf=["loinc:LP000001"])
        self.system_root = SystemClass(id="loinc:LP000003", label="System", subClassOf=["loinc:LP000001"])
        self.class_root = PartClass(id="loinc:LP000004", label="Class", subClassOf=["loinc:LP000001"])
        self.part_classes = [self.part_root, self.component_root, self.system_root, self.class_root]

    def generate_part_type_lookup(self, loinc_part_file):
        """

        :param loinc_part_file:
        :return:
        """
        part_lookups = PartLookups(loinc_part_file) #"../local_data/Part.csv"
        self.part_type_lookup = part_lookups.generate_part_type_lookup()
        self.part_name_lookup.update(part_lookups.generate_part_name_lookup())

    def generate_part_hierarchy_lookup(self, chem_hierarchy_file):
        """

        :param chem_hierarchy_file:
        :return:
        """
        part_hierarchy = PartHierarchy(chem_hierarchy_file) # "../local_data/CHEM_HIERARCHY_LPL_DATA.xlsx"
        self.part_parents_lookup = part_hierarchy.generate_parent_relationships()
        self.part_name_lookup.update(part_hierarchy.generate_label_map())

    def generate_ontology(self):
        """

        :return:
        """
        for index, part_parent in enumerate(self.part_parents_lookup.items()):
            part, parents = part_parent
            parents_list = [loincify(x) for x in parents]
            part_type = "PART"
            superclass = False
            part_name = None
            part_curie = loincify(part)
            if part in self.part_name_lookup.keys():
                part_name = self.part_name_lookup[part]
            if part in self.part_type_lookup.keys():
                part_type = self.part_type_lookup[part]
            if len(parents) == 1 and parents[0] == part:
                superclass = True
            if part_type == "PART":
                if superclass:
                    parents_list.append(self.part_root.id)
                part_class = PartClass(id=part_curie, subClassOf=parents_list, label=part_name)
                self.part_classes.append(part_class)
            if part_type == "COMPONENT":
                if superclass:
                    parents_list.append(self.component_root.id)
                component_class = ComponentClass(id=part_curie, subClassOf=parents_list, label=part_name)
                self.part_classes.append(component_class)
            if part_type == "SYSTEM" or part_type == "SUPER SYSTEM":
                if superclass:
                    parents_list.append(self.system_root.id)
                system_class = SystemClass(id=part_curie, subClassOf=parents_list, label=part_name)
                self.part_classes.append(system_class)
            if part_type == "CLASS":
                if superclass:
                    parents_list.append(self.class_root.id)
                class_class = PartClass(id=part_curie, subClassOf=parents_list, label=part_name)
                self.part_classes.append(class_class)

    def write_to_output(self, output_path):
        """

        :param output_path:
        :return:
        """
        with open(output_path, 'w') as ccl_owl: # "../data/output/part_classes_test.owl"
            ccl_owl.write(self.od.dumps(self.part_classes, schema=self.sv.schema))
