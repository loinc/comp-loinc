from __future__ import annotations

import pickle
import re
import typing as t
from dataclasses import dataclass
from enum import StrEnum, Enum
from pathlib import Path

import networkx as nx


#
# SCHEMA_KEY = '__SCHEMA__'
#
# TAGS_KEY = '__TAGS__'


class ElementKeys(StrEnum):
  TYPE_KEY = "_type"
  SOURCES_KEY = "_sources"


class Schema:
  def __init__(self, graph: LoinclibGraph, strict: bool = False):
    self.graph: LoinclibGraph = graph
    self.nx_graph = graph.nx_graph
    self.strict = strict
    self.node_handlers: t.Dict[NodeType, NodeHandler] = {}

    self.node_handler_class_map: t.Dict[NodeType, t.Type[NodeHandler]] = {}
    self.default_node_handler: t.Type[NodeHandler] = NodeHandler

    self.edge_handler_class_map: t.Dict[EdgeType, t.Type[EdgeHandler]] = {}
    self.default_edge_handler: t.Type[EdgeHandler] = EdgeHandler

    self.property_handler_class_map: t.Dict[PropertyType, t.Type[PropertyHandler]] = {}
    self.default_property_handler: t.Type[PropertyHandler] = PropertyHandler

  def add_node_handler(self, *, node_handler: NodeHandler) -> Schema:
    if node_handler.type_ in self.node_handlers:
      raise ValueError(f"Duplicate node handler: {node_handler}")
    self.node_handlers[node_handler.type_] = node_handler
    return self

  def get_node_handler(self, node_type: NodeType) -> NodeHandler:
    node_handler = self.node_handlers.get(node_type, None)
    if node_handler:
      return node_handler
    if self.strict:
      raise ValueError(f"Unknown node type: {node_type}")
    node_handler = self.create_node_handler(type_=node_type, dynamic=True, strict=self.strict)
    self.node_handlers[node_type] = node_handler
    return node_handler

  def create_node_handler(
      self,
      *,
      type_: NodeType,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      base_url: t.Optional[str] = None,
      code_prefix: t.Optional[str] = None,
      curie_prefix: t.Optional[str] = None,
      url_regex: t.Optional[str] = None,
      url_regex_ignore_case: bool = True,
      strict: bool = False,
      dynamic: bool = False,
  ) -> NodeHandler:

    node_type_class = self.node_handler_class_map.get(type_, self.default_node_handler)

    if node_type_class is None:
      raise ValueError(f"Unknown node type: {type_}")

    return node_type_class(
        type_=type_,
        name=name,
        description=description,
        schema=self,
        base_url=base_url,
        code_prefix=code_prefix,
        curie_prefix=curie_prefix,
        url_regex=url_regex,
        url_regex_ignore_case=url_regex_ignore_case,
        strict=strict,
        dynamic=dynamic,
    )

  def create_edge_handler(
      self,
      *,
      type_: EdgeType,
      from_node_handler: NodeHandler,
      to_node_handler: NodeHandler,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      strict: bool,
      dynamic: bool = False,
  ) -> EdgeHandler:

    edge_handler_class: t.Type[EdgeHandler] = self.edge_handler_class_map.get(
        type_, self.default_edge_handler
    )

    if edge_handler_class is None:
      raise ValueError(f"Unknown edge type: {type_}")

    return edge_handler_class(
        type_=type_,
        from_node_handler=from_node_handler,
        to_node_handler=to_node_handler,
        name=name,
        description=description,
        schema=self,
        strict=strict,
        dynamic=dynamic,
    )

  def create_property_handler(
      self,
      *,
      type_: PropertyType,
      property_owner_handler: PropertyOwnerHandler,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      strict: bool,
      dynamic: bool,
  ) -> PropertyHandler:

    property_handler_class = self.property_handler_class_map.get(type_, PropertyHandler)

    return property_handler_class(
        type_=type_,
        property_owner_handler=property_owner_handler,
        name=name,
        description=description,
        strict=strict,
        dynamic=dynamic,
    )


