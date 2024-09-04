from pathlib import Path
from pprint import pprint

import loinclib

home = Path(__file__).resolve().parent.parent.parent.parent

release = loinclib.LoincRelease(home / 'data' / 'loinc_release' / 'extracted',
                                '2.74',
                                home / 'data' / 'loinc_trees' / '2023-06-14')

release.load_AccessoryFiles_PartFile_Part_csv()
release.load_tree_component()

nodes = release.out_node_ids(loinclib.NodeType.type_for_identifier('LP343315-0').node_id_of_identifier('LP343315-0'),
                           loinclib.EdgeType.LoincLib_HasParent)

related_node = list(nodes.values())[0]
node_type = loinclib.NodeType.type_for_node_id(related_node)

lp = nodes['LP:LP101394-7']

part_ids = release.node_ids_for_type(loinclib.NodeType.loinc_part)

for part_id in part_ids:
    properties = release.node_properties(part_id, loinclib.NodeType.loinc_part)
    pprint(properties)
