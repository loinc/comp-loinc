from fontTools.misc.bezierTools import namedtuple
from networkx.classes import MultiDiGraph

from comp_loinc import Runtime
import typing as t

from loinclib import Configuration, LoincLoader, LoincNodeType, Node, EdgeType, Edge, ElementProps, ElementKeys
from loinclib.loinc_schema import LoincTermEdgeType, LoincTermPrimaryEdges, LoincPartProps, LoincPartEdge, \
  LoincTermSupplementaryEdges
from loinclib.loinc_tree_loader import LoincTreeLoader
from loinclib.loinc_tree_schema import LoincEdges, LoincTreeProps, LoincTreeEdges, LoincDanglingNlpEdges
import typing as t


class GraphCommands:

  def __init__(self, *, config: Configuration):
    self.runtime: t.Optional[Runtime] = None
    self.config = config

    self.seen_nodes: t.Dict[str, Node] = {}

  def setup_builder(self, builder):
    builder.cli.command(
        "graph-find-part-cycles", help="Finds cycles in the LOINC parts hierarchy."
    )(self.find_part_cycles)

  def find_part_cycles(self):
    loinc_loader = LoincLoader(graph=self.runtime.graph, configuration=self.config)
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    loinc_loader.load_accessory_files__part_file__part_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

    tree_loader: LoincTreeLoader = LoincTreeLoader(graph=self.runtime.graph, config=self.config)
    tree_loader.load_all_trees()
    # tree_loader.load_component_tree()
    # tree_loader.load_component_by_system_tree()
    # tree_loader.load_system_tree()
    # tree_loader.load_document_tree()
    # tree_loader.load_class_tree()
    # tree_loader.load_panel_tree()
    # tree_loader.load_method_tree()
    # tree_loader.load_nlp_tree()


    self.fix_graph_part_hierarchy()

    # self.find_cycles_primary()
    # self.find_cycles_supplemental()
    self.find_cycles_other()

    print(f"Seen parts: {len(self.seen_nodes)}")

  def find_cycles_primary(self):
    print("============================= from primary  ========================")
    self.seen_nodes = {}
    for node in self.runtime.graph.get_nodes(type_=LoincNodeType.LoincTerm):
      for edge in node.get_all_out_edges():
        if isinstance(edge.handler.type_, LoincTermPrimaryEdges):
          self._find_part_cycle_by_type(part_node=edge.to_node,
                                        edge_types=[LoincTreeEdges.tree_parent, LoincPartEdge.parent_comp_by_system, LoincDanglingNlpEdges.nlp_parent],
                                        path=list(),
                                        seen=self.seen_nodes)

  def find_cycles_supplemental(self):
    print("============================= from supplementary ========================")
    self.seen_nodes = {}
    for node in self.runtime.graph.get_nodes(type_=LoincNodeType.LoincTerm):
      for edge in node.get_all_out_edges():
        if isinstance(edge.handler.type_, LoincTermSupplementaryEdges):
          self._find_part_cycle_by_type(part_node=edge.to_node,
                                        edge_types=[LoincTreeEdges.tree_parent, LoincPartEdge.parent_comp_by_system, LoincDanglingNlpEdges.nlp_parent],
                                        path=list(),
                                        seen=self.seen_nodes)

  def find_cycles_other(self):
    print("============================= from other  ========================")
    self.seen_nodes = {}
    node_counter = 0
    for node in self.runtime.graph.get_nodes(type_=LoincNodeType.LoincPart):
      node_counter += 1
      if (node_counter % 10) == 0:
        print(f"Node counter: {node_counter}")
      # print(f"Other: {node}")
      self._find_part_cycle_by_type(part_node=node,
                                    edge_types=[LoincTreeEdges.tree_parent, LoincPartEdge.parent_comp_by_system, LoincDanglingNlpEdges.nlp_parent], path=list(),
                                    seen=self.seen_nodes)

      self._find_part_cycle_any_type(part_node=node,
                                    edge_types=[LoincTreeEdges.tree_parent, LoincPartEdge.parent_comp_by_system, LoincDanglingNlpEdges.nlp_parent], path=list(),
                                    seen=self.seen_nodes)

  def _find_part_cycle_by_type(self, part_node: Node, edge_types: t.List[EdgeType], path: t.List[Node | Edge],
      seen: t.Dict[str, Node]):
    # if part_node.node_id in seen:
    #   return

    if part_node in path:
      nice_path = ""
      for path_item in path:
        if isinstance(path_item, Node):
          nice_path += f"Node: {path_item.get_property(LoincPartProps.part_number)}-{path_item.get_property(LoincPartProps.part_name or path_item.get_property(LoincTreeProps.code_text))}, sources: {path_item.get_property(ElementProps.sources)}\n"
        if isinstance(path_item, Edge):
          nice_path += f"Edge: {path_item.handler.type_}- sources: {path_item.get_property(ElementProps.sources)}\n"

      nice_path += f"Node: {part_node.get_property(LoincPartProps.part_number)}-{part_node.get_property(LoincPartProps.part_name or part_node.get_property(LoincTreeProps.code_text))}, sources: {part_node.get_property(ElementProps.sources)}\n"
      print(nice_path)
      print("========================")
      return
    path.append(part_node)


    for edge_type in edge_types:  # follow one edge type at a time to find edge specific cycles
      for edge in part_node.get_all_out_edges():
        if edge.handler.type_ == edge_type:
          sub_path = list(path)
          sub_path.append(edge)
          self._find_part_cycle_by_type(edge.to_node, edge_types, sub_path, seen)

    seen[part_node.node_id] = part_node


  def _find_part_cycle_any_type(self, part_node: Node, edge_types: t.List[EdgeType], path: t.List[Node | Edge],
      seen: t.Dict[str, Node]):
    # if part_node.node_id in seen:
    #   return

    if part_node in path:
      nice_path = ""
      for path_item in path:
        if isinstance(path_item, Node):
          nice_path += f"Node: {path_item.get_property(LoincPartProps.part_number)}-{path_item.get_property(LoincPartProps.part_name or path_item.get_property(LoincTreeProps.code_text))}, sources: {path_item.get_property(ElementProps.sources)}\n"
        if isinstance(path_item, Edge):
          nice_path += f"Edge: {path_item.handler.type_}- sources: {path_item.get_property(ElementProps.sources)}\n"

      nice_path += f"Node: {part_node.get_property(LoincPartProps.part_number)}-{part_node.get_property(LoincPartProps.part_name or part_node.get_property(LoincTreeProps.code_text))}, sources: {part_node.get_property(ElementProps.sources)}\n"
      print(nice_path)
      print("========================")
      return
    path.append(part_node)

    for edge in part_node.get_all_out_edges():  # follow by any edge to find any edge cycles
      if edge.handler.type_ in edge_types:
        sub_path = list(path)
        sub_path.append(edge)
        self._find_part_cycle_any_type(edge.to_node, edge_types, sub_path, seen)

    seen[part_node.node_id] = part_node

  def fix_graph_part_hierarchy(self):

    # ToRemove = namedtuple("ToRemove", ["f", "type", "t"])

    def pid(part_number):
      return f"{LoincNodeType.LoincPart.value.id_prefix}:{part_number}"

    # edges_to_remove = [
    #   ToRemove(f=pid(""), type=LoincTreeEdges.tree_parent, t=pid("")),
    #   ToRemove(f=pid(""), type=LoincTreeEdges.tree_parent, t=pid("")),
    #   ToRemove(f=pid(""), type=LoincTreeEdges.tree_parent, t=pid("")),
    # ]

    edges_to_remove = {
      pid("LP30366-6"): {  # LP30366-6-Urinary bladder+Urethra
        pid("LP30366-6"): LoincTreeEdges.tree_parent,
      },

      pid("LP343630-2"): {  # LP343630-2-Lab report general comments
        pid("LP343630-2"): LoincTreeEdges.tree_parent,
      },

    }

    nx_graph: MultiDiGraph = self.runtime.graph.nx_graph

    to_process = list(nx_graph.out_edges(nbunch=edges_to_remove.keys(), data=True, keys=True))

    for out_edge in to_process:
      from_edge = edges_to_remove.get(out_edge[0], None)
      if from_edge:
        to_edge = from_edge.get(out_edge[1], None)
        if to_edge and out_edge[3][ElementKeys.TYPE_KEY] == to_edge:
          nx_graph.remove_edge(u=out_edge[0], v=out_edge[1], key=out_edge[2])