#
# @dataclass(kw_only=True)
# class TypeArgs:
#     name: str

@dataclass(kw_only=True)
class TypeArgs:
  name: str
  abbr: t.Optional[str] = None
  path: t.Optional[str] = None

  def __post_init__(self):
    if self.abbr is None:
      self.abbr = self.name


class Type(Enum):
  pass


# @dataclass(kw_only=True)
# class NodeTypeArgs(TypeArgs):
#     id_prefix: str

@dataclass(kw_only=True)
class NodeTypeArgs(TypeArgs):
  id_prefix: str


class NodeType(Type):
  pass


# @dataclass(kw_only=True)
# class EdgeTypeArgs(TypeArgs):
#     pass

@dataclass(kw_only=True)
class EdgeTypeArgs(TypeArgs):
  pass


class EdgeType(Type):
  pass


@dataclass(kw_only=True)
class GeneralEdgeTypeArgs(EdgeTypeArgs):
  pass


class GeneralEdgeType(EdgeType):
  has_parent = GeneralEdgeTypeArgs(name="has_parent")
  maps_to = GeneralEdgeTypeArgs(name="maps_to")


@dataclass(kw_only=True)
class PropertyTypeArgs(TypeArgs):
  pass


class PropertyType(Type):
  pass


# todo: should be abstract
class Handler:
  def __init__(
      self,
      *,
      # type_: Type,
      schema: Schema,
      name: t.Optional[str],
      description: t.Optional[str],
      strict: bool,
      dynamic: bool,
  ):
    # self.type_ = type_
    self.schema = schema
    self.name = name
    self.description = description
    self.strict = strict
    self.dynamic = dynamic


# todo: should be abstract
class PropertyOwnerHandler(Handler):
  def __init__(
      self,
      *,
      # type_: Type,
      schema: Schema,
      name: t.Optional[str],
      description: t.Optional[str],
      strict: bool,
      dynamic: bool,
  ):
    super().__init__(
        # type_=type_,
        name=name,
        description=description,
        schema=schema,
        strict=strict,
        dynamic=dynamic,
    )
    self.property_handlers: t.Dict[PropertyType, PropertyHandler] = {}

  def add_property_type(self, property_handler: PropertyHandler):
    if property_handler.type_ in self.property_handlers:
      raise ValueError(f"Duplicate property handler: {property_handler}")
    self.property_handlers[property_handler.type_] = property_handler

  def get_property_handler(self, type_: PropertyType) -> t.Optional[PropertyHandler]:

    prop = self.property_handlers.get(type_, None)
    if prop:
      return prop
    if self.strict:
      raise ValueError(f"Unknown property type: {type_}")
    prop = self.schema.create_property_handler(
        type_=type_, property_owner_handler=self, dynamic=True, strict=self.strict
    )
    self.property_handlers[type_] = prop
    return prop


