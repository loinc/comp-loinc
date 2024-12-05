import pickle
import sys
import typing as t
from pathlib import Path
from pickle import Pickler

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.groups.property_use import PropertyUse, PartNode
from loinclib.loinc_schema import LoincNodeType, LoincTermPrimaryEdges, LoincPartProps, LoincPartEdge, \
  LoincTermSupplementaryEdges
from loinclib.loinc_tree_loader import LoincTreeLoader
from loinclib.loinc_tree_schema import LoincTreeEdges, LoincTreeProps


class Index:

  def __init__(self):
    self.use_by_key: t.Dict[str, PropertyUse] = {}
    self.use_by_name_key: t.Dict[str, t.Dict[str, PropertyUse]] = {}
    self.parts: t.Dict[str, PartNode] = {}
    self.parts_roots_no_children: t.Dict[str, PartNode] = {}
    self.parts_roots_with_children: t.Dict[str, PartNode] = {}
    self.parts_roots_no_children_by_type: t.Dict[str, t.Dict[str, PartNode]] = {}
    self.search_parts: t.Dict[str, PartNode] = {}
    self.parts_multiple_prop_names: t.Dict[str, PartNode] = {}
    self.inferred_props = {}


class Grouper:

  def __init__(self):
    self.use_abstract_by_name: t.Dict[str, t.Dict[str, PropertyUse]] = {}
    self.use_after_abstract_by_name: t.Dict[str, t.Dict[str, PropertyUse]] = {}
    self.indent = ' '

  def do_use_abstract_by_name(self, index: Index):
    part: PartNode
    stack = list()
    for part_key, part in index.parts_roots_with_children.items():
      for use_key, use in part.prop_use_by_key.items():
        self._do_use_abstract_by_name(use, 0, stack)

  def _do_use_abstract_by_name(self, use: PropertyUse, depth: int, stack: t.List[PropertyUse]):
    if use in stack:
      print(f'{"".join(self.indent * depth)}: {str(use)}')
      print(f'{"".join(self.indent * depth)}: ++++++++++++ CYCLE  ++++++  ')
      print(str(stack))
      print(f'At index: { stack.index(use)}  with: {use}')
      return

    print(f'{"".join(self.indent * depth)}: {str(use)}')
    if use.count == 0:
      print(f'{"".join(self.indent * depth)}: ===============  ')
      name = use.get_simple_property_name()
      uses = self.use_abstract_by_name.setdefault(name, {})
      uses[use.get_key()] = use
    if len(stack) >0:
      tmp = stack[-1]
      if tmp.count == 0  and use.count > 0:
        name = use.get_simple_property_name()
        uses = self.use_after_abstract_by_name.setdefault(name, {})
        uses[use.get_key()] = use
    stack.append(use)
    for child_use in use.child_prop_use_by_key.values():
      self._do_use_abstract_by_name(child_use, depth + 1, stack)
    del stack[-1]

    # print(f'Finished abstract uses count with dict: ' + str(self.use_abstract_by_name))


