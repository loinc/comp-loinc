from pathlib import Path
from unittest import TestCase

from comp_loinc import Runtime
from loinclib.loinc_loader import LoincLoader
from loinclib.loinc_schema import LoincNodeType
from loinclib import SnomedLoader, SnomedNodeType, SnomedEdges, Configuration
from loinclib.loinc_snomed_loader import LoincSnomedLoader
from loinclib.loinc_tree_loader import LoincTreeLoader

LOINC_PATH = Path('loinc_release/2.67')
TREE_PATH = Path('loinc_trees/2023-09-26')


class TestLoading(TestCase):

  def test_load_loinc_table(self):
    pass

  def test_load_primary(self):
    configuration = Configuration()
    runtime = Runtime(configuration=configuration)
    loinc_loader = LoincLoader(graph=runtime.graph, configuration=configuration)
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    node = runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code='100021-5')

    for edge in node.get_all_out_edges():
      print(edge)

    print(runtime)

  def test_load_snomed(self):
    configuration = Configuration()
    runtime = Runtime(configuration=configuration)
    snomed_loader = SnomedLoader(config=configuration, graph=runtime.graph)
    #
    snomed_loader.load_selected_relations(SnomedEdges.is_a)
    #
    node = runtime.graph.get_node_by_code(type_=SnomedNodeType.Concept, code='237334005')
    for edge in node.get_all_out_edges():
      print(edge)


    print('done')

  def tests_load_loinc_snomed(self):
    configuration = Configuration()
    runtime = Runtime(configuration=configuration)

    loinc_snomed_loader = LoincSnomedLoader(config=configuration, graph=runtime.graph)
    loinc_snomed_loader.load_description()
    loinc_snomed_loader.load_identifier()
    loinc_snomed_loader.load_relationship()

    node = runtime.graph.get_node_by_code(type_=SnomedNodeType.Concept, code='40081010000107')
    for edge in node.get_all_out_edges():
      print(edge)

  def test_load_part_parent(self):
    configuration = Configuration()
    runtime = Runtime(configuration=configuration)
    loinc_loader = LoincLoader(graph=runtime.graph, configuration=configuration)
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()


  def test_load_trees(self):
    configuration = Configuration()
    runtime = Runtime(configuration=configuration)
    tree_loader = LoincTreeLoader(config=configuration, graph=runtime.graph)
    tree_loader.load_class_tree()
    tree_loader.load_component_tree()
    tree_loader.load_component_by_system_tree()
    tree_loader.load_document_tree()
    tree_loader.load_method_tree()
    tree_loader.load_panel_tree()
    tree_loader.load_system_tree()