class NodeHandler(PropertyOwnerHandler):

  def __init__(
      self,
      *,
      type_: NodeType,
      schema: Schema,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      base_url: str = None,
      code_prefix: t.Optional[str] = None,
      curie_prefix: str = None,
      url_regex: str = None,
      url_regex_ignore_case: bool = True,
      strict: bool = False,
      dynamic: bool = False,
  ):
    super().__init__(
        # type_=type_,
        name=name,
        description=description,
        schema=schema,
        strict=strict,
        dynamic=dynamic,
    )

    self.type_ = type_

    if base_url is None:
      base_url = f"tag:loinclib:{type_.name}.{type_.value}/"

    if url_regex is None:
      url_regex = rf"^{base_url}(?P<code>.+)$"
    self.url_regex = url_regex

    self.base_url = base_url
    self.code_prefix = code_prefix
    self.curie_prefix = curie_prefix
    self.property_handlers: t.Dict[PropertyType, PropertyHandler] = dict()
    self.out_edge_handlers: t.Dict[EdgeType, t.Dict[NodeType, EdgeHandler]] = dict()
    self.in_edge_handlers: t.Dict[EdgeType, t.Dict[NodeType, EdgeHandler]] = dict()

    flags = 0
    if url_regex_ignore_case:
      flags = flags | re.IGNORECASE
    self.url_regex_pattern: re.Pattern = re.compile(self.url_regex, flags)

  def get_node_by_id(self, node_id: str) -> t.Optional[Node]:
    data = self.schema.graph.nx_graph.nodes.get(node_id)
    if data is not None:
      return Node(node_id=node_id, node_handler=self, properties=data)
    return None

  def get_node_by_code(self, code: str) -> t.Optional[Node]:
    node_id = self.get_id_from_code(code)
    return self.get_node_by_id(node_id)

  def getsert_node_by_code(self, code: str, source: str = None) -> Node:
    node = self.get_node_by_code(code)
    if node is None:
      graph = self.schema.graph.nx_graph
      node_id = self.get_id_from_code(code)
      graph.add_node(node_id)
      data = graph.nodes[node_id]
      data[ElementKeys.TYPE_KEY] = self.type_
      node = Node(node_id=node_id, node_handler=self, properties=data)

    if source is not None:
      sources = node.get_property(ElementProps.sources)
      if sources is None:
        sources = set()
        node.set_property(type_=ElementProps.sources, value=sources)
      sources.add(source)
    return node

  def get_id_from_code(self, code: str) -> str:
    return f"{self.type_.value.id_prefix}:{code}"
    # return self.get_url_from_code(code)

  def get_code_from_id(self, node_id: str) -> str:
    match = self.url_regex_pattern.match(node_id)
    return match.group("code")

  def get_url_from_code(self, code: str) -> str:
    return self.base_url + code

  def get_properties(self, node_id: str) -> t.Optional[t.Dict[str, t.Any]]:
    return self.schema.graph.nx_graph.nodes[node_id]

  def add_out_edge_handler(self, edge_handler: EdgeHandler):
    to_edge_handlers = self.out_edge_handlers.get(edge_handler.type_, {})
    if edge_handler.to_node_handler.type_ in to_edge_handlers:
      raise ValueError(f"Duplicate edge type: {edge_handler}")
    to_edge_handlers[edge_handler.to_node_handler.type_] = edge_handler

  def get_out_edge_handler(
      self, type_: EdgeType, to_node_handler: NodeHandler
  ) -> t.Optional[EdgeHandler]:
    to_edge_handlers_by_type = self.out_edge_handlers.get(type_, {})
    edge_handler: EdgeHandler = to_edge_handlers_by_type.get(to_node_handler.type_, None)
    if edge_handler:
      return edge_handler

    if self.strict:
      raise ValueError(
          f"Unknown edge type: {type_} to node type: {to_node_handler.type_}"
      )

    edge_handler = self.schema.create_edge_handler(
        type_=type_,
        from_node_handler=self,
        to_node_handler=to_node_handler,
        strict=self.strict,
        dynamic=True,
    )
    to_edge_handlers_by_type[to_node_handler.type_] = edge_handler
    return edge_handler

  def get_in_edge_handler(
      self, type_: EdgeType, from_node_handler: NodeHandler
  ) -> t.Optional[EdgeHandler]:
    from_edge_handlers_by_type = self.in_edge_handlers.get(type_, {})
    edge_handler: EdgeHandler = from_edge_handlers_by_type.get(from_node_handler.type_, None)
    if edge_handler:
      return edge_handler

    if self.strict:
      raise ValueError(
          f"Unknown edge type: {type_} to node type: {from_node_handler.type_}"
      )

    edge_handler = self.schema.create_edge_handler(
        type_=type_,
        from_node_handler=from_node_handler,
        to_node_handler=self,
        strict=self.strict,
        dynamic=True,
    )
    from_edge_handlers_by_type[from_node_handler.type_] = edge_handler
    return edge_handler

  def get_all_out_edges(
      self, node_id
  ) -> t.Iterator[t.Tuple[str, str, int, t.Dict[PropertyType, t.Any]]]:
    nx_graph = self.schema.graph.nx_graph
    for tup in nx_graph.out_edges(nbunch=node_id, keys=True, data=True):
      yield tup

  def get_all_in_edges(
      self, node_id
  ) -> t.Iterator[t.Tuple[str, str, int, t.Dict[PropertyType, t.Any]]]:
    nx_graph = self.schema.graph.nx_graph
    for tup in nx_graph.in_edges(nbunch=node_id, keys=True, data=True):
      yield tup