class GroupsBuilderSteps:
  def __init__(self, config: ll.Configuration, ):

    self.pickle_path: t.Optional[Path] = None
    self.config = config
    self.runtime: cl.Runtime = t.Optional[cl.Runtime]
    self.index = Index()

    self.primary = False

  def do_groups(self):
    grouper = Grouper()
    grouper.do_use_abstract_by_name(self.index)
    print("debug")
    # print(f'Doing groups' + str(grouper.use_abstract_by_name))

    # self.use_index: PropertyUse = PropertyUse(part_number="_0_", part_name="_0_", prop_type=None)

    # self.use_by_key: t.Dict[str, PropertyUse] = {}
    # self.use_by_name_key: t.Dict[str, t.Dict[str, PropertyUse]] = {}
    #
    # self.parts: t.Dict[str, PartNode] = {}
    # self.parts_roots_no_children: t.Dict[str, PartNode] = {}
    # self.parts_roots_with_children: t.Dict[str, PartNode] = {}
    #
    # self.parts_roots_no_children_by_type: t.Dict[str, t.Dict[str, PartNode]] = {}
    #
    # self.search_parts: t.Dict[str, PartNode] = {}
    #
    # self.parts_multiple_prop_names: t.Dict[str, PartNode] = {}
    #
    # self.inferred_props = {}

  def setup_builder(self, builder):
    builder.cli.command('groups-index-props', help='Indexes the use of LOINC properties by property and part.')(
        self.index_prop_use)

  def index_prop_use(self,
      supplementary: t.Annotated[bool, typer.Option('--sup', help='Use primary vs supplementary.')] = False
  ):

    self.primary = not supplementary

    print(f'===========   {sys.getrecursionlimit()}  ===================')
    sys.setrecursionlimit(5000000)
    print(f'===========   {sys.getrecursionlimit()}  ===================')
    if self.primary:
      self.pickle_path = self.config.home_path / 'tmp/primary.pkl'
    else:
      self.pickle_path = self.config.home_path / 'tmp/suppl.pkl'

    if self.pickle_path.exists():
      with open(self.pickle_path, 'rb') as f:
        self.index = pickle.load(f)
    else:
      self.do_index_prop_use()
      with open(self.pickle_path, 'wb') as f:
        try:
          # pickle.dump(self.index, f)
          # noinspection PyTypeChecker
          Pickler(file=f).dump(self.index)

        except Exception as exc:
          print('Got pickling error: {0}'.format(exc))

        print(f'Finished pickling...')

    self.do_groups()

  def do_index_prop_use(self):
    loinc_loader = ll.loinc_loader.LoincLoader(graph=self.runtime.graph, configuration=self.config)
    if self.primary:
      loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    else:
      loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()
    loinc_loader.load_accessory_files__part_file__part_csv()
    loinc_loader.load_loinc_table__loinc_csv()
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

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
      child_part_node = self.index.parts.setdefault(part_number, PartNode(part_number=part_number))
      child_part_node.part_name = part_name if part_name is not None else f'TREE: {part_tree_text}'
      child_part_node.part_type_name = part_type_name
      child_part_node.part_graph_id = part.node_id

      out_edges = list(part.get_all_out_edges())
      edge: ll.Edge
      for edge in out_edges:
        parent_part_number = edge.to_node.get_property(LoincPartProps.part_number)
        parent_part_node = self.index.parts.setdefault(parent_part_number, PartNode(part_number=parent_part_number))
        match edge.edge_type.type_:
          case LoincTreeEdges.tree_parent:
            child_part_node.parents[parent_part_number] = parent_part_node
            parent_part_node.children[part_number] = child_part_node
          case LoincPartEdge.parent_comp_by_system:
            child_part_node.parents[parent_part_number] = parent_part_node
            parent_part_node.children[part_number] = child_part_node

    # if True:
    #   return

    for part_node in self.index.parts.values():
      if len(part_node.parents) == 0:
        if len(part_node.children) > 0:
          self.index.parts_roots_with_children[part_node.part_number] = part_node
        else:
          self.index.parts_roots_no_children[part_node.part_number] = part_node
          self.index.parts_roots_no_children_by_type.setdefault(part_node.part_type_name, {})[
            part_node.part_number] = part_node

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
          self.index.parts[search_part_number].is_search = True
          self.index.search_parts[search_part_number] = self.index.parts[search_part_number]
          continue

        if not isinstance(edge_type, LoincTermPrimaryEdges) and not isinstance(edge_type, LoincTermSupplementaryEdges):
          continue

        part_number = edge.to_node.get_property(type_=LoincPartProps.part_number)
        part_name = edge.to_node.get_property(type_=LoincPartProps.part_name)
        if part_number is None:
          continue
        property_use = PropertyUse(part_number=part_number,
                                   part_name=part_name,
                                   prop_type=edge_type)
        key = property_use.get_key()
        property_use = self.index.use_by_key.setdefault(key, property_use)
        property_use.count += 1
        keys[key] = property_use
        simple_property_name = property_use.get_simple_property_name()

        part_node = self.index.parts[part_number]
        property_use.part_node = part_node
        part_node.prop_use_by_key[key] = property_use
        part_node.prop_use_by_name_key.setdefault(simple_property_name, {})[key] = property_use

        self.index.use_by_name_key.setdefault(simple_property_name, {})[key] = property_use

      for top_key, top_prop in keys.items():
        for key, prop in keys.items():
          if key == top_key:
            continue
          top_prop.related_props_by_key[key] = prop
          top_prop.related_props_by_name_key.setdefault(prop.get_simple_property_name(), {})[key] = prop
      print('hello')

    for number, part_node in self.index.parts.items():
      if len(part_node.prop_use_by_name_key) > 1:
        self.index.parts_multiple_prop_names[number] = part_node

    for key, use in self.index.use_by_key.items():
      if key in self.index.parts_roots_no_children:
        continue
      self.infer_prop_use(use, self.index.inferred_props)

  def infer_prop_use(self, prop_use: PropertyUse, inferred_props: t.Dict[str, PropertyUse]) -> None:
    key = prop_use.get_key()
    if key in inferred_props:
      return

    inferred_props[key] = prop_use

    for parent_part in prop_use.part_node.parents.values():
      parent_use = PropertyUse(part_number=parent_part.part_number, part_name=parent_part.part_name,
                               prop_type=prop_use.prop_type)
      parent_use_key = parent_use.get_key()
      parent_use = parent_part.prop_use_by_key.setdefault(parent_use_key, parent_use)

      parent_use.part_node = parent_part
      parent_part.prop_use_by_key[parent_use_key] = parent_use

      prop_use.parent_prop_use_by_key[parent_use_key] = parent_use
      parent_use.child_prop_use_by_key[key] = prop_use

      self.infer_prop_use(parent_use, inferred_props)
