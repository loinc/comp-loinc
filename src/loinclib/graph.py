from __future__ import annotations

import pickle
import re
import typing as t
from enum import StrEnum
from pathlib import Path

import networkx as nx


#
# SCHEMA_KEY = '__SCHEMA__'
#
# TAGS_KEY = '__TAGS__'


class SchemaEnum(StrEnum):
  TYPE_KEY = 'type'


class Schema:
  def __init__(self, graph: LoinclibGraph, strict: bool = False):
    self.graph: LoinclibGraph = graph
    self.nx_graph = graph.nx_graph
    self.strict = strict
    self.node_types: t.Dict[StrEnum, NodeType] = {}

    self.node_type_class_map: t.Dict[StrEnum, t.Type[NodeType]] = {}
    self.default_node_type: t.Type[NodeType] = NodeType

    self.edge_type_class_map: t.Dict[StrEnum, t.Type[EdgeType]] = {}
    self.default_edge_type: t.Type[EdgeType] = EdgeType

    self.property_type_class_map: t.Dict[StrEnum, t.Type[PropertyType]] = {}
    self.default_property_type: t.Type[PropertyType] = PropertyType

  def add_node_type(self, *, node_type: NodeType) -> Schema:
    if node_type.type_ in self.node_types:
      raise ValueError(f"Duplicate type: {node_type}")
    self.node_types[node_type.type_] = node_type
    return self

  def get_node_type(self, type_: StrEnum) -> NodeType:
    node_type = self.node_types.get(type_, None)
    if node_type:
      return node_type
    if self.strict:
      raise ValueError(f"Unknown node type: {type_}")
    node_type = self.create_node_type(type_=type_, dynamic=True, strict=self.strict)
    self.node_types[type_] = node_type
    return node_type

  def create_node_type(self, *, type_: StrEnum, name: t.Optional[str] = None, description: t.Optional[str] = None,
      base_url: t.Optional[str] = None, code_prefix: t.Optional[str] = None, curie_prefix: t.Optional[str] = None,
      url_regex: t.Optional[str] = None, url_regex_ignore_case: bool = True, strict: bool = False,
      dynamic: bool = False, ) -> NodeType:

    node_type_class = self.node_type_class_map.get(type_, self.default_node_type)

    if node_type_class is None:
      raise ValueError(f"Unknown node type: {type_}")

    return node_type_class(type_=type_, name=name, description=description, schema=self, base_url=base_url,
                           code_prefix=code_prefix, curie_prefix=curie_prefix, url_regex=url_regex,
                           url_regex_ignore_case=url_regex_ignore_case, strict=strict, dynamic=dynamic)

  def create_edge_type(self, *, type_: StrEnum, from_node_type: NodeType, to_node_type: NodeType,
      name: t.Optional[str] = None, description: t.Optional[str] = None, strict: bool,
      dynamic: bool = False, ) -> EdgeType:

    edge_type_class: t.Type[EdgeType] = self.edge_type_class_map.get(type_, self.default_edge_type)

    if edge_type_class is None:
      raise ValueError(f"Unknown edge type: {type_}")

    return edge_type_class(type_=type_, from_node_type=from_node_type, to_node_type=to_node_type, name=name,
                           description=description, schema=self, strict=strict, dynamic=dynamic)

  def create_property_type(self, *, type_: StrEnum, property_owner_type: PropertyOwnerType,
      name: t.Optional[str] = None, description: t.Optional[str] = None, strict: bool, dynamic: bool) -> PropertyType:

    property_class = self.property_type_class_map.get(type_, PropertyType)

    return property_class(type_=type_, property_owner_type=property_owner_type, name=name, description=description,
                          strict=strict, dynamic=dynamic, )


# todo: should be abstract
class SchemaType:
  def __init__(self, *, type_: StrEnum, schema: Schema, name: t.Optional[str], description: t.Optional[str],
      strict: bool, dynamic: bool):
    self.type_ = type_
    self.schema = schema
    self.name = name
    self.description = description
    self.strict = strict
    self.dynamic = dynamic


# todo: should be abstract
class PropertyOwnerType(SchemaType):
  def __init__(self, *, type_: StrEnum, schema: Schema, name: t.Optional[str], description: t.Optional[str],
      strict: bool, dynamic: bool):
    super().__init__(type_=type_, name=name, description=description, schema=schema, strict=strict, dynamic=dynamic)
    self.property_types: t.Dict[StrEnum, PropertyType] = {}

  def add_property_type(self, property_type: PropertyType):
    if property_type.type_ in self.property_types:
      raise ValueError(f"Duplicate property type: {property_type}")
    self.property_types[property_type.type_] = property_type

  def get_property_type(self, type_: StrEnum) -> t.Optional[PropertyType]:

    prop = self.property_types.get(type_, None)
    if prop:
      return prop
    if self.strict:
      raise ValueError(f"Unknown property type: {type_}")
    prop = self.schema.create_property_type(type_=type_, property_owner_type=self, dynamic=True, strict=self.strict)
    self.property_types[type_] = prop
    return prop


