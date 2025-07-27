import os.path
import pickle
import sys
import time
import typing as t
from pathlib import Path
from pickle import Pickler

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.datamodel import LoincTerm, LoincPartId
from comp_loinc.groups.property_use import Property, Part
from comp_loinc.module import Module
from comploinc_schame import ComploincNodeType
from loinclib.loinc_schema import (
    LoincNodeType,
    LoincTermPrimaryEdges,
    LoincPartProps,
    LoincPartEdge,
    LoincTermSupplementaryEdges,
)
from loinclib.loinc_tree_loader import LoincTreeLoader
from loinclib.loinc_tree_schema import (
    LoincDanglingNlpEdges,
    LoincTreeEdges,
    LoincTreeProps,
)
from loinclib.nlp_taxonomification import parts_to_tsv


class Index:

    def __init__(self):
        self.property_by_key: t.Dict[str, Property] = {}
        self.property_by_name_key: t.Dict[str, t.Dict[str, Property]] = {}
        self.property_roots_by_name_key: t.Dict[str, t.Dict[str, Property]] = {}

        self.parts: t.Dict[str, Part] = {}
        self.parts_roots_no_children: t.Dict[str, Part] = {}
        self.parts_roots_with_children: t.Dict[str, Part] = {}
        self.parts_roots_no_children_by_type: t.Dict[str, t.Dict[str, Part]] = {}
        self.search_parts: t.Dict[str, Part] = {}
        self.parts_multiple_prop_names: t.Dict[str, Part] = {}
        self.inferred_props = {}

        self.used_after_not_used: t.Dict[str, t.Dict[str, Property]] = {}
        self.not_used_before_used: t.Dict[str, t.Dict[str, Property]] = {}
        self.by_child_desc_count: t.Dict[str, t.Dict[str, Property]] = {}

        self.component_to_systems: t.Dict[str, t.Dict[str, Property]] = {}
        self.joint_comp_count: int
        self.joint_sys_count: int


class Grouper:

    def __init__(self, index: Index):
        self.index = index

        self.use_abstract_by_name: t.Dict[str, t.Dict[str, Property]] = {}
        self.use_after_abstract_by_name: t.Dict[str, t.Dict[str, Property]] = {}
        self.indent = " "

        self.related_use_index: t.Dict[str, t.Dict[Property, t.Dict[str, set]]] = {}

    def process_property(self, property_names: list):

        for name in property_names:
            root_props = self.index.property_roots_by_name_key[name]
            for property_key, _property in root_props.items():
                self._build_path(_property, list())
                self.find_by_count_averages(_property, set())

        # print("debug")

    def _build_path(self, _property: Property, path: list[Property]):
        # print("in _build_path")
        if _property in path:
            self.process_path(path)
            return
        path.append(_property)
        if len(_property.child_prop_use_by_key) == 0:
            self.process_path(path)
        else:
            for child_prop in _property.child_prop_use_by_key.values():
                self._build_path(child_prop, path)
        del path[-1]

    def process_path(self, path: t.List[Property]):

        (used_after_not_used, not_used_before_used) = self.find_used_after_unused(path)

        for p in used_after_not_used:
            name = p.get_simple_property_name()
            self.index.used_after_not_used.setdefault(name, {})[p.get_key()] = p

        for p in not_used_before_used:
            name = p.get_simple_property_name()
            self.index.not_used_before_used.setdefault(name, {})[p.get_key()] = p

        # print("debug")

    def find_used_after_unused(
        self, path: list[Property]
    ) -> t.Tuple[list[Property], list[Property]]:
        used_after_not_used: list[Property] = []
        not_used_before_used: list[Property] = []
        last_property: t.Optional[Property] = None
        for _property in path:
            if (
                last_property is not None
                and last_property.count == 0
                and _property.count > 0
            ):
                used_after_not_used.append(_property)
                not_used_before_used.append(last_property)
            last_property = _property
        return (used_after_not_used, not_used_before_used)

    def find_by_count_averages(self, _property: Property, seen: set):
        if _property in seen:
            print("CYCLE ============= in find_by_count_averages")
            return
        seen.add(_property)
        # print("in find_by_count_averages")
        descendants_count = _property.get_descendants_count(set())
        children_count = len(_property.child_prop_use_by_key)
        if children_count == 0:
            return

        average = descendants_count / children_count
        for child in _property.child_prop_use_by_key.values():
            child_desc_count = child.get_descendants_count(set())
            if child_desc_count > average * 2:
                name = child.get_simple_property_name()
                self.index.by_child_desc_count.setdefault(name, {})[
                    child.get_key()
                ] = child
            self.find_by_count_averages(child, seen)

    def comp_to_systems(self):
        components = dict(self.index.not_used_before_used["COMPONENT"])
        components.update(self.index.by_child_desc_count["COMPONENT"])

        comp_count = 0
        sys_count = 0

        for comp_key, comp in components.items():
            comp_count += 1
            systems_map = comp.get_comp_related_systems_up(set())
            self.index.component_to_systems.setdefault(comp_key, {}).update(systems_map)

            sys_count += len(systems_map)

        self.index.joint_comp_count = comp_count
        self.index.joint_sys_count = sys_count


