import re
import typing
from pathlib import Path

from loinclib import LoincGraph

project_path = Path(__file__).parent.parent.parent.parent

release = LoincGraph(project_path / 'data' / 'loinc_release' / 'extracted',
                       '2.7.4', project_path / 'data' / 'loinc_trees' / '2023-06-14')

rels: typing.Set[typing.Tuple] = set()

for tpl in release.read_AccessoryFiles_PartFile_LoincPartLink_Supplementary_csv().itertuples():
    (row_number, loinc_number, long_common_name, part_number, part_name,
     part_code_system, part_type_name, link_type_name, property_uri) = tpl

    rel = f'{link_type_name}_{part_type_name}_{property_uri[property_uri.rindex("/"):]}'
    rel = re.sub('[^0-9a-zA-Z]+', '_', rel)
    rel = re.sub('_+', '_', rel)

    rels.add((rel, link_type_name, part_type_name, property_uri))

l = list(rels)
l.sort()
for (enum_name, group, name, uri) in l:
    print(f"{enum_name} = '{group}', '{name}', '{uri}'")