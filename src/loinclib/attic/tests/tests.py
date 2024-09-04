from pathlib import Path
from unittest import TestCase

from networkx import MultiDiGraph


from loinclib.loinc_schema import loinc_schema, LoincNodeType, LoincTermProps

LOINC_PATH = Path('../../../loinc_release/2.67')
TREE_PATH = Path('../../../loinc_trees/2023-09-26')



class TestHello(TestCase):

    def test_hello(self):

        loinc_graph = LoincGraph(release_path=LOINC_PATH, trees_path=TREE_PATH, loinc_version='2.67', schema=loinc_schema)
        loinc_graph.load_loinc_table__loinc_csv()

        print(loinc_graph)
        #
        #
        # loinc_term_type = loinc_schema.get_node_type(LoincNodes.LoincTerm)
        # self.assertIsNotNone(loinc_term_type)
        #
        # loinc_number_prop = loinc_term_type.get_property(LoincTermProps.loinc_number)
        # self.assertIsNotNone(loinc_number_prop)
        #
        # value = loinc_number_prop.set_value(code='1234-5', value='test', graph=g.graph, create_node=True)
        # self.assertIn(LoincTermProps.loinc_number.loinc_number, value, 'Not there')
        # self.assertEqual('test', loinc_number_prop.get_value(code='1234-5', graph=g.graph), 'Not there')

    # def test_hello_node_view(self):
    #     g = LoincGraph(release_path=LOINC_PATH, trees_path=TREE_PATH, loinc_version='2.67')
    #
    #     loinc_term_type = loinc_schema.get_node_type(LoincNodes.LoincTerm)
    #     self.assertIsNotNone(loinc_term_type)
    #
    #     node_view = loinc_term_type.get_node_view_by_code(code='1234-5', graph=g.graph, create=True)
    #     self.assertIsNotNone(node_view)
    #
    #     node_view = node_view.set_property(property_=LoincTermProps.loinc_number, value='test')
    #     self.assertIsNotNone(node_view)
    #
    #     value = node_view.get_property(LoincTermProps.loinc_number)
    #     self.assertEqual('test', value, 'Not there')


    def test_multidi_edges(self):
        mdg = MultiDiGraph()
        mdg.add_edge('from', 'to', color='red', name='test')

        from_ = mdg.succ['from']
        to_= from_['too']
        # from_ = mdg.out_edges.get('from', None)


        out_view = mdg.out_edges()
        # get = out_view.get('from', None)

        print(out_view)
