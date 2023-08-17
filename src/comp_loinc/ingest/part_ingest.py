"""Part ingest

# ## Example
# po = PartOntology("./model/schema/part_schema.yaml", "./local_data/part_files")
# po.generate_ontology()
# po.write_to_output('./data/output/owl_component_files/part_ontology.owl')
# # po.write_to_output('./local_data/part_ontology_files/part_ontology.owl')
"""

from comp_loinc.ingest.source_data_utils import loincify, counter
from comp_loinc.datamodel import ComponentClass, SystemClass, ScaleClass, TimeClass, MethodClass, PropertyClass

import pandas as pd
from linkml_owl.dumpers.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
import os
from pathlib import Path
import sys
import datetime

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))


class PartOntology(object):
    """
    Part Ontology
    Builds the part ontology from the part files
    """
    def __init__(self, schema_path: str, part_file_directory_path: str):
        print(f"Beginning Part Ingest at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
        Iterate through the part files and generate the part ontology
        :return:
        """
        part_groups = self.all_parts_df.groupby("ChildPartNumber")[['ChildPart', "ChildPartTypeName", "ParentPartNumber"]]
        for i, pg in enumerate(part_groups):
            counter(i+1, len(part_groups))
            params = {
                "id": loincify(pg[0]),
                "part_number": pg[0]
            }
            part_attributes = pg[1].reset_index()
            params['label'] = part_attributes["ChildPart"].unique()[0]
            params['part_type'] = part_attributes["ChildPartTypeName"].unique()[0]
            # if the part has a parent part, add it to the subClassOf list
            parent_part_numbers = [
                loincify(x) for x in part_attributes['ParentPartNumber'].unique() if loincify(x) != params['id']
            ]
            if len(parent_part_numbers):
                params['subClassOf'] = parent_part_numbers
            else:
                params['subClassOf'] = "owl:Thing"
            part = None
            # choose the proper data model class based on the part type
            # Currently, the only specific part types ingested are: TIME, METHOD, COMPONENT, PROPERTY, SYSTEM, SCALE
            # match params['part_type']:
            #     case "TIME":
            #         part = TimeClass(**params)
            #     case "METHOD":
            #         part = MethodClass(**params)
            #     case "COMPONENT":
            #         part = ComponentClass(**params)
            #     case "CLASS":
            #         # Some components are of part type CLASS (I thought this was only for abstract classes)
            #         part = ComponentClass(**params)
            #     case "PROPERTY":
            #         part = PropertyClass(**params)
            #     case "SYSTEM":
            #         part = SystemClass(**params)
            #     case "SCALE":
            #         part = ScaleClass(**params)

            # match not available in 3.8
            part_classes = {
                'TIME': datamodel.TimeClass,
                'METHOD': datamodel.MethodClass,
                'COMPONENT': datamodel.ComponentClass,
                'CLASS': datamodel.ComponentClass,
                'PROPERTY': datamodel.PropertyClass,
                'SYSTEM': datamodel.SystemClass,
                'SCALE': datamodel.ScaleClass
            }

            if params['part_type'] in part_classes:
                part = part_classes[params['part_type']](**params)

            if part:
                self.part_classes.append(part)

    def write_to_output(self, output_path):
        """
        Use the OWLDumper to write the ontology to the output path
        :param output_path: str
        """
        print("\n" + f"Writing Part Ontology to output {output_path}")
        with open(output_path, 'w') as ccl_owl:  # ./data/output/owl_component_files/part_ontology.owl
            ccl_owl.write(self.od.dumps(self.part_classes, schema=self.sv.schema,))
        print("\n" + f"Finished writing Part Ontology to output {output_path} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