class GroupsBuilderSteps:
    def __init__(
        self,
        config: ll.Configuration,
    ):

        self.pickle_path: t.Optional[Path] = None
        self.config = config
        self.runtime: cl.Runtime = t.Optional[cl.Runtime]
        self.index: t.Optional[Index] = None

        self.primary = False
        self.pickle: t.Optional[bool] = False

        self.start_time = time.time()

    def setup_builder(self, builder):
        sys.setrecursionlimit(5000000)
        builder.cli.command(
            "groups-index-props",
            help="Indexes the use of LOINC properties by property and part.",
        )(self.__main)

    def __main(
        self,
        supplementary: t.Annotated[
            bool, typer.Option("--supl", help="Use primary vs supplementary.")
        ] = False,
        _pickle: t.Annotated[
            bool, typer.Option("--pickle", help="Use primary vs supplementary.")
        ] = False,
    ):
        self.pickle = _pickle
        self.primary = not supplementary

        if self.pickle:
            self.do_pickle_read()

        if self.index is None:
            self.index = Index()
            self.do_index()
            self.do_groups()

        # Save dangling parts for NLP semantic similarity pipeline
        dangling: t.List[Part] = list(self.index.parts_roots_no_children.values())
        parts_to_tsv(dangling)

        self.do_abstracts2()

        if self.pickle:
            self.do_pickle_write()

    def do_abstracts2(self):

        components = self.index.property_by_name_key.get("COMPONENT", {})

        _more_than = {}
        _more_than_components = set()
        _more_than_systems = set()
        _more_than_pairs: t.List[t.Tuple[Property, Property]] = []

        for c in components.values():
            for ac in c.abstract_to_more_than_count(10, set()).values():
                _more_than_components.add(ac)
                for s in c.related_properties_by_name_key.get("SYSTEM", {}).values():
                    for _as in s.abstract_to_more_than_count(1, set()).values():
                        _more_than.setdefault(ac, set()).add(_as)
                        _more_than_systems.add(_as)

        seen = set()
        for c in _more_than_components:
            closure = c.parent_closure(set())
            seen.update(closure.values())
        _more_than_components = seen

        seen = set()
        for s in _more_than_systems:
            closure = s.parent_closure(set())
            seen.update(closure.values())
        _more_than_systems = seen

        for c, s_set in _more_than.items():
            for s in s_set:
                _more_than_pairs.append((c, s))

        # component groups
        cl.cli.comploinc_cli_object.builder_cli.set_current_module("group_components")
        module: Module = self.runtime.current_module
        for c in _more_than_components:
            loinc_term: LoincTerm = module.getsert_entity(
                entity_id=f"{ComploincNodeType.group_node.value.id_prefix}:group/component/{c.part_number}",
                entity_class=LoincTerm,
            )
            loinc_term.entity_label = f"GRP_CMP {c.part_node.part_display}"
            loinc_term.primary_component = LoincPartId(f"{LoincNodeType.LoincPart.value.id_prefix}:{c.part_number}")

        cl.cli.comploinc_cli_object.loinc_builders.load_schema(
            filename="comp_loinc.yaml",
            equivalent_term=True,
            reload=True,
            single_property=True,
        )
        cl.cli.comploinc_cli_object.loinc_builders.save_to_owl()

        # systems groups
        cl.cli.comploinc_cli_object.builder_cli.set_current_module("group_systems")
        module: Module = self.runtime.current_module
        for s in _more_than_systems:
            loinc_term: LoincTerm = module.getsert_entity(
                entity_id=f"{ComploincNodeType.group_node.value.id_prefix}:group/system/{s.part_number}",
                entity_class=LoincTerm,
            )
            loinc_term.entity_label = f"GRP_SYS {s.part_node.part_display}"
            loinc_term.primary_system = LoincPartId(f"{LoincNodeType.LoincPart.value.id_prefix}:{s.part_number}")

        cl.cli.comploinc_cli_object.loinc_builders.load_schema(
            filename="comp_loinc.yaml",
            equivalent_term=True,
            reload=True,
            single_property=True,
        )
        cl.cli.comploinc_cli_object.loinc_builders.save_to_owl()

        # component/systems groups
        cl.cli.comploinc_cli_object.builder_cli.set_current_module(
            "group_components_systems"
        )
        module: Module = self.runtime.current_module
        for c, s in _more_than_pairs:
            loinc_term: LoincTerm = module.getsert_entity(
                entity_id=f"{ComploincNodeType.group_node.value.id_prefix}:group/component-system/{c.part_number}-{s.part_number}",
                entity_class=LoincTerm,
            )
            loinc_term.entity_label = f"GRP_CMP_SYS {c.part_node.part_display}  ||  {s.part_node.part_display}"
            loinc_term.primary_component = LoincPartId(f"{LoincNodeType.LoincPart.value.id_prefix}:{c.part_number}")
            loinc_term.primary_system = LoincPartId(f"{LoincNodeType.LoincPart.value.id_prefix}:{s.part_number}")

        cl.cli.comploinc_cli_object.loinc_builders.load_schema(
            filename="comp_loinc.yaml", equivalent_term=True, reload=True
        )
        cl.cli.comploinc_cli_object.loinc_builders.save_to_owl()

        # print("debug")

    def do_abstracts(self):
        components = dict(self.index.used_after_not_used["COMPONENT"])
        components.update(self.index.by_child_desc_count["COMPONENT"])
        components_2 = {c.get_key(): c for c in components.values() if c.count > 0}

        #
        cc: t.Optional[Property] = None
        ac: t.Optional[Property] = None
        cs: t.Optional[Property] = None
        _as: t.Optional[Property] = None

        # both abstract
        abstracted: t.Dict[Property, t.Set[Property]] = {}
        for cc in components_2.values():
            for ac in cc.get_abstracted(2, set()).values():
                for cs in cc.related_properties_by_name_key.get("SYSTEM", {}).values():
                    for _as in cs.get_abstracted(2, set()).values():
                        abstracted.setdefault(ac, set()).add(_as)

        abstract_pairs: t.List[t.Tuple[Property, Property]] = []
        for component, systems in abstracted.items():
            for _system in systems:
                abstract_pairs.append((component, _system))

        # more than counts
        _more_than_components = set()
        _more_than_systems = set()
        _more_than = {}
        _more_than_pairs: t.List[t.Tuple[Property, Property]] = []
        for cc in components_2.values():
            for cc_more in cc.abstract_to_more_than_count(10, set()).values():
                for cs in cc.related_properties_by_name_key.get("SYSTEM", {}).values():
                    for cs_more in cs.abstract_to_more_than_count(1, set()).values():
                        _more_than.setdefault(cc_more, set()).add(cs_more)

        for c, s_set in _more_than.items():
            _more_than_components.add(c)
            for s in s_set:
                _more_than_systems.add(s)
                _more_than_pairs.append((c, s))

        # component abstract, system concrete
        c_abstracted: t.Dict[str, t.Set[Property]] = {}
        for cc in components_2.values():
            top_concretes = cc.get_top_concrete(3, set()).values()
            for ac in top_concretes:
                for cs in cc.related_properties_by_name_key.get("SYSTEM", {}).values():
                    c_abstracted.setdefault(ac.get_key(), set()).add(cs)

        c_abstract_pairs: t.List[t.Tuple[Property, Property]] = []
        for component_key, systems in c_abstracted.items():
            for _system in systems:
                c_abstract_pairs.append(
                    (self.index.property_by_key[component_key], _system)
                )

        # both concrete
        concretes: t.Dict[str, t.Set[Property]] = {}
        for cc in components_2.values():
            for cs in cc.related_properties_by_name_key.get("SYSTEM", {}).values():
                concretes.setdefault(cc.get_key(), set()).add(cs)

        concrete_pairs: t.List[t.Tuple[Property, Property]] = []
        for cc_key, systems in concretes.items():
            for _system in systems:
                concrete_pairs.append((self.index.property_by_key[cc_key], _system))

        # print("debug")

    def do_groups(self):

        grouper = Grouper(self.index)
        grouper.process_property(["COMPONENT", "SYSTEM"])
        grouper.comp_to_systems()

    def do_pickle_read(self):
        if self.primary:
            self.pickle_path = self.config.home_path / "tmp/primary.pkl"
        else:
            self.pickle_path = self.config.home_path / "tmp/suppl.pkl"
        if self.pickle_path.exists():
            with open(self.pickle_path, "rb") as f:
                self.index = pickle.load(f)

    def do_pickle_write(self):
        pickle_dir = os.path.dirname(self.pickle_path)
        if not os.path.exists(pickle_dir):
            os.makedirs(pickle_dir)
        with open(self.pickle_path, "wb") as f:
            try:
                # pickle.dump(self.index, f)
                # noinspection PyTypeChecker
                Pickler(file=f).dump(self.index)
            except Exception as exc:
                print("Got pickling error: {0}".format(exc))
        print(f"Finished pickling...")

    def do_index_load_graph(self):
        print(f"loading graph: {(time.time() - self.start_time) / 60}")
        loinc_loader = ll.loinc_loader.LoincLoader(
            graph=self.runtime.graph, configuration=self.config
        )
        loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
        loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()  # for search tags even if doing primary
        loinc_loader.load_accessory_files__part_file__part_csv()
        loinc_loader.load_loinc_table__loinc_csv()
        loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

        loinc_tree_loader = LoincTreeLoader(
            config=self.config, graph=self.runtime.graph
        )
        loinc_tree_loader.load_all_trees()

    def do_index_parts_tree(self):
        print(f"parts tree: {(time.time() - self.start_time) / 60}")
        parts: t.Iterator[ll.Node] = self.runtime.graph.get_nodes(
            LoincNodeType.LoincPart
        )
        for part in parts:
            part_number = part.get_property(LoincPartProps.part_number)
            # part_name = part.get_property(LoincPartProps.part_name)
            part_display_name = part.get_property(LoincPartProps.part_display_name)
            part_type_name = part.get_property(LoincPartProps.part_type_name)
            part_tree_text = part.get_property(LoincTreeProps.code_text)

            child_part_node = self.index.parts.setdefault(
                part_number, Part(part_number=part_number)
            )
            child_part_node.part_display = (
                part_display_name
                if part_display_name is not None
                else f"TREE: {part_tree_text}"
            )
            child_part_node.part_type = part_type_name
            child_part_node.part_graph_id = part.node_id

            out_edges = list(part.get_all_out_edges())
            edge: ll.Edge
            for edge in out_edges:
                parent_part_number = edge.to_node.get_property(
                    LoincPartProps.part_number
                )
                parent_part_node = self.index.parts.setdefault(
                    parent_part_number, Part(part_number=parent_part_number)
                )
                match edge.handler.type_:
                    case LoincTreeEdges.tree_parent:
                        child_part_node.parents[parent_part_number] = parent_part_node
                        parent_part_node.children[part_number] = child_part_node
                    case LoincDanglingNlpEdges.nlp_parent:
                        child_part_node.parents[parent_part_number] = parent_part_node
                        parent_part_node.children[part_number] = child_part_node
                    case LoincPartEdge.parent_comp_by_system:
                        child_part_node.parents[parent_part_number] = parent_part_node
                        parent_part_node.children[part_number] = child_part_node

    def do_index_part_roots(self):
        print("parts roots")
        print(f"parts roots: {(time.time() - self.start_time) / 60}")
        for part_node in self.index.parts.values():
            if len(part_node.parents) == 0:
                if len(part_node.children) > 0:
                    self.index.parts_roots_with_children[part_node.part_number] = (
                        part_node
                    )
                else:
                    self.index.parts_roots_no_children[part_node.part_number] = (
                        part_node
                    )
                    self.index.parts_roots_no_children_by_type.setdefault(
                        part_node.part_type, {}
                    )[part_node.part_number] = part_node

    def do_index_property_use(self):
        print("property use")
        print(f"property use: {(time.time() - self.start_time) / 60}")
        term_count: int = 0
        # parse loinc term phrases
        loinc_term_nodes = self.runtime.graph.get_nodes(LoincNodeType.LoincTerm)
        for term_node in loinc_term_nodes:
            # status = term_node.get_property(LoincTermProps.status)
            # if status != "ACTIVE":
            #   continue

            edges = term_node.get_all_out_edges()

            term_properties: dict[str, Property] = {}

            for edge in edges:
                edge_type = edge.handler.type_

                if edge_type is LoincTermSupplementaryEdges.supplementary_search:
                    search_part_number = edge.to_node.get_property(
                        LoincPartProps.part_number
                    )
                    self.index.parts[search_part_number].is_search = True
                    self.index.search_parts[search_part_number] = self.index.parts[
                        search_part_number
                    ]
                    continue

                if self.primary and not isinstance(edge_type, LoincTermPrimaryEdges):
                    continue

                if not self.primary and not isinstance(
                    edge_type, LoincTermSupplementaryEdges
                ):
                    continue

                part_number = edge.to_node.get_property(
                    type_=LoincPartProps.part_number
                )

                part_name = edge.to_node.get_property(type_=LoincPartProps.part_name)
                if part_number is None:
                    continue
                _property = Property(
                    part_number=part_number, part_name=part_name, prop_type=edge_type
                )
                related_key = _property.get_key()
                _property = self.index.property_by_key.setdefault(
                    related_key, _property
                )
                _property.count += 1
                term_properties[related_key] = _property
                simple_property_name = _property.get_simple_property_name()

                part_node = self.index.parts[part_number]
                _property.part_node = part_node
                part_node.property_by_key[related_key] = _property
                part_node.property_by_name_key.setdefault(simple_property_name, {})[
                    related_key
                ] = _property

                self.index.property_by_name_key.setdefault(simple_property_name, {})[
                    related_key
                ] = _property

            # assert related properties per term
            for relating_key, relating_property in term_properties.items():
                for related_key, related_property in term_properties.items():
                    if related_key == relating_key:
                        continue
                    relating_property.related_properties_by_key[related_key] = (
                        related_property
                    )
                    relating_property.related_properties_by_name_key.setdefault(
                        related_property.get_simple_property_name(), {}
                    )[related_key] = related_property

            term_count += 1
            if term_count % 1000 == 0:
                print(f"TC: {term_count}")

    def do_index_check_property_part_overloads(self):
        print("property part overloads")
        print(f"property part overload: {(time.time() - self.start_time) / 60}")
        for part_number, part in self.index.parts.items():
            if len(part.property_by_name_key) > 1:
                self.index.parts_multiple_prop_names[part_number] = part

    def do_index_infer_parent_properties(self):
        d = dict(self.index.property_by_key)
        for property_key, _property in d.items():
            if property_key in self.index.parts_roots_no_children:
                continue
            self._infer_parent_properties(_property, self.index.inferred_props)

        for property_key, _property in self.index.property_by_key.items():
            if (
                len(_property.parent_prop_use_by_key) == 0
                and len(_property.child_prop_use_by_key) > 0
            ):
                self.index.property_roots_by_name_key.setdefault(
                    _property.get_simple_property_name(), {}
                )[property_key] = _property

    def do_index_property_depths(self):
        print("property depths")
        print(f"property depths: {(time.time() - self.start_time) / 60}")
        # first set depths
        for property_name, properties in self.index.property_roots_by_name_key.items():
            for _property in properties.values():
                self._do_property_depths(_property, 1, list())

        print("property depth percentage")
        print(f"property depth percentage: {(time.time() - self.start_time) / 60}")
        # set percentages
        for property_name, properties in self.index.property_roots_by_name_key.items():
            for _property in properties.values():
                self._do_property_depths_percentage(_property, list())

    def _do_property_depths(
        self, _property: Property, depth: int, path: t.List[Property]
    ):
        if _property in path:
            return
        path.append(_property)
        if _property.depth is None:
            _property.depth = depth
        else:
            if _property.depth < depth:  # keep longest as opposed to shortest
                _property.depth = depth
        for child_property in _property.child_prop_use_by_key.values():
            self._do_property_depths(child_property, depth + 1, path)
        del path[-1]

    def _do_property_depths_percentage(
        self, _property: Property, path: t.List[Property]
    ):
        if _property in path:
            return
        path.append(_property)
        if len(_property.child_prop_use_by_key) == 0:
            self._do_property_depths_percentage_set(path)

        for child_property in _property.child_prop_use_by_key.values():
            self._do_property_depths_percentage(child_property, path)

        del path[-1]

    def _do_property_depths_percentage_set(self, path: t.List[Property]):
        path_length = len(path)
        for _property in path:
            percentage: float = _property.depth / path_length
            if _property.depth_percentage is None:
                _property.depth_percentage = percentage
            else:
                if _property.depth_percentage > percentage:
                    _property.depth_percentage = percentage

    def do_index(self):

        self.do_index_load_graph()
        self.do_index_parts_tree()
        self.do_index_part_roots()
        self.do_index_property_use()
        self.do_index_infer_parent_properties()
        self.do_index_check_property_part_overloads()
        self.do_index_property_depths()

        print("Done indexing")

    def _infer_parent_properties(
        self, _property: Property, inferred_props: t.Dict[str, Property]
    ) -> None:
        property_key = _property.get_key()
        if property_key in inferred_props:
            return

        inferred_props[property_key] = _property

        for parent_part in _property.part_node.parents.values():
            parent_property = Property(
                part_number=parent_part.part_number,
                part_name=parent_part.part_display,
                prop_type=_property.prop_type,
            )
            parent_property_key = parent_property.get_key()
            parent_property = parent_part.property_by_key.setdefault(
                parent_property_key, parent_property
            )
            self.index.property_by_key[parent_property_key] = parent_property

            parent_property.part_node = parent_part
            # parent_part.property_by_key[parent_property_key] = parent_property

            _property.parent_prop_use_by_key[parent_property_key] = parent_property
            parent_property.child_prop_use_by_key[property_key] = _property

            self._infer_parent_properties(parent_property, inferred_props)