class NodeType(PropertyOwnerType):

  def __init__(self, *, type_: StrEnum, schema: Schema, name: t.Optional[str] = None,
      description: t.Optional[str] = None, base_url: str = None, code_prefix: t.Optional[str] = None,
      curie_prefix: str = None, url_regex: str = None, url_regex_ignore_case: bool = True, strict: bool = False,
      dynamic: bool = False):
    super().__init__(type_=type_, name=name, description=description, schema=schema, strict=strict, dynamic=dynamic)

    if base_url is None:
      base_url = f'tag:loinclib:{type_.name}.{type_.value}/'

    if url_regex is None:
      url_regex = fr'^{base_url}(P<code>.+)$'

    self.base_url = base_url
    self.code_prefix = code_prefix
    self.curie_prefix = curie_prefix
    self.property_types: t.Dict[StrEnum, PropertyType] = dict()
    self.out_edge_types: t.Dict[StrEnum, t.Dict[StrEnum, EdgeType]] = dict()

    flags = 0
    if url_regex_ignore_case:
      flags = flags | re.IGNORECASE
    self.url_regex_pattern: re.Pattern = re.compile(url_regex, flags)

  def get_node(self, code: str) -> t.Optional[Node]:
    node_id = self.get_id_from_code(code)
    data = self.schema.graph.nx_graph.nodes.get(node_id)
    if data is not None:
      return Node(node_id=node_id, node_type=self, properties=data)

  def getsert_node(self, code: str) -> Node:
    node = self.get_node(code)
    if node:
      return node
    node_id = self.get_id_from_code(code)
    graph = self.schema.graph.nx_graph
    graph.add_node(node_id)
    data =graph.nodes[node_id]
    data[SchemaEnum.TYPE_KEY] = self.type_
    node = Node(node_id=node_id, node_type=self, properties=data)
    return node

  def get_id_from_code(self, code: str) -> str:
    return self.get_url_from_code(code)

  def get_url_from_code(self, code: str) -> str:
    return self.base_url + code

  def get_properties(self, node_id: str) -> t.Optional[t.Dict[StrEnum, t.Any]]:
    return self.schema.graph.nx_graph.nodes[node_id]

  def add_out_edge_type(self, edge_type: EdgeType):
    to_edge_types = self.out_edge_types.get(edge_type.type_, {})
    if edge_type.to_node_type in to_edge_types:
      raise ValueError(f"Duplicate edge type: {edge_type}")
    to_edge_types[edge_type.to_node_type.type_] = edge_type

  def get_out_edge_type(self, type_: StrEnum, to_node_type: NodeType) -> t.Optional[EdgeType]:
    to_edge_types = self.out_edge_types.get(type_, {})
    edge_type: EdgeType = to_edge_types.get(to_node_type.type_, None)
    if edge_type:
      return edge_type

    if self.strict:
      raise ValueError(f"Unknown edge type: {type_} to node type: {to_node_type.type_}")

    edge_type = self.schema.create_edge_type(type_=type_, from_node_type=self, to_node_type=to_node_type,
                                             strict=self.strict, dynamic=True)
    to_edge_types[to_node_type.type_] = edge_type
    return edge_type

  def get_all_out_edges(self, node_id) -> t.Iterator[t.Tuple[str, str, int, t.Dict[StrEnum, t.Any]]]:
    nx_graph = self.schema.graph.nx_graph
    for tup in nx_graph.out_edges(nbunch=node_id, keys=True, data=True):
      yield tup


