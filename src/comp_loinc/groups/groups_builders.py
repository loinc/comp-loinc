import typing as t

import comp_loinc as cl
import loinclib as ll
from comp_loinc.groups.property_use import PropertyUse, PartNode
from loinclib.loinc_schema import LoincNodeType, LoincTermPrimaryEdges, LoincPartProps, LoincTermProps, LoincPartEdge, \
  LoincTermSupplementaryEdges
from loinclib.loinc_tree_loader import LoincTreeLoader
from loinclib.loinc_tree_schema import LoincTreeEdges, LoincTreeProps


class GroupsBuilderSteps:
  def __init__(self, config: ll.Configuration, ):
    self.config = config
    self.runtime: cl.Runtime = t.Optional[cl.Runtime]

    self.use_index: PropertyUse = PropertyUse(part_number="_0_", part_name="_0_", prop_type=None)

    self.parts: t.Dict[str, PartNode] = {}
    self.parts_roots_no_children: t.Dict[str, PartNode] = {}
    self.parts_roots_with_children: t.Dict[str, PartNode] = {}

    self.parts_roots_no_children_by_type: t.Dict[str, t.Dict[str, PartNode]] = {}

    self.search_parts: t.Dict[str, PartNode] = {}

    self.parts_multiple_prop_names: t.Dict[str, PartNode] = {}

    self.inferred_props = {}

  def setup_builder(self, builder):
    builder.cli.command('groups-index-props', help='Indexes the use of LOINC properties by property and part.')(
        self.index_prop_use)

  def index_prop_use(self):
    loinc_loader = ll.loinc_loader.LoincLoader(graph=self.runtime.graph, configuration=self.config)
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    loinc_loader.load_accessory_files__part_file__part_csv()
    loinc_loader.load_loinc_table__loinc_csv()
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    loinc_tree_loader = LoincTreeLoader(config=self.config, graph=self.runtime.graph)
    loinc_tree_loader.load_class_tree()
    loinc_tree_loader.load_component_tree()
    loinc_tree_loader.load_component_by_system_tree()
    loinc_tree_loader.load_panel_tree()
    loinc_tree_loader.load_system_tree()
    loinc_tree_loader.load_method_tree()
    loinc_tree_loader.load_document_tree()


 # build parts tree
    parts: t.Iterator[ll.Node] = self.runtime.graph.get_nodes(LoincNodeType.LoincPart)
    for part in parts:
      part_number = part.get_property(LoincPartProps.part_number)
      part_name = part.get_property(LoincPartProps.part_name)
      part_type_name = part.get_property(LoincPartProps.part_type_name)
      part_tree_text = part.get_property(LoincTreeProps.code_text)

      part.get_property(LoincPartProps.part_name)
      child_part_node = self.parts.setdefault(part_number, PartNode(part_number=part_number))
      child_part_node.part_name = part_name if part_name is not None else f'TREE: {part_tree_text}'
      child_part_node.part_type_name = part_type_name
      child_part_node.part_graph_id = part.node_id

      out_edges = list(part.get_all_out_edges())
      edge: ll.Edge
      for edge in out_edges:
        parent_part_number = edge.to_node.get_property(LoincPartProps.part_number)
        parent_part_node = self.parts.setdefault(parent_part_number, PartNode(part_number=parent_part_number))
        match edge.edge_type.type_:
          case LoincTreeEdges.tree_parent:
            child_part_node.parents[parent_part_number] = parent_part_node
            parent_part_node.children[part_number] = child_part_node
          case LoincPartEdge.parent_comp_by_system:
            child_part_node.parents[parent_part_number] = parent_part_node
            parent_part_node.children[part_number] = child_part_node

    for part_node in self.parts.values():
      if len(part_node.parents) == 0:
        if len(part_node.children) > 0:
          self.parts_roots_with_children[part_node.part_number] = part_node
        else:
          self.parts_roots_no_children[part_node.part_number] = part_node
          self.parts_roots_no_children_by_type.setdefault(part_node.part_type_name, {})[part_node.part_number] = part_node

    # parse loinc term phrases
    nodes = self.runtime.graph.get_nodes(LoincNodeType.LoincTerm)
    for term_node in nodes:
      # status = term_node.get_property(LoincTermProps.status)
      # if status != "ACTIVE":
      #   continue

      edges = term_node.get_all_out_edges()

      keys: dict[str, PropertyUse] = {}

      for edge in edges:
        edge_type = edge.edge_type.type_

        if edge_type is LoincTermSupplementaryEdges.supplementary_search:
          search_part_number = edge.to_node.get_property(LoincPartProps.part_number)
          self.parts[search_part_number].is_search = True
          self.search_parts[search_part_number] = self.parts[search_part_number]
          continue

        if not isinstance(edge_type, LoincTermPrimaryEdges):
          continue

        part_number = edge.to_node.get_property(type_=LoincPartProps.part_number)
        part_name = edge.to_node.get_property(type_=LoincPartProps.part_name)
        if part_number is None:
          continue
        property_use = PropertyUse(part_number=part_number,
                    part_name=part_name,
                    prop_type=edge_type)
        key = property_use.get_key()
        property_use = self.use_index.related_props_by_key.setdefault(key, property_use)
        property_use.count += 1
        keys[key] = property_use
        simple_property_name = property_use.get_simple_property_name()

        part_node = self.parts[part_number]
        property_use.part_node = part_node
        part_node.prop_use_by_key[key] = property_use
        part_node.prop_use_by_name_key.setdefault(simple_property_name, {})[key] = property_use

        self.use_index.related_props_by_name_key.setdefault(simple_property_name, {})[key] = property_use

      for top_key, top_prop in keys.items():
        for key, prop in keys.items():
          if key == top_key:
            continue
          top_prop.related_props_by_key[key] = prop
          top_prop.related_props_by_name_key.setdefault(prop.get_simple_property_name(), {})[key] = prop
      print('hello')

    for number, part_node in self.parts.items():
      if len(part_node.prop_use_by_name_key) > 1:
        self.parts_multiple_prop_names[number] = part_node

    for key, use in self.use_index.related_props_by_key.items():
      if key in self.parts_roots_no_children:
        continue
      self.infer_prop_use(use, self.inferred_props)


    print('hello')

  def infer_prop_use(self, prop_use: PropertyUse, inferred_props: t.Dict[str, PropertyUse]) -> None:
    key = prop_use.get_key()
    if key in inferred_props:
      return

    inferred_props[key] = prop_use

    for parent_part in prop_use.part_node.parents.values():
      parent_use = PropertyUse(part_number=parent_part.part_number, part_name=parent_part.part_name,
                        prop_type=prop_use.prop_type )
      parent_use_key = parent_use.get_key()
      parent_use = parent_part.prop_use_by_key.setdefault(parent_use_key, parent_use)

      parent_use.part_node = parent_part
      parent_part.prop_use_by_key[parent_use_key] = parent_use

      prop_use.parent_prop_use_by_key[parent_use_key] = parent_use
      parent_use.child_prop_use_by_key[key] = prop_use

      self.infer_prop_use(parent_use, inferred_props)


