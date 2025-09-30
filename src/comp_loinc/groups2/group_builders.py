import sys
import typing as t
from operator import truediv

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.datamodel.comp_loinc import LoincTerm, LoincPartId
from comp_loinc.groups2.group import Group, GroupProperty, GroupPart
from comp_loinc.groups2.groups import Groups
from loinclib import LoincNodeType, EdgeType
from loinclib.graph import Node, Edge
from loinclib.loinc_schema import LoincPartProps, LoincTermProps
from loinclib.loinc_tree_schema import LoincTreeProps
from loinclib.loinc_tree_loader import LoincTreeLoader
from comp_loinc.comploinc_schema import ComploincNodeType
from comp_loinc import root_classes


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

        self.circles: set = set()

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
        # loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()
        loinc_loader.load_accessory_files__part_file__part_csv()

        groups = self._get_groups_object()
        loinc_counts = 0
        group_counts = 0
        for loinc_node in self.runtime.graph.get_nodes(LoincNodeType.LoincTerm):
            loinc_counts += 1
            out_edges = loinc_node.get_all_out_edges()

            # properties = dict()
            group: Group = Group()
            # indexing the parts by group properties, per loinc
            for out_edge in out_edges:
                type_ = out_edge.handler.type_
                if self._use_property(type_):
                    properties = group.properties.setdefault(type_, set())
                    group_property = GroupProperty(edge_type=type_, group_part=GroupPart(out_edge.to_node))
                    properties.add(group_property)

            group_key = group.group_key()

            if group_key is not None:
                group_counts += 1
                group = groups.groups.setdefault(group_key, group)

                group.loincs[loinc_node.get_property(LoincTermProps.loinc_number)] = loinc_node
                group.key = group_key

        print("debug")

        loinc_counts = 0
        for group in groups.groups.values():
            count = group.get_descendants_loincs_count()
            loinc_counts += count

        print("\n\n======= loinc counts from all groups =========")
        print(loinc_counts)

    def group_roots(self):
        loinc_loader = ll.loinc_loader.LoincLoader(
            graph=self.runtime.graph, configuration=self.config
        )
        # loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

        tree_loader: LoincTreeLoader = LoincTreeLoader(graph=self.runtime.graph, config=self.config)
        tree_loader.load_component_tree()
        # tree_loader.load_component_by_system_tree()
        tree_loader.load_system_tree()
        tree_loader.load_document_tree()
        tree_loader.load_class_tree()
        tree_loader.load_panel_tree()
        tree_loader.load_method_tree()

        groups_object = self._get_groups_object()

        seen_by_property: t.Dict[EdgeType, t.Set[str]] = dict()

        debug_counter = 0
        for key, group in groups_object.groups.copy().items():
            debug_counter += 1
            if debug_counter % 1000 == 0:
                print(f"Root: {debug_counter}")
            # if group.is_abstract():
            #   continue
            for prop, part_node in group.property_dict.items():
                # seen = seen_by_property.setdefault(prop, set())
                self._do_roots(prop, part_node, group, list())

        for key, group in groups_object.groups.items():
            if (len(group.parent_groups) == 0
                    # and group.get_descendants_loincs_count() > 0
                    and len(group.child_groups) > 0):
                # for child_group in group.child_groups.values():
                # if not child_group.is_complex():
                groups_object.roots[key] = group

        print("debug")

    def group_generate(self):
        groups: Groups = self.runtime.current_module.runtime_objects.get("groups")
        loinc_counts = 0
        # for group in groups.roots.values():
        #   count = group.get_descendants_loincs_count()
        #   loinc_counts += count
        #   print(f"{group} has descendants count:\n{count}")
        #
        # print("\n\n======= loinc counts from root groups =========")
        # print(loinc_counts)
        #
        # loinc_counts = 0
        # for group in groups.groups.values():
        #   count = group.get_descendants_loincs_count()
        #   loinc_counts += count
        #
        # print("\n\n======= total counts with possible duplicates =========")
        # print(loinc_counts)
        #
        # print("\n\n=============== root group count =================")
        # print(len(groups.roots))
        generated_count = 0
        for key, group in groups.groups.items():
            generated_count += 1
            if generated_count % 1000 == 0:
                print(f"Generated: {generated_count}")
            self._do_generate(key, group)
            # loinc_group = self.runtime.current_module.get_entity(entity_id=f"{ComploincNodeType.group_node.value.id_prefix}:{key}", entity_class=LoincTerm)
            # if loinc_group is None:
            #   loinc_group = self.runtime.current_module.getsert_entity(entity_id=f"{ComploincNodeType.group_node.value.id_prefix}:{key}", entity_class=LoincTerm)
            #   edge_type: EdgeType
            #   part_node: Node
            #   for edge_type, part_node in group.properties.items():
            #     part_id = LoincPartId(f"{LoincNodeType.LoincPart.value.id_prefix}:{part_node.get_property(LoincPartProps.part_number)}")
            #     setattr(loinc_group, edge_type.name.lower(), part_id)

            circles = list(self.circles)
            circles.sort()
            for circle in circles:
                print(f"Circle: {circle}")

    def _do_generate(self, key: str, group: Group, parent_group: Group = None):

        if self._can_generate(group=group, parent_group=parent_group):
            loinc_group = self.runtime.current_module.get_entity(
                entity_id=f"{ComploincNodeType.group_node.value.id_prefix}:{key}", entity_class=LoincTerm)
            if loinc_group is not None:
                return

            loinc_group = self.runtime.current_module.getsert_entity(
                entity_id=f"{ComploincNodeType.group_node.value.id_prefix}:{key}", entity_class=LoincTerm)

            edge_type: EdgeType
            part_node: Node
            label = ""
            group_prefix = "G-"
            for edge_type, part_node in group.property_dict.items():
                group_prefix += edge_type.value.abbr
            group_prefix += "--"

            for edge_type, part_node in group.property_dict.items():
                part_number = part_node.get_property(LoincPartProps.part_number)
                part_id = LoincPartId(f"{LoincNodeType.LoincPart.value.id_prefix}:{part_number}")
                setattr(loinc_group, edge_type.name.lower(), part_id)
                name = part_node.get_property(LoincPartProps.part_name)
                if name is not None:
                    name += f"_({part_node.get_property(LoincPartProps.part_display_name)})"
                if name is None:
                    name = part_node.get_property(LoincTreeProps.code_text)

                label += f"{group_prefix}{edge_type.value.abbr}_{name}_{part_number}--"
            loinc_group.entity_label = label
            if group.get_descendants_count() > 2 and len(group.parent_groups) == 0:
                root_classes.group_tree_root(loinc_group, self.runtime.current_module)
            else:
                root_classes.group_single_root(loinc_group, self.runtime.current_module)

        # seen_keys = set()
        # for child_key, child_group in group.child_groups.items():
        #   self._do_generate(child_key, group=child_group, parent_group=group, seen_keys=seen_keys)

    def _can_generate(self, group: Group, parent_group: Group, ) -> bool:
        return True
        if parent_group is None:
            return True
        if not group.is_abstract():
            return True

        if group.has_concrete_child():
            return True

        return False

    def _do_roots(self,
                  prop: EdgeType,
                  part_node: Node,
                  child_group: Group,
                  seen: t.List[str],
                  ):
        part_number = part_node.get_property(LoincPartProps.part_number)

        if part_number in seen:
            i = seen.index(part_number)
            sub = seen[i:]
            sub.append(part_number)
            self.circles.add(tuple(sub))
            # print(f"Seen hit circle: with part number: {part_number} and path: {repr(seen)}")
            return
        seen.append(part_number)

        group_key = Group.group_key({prop: part_node})
        groups_object = self._get_groups_object()
        parent_group = groups_object.groups.get(group_key, None)
        if parent_group is None:
            parent_group = Group(properties)
            parent_group.property_dict[prop] = part_node
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
            else:
                print("debug")

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