class EdgeType(PropertyOwnerType):
  def __init__(self, *, type_: StrEnum, from_node_type: NodeType, to_node_type: NodeType, name: t.Optional[str] = None,
      description: t.Optional[str] = None, schema: Schema, strict: bool = False, dynamic: bool):
    super().__init__(type_=type_, name=name, description=description, strict=strict, schema=schema, dynamic=dynamic)
    self.from_node_type: NodeType = from_node_type
    self.to_node_type: NodeType = to_node_type

  def get_edge_single(self, from_node_id: str, to_node_id: str) -> t.Optional[int]:
    edges: t.List[int] = []
    for from_id, to_id, key, data in self.schema.graph.nx_graph.out_edges(nbunch=from_node_id, data=True, keys=True):
      if data[SchemaEnum.TYPE_KEY] == self.type_ and to_id == to_node_id:
        edges.append(key)

    length = len(edges)
    if length == 0:
      return None

    if length == 1:
      return edges[0]

    raise ValueError(f"Duplicate edge type: {self.type_} from node: {from_node_id} to node: {to_node_id}")

  def add_edge_single(self, from_node_id: str, to_node_id: str, error_if_duplicate=False) -> int:
    current_key = self.get_edge_single(from_node_id=from_node_id, to_node_id=to_node_id)
    nx_graph = self.schema.nx_graph
    if current_key is not None and error_if_duplicate:
      data = nx_graph.out_edges[from_node_id, to_node_id, current_key]
      raise ValueError(
          f"Duplicate edge type: {self.type_} from node id: {from_node_id} to node id: {to_node_id} with key: {current_key} and data: {data}")

    if current_key is not None:
      return current_key

    current_key = self.schema.graph.nx_graph.add_edge(u_for_edge=from_node_id, v_for_edge=to_node_id)
    data = nx_graph.out_edges[from_node_id, to_node_id, current_key]
    data[SchemaEnum.TYPE_KEY] = self.type_
    return current_key


class PropertyType(SchemaType):
  def __init__(self, *, type_: StrEnum, property_owner_type: PropertyOwnerType, name: t.Optional[str],
      description: t.Optional[str], strict: bool, dynamic: bool, ):
    super().__init__(type_=type_, name=name, description=description, schema=property_owner_type.schema, strict=strict,
                     dynamic=dynamic)
    self.property_owner_type = property_owner_type

  def get_value(self, element: Node | Edge) -> t.Any:
    properties = element.get_properties()
    return properties.get(self.type_)

  def set_value(self, element: Node | Edge, value: t.Any) -> None:
    if value is None:
      del element.get_properties()[self.type_]
    else:
      element.get_properties()[self.type_] = value


class LoinclibGraph:
  def __init__(self, *, graph_path: Path = None, graph: nx.MultiDiGraph = None):
    self.graph_path: Path = graph_path
    self.nx_graph: nx.MultiDiGraph = graph

    if self.nx_graph is None:
      if self.graph_path is None:
        self.nx_graph = nx.MultiDiGraph()
      else:
        with open(self.graph_path, 'rb') as f:
          self.nx_graph: nx.MultiDiGraph = pickle.load(f)

    self.loaded_sources = self.nx_graph.graph.setdefault('loaded_sources', {})
    self.schema = self.nx_graph.graph.setdefault('schema', Schema(self))

  def get_node_by_code(self, *, type_: StrEnum, code: str) -> t.Optional[Node]:
    return self.schema.get_node_type(type_).get_node(code=code)

  def get_node_by_id(self, *, node_id: str) -> t.Optional[Node]:
    node_data = self.nx_graph.nodes.get(node_id)
    if node_data:
      type_ = node_data[SchemaEnum.TYPE_KEY]
      node_type = self.schema.get_node_type(type_)
      return Node(node_id=node_id, node_type=node_type, properties=node_data)

  def get_nodes(self, type_: StrEnum) -> t.Iterator[Node]:
    for node, node_data in self.nx_graph.nodes.items():
      node_type = node_data.get(SchemaEnum.TYPE_KEY, None)
      if type_ is node_type:
        yield Node(node_id=node, node_type=self.schema.get_node_type(type_),properties=node_data)

  def getsert_node(self, type_: StrEnum, code: str) -> Node:
    return self.schema.get_node_type(type_).getsert_node(code=code)

  def pickle(self, path: Path = None):

    if path is None:
      if self.graph_path is None:
        raise ValueError('No path argument given and {self} does not have a path either')
      else:
        with open(self.graph_path, 'wb') as f:
          pickle.dump(self.nx_graph, f)
    else:
      with open(path, 'wb') as f:
        pickle.dump(self.nx_graph, f)


# todo: make abstract
class Element:
  def __init__(self, *, graph: LoinclibGraph):
    self.graph: LoinclibGraph = graph

  def get_properties(self) -> t.Dict[StrEnum, t.Any]:
    pass


