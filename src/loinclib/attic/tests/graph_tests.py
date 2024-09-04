import unittest
from enum import StrEnum

from loinclib.graph import LoinclibGraph
from loinclib.loinc_schema import LoincNodeType, LoincTermProps


class GraphTests(unittest.TestCase):

  def test_graph_1(self):
    graph = LoinclibGraph()
    self.assertIsNotNone(graph)

    node_type = graph.schema.get_node_type(LoincNodeType.LoincTerm)
    self.assertIsNotNone(node_type)

    node = graph.getsert_node(type_=LoincNodeType.LoincTerm, code='123')
    node.set_property(type_=LoincTermProps.loinc_number, value='123')
    loinc_number = node.get_property_type(type_=LoincTermProps.loinc_number)
    self.assertEqual(loinc_number, '123')

    node.set_property(type_=LoincTermProps.loinc_number, value=None)
    self.assertNotIn(member=LoincTermProps.loinc_number, container=node.get_properties())

    node2 = graph.getsert_node(type_=LoincNodeType.LoincTerm, code='123')
    self.assertIs(node.get_properties(), node2.get_properties())


    print(node)