class EdgeHandler(PropertyOwnerHandler):
  def __init__(
      self,
      *,
      type_: EdgeType,
      from_node_handler: NodeHandler,
      to_node_handler: NodeHandler,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      schema: Schema,
      strict: bool = False,
      dynamic: bool,
  ):
    super().__init__(
        # type_=type_,
        name=name,
        description=description,
        strict=strict,
        schema=schema,
        dynamic=dynamic,
    )
    self.type_ = type_
    self.from_node_type: NodeHandler = from_node_handler
    self.to_node_handler: NodeHandler = to_node_handler

  def __repr__(self):
    return f"EdgeType(type_={self.type_!r})"

  def get_edge_single(self, from_node_id: str, to_node_id: str) -> t.Optional[int]:
    edges: t.List[int] = []
    for from_id, to_id, key, data in self.schema.graph.nx_graph.out_edges(
        nbunch=from_node_id, data=True, keys=True
    ):
      if data[ElementKeys.TYPE_KEY] == self.type_ and to_id == to_node_id:
        edges.append(key)

    length = len(edges)
    if length == 0:
      return None

    if length == 1:
      return edges[0]

    raise ValueError(
        f"Duplicate edge type: {self.type_} from node: {from_node_id} to node: {to_node_id}"
    )

  def add_edge_single(
      self, from_node_id: str, to_node_id: str, error_if_duplicate=False
  ) -> int:
    edge_key = self.get_edge_single(
        from_node_id=from_node_id, to_node_id=to_node_id
    )
    nx_graph = self.schema.nx_graph
    if edge_key is not None and error_if_duplicate:
      data = nx_graph.out_edges[from_node_id, to_node_id, edge_key]
      raise ValueError(
          f"Duplicate edge type: {self.type_} from node id: {from_node_id} to node id: {to_node_id} with key: {edge_key} and data: {data}"
      )

    if edge_key is not None:
      return edge_key

    edge_key = self.schema.graph.nx_graph.add_edge(
        u_for_edge=from_node_id, v_for_edge=to_node_id
    )
    data = nx_graph.out_edges[from_node_id, to_node_id, edge_key]
    data[ElementKeys.TYPE_KEY] = self.type_
    return edge_key


class PropertyHandler(Handler):
  def __init__(
      self,
      *,
      type_: PropertyType,
      property_owner_handler: PropertyOwnerHandler,
      name: t.Optional[str],
      description: t.Optional[str],
      strict: bool,
      dynamic: bool,
  ):
    super().__init__(
        # type_=type_,
        name=name,
        description=description,
        schema=property_owner_handler.schema,
        strict=strict,
        dynamic=dynamic,
    )
    self.type_ = type_
    self.property_owner_handler = property_owner_handler

  def get_value(self, element: Node | Edge) -> t.Any:
    properties = element.get_properties()
    return properties.get(self.type_.name, None)

  def set_value(self, element: Node | Edge, value: t.Any) -> None:
    if value is None:
      del element.get_properties()[self.type_.name]
    else:
      element.get_properties()[self.type_.name] = value


