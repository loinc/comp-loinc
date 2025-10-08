import dataclasses
import sys
import typing as t
import urllib.parse
import uuid
from operator import truediv

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.datamodel import LoincTermId, Entity
from comp_loinc.datamodel.comp_loinc import LoincTerm, LoincPartId
from comp_loinc.groups2.group import Group, GroupProperty, GroupPart
from comp_loinc.groups2.group import Groups
from loinclib import LoincNodeType, EdgeType, SnomedNodeType, GeneralEdgeType, SnomedLoader, SnomedEdges, LoincLoader
from loinclib.graph import Node, Edge, NodeType
from loinclib.graph_commands import GraphCommands
from loinclib.loinc_schema import LoincPartProps, LoincTermProps, LoincTermPrimaryEdges, LoincTermSupplementaryEdges, \
  LoincTermPrimaryEdgesArgs
from loinclib.loinc_snomed_loader import LoincSnomedLoader
from loinclib.loinc_tree_schema import LoincTreeProps
from loinclib.loinc_tree_loader import LoincTreeLoader
from comp_loinc.comploinc_schema import ComploincNodeType
from comp_loinc import root_classes


class Groups2BuilderSteps:
  def __init__(
      self,
      config: ll.Configuration,
  ):
    self.base_groups: t.Dict[str, Group] = None
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

    self.generated_groups: t.Dict[str, Group] = {}

    self.__all_part_node_types: t.Dict[str, NodeType] = {
      "loinc": LoincNodeType.LoincPart,
      "snomed": SnomedNodeType.Concept
    }
    self._part_node_types: t.Dict[str, NodeType] = {}

    self.__all_part_parent_edge_types: t.Dict[str, type(EdgeType)] = {
      "has-parent": GeneralEdgeType.has_parent,
      "mapped-to": GeneralEdgeType.mapped_to
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
        "part-parent-edges",
        help="Specify the edge types to find nodes to consider as LOINC part parents).",
    )(self.part_parent_edges)

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
      self._part_node_types[parent_type] = self.__all_part_node_types.get(parent_type)

    if "snomed" in parent_types:
      snomed_loader = SnomedLoader(graph=self.runtime.graph, config=self.config)
      snomed_loader.load_selected_relations(SnomedEdges.is_a)
      snomed_loader.load_fully_specified_names()

      loinc_snomed_loader = LoincSnomedLoader(config=self.config, graph=self.runtime.graph)
      loinc_snomed_loader.load_part_mapping()

      loinc_loader = LoincLoader(graph=self.runtime.graph, configuration=self.config)
      loinc_loader.load_accessory_files__part_file__part_csv()




  def part_parent_edges(self, edge_types: t.Annotated[list[str], typer.Option("--edge",

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

      # if loinc_number == "77108-9":
      #   print("debug")

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
        if self._use_group_edge(type_):
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
        group.from_loinc = True
        group.sources.add(loinc_number)
      else:
        raise ValueError("group key is null")

    # print("debug")

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

    graph_commands = GraphCommands(config=self.config)
    graph_commands.runtime = self.runtime
    graph_commands.configuration = self.config
    graph_commands.fix_graph_part_hierarchy()

    groups_object = self._get_groups_object()
    groups_object.do_closure(part_parent_edge_types=list(self._part_parent_edge_types.values()),
                             part_parent_node_types=list(self._part_node_types.values()))

    # print("debug")

  def group_generate(self,
      parent_group: t.Annotated[bool, typer.Option("--parent-group",
                                                   help="Create the direct parent groups of a LOINC term")] = False,
      parent_rounds: t.Annotated[int, typer.Option("--parent-rounds",
                                                   help="How many parent lookups (i.e. parent, grandparent, etc.). Defaults to 1.")] = 1,
      base_rounds: t.Annotated[int, typer.Option("--base-rounds",
                                                 help="How many base/root lookups (tree root levels). Defaults to 3.")] = 3,
      base_min_size: t.Annotated[int, typer.Option("--base-minimum-size",
                                                   help="The minimum size of sub groups for a base group to be created. Defaults to 25")] = 25

  ):

    self.parse_loincs()
    self._do_closures()

    groups_object = self._get_groups_object()
    edge_types = list(self._part_parent_edge_types.values())
    node_types = list(self._part_node_types.values())

    if parent_group:
      self.generate_parent_groups(groups_object=groups_object, rounds=parent_rounds, edge_types=edge_types,
                                  node_types=node_types)

    self.generate_base_groups(min_tree_size=base_min_size, tree_depth=base_rounds)

    self.populate_module()
    # print(f"populated entities: {len(self.runtime.current_module.entities_by_type[LoincTerm])}")

    # print(f"debug generated group counts: {len(self.generated_groups)}")

  def generate_parent_groups(self, *, groups_object: Groups, rounds: int, edge_types, node_types):
    for group in groups_object.groups.values():
      if not group.from_loinc:
        continue
      parent: Group | None = None
      this_round = rounds
      while this_round > 0:
        parent = group.get_parent(part_parent_edge_types=edge_types, part_parent_node_types=node_types)
        if parent is None:
          break
        this_round -= 1
        group = parent
      if parent is not None:
        self.generated_groups[parent.key()] = parent

  def generate_base_groups(self, min_tree_size, tree_depth):
    groups_object = self._get_groups_object()

    self.base_groups = {k: g for k, g in groups_object.group_trees.items() if g.get_descendants_count() > min_tree_size}
    # print(f"Initial size of base trees: {self.base_groups}")
    round_groups = dict(self.base_groups)
    next_groups = {}

    while tree_depth > 0:
      for key, group in round_groups.items():
        if group.get_descendants_count() > min_tree_size:
          next_groups.update(group.children)
      self.base_groups.update(next_groups)
      round_groups = next_groups
      tree_depth -= 1
      # print(f"\tSize of base trees: {self.base_groups}")

  def populate_module(self):
    sorted_edges = self._get_used_edges_sorted()
    grouping_parent_entity = root_classes.groups_named(
        grouping_name=" ".join([e.value.label_fragment for e in sorted_edges]), module=self.runtime.current_module)
    self._do_populate_module(groups_dict=self.generated_groups, parent_entity=grouping_parent_entity)

    base_parent_entity = root_classes.groups_named(
        grouping_name=" ".join([e.value.label_fragment for e in sorted_edges]) + " Base Groups",
        module=self.runtime.current_module)
    self._do_populate_module(groups_dict=self.base_groups, parent_entity=base_parent_entity)

  def _do_populate_module(self, groups_dict: t.Dict[str, Group], parent_entity: Entity):
    for key, group in groups_dict.items():
      entities: t.List[LoincTerm] = []
      group_edges = list(group.properties.keys())
      group_edges.sort(key=lambda x: x.value.label_fragment)

      for edge in group_edges:
        parts = list(group.properties[edge].parts)
        parts.sort(key=lambda x: x.get_part_number())
        if len(entities) == 0:
          for part in parts:
            entity = LoincTerm(id=LoincTermId(""))
            setattr(entity, edge.name, LoincPartId(part.key()))
            entity.entity_label = "LG  " + edge.value.label_fragment + " " + part.label()
            for source in group.sources:
              if source not in entity.sources:
                entity.sources.append(source)

            entities.append(entity)
        else:
          next_entities: t.List[LoincTerm] = []
          for part in parts:
            current_entity: Entity
            for current_entity in entities:
              properties = dataclasses.asdict(current_entity)
              next_entity: LoincTerm = LoincTerm(**properties)
              setattr(next_entity, edge.name, LoincPartId(part.key()))
              next_entity.entity_label += "  ||  " + edge.value.label_fragment + part.label()
              for source in group.sources:
                if source not in next_entity.sources:
                  next_entity.sources.append(source)
              next_entities.append(next_entity)

          entities = next_entities
      for entity in entities:
        entity.id = LoincTermId(
            ComploincNodeType.group_node.value.id_prefix + ":" + urllib.parse.quote(entity.entity_label))
        entity.sub_class_of.append(parent_entity.id)

        module_entity = self.runtime.current_module.get_entity(entity_id=entity.id, entity_class=LoincTerm)
        if module_entity:
          for source in entity.sources:
            if source not in module_entity.sources:
              module_entity.sources.append(source)
        else:
          self.runtime.current_module.add_entity(entity)

  def _get_groups_object(self) -> Groups:
    current_module = self.runtime.current_module
    return self.runtime.current_module.runtime_objects.setdefault('groups',
                                                                  Groups(module=current_module))

  def _use_group_edge(self, edge: EdgeType):
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

  def _get_grouping_name(self):
    edges = list(self._used_group_edges.keys())
    edges.sort(key=lambda x: x.value.label_fragment)
    return " ".join([e.value.label_fragment for e in self._get_used_edges_sorted()])

  def _get_used_edges_sorted(self):
    edges = [e for e, truth in self._used_group_edges.items() if truth is True]
    edges.sort(key=lambda x: x.value.label_fragment)
    return edges
