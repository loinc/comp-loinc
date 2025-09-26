import typing as t

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.groups2.group import Group
from comp_loinc.groups2.groups import Groups
from loinclib import LoincNodeType, EdgeType
from loinclib.graph import Node, Edge
from loinclib.loinc_schema import LoincPartProps, LoincTermProps
from loinclib.loinc_tree_loader import LoincTreeLoader



# from enum import StrEnum


class Groups2BuilderSteps:
  def __init__(
      self,
      config: ll.Configuration,
  ):
    self.config = config
    self.runtime: t.Optional[cl.Runtime] = None

    self.property_strings: t.List[str] = []
    self.property_edges: t.List[EdgeType] = []
    self.not_property_edges: t.List[EdgeType] = []

    self.parent_strings: t.List[str] = []
    self.parent_edges: t.List[EdgeType] = []
    self.not_parent_edges: t.List[EdgeType] = []

  def setup_builder_cli(self, builder):
    builder.cli.command(
        "group-properties",
        help="Specify the LOINC properties to use for grouping",
    )(self.group_properties)

    builder.cli.command(
        "group-parents",
        help="Specify the edge names to use for finding parent parts",
    )(self.group_parents)

    builder.cli.command(
        "group-parse-loincs",
        help="Parse LOINC definitions into base groups.",
    )(self.group_parse_loincs)

    builder.cli.command(
        "group-roots",
        help="Build the root groups.",
    )(self.group_roots)

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

  def group_parents(self, parent_strings: t.Annotated[list[str], typer.Option("--parents",
                                                                              help="One or more parent edge strings. Full edge URL, or last segment. Case insensitive")]):
    self.parent_strings = parent_strings

  def group_parse_loincs(self):
    loinc_loader = ll.loinc_loader.LoincLoader(
        graph=self.runtime.graph, configuration=self.config
    )
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()
    loinc_loader.load_accessory_files__part_file__part_csv()

    groups = self._get_groups_object()
    loinc_counts = 0
    group_counts = 0
    for loinc_node in self.runtime.graph.get_nodes(LoincNodeType.LoincTerm):
      loinc_counts +=1
      out_edges = loinc_node.get_all_out_edges()

      properties = dict()

      # indexing the parts by group properties, per loinc
      for out_edge in out_edges:
        type_ = out_edge.handler.type_
        if self._use_property(type_):
          properties[type_] = out_edge.to_node


      group_key = Group.group_key(properties)

      if group_key is not None:
        group_counts +=1
        group = groups.groups.setdefault(group_key, Group())
        group.properties = properties
        group.loincs[loinc_node.get_property(LoincTermProps.loinc_number)] = loinc_node
        group.key = group_key
      else:
        print("debug")

    print("debug")

  def group_roots(self):
    loinc_loader = ll.loinc_loader.LoincLoader(
        graph=self.runtime.graph, configuration=self.config
    )
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

    tree_loader: LoincTreeLoader = LoincTreeLoader(graph=self.runtime.graph, config=self.config)
    tree_loader.load_component_tree()
    tree_loader.load_component_by_system_tree()
    tree_loader.load_system_tree()
    tree_loader.load_document_tree()
    tree_loader.load_class_tree()
    tree_loader.load_panel_tree()
    tree_loader.load_method_tree()

    groups_object = self._get_groups_object()

    seen_by_property: t.Dict[EdgeType, t.Set[str]] = dict()


    for key, group in groups_object.groups.copy().items():
      # if group.is_abstract():
      #   continue
      for prop, part_node in group.properties.items():
        seen = seen_by_property.setdefault(prop, set())
        self._do_roots(prop, part_node, group, seen)

    for group in groups_object.groups.values():
      if len(group.parent_groups) == 0:
        for child_group in group.child_groups.values():
          if not child_group.is_complex():
            groups_object.roots[group.key] = group

    print("debug")


  def group_generate(self):
    groups: Groups = self.runtime.current_module.runtime_objects.get("groups")
    for group in groups.roots.values():
      print(f"{group} has descendants count:\n{group.get_descendants_loincs_count()}")

  def _do_roots(self,
      prop: EdgeType,
      part_node: Node,
      child_group: Group,
      seen: t.Set[str],
  ):
    part_number = part_node.get_property(LoincPartProps.part_number)

    if part_number in seen:
      return
    seen.add(part_number)

    group_key = Group.group_key({prop: part_node})
    groups_object = self._get_groups_object()
    parent_group = groups_object.groups.get(group_key, None)
    if parent_group is None:
      parent_group = Group()
      parent_group.properties[prop] = part_node
      parent_group.key = group_key
      groups_object.groups[group_key] = parent_group

    parent_group.child_groups[child_group.key] = child_group
    child_group.parent_groups[parent_group.key] = parent_group

    out_edge: Edge
    for out_edge in part_node.get_all_out_edges():
      type_ = out_edge.handler.type_
      if self._use_parent(type_):
        parent_node = out_edge.to_node
        self._do_roots(prop, parent_node, parent_group, seen)

  def _get_groups_object(self) -> Groups:
    current_module = self.runtime.current_module
    return self.runtime.current_module.runtime_objects.setdefault('groups',
                                                                  Groups(module=current_module))

  def _use_property(self, prop: EdgeType):
    if prop in self.property_edges:
      return True
    if prop in self.not_property_edges:
      return False

    for property_string in self.property_strings:
      property_string = property_string.lower()
      prop_name = prop.value.name.lower()
      if prop_name == property_string or prop_name.endswith(property_string):
        self.property_edges.append(prop)
        self.property_edges.sort(key=lambda prop: prop.value.order)
        return True

    self.not_property_edges.append(prop)
    return False

  def _use_parent(self, prop: EdgeType):
    if prop in self.parent_edges:
      return True
    if prop in self.not_parent_edges:
      return False

    for parent_string in self.parent_strings:
      parent_string = parent_string.lower()
      prop_name = prop.value.name.lower()
      if prop_name == parent_string or prop_name.endswith(parent_string):
        self.parent_edges.append(prop)
        return True

    self.not_parent_edges.append(prop)
    return False
