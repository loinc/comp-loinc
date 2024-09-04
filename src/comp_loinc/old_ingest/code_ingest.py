import pandas as pd
from linkml_owl.dumpers.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
import datetime
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
from comp_loinc.ingest.source_data_utils import loincify, counter
from comp_loinc.datamodel import LoincTerm


class CodeIngest(object):
    """
    Code ingest

    """
    def __init__(self, schema_path: str, code_file_path: str):
        print(f"Beginning Code Ingest at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.code_file_path = code_file_path
        self.lpl_dataframe = self.process_lpl_file()
        self.code_dataframe = self.process_loinc_file()
        self.code_classes = []
        self.concatentate_formal_name()
        self.group_map = self.group_by_code()
        self.generate_codes()
        self.sv = SchemaView(schema_path) # '../model/schema/code_schema.yaml'
        self.od = OWLDumper()

    def process_lpl_file(self):
        """
        Read the LoincPartLink_Primary.csv file into a pandas dataframe
        "LoincNumber","LongCommonName","PartNumber","PartName","PartCodeSystem","PartTypeName","LinkTypeName","Property"
        """
        return pd.read_csv(f'{self.code_file_path}/LoincPartLink_Primary.csv', sep=",", dtype=str)

    def process_loinc_file(self):
        """
        Read the Loinc.csv file into a pandas dataframe
        "LOINC_NUM","COMPONENT","PROPERTY","TIME_ASPCT","SYSTEM","SCALE_TYP","METHOD_TYP","CLASS","VersionLastChanged",
        "CHNG_TYPE","DefinitionDescription","STATUS","CONSUMER_NAME","CLASSTYPE","FORMULA","EXMPL_ANSWERS",
        "SURVEY_QUEST_TEXT","SURVEY_QUEST_SRC","UNITSREQUIRED","RELATEDNAMES2","SHORTNAME","ORDER_OBS",
        "HL7_FIELD_SUBFIELD_ID","EXTERNAL_COPYRIGHT_NOTICE","EXAMPLE_UNITS","LONG_COMMON_NAME","EXAMPLE_UCUM_UNITS",
        "STATUS_REASON","STATUS_TEXT","CHANGE_REASON_PUBLIC","COMMON_TEST_RANK","COMMON_ORDER_RANK",
        "COMMON_SI_TEST_RANK","HL7_ATTACHMENT_STRUCTURE","EXTERNAL_COPYRIGHT_LINK","PanelType","AskAtOrderEntry",
        "AssociatedObservations","VersionFirstReleased","ValidHL7AttachmentRequest","DisplayName"
        """
        return pd.read_csv(f'{self.code_file_path}/Loinc.csv', sep=",", dtype=str)

    def concatentate_formal_name(self):
        """
        Concatenate the columns of the LoincPartLink_Primary.csv file to create the LoincFormalName
        ‘COMPONENT:PROPERTY:TIME_ASPCT:SYSTEM:SCALE_TYP:METHOD_TYP’
        """
        cols = ['COMPONENT', 'PROPERTY', 'TIME_ASPCT', 'SYSTEM', 'SCALE_TYP', 'METHOD_TYP']
        self.code_dataframe['LoincFormalName'] = self.code_dataframe[cols].apply(lambda row: ':'.join(row.values.astype(str)), axis=1)

    def get_included_codes(self):
        """
        Get the list of codes that should be ingested
        Initial set is chemical component codes
        """
        with open(f"{self.code_file_path}/included_codes.tsv", 'r') as f:
            return [line.strip() for line in f.readlines()]

    def group_by_code(self):
        """
        Group parts by code
        """
        group_map = {}
        groups = self.lpl_dataframe.groupby(['LoincNumber'])[["PartNumber", "PartTypeName"]]
        for group, data in groups:
            group_map[group] = {
                "name": group,
                "parts": list(zip(data['PartNumber'], data['PartTypeName']))
            }
        return group_map

    def generate_codes(self):
        part_pred_map = {
            "TIME": "has_time",
            "PROPERTY": "has_property",
            "METHOD": "has_method",
            "COMPONENT": "has_component",
            "SYSTEM": "has_system",
            "SCALE": "has_scale"
        }
        included_codes = self.get_included_codes()
        for i, loinc_number in enumerate(included_codes):
            counter(i + 1, len(included_codes))
            if loinc_number in self.group_map.keys():
                row = self.code_dataframe[self.code_dataframe['LOINC_NUM'] == loinc_number].iloc[0]
                params = {
                            "id": loincify(row.LOINC_NUM),
                            "label": row.LoincFormalName,
                            "formal_name": row.LoincFormalName,
                            "loinc_number": row.LOINC_NUM,
                            "long_common_name": row.LONG_COMMON_NAME,
                            "status": row.STATUS,
                            "short_name": row.SHORTNAME,
                            "subClassOf": loincify("lc0000001")
                        }
                lpl = self.group_map[row.LOINC_NUM]
                for part, part_type in lpl['parts']:
                    if part_type in part_pred_map.keys():
                        params[part_pred_map[part_type]] = loincify(part)
                self.code_classes.append(LoincTerm(**params))

    def write_output_to_file(self, output_path):
        #"../../data/output/code_classes.owl"
        print(f"\nWriting to ouput at {output_path}")
        with open(output_path, 'w') as ccl_owl:
            ccl_owl.write(self.od.dumps(self.code_classes, schema=self.sv.schema))
        print(f"Finished Code Ingest at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
