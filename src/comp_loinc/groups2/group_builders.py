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
    self.config = config
    self.runtime: t.Optional[cl.Runtime] = None

    self.property_strings: t.List[str] = []
    self._used_edges: t.Dict[EdgeType, bool] = {}
    # self.not_property_edges: t.List[EdgeType] = []

    self.parent_strings: t.List[str] = []
    self.parent_edges: t.List[EdgeType] = []
    self.not_parent_edges: t.List[EdgeType] = []

    self.circles: set = set()
    self.group_part_all_parent_types: t.Dict[str, NodeType] = {
      "loinc": LoincNodeType.LoincPart,
      "snomed": SnomedNodeType.concept
    }
    self.group_part_parent_types: t.List[NodeType] = []


    self.group_all_model_types: t.Dict[str, type(EdgeType)] = {
      "primary": LoincTermPrimaryEdges,
      "detailed": LoincTermSupplementaryEdges

    }
  def setup_builder_cli(self, builder):
    builder.cli.command(
        "group-properties",
        help="Specify the LOINC properties to use for grouping",
    )(self.group_properties)
    #
    # builder.cli.command(
    #     "parent-types",
    #     help="Specify the parent type names to use for finding parent parts",
    # )(self.group_parent_type)

    builder.cli.command(
        "group-parse-loincs",
        help="Parse LOINC definitions into base groups.",
    )(self.group_parse_loincs)

    # builder.cli.command(
    #     "group-roots",
    #     help="Build the root groups.",
    # )(self.group_roots)

    builder.cli.command(
        "part-ancestors",
        help="Build the part ancestor closures (to support later group building).",
    )(self.group_parts_root_closure)

    builder.cli.command(
        "group-generate",
        help="Generate the output groups.",
    )(self.group_generate)

    # builder.cli.command(
    #     "group2-save",
    #     help="Group 2 hello",
    # )(self.hello)

  # def hello(self):
  #   module = self.runtime.current_module
  #   grouper: Groups = module.runtime_objects.setdefault('grouper2', Groups( module=module))
  #   grouper.init()
  #   print("==================  GROUP 2 HELLO  =================")

  def group_properties(self,
      property_strings: t.Annotated[list[str], typer.Option("--properties",
                                                            help="One or more property strings. Full property URL, or last segment. Case insensitive")]):
    """
    Select the LOINC grouping properties.
    """
    self.property_strings = property_strings

  def group_parent_type(self, parent_types: t.Annotated[list[str], typer.Option("--type",

                                                                                help="One or more parent edge strings. Full edge URL, or last segment. Case insensitive")]):
    for parent_type in parent_types:
      self.group_part_parent_types.append(self.group_part_all_parent_types.get(parent_type))

  def group_model_type(self, parent_types: t.Annotated[list[str], typer.Option("--type",

                                                                                help="One or more parent edge strings. Full edge URL, or last segment. Case insensitive")]):
    for parent_type in parent_types:
      self.group_part_parent_types.append(self.group_part_all_parent_types.get(parent_type))

  def group_parse_loincs(self):
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
      loinc_counts += 1
      out_edges = loinc_node.get_out_edges()

      properties: t.Dict[EdgeType, t.Set[GroupPart]] = dict()
      # group: Group = Group()
      # indexing the parts by group properties, per loinc

      for out_edge in out_edges:
        type_ = out_edge.handler.type_
        if self._use_edge(type_):
          parts = properties.setdefault(type_, set())
          part = GroupPart(groups=groups, part_node=out_edge.to_node)
          part = groups.parts.setdefault(part.key(), part)
          parts.add(part)

      group = Group(groups=groups)
      for edge, parts in properties.items():
        prop = GroupProperty(groups=groups, edge_type=edge, group_parts=parts)
        prop = groups.properties.setdefault(prop.key(), prop)
        group.properties[edge] = prop
      group_key = group.key()

      if group_key is not None:
        group_counts += 1
        group = groups.groups.setdefault(group_key, group)
        group.loincs[loinc_node.get_property(LoincTermProps.loinc_number)] = loinc_node

    print("debug")

    loinc_counts = 0
    for group in groups.groups.values():
      count = group.get_descendants_loincs_count()
      loinc_counts += count

    print("\n\n======= loinc counts from all groups =========")
    print(loinc_counts)



  def group_parts_root_closure(self, parent_types: t.Annotated[list[str], typer.Option("--parent-type",
                                                                                       help="One or more parent edge strings. Full edge URL, or last segment. Case insensitive")]):
    for parent_type in parent_types:
      self.group_part_parent_types.append(self.group_part_all_parent_types.get(parent_type))

    loinc_loader = ll.loinc_loader.LoincLoader(graph=self.runtime.graph, configuration=self.config)
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

    groups = self._get_groups_object()
    seen_group_parts = set()
    for group_part in set(groups.parts.values()):
      if group_part.key() in seen_group_parts:
        continue
      seen_group_parts.add(group_part)
      seen_group_parts.update(group_part.get_ancestors(parent_node_types=self.group_part_parent_types,
                                                       edge_types=[GeneralEdgeType.has_parent]))

    print("debug")

  def group_generate(self,
      parent_group: t.Annotated[bool, typer.Option("--parent-group",
                                                   help="Create the direct parent groups of a LOINC term")] = False):

    if parent_group:
      self._do_parent_groups()

  def _do_parent_groups(self):
    groups = self._get_groups_object()
    all_groups = {}
    duplicate_count = 0
    group_count = 0
    for group in set(groups.groups.values()):
      if group.is_abstract() or group.generated:
        continue

      group_builder_config: t.Dict[EdgeType, t.Set[GroupPart]] = dict()
      for edge_type, prop in group.properties.items():
        parts = set()
        for p in prop.parts:
          # parts.update(p.group_part.get_parents(parent_node_types=self.group_part_parent_types, edge_types=[GeneralEdgeType.has_parent]))
          parts.update(self._get_part_parents(part=p, rounds=1, parent_node_types=self.group_part_parent_types,
                                              edge_types=[GeneralEdgeType.has_parent]))
        if len(parts) > 0:
          group_builder_config[edge_type] = parts
      if len(group_builder_config) > 0:
        new_groups = self._groups_builder(group_builder_config, set())
        for group in new_groups:
          if group.key() in all_groups:
            duplicate_count += 1
          else:
            group_count += 1
            all_groups[group.key()] = group

    print(f"duplicate groups: {duplicate_count}")
    print(f"groups: {group_count}")
    print("debug")

  def _get_part_parents(self, *, part: GroupPart, rounds: int, parent_node_types: t.List[NodeType],
      edge_types: t.List[EdgeType]) -> t.Set[GroupPart]:
    final_parts = set()
    final_parts.add(part)
    while rounds > 0:
      round_parts = set()
      for p in final_parts:
        part_parents = set(p.get_parents(parent_node_types=parent_node_types, edge_types=edge_types))
        if len(part_parents) == 0:
          pass
          # round_parts.add(part)
        else:
          round_parts.update(part_parents)
      final_parts = round_parts
      rounds -= 1
    return final_parts

  def _groups_builder(self, property_type_parts: t.Dict[EdgeType, t.Set[GroupPart]], generated_groups: t.Set[Group]) -> \
      t.Set[Group]:
    edge_type = None
    try:
      edge_type = next(iter(property_type_parts))
    except StopIteration:
      return generated_groups
    parts = property_type_parts[edge_type]
    del property_type_parts[edge_type]
    groups = self._get_groups_object()
    part: GroupPart
    built_groups: t.Set[Group] = set()

    if len(generated_groups) == 0:
      group = Group(groups=groups)
      group.generated = True
      prop = GroupProperty(group_parts=parts, edge_type=edge_type, groups=groups)
      prop = groups.properties.setdefault(prop.key(), prop)

      group.properties.setdefault(edge_type, prop)
      group = groups.groups.setdefault(group.key(), group)

      built_groups.add(group)
    else:
      for group in generated_groups:
        prop = GroupProperty(group_parts=parts, edge_type=edge_type, groups=groups)
        prop = groups.properties.setdefault(prop.key(), prop)
        props = group.copy_properties()
        props.setdefault(edge_type, prop)

        g = Group(groups=groups)
        g.generated = True
        g.properties = props
        g = groups.groups.setdefault(g.key(), g)
        built_groups.add(g)
    return self._groups_builder(property_type_parts=property_type_parts, generated_groups=built_groups)


  def _get_groups_object(self) -> Groups:
    current_module = self.runtime.current_module
    return self.runtime.current_module.runtime_objects.setdefault('groups',
                                                                  Groups(module=current_module))

  def _use_edge(self, edge: EdgeType):
    use = self._used_edges.get(edge, None)
    if use:
      return use

    for property_string in self.property_strings:
      property_string = property_string.lower()
      prop_name = edge.value.name.lower()
      if prop_name == property_string or prop_name.endswith(property_string):
        self._used_edges[edge] = True
      else:
        self._used_edges[edge] = False
    return self._used_edges[edge]
