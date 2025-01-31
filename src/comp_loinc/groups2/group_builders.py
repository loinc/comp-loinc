import typing as t

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.groups2.group import Group
from comp_loinc.groups2.groups import Groups
from loinclib import LoincNodeType
from loinclib.loinc_schema import LoincPartProps, LoincTermProps


class Groups2BuilderSteps:
  def __init__(
      self,
      config: ll.Configuration,
  ):
    self.config = config
    self.runtime: t.Optional[cl.Runtime] = None
    self.properties = []

  def setup_builder_cli(self, builder):
    builder.cli.command(
        "group2-hello",
        help="Group 2 hello",
    )(self.hello)

    builder.cli.command(
        "group-properties",
        help="Specify the LOINC properties to use for grouping",
    )(self.group_properties)

    builder.cli.command(
        "group-parse-loincs",
        help="Parse LOINC definitions into base groups.",
    )(self.group_parse_loincs)

  def hello(self):
    module = self.runtime.current_module
    grouper: Groups = module.runtime_objects.setdefault('grouper2', Groups(config=self.config, module=module))
    grouper.init()
    print("==================  GROUP 2 HELLO  =================")

  def group_properties(self, properties: t.Annotated[list[str], typer.Option("--properties", "-p",
                                                                             help="One or more property strings. Full property URL, or last segment. Case insensitive")]):
    for p in properties:
      enum = ll.loinc_schema.LoincTermPrimaryEdges.get_enum(p)
      if enum is not None:
        self.properties.append(enum)
        order = enum.order
        prefix = enum.prefix
        continue
      enum = ll.loinc_schema.LoincTermSupplementaryEdges.get_enum(p)
      if enum is not None:
        self.properties.append(enum)
        continue

      raise ValueError(f"Unknown LOINC property: {p}")

    self.properties.sort(key=lambda prop: prop.order)

  def group_parse_loincs(self):
    loinc_loader = ll.loinc_loader.LoincLoader(
        graph=self.runtime.graph, configuration=self.config
    )
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    # loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    groups = self._get_groups()
    for loinc_node in self.runtime.graph.get_nodes(LoincNodeType.LoincTerm):
      out_edges = loinc_node.get_all_out_edges()

      properties = dict()

      for out_edge in out_edges:
        type_ = out_edge.edge_type.type_
        if type_ in self.properties:
          part_number = out_edge.to_node.get_property(LoincPartProps.part_number)
          properties[type_] = out_edge.to_node

      key = Group.group_key(properties)

      if key is not None:
        group = groups.groups.setdefault(key, Group())
        group.properties = properties
        group.loincs[loinc_node.get_property(LoincTermProps.loinc_number)] = loinc_node
        group.key = key

      # print(key)
    print("debug")

  def _get_groups(self) -> Groups:
    current_module = self.runtime.current_module
    return self.runtime.current_module.runtime_objects.setdefault('groups',
                                                                  Groups(config=self.config, module=current_module))
