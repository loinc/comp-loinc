import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from sssom.io import convert_file
from sssom import context
from comp_loinc.ingest.source_data_utils import loincify
from pathlib import Path
import os
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))


class Mappings(object):
    def __init__(self, user, pwd):
        self.fhir_endpoint = 'https://fhir.loinc.org'
        self.username = user
        self.password = pwd

    def get_fhir_chebi_mappings(self):
        r = requests.get(f"{self.fhir_endpoint}/ConceptMap/?url=http://loinc.org/cm/loinc-parts-to-chebi",
                         auth=HTTPBasicAuth(self.username, self.password))
        return r.json()

    def create_chebi_loinc_sssom(self):
        chebi_context_map =  """# curie_map:
#   linkml: https://w3id.org/linkml/
#   sempav: https://w3id.org/sempav
#   loinc: https://loinc.org/ 
#   CHEBI: http://purl.obolibrary.org/obo/CHEBI_
#   skos: http://www.w3.org/2004/02/skos/core#
# license: https://github.com/mapping-commons/mapping-commons.github.io/blob/main/docs/original_license_applies.md
# mapping_date: '2022-02-23'
# mapping_set_id: http://w3id.org/mapping_commons/disease-mappings/onto-icd10
# mapping_tool: https://github.com/mapping-commons/sssom-py
"""
        chebi_loinc_fhir = self.get_fhir_chebi_mappings()
        part_mappings = chebi_loinc_fhir['entry'][0]['resource']['group'][0]['element']
        sssom_mappings = []
        for part_map in part_mappings:
            predicate_map = {
                "equivalent": 'skos:exactMatch',
                "relatedto": 'skos:relatedMatch'
            }
            sssom_obj = dict()

            sssom_obj['subject_id'] = loincify(part_map['code'])
            sssom_obj['predicate_id'] = predicate_map[part_map['target'][0]['equivalence']]
            sssom_obj['object_id'] = part_map['target'][0]['code']
            sssom_obj['object_label'] = part_map['target'][0]['display']
            sssom_obj['mapping_justification'] = "sempav:HumanCuration"
            sssom_mappings.append(sssom_obj)
        l2c_df = pd.DataFrame(sssom_mappings)

        with open(f"{path_root}/data/sssom_mapping_files/loinc2chebi.tsv", 'w') as lc:
            lc.write(chebi_context_map)
            l2c_df.to_csv(lc, sep="\t", index=False)

    def sssom_chebi_to_owl(self):
        with open(f"{path_root}/data/output/owl_component_files/loinc2chebi.owl", 'w') as l2co:
            convert_file(f"{path_root}/data/sssom_mapping_files/loinc2chebi.tsv", output=l2co, output_format='owl')