class LoinclibGraph:
  def __init__(self, *, graph_path: Path = None, graph: nx.MultiDiGraph = None):
    self.graph_path: Path = graph_path
    self.nx_graph: nx.MultiDiGraph = graph

    if self.nx_graph is None:
      if self.graph_path is None:
        self.nx_graph = nx.MultiDiGraph()
      else:
        with open(self.graph_path, "rb") as f:
          self.nx_graph: nx.MultiDiGraph = pickle.load(f)

    self.loaded_sources = self.nx_graph.graph.setdefault("loaded_sources", {})
    self.schema = self.nx_graph.graph.setdefault("schema", Schema(self))

  def get_node_by_code(self, *, type_: NodeType, code: str) -> t.Optional[Node]:
    return self.schema.get_node_handler(type_).get_node_by_code(code=code)

  def get_node_by_id(self, *, node_id: str) -> t.Optional[Node]:
    node_data = self.nx_graph.nodes.get(node_id)
    if node_data:
      type_ = node_data[ElementKeys.TYPE_KEY]
      node_handler = self.schema.get_node_handler(type_)
      return Node(node_id=node_id, node_handler=node_handler, properties=node_data)
    return None

  def get_nodes(self, type_: NodeType) -> t.Iterator[Node]:
    for node, node_data in self.nx_graph.nodes.items():
      node_type = node_data.get(ElementKeys.TYPE_KEY, None)
      if type_ is node_type:
        yield Node(
            node_id=node,
            node_handler=self.schema.get_node_handler(type_),
            properties=node_data,
        )

  def getsert_node(self, type_: NodeType, code: str, source: str = None) -> Node:
    return self.schema.get_node_handler(type_).getsert_node_by_code(code=code, source=source)

  def pickle(self, path: Path = None):

    if path is None:
      if self.graph_path is None:
        raise ValueError(
            "No path argument given and {self} does not have a path either"
        )
      else:
        with open(self.graph_path, "wb") as f:
          pickle.dump(self.nx_graph, f)
    else:
      with open(path, "wb") as f:
        pickle.dump(self.nx_graph, f)


@dataclass(kw_only=True)
class ElementSourceArgs:
  name: str
  abbr: t.Optional[str] = None

  def __post_init__(self):
    if self.abbr is None:
      self.abbr = self.name


class ElementProps(PropertyType):
  type = PropertyTypeArgs(name="_type")
  sources = PropertyTypeArgs(name="_sources")


# todo: make abstract
class Element:
  def __init__(self, *, graph: LoinclibGraph):
    self.graph: LoinclibGraph = graph

  def get_properties(self) -> t.Dict[PropertyType, t.Any]:
    pass


