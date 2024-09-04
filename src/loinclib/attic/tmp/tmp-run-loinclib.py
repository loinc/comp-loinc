from pathlib import Path

from loinclib import LoincRelease
from loinclib.enums import NodePrefix

project_path = Path(__file__).parent.parent.parent

release = LoincRelease(project_path / 'data' / 'loinc_release' / 'extracted',
                       '2.7.4', project_path / 'data' / 'loinc_trees' / '2023-06-14')

release.load_AccessoryFiles_PartFile_Part_csv()
release.parse_LoincTable_Loinc_csv()
release.load_tree_component()

print(release.nx_graph.nodes(data=True)[NodePrefix.loinc_part + 'LP115711-6'])



