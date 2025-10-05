import sys
import typing as t
from operator import truediv

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.datamodel.comp_loinc import LoincTerm, LoincPartId
from comp_loinc.groups2.group import Group, GroupProperty, GroupPart
from comp_loinc.groups2.group import Groups
from loinclib import LoincNodeType, EdgeType, SnomedNodeType, GeneralEdgeType
from loinclib.graph import Node, Edge, NodeType
from loinclib.loinc_schema import LoincPartProps, LoincTermProps, LoincTermPrimaryEdges, LoincTermSupplementaryEdges
from loinclib.loinc_tree_schema import LoincTreeProps
from loinclib.loinc_tree_loader import LoincTreeLoader
from comp_loinc.comploinc_schema import ComploincNodeType
from comp_loinc import root_classes


class Groups2BuilderSteps:
  def __init__(
      self,
      config: ll.Configuration,
  ):
    self._loinc_parsed = None
    self.config = config
    self.runtime: t.Optional[cl.Runtime] = None

    self.group_property_strings: t.List[str] = []
    self._used_group_edges: t.Dict[EdgeType, bool] = {}
    # self.not_property_edges: t.List[EdgeType] = []

    self.parent_strings: t.List[str] = []
    self.parent_edges: t.List[EdgeType] = []
    self.not_parent_edges: t.List[EdgeType] = []

    self.circles: set = set()

    self.__all_part_parent_types: t.Dict[str, NodeType] = {
      "loinc": LoincNodeType.LoincPart,
      "snomed": SnomedNodeType.Concept
    }
    self._part_parent_types: t.Dict[str, NodeType] = {}

    self.__all_part_parent_edge_types: t.Dict[str, type(EdgeType)] = {
      "has_parent": GeneralEdgeType.has_parent
    }

    self._part_parent_edge_types: t.Dict[str, EdgeType] = {
      "has_parent": GeneralEdgeType.has_parent
    }

  def setup_builder_cli(self, builder):
    builder.cli.command(
        "group-properties",
        help="Specify the LOINC properties to use for grouping",
    )(self.group_properties)

    builder.cli.command(
        "part-parent-types",
        help="Specify the part node types to consider as LOINC part parent).",
    )(self.part_parent_types)

    builder.cli.command(
        "part-edge-types",
        help="Specify the edge type to find nodes to consider as LOINC part parents).",
    )(self.part_edge_types)

    builder.cli.command(
        "group-generate",
        help="Generate the output groups.",
    )(self.group_generate)

  def group_properties(self,
      property_strings: t.Annotated[list[str], typer.Option("--property",
                                                            help="One or more property strings. Full property URL, or last segment. Case insensitive")]):
    """
    Select the LOINC grouping properties.
    """
    self.group_property_strings = property_strings

  def part_parent_types(self, parent_types: t.Annotated[list[str], typer.Option("--type",

                                                                                help="One or more parent edge strings. Full edge URL, or last segment. Case insensitive")]):
    for parent_type in parent_types:
      self._part_parent_types[parent_type] = self.__all_part_parent_types.get(parent_type)

  def part_edge_types(self, edge_types: t.Annotated[list[str], typer.Option("--type",

                                                                            help="One or more parent edge strings. Full edge URL, or last segment. Case insensitive")]):
    for edge_type in edge_types:
      self._part_parent_edge_types[edge_type] = self.__all_part_parent_edge_types.get(edge_type)

  def parse_loincs(self):
    if self._loinc_parsed:
      return
    self._loinc_parsed = True
    loinc_loader = ll.loinc_loader.LoincLoader(
        graph=self.runtime.graph, configuration=self.config
    )
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    # loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()
    loinc_loader.load_accessory_files__part_file__part_csv()

    groups = self._get_groups_object()
    loinc_counts = 0
    group_counts = 0
    for loinc_node in self.runtime.graph.get_nodes(LoincNodeType.LoincTerm):

      loinc_number = loinc_node.get_property(LoincTermProps.loinc_number)

      # if loinc_number == "4169-9":
      #   print("4169-9")
      #
      # if loinc_node.node_id == 'loinc:4169-9':
      #   print("dbug")

      loinc_counts += 1
      out_edges = loinc_node.get_out_edges()

      properties: t.Dict[EdgeType, t.Set[GroupPart]] = dict()

      for out_edge in out_edges:
        type_ = out_edge.handler.type_
        if self._use_group_property(type_):
          parts = properties.setdefault(type_, set())
          part = GroupPart(groups=groups, part_node=out_edge.to_node)
          part = groups.parts.setdefault(part.key(), part)
          parts.add(part)

      group = Group(groups_object=groups)
      for edge, parts in properties.items():
        prop = GroupProperty(groups_object=groups, edge_type=edge, parts=parts)
        prop = groups.properties.setdefault(prop.key(), prop)
        group.properties[edge] = prop
      group_key = group.key()

      if group_key is not None:
        group_counts += 1
        group = groups.groups.setdefault(group_key, group)
        group.add_referrer_to_properties()
        group.loincs[loinc_node.get_property(LoincTermProps.loinc_number)] = loinc_node

    print("debug")

  # def group_parts_root_closure(self, parent_types: t.Annotated[list[str], typer.Option("--parent-type",
  #                                                                                      help="One or more parent edge strings. Full edge URL, or last segment. Case insensitive")]):
  #   for parent_type in parent_types:
  #     self._part_parent_types[parent_type] = self.__all_part_parent_types.get(parent_type)
  #
  #   loinc_loader = ll.loinc_loader.LoincLoader(graph=self.runtime.graph, configuration=self.config)
  #   # loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()
  #
  #   tree_loader: LoincTreeLoader = LoincTreeLoader(graph=self.runtime.graph, config=self.config)
  #   tree_loader.load_all_trees()
  #   # tree_loader.load_component_tree()
  #   # # tree_loader.load_component_by_system_tree()
  #   # tree_loader.load_system_tree()
  #   # tree_loader.load_document_tree()
  #   # tree_loader.load_class_tree()
  #   # tree_loader.load_panel_tree()
  #   # tree_loader.load_method_tree()
  #
  #   groups = self._get_groups_object()
  #   seen_group_parts = set()
  #   for group_part in set(groups.parts.values()):
  #     if group_part.key() in seen_group_parts:
  #       continue
  #     seen_group_parts.add(group_part)
  #     seen_group_parts.update(group_part.get_ancestors(parent_node_types=self._part_parent_types,
  #                                                      edge_types=[GeneralEdgeType.has_parent]))
  #
  #   print("debug")

  def _do_closures(self):
    loinc_loader = ll.loinc_loader.LoincLoader(graph=self.runtime.graph, configuration=self.config)
    loinc_loader.load_accessory_files__part_file__part_csv()
    # loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

    tree_loader: LoincTreeLoader = LoincTreeLoader(graph=self.runtime.graph, config=self.config)
    tree_loader.load_all_trees()
    # tree_loader.load_component_tree()
    # # tree_loader.load_component_by_system_tree()
    # tree_loader.load_system_tree()
    # tree_loader.load_document_tree()
    # tree_loader.load_class_tree()
    # tree_loader.load_panel_tree()
    # tree_loader.load_method_tree()

    groups_object = self._get_groups_object()
    groups_object.do_closure(part_parent_edge_types=list(self._part_parent_edge_types.values()),
                             part_parent_node_types=list(self._part_parent_types.values()))

    print("debug")

  def group_generate(self,
      parent_group: t.Annotated[bool, typer.Option("--parent-group",
                                                   help="Create the direct parent groups of a LOINC term")] = False):


    self.parse_loincs()
    self._do_closures()

    groups_object = self._get_groups_object()
    edge_types = list(self._part_parent_edge_types.values())
    node_types = list(self._part_parent_types.values())

    generated_groups: t.Dict[str, Group] = {}
    if parent_group:
      for  group in groups_object.groups.values():
        if group.generated:
          continue
        self._do_group_rounds(group=group,edge_types= edge_types,node_types= node_types, generated_groups=generated_groups, rounds=3)


    print(f"debug generated group counts: {len(generated_groups)}")

  def _do_group_rounds(self, group: Group,  generated_groups:  t.Dict[str, Group], rounds: int, edge_types, node_types):
    if rounds > 0:
      parent = group.get_parent(part_parent_edge_types=edge_types, part_parent_node_types=node_types)
      if parent is None:
        return
      self._do_group_rounds(group=parent, generated_groups=generated_groups, rounds=rounds - 1, edge_types=edge_types, node_types=node_types)
    else:
      generated_groups[group.key()] = group


  def _get_groups_object(self) -> Groups:
    current_module = self.runtime.current_module
    return self.runtime.current_module.runtime_objects.setdefault('groups',
                                                                  Groups(module=current_module))

  def _use_group_property(self, edge: EdgeType):
    use = self._used_group_edges.get(edge, None)
    if use is not None:
      return use

    for property_string in self.group_property_strings:
      property_string = property_string.lower()
      prop_name = edge.name.lower()
      if prop_name == property_string or prop_name.endswith(property_string):
        self._used_group_edges[edge] = True
        return True

    self._used_group_edges[edge] = False
    return False