class Node(Element):
  def __init__(self, *, node_id: str, node_handler: NodeHandler, properties: dict):
    super().__init__(graph=node_handler.schema.graph)
    self.node_id = node_id
    self.node_handler: NodeHandler = node_handler
    self.properties = properties

  def get_property(self, type_: PropertyType) -> t.Any:
    return self.node_handler.get_property_handler(type_).get_value(self)

  def set_property(self, *, type_: PropertyType, value: t.Any) -> Node:
    self.node_handler.get_property_handler(type_).set_value(self, value)
    return self

  def get_properties(self) -> t.Dict[str, t.Any]:
    return self.node_handler.get_properties(self.node_id)

  def add_edge_single(
      self, type_: EdgeType, to_node: Node, error_if_duplicate: bool = False, source: str = None
  ) -> Edge:
    edge_handler = self.node_handler.get_out_edge_handler(
        type_=type_, to_node_handler=to_node.node_handler
    )
    key = edge_handler.add_edge_single(
        from_node_id=self.node_id,
        to_node_id=to_node.node_id,
        error_if_duplicate=error_if_duplicate,
    )
    edge = Edge(from_node=self, to_node=to_node, edge_key=key, edge_handler=edge_handler)
    if source is not None:
      sources: set = edge.get_property(ElementProps.sources)
      if sources is None:
        sources = set()
        edge.set_property(type_=ElementProps.sources, value=sources)
      sources.add(source)

    return edge

  def get_edge_single(self, type_: EdgeType, to_node: Node) -> t.Optional[Edge]:
    edge_type = self.node_handler.get_out_edge_handler(
        type_=type_, to_node_handler=to_node.node_handler
    )
    key = edge_type.get_edge_single(
        from_node_id=self.node_id, to_node_id=to_node.node_id
    )
    if key:
      return Edge(
          from_node=self,
          to_node=self.graph.get_node_by_id(node_id=to_node.node_id),
          edge_key=key,
          edge_handler=edge_type,
      )
    return None

  def get_all_out_edges(self):
    for from_id, to_id, key, data in self.node_handler.get_all_out_edges(self.node_id):
      from_node = self.graph.get_node_by_id(node_id=from_id)
      to_node = self.graph.get_node_by_id(node_id=to_id)
      edge_type = self.node_handler.get_out_edge_handler(
          type_=data[ElementKeys.TYPE_KEY], to_node_handler=to_node.node_handler
      )
      yield Edge(
          from_node=from_node, to_node=to_node, edge_key=key, edge_handler=edge_type)

  def get_out_edges(self, *, edge_types: t.List[EdgeType]) -> t.Generator[Edge]:
    return (edge for edge in self.get_all_out_edges() if edge.handler.type_ in edge_types)
    # return [ edge for edge in self.get_all_out_edges() if edge.handler.type_ in edge_types ]

  def get_all_out_nodes(self):
    return (edge.to_node for edge in self.get_all_out_edges())

  def get_out_nodes(self, *, edge_types: t.List[EdgeType], node_types: t.List[NodeType]):
    edges = list(self.get_out_edges(edge_types=edge_types))
    # if len(edges) > 0:
    #   print("debug")
    return (edge.to_node for edge in edges if edge.handler.type_ in edge_types and
            edge.to_node.get_node_type() in node_types)

  def get_all_in_edges(self):
    for from_id, to_id, key, data in self.node_handler.get_all_in_edges(self.node_id):
      from_node = self.graph.get_node_by_id(node_id=from_id)
      to_node = self.graph.get_node_by_id(node_id=to_id)
      edge_type = self.node_handler.get_in_edge_handler(
          type_=data[ElementKeys.TYPE_KEY], from_node_handler=from_node.node_handler
      )
      yield Edge(
          from_node=from_node, to_node=to_node, edge_key=key, edge_handler=edge_type
      )

  def get_in_edges(self, *, edge_types: t.List[EdgeType]) -> t.Generator[Edge, None, None]:
    return (edge for edge in self.get_all_in_edges() if edge.handler.type_ in edge_types)

  def get_all_in_nodes(self):
    return (edge.to_node for edge in self.get_all_in_edges())

  def get_in_nodes(self, *, edge_types: t.List[EdgeType], node_types: t.List[NodeType]):
    return (edge.from_node for edge in self.get_in_edges(edge_types=edge_types) if edge.handler.type_ in edge_types and
            edge.from_node.get_node_type() in node_types)

  def get_node_type(self):
    return self.node_handler.type_

  def get_id_code(self):
    return self.node_handler.get_code_from_id()

  def __str__(self):
    return f"Node: {self.node_id} with data {self.get_properties()}"

  def __eq__(self, other):
    if isinstance(other, Node):
      return self.node_id == other.node_id
    return False

  def __hash__(self):
    return hash(self.node_id)


class Edge(Element):
  def __init__(
      self, *, from_node: Node, to_node: Node, edge_key: int, edge_handler: EdgeHandler
  ):
    super().__init__(graph=edge_handler.schema.graph)
    self.from_node: Node = from_node
    self.to_node: Node = to_node
    self.edge_key = edge_key
    self.handler = edge_handler
    self.properties = self.graph.nx_graph.get_edge_data(u=self.from_node.node_id, v=self.to_node.node_id,
                                                        key=self.edge_key)

  def get_property(self, type_: PropertyType) -> t.Any:
    property_handler = self.handler.get_property_handler(type_)
    if property_handler is None:
      return None
    return property_handler.get_value(self)

  def set_property(self, *, type_: PropertyType, value: t.Any) -> Edge:
    property_handler = self.handler.get_property_handler(type_=type_)
    property_handler.set_value(self, value)
    return self

  def get_properties(self) -> t.Dict[PropertyType, t.Any]:
    return self.handler.schema.graph.nx_graph.edges[
      self.from_node.node_id, self.to_node.node_id, self.edge_key
    ]

  def __str__(self):
    return f"Edge {self.edge_key}: {self.from_node.node_id}  {self.handler.type_.value}  {self.to_node.node_id} with data: {self.get_properties()}"