class Node(Element):
  def __init__(self, *, node_id: str, node_type: NodeType, properties: dict):
    super().__init__(graph=node_type.schema.graph)
    self.node_id = node_id
    self.node_type: NodeType = node_type
    self.properties = properties

  def get_property(self, type_: StrEnum) -> t.Any:
    return self.node_type.get_property_type(type_).get_value(self)

  def set_property(self, *, type_: StrEnum, value: t.Any) -> Node:
    self.node_type.get_property_type(type_).set_value(self, value)
    return self

  def get_properties(self) -> t.Dict[StrEnum, t.Any]:
    return self.node_type.get_properties(self.node_id)

  def add_edge_single(self, type_: StrEnum, to_node: Node, error_if_duplicate: bool = False) -> Edge:
    edge_type = self.node_type.get_out_edge_type(type_=type_, to_node_type=to_node.node_type)
    key = edge_type.add_edge_single(from_node_id=self.node_id, to_node_id=to_node.node_id, error_if_duplicate=error_if_duplicate)
    return Edge(from_node=self, to_node=to_node, edge_key=key, edge_type=edge_type)

  def get_edge_single(self, type_: StrEnum, to_node: Node) -> t.Optional[Edge]:
    edge_type = self.node_type.get_out_edge_type(type_=type_, to_node_type=to_node.node_type)
    key = edge_type.get_edge_single(from_node_id=self.node_id, to_node_id=to_node.node_id)
    if key:
      return Edge(from_node=self, to_node=self.graph.get_node_by_id(node_id=to_node.node_id), edge_key=key,
                  edge_type=edge_type)

  def get_all_out_edges(self):
    for from_id, to_id, key, data in self.node_type.get_all_out_edges(self.node_id):
      from_node = self.graph.get_node_by_id(node_id=from_id)
      to_node = self.graph.get_node_by_id(node_id=to_id)
      edge_type = self.node_type.get_out_edge_type(type_=data[SchemaEnum.TYPE_KEY], to_node_type=to_node.node_type)
      yield Edge(from_node=from_node, to_node=to_node, edge_key=key, edge_type=edge_type)

  def __str__(self):
    return f'Node: {self.node_id} with data {self.get_properties()}'

  # def get_out_edges(self, type_keys: t.Optional[StrEnum | t.Set[StrEnum]] = None) -> \  #     t.Iterator[Edge]:  #   type_keys = type_keys if isinstance(type_keys, set) else set(  #       type_keys) if type_keys else None  # todo: fix?  #   for from_node, to_node, edge_key, data in self.graph.edges(  #       nbunch=self.node_id, data=True, keys=True):  #     type_key = data.get(TYPE_KEY, None)  #     self.node_type.get_edge()  #     if type_keys is None or type_key in type_keys:  #       edge_view = Edge(edge_type_key=type_key, from_node_id=from_node,  #                        to_node_id=to_node,  #                        edge_key=edge_key, graph=self.graph)  #   # todo: fix  #   return None

  # def get_out_edges_by_type(self, type_key:StrEnum) -> t.Iterator[Edge]:  #  #   for from_node, to_node, edge_key, data in self.graph.edges(  #       nbunch=self.node_id, data=True, keys=True):  #     if TYPE_KEY in data and data[TYPE_KEY] == type_key:  #       edge_view = Edge(edge_type_key=type_key, from_node_id=from_node,  #                        to_node_id=to_node,  #                        edge_key=edge_key, graph=self.graph)  #       yield edge_view

  # def get_or_create_out_edge_type(self, *,  #     edge_type_key:StrEnum, target_type_key:StrEnum,  #     target_code_code: str) -> Edge:  #  #   target_type = self.node_type_key.schema.get_node_type()  #   target_id = target_type.get_id_from_code(target_code_code)  #  #   target = self.graph.succ[self.node_id].get(target_id, None)  #   if target is None:  #     self.graph.add_edge(self.node_id, target_id,  #                         TYPE_KEY=target_node_type.type_)  #   else:  #     pass

  # @staticmethod  # def get_node_by_code(code: str, type_key:StrEnum, graph: nx.Graph, schema: Schema, create: bool = False) -> \  #         t.Optional[Node]:  #     node_type = schema.get_node_type(type_key)  #     node_id = node_type.get_id_from_code(code)  #     node = graph.nodes.get(node_id)  #     if node is None and create:  #         graph.add_node(node_id)  #         node = graph.nodes.get(node_id)  #  #     return Node(node_type, node_id, graph)


class Edge(Element):
  def __init__(self, *, from_node: Node, to_node: Node, edge_key: int, edge_type: EdgeType):
    super().__init__(graph=edge_type.schema.graph)
    self.from_node: Node = from_node
    self.to_node: Node = to_node
    self.edge_key = edge_key
    self.edge_type = edge_type

  def get_property(self, type_: StrEnum) -> t.Any:
    property_type = self.edge_type.get_property_type(type_)
    if property_type is None:
      return None
    return property_type.get_value(self)

  def set_property(self, *, type_: StrEnum, value: t.Any) -> Edge:
    property_type = self.edge_type.get_property_type(type_=type_)
    property_type.set_value(self, value)
    return self

  def get_properties(self) -> t.Dict[StrEnum, t.Any]:
    return self.edge_type.schema.graph.nx_graph.edges[self.from_node.node_id, self.to_node.node_id, self.edge_key]

  def __str__(self):
    return f'Edge {self.edge_key}: {self.from_node.node_id}  {self.edge_type.type_.value}  {self.to_node.node_id} with data: {self.get_properties()}'
