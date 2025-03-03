import pickle
import sys
import time
import typing as t
from pathlib import Path
from pickle import Pickler

import typer

import comp_loinc as cl
import loinclib as ll
from comp_loinc.groups.property_use import Property, Part
from loinclib.loinc_schema import (
    LoincNodeType,
    LoincTermPrimaryEdges,
    LoincPartProps,
    LoincPartEdge,
    LoincTermSupplementaryEdges,
)
from loinclib.loinc_tree_loader import LoincTreeLoader
from loinclib.loinc_tree_schema import LoincDanglingNlpEdges, LoincTreeEdges, LoincTreeProps


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


class Grouper:

    def __init__(self, index: Index):
        self.index = index

        self.use_abstract_by_name: t.Dict[str, t.Dict[str, Property]] = {}
        self.use_after_abstract_by_name: t.Dict[str, t.Dict[str, Property]] = {}
        self.indent = " "

        self.related_use_index: t.Dict[str, t.Dict[Property, t.Dict[str, set]]] = {}

    def process_property(self, property_name: str):
        root_props = self.index.property_roots_by_name_key[property_name]

        for property_key, _property in root_props.items():
            self._build_path(_property, list())

    def _build_path(self, _property: Property, path: list[Property]):
        if _property in path or len(_property.child_prop_use_by_key) == 0:
            self.process_path(path)
            return
        path.append(_property)
        for child_prop in _property.child_prop_use_by_key.values():
            self._build_path(child_prop, path)
        del path[-1]

    def process_path(self, path: t.List[Property]):
        (used_after_not_used, not_used_before_used) = self.find_used_after_unused(path)

        print("debug")

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

    def do_use_abstract_by_name(self, index: Index):
        part: Part
        stack = list()
        for part_key, part in index.parts_roots_with_children.items():
            for use_key, use in part.property_by_key.items():
                self._do_use_abstract_by_name(use, 0, stack)

    def _do_use_abstract_by_name(
        self, use: Property, depth: int, stack: t.List[Property]
    ):
        if use in stack:
            print(f'{"".join(self.indent * depth)}: {str(use)}')
            print(f'{"".join(self.indent * depth)}: ++++++++++++ CYCLE  ++++++  ')
            print(str(stack))
            print(f"At index: {stack.index(use)}  with: {use}")
            return

        print(f'{"".join(self.indent * depth)}: {str(use)}')
        if use.count == 0:
            print(f'{"".join(self.indent * depth)}: ===============  ')
            name = use.get_simple_property_name()
            uses = self.use_abstract_by_name.setdefault(name, {})
            uses[use.get_key()] = use
        if len(stack) > 0:
            tmp = stack[-1]
            if tmp.count == 0 and use.count > 0:
                name = use.get_simple_property_name()
                uses = self.use_after_abstract_by_name.setdefault(name, {})
                uses[use.get_key()] = use
        stack.append(use)
        for child_use in use.child_prop_use_by_key.values():
            self._do_use_abstract_by_name(child_use, depth + 1, stack)
        del stack[-1]

        # print(f'Finished abstract uses count with dict: ' + str(self.use_abstract_by_name))


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

    def do_groups(self):
        grouper = Grouper(self.index)
        grouper.process_property("COMPONENT")
        # grouper.do_use_abstract_by_name(self.index)
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
        sys.setrecursionlimit(5000000)
        builder.cli.command(
            "groups-index-props",
            help="Indexes the use of LOINC properties by property and part.",
        )(self.index_prop_use)

    def index_prop_use(
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

        if self.pickle:
            self.do_pickle_write()

        self.do_groups()

    def do_pickle_read(self):
        if self.primary:
            self.pickle_path = self.config.home_path / "tmp/primary.pkl"
        else:
            self.pickle_path = self.config.home_path / "tmp/suppl.pkl"
        if self.pickle_path.exists():
            with open(self.pickle_path, "rb") as f:
                self.index = pickle.load(f)

    def do_pickle_write(self):
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
            part_name = part.get_property(LoincPartProps.part_name)
            part_type_name = part.get_property(LoincPartProps.part_type_name)
            part_tree_text = part.get_property(LoincTreeProps.code_text)

            part.get_property(LoincPartProps.part_name)
            child_part_node = self.index.parts.setdefault(
                part_number, Part(part_number=part_number)
            )
            child_part_node.part_display = (
                part_name if part_name is not None else f"TREE: {part_tree_text}"
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
                match edge.edge_type.type_:
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
                edge_type = edge.edge_type.type_

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
            print(f"TC: {term_count}")

    def do_index_check_property_part_overloads(self):
        print("property part overloads")
        print(f"property part overload: {(time.time() - self.start_time) / 60}")
        for part_number, part in self.index.parts.items():
            if len(part.property_by_name_key) > 1:
                self.index.parts_multiple_prop_names[part_number] = part

    def do_index_infer_parent_properties(self):
        for property_key, _property in self.index.property_by_key.items():
            if property_key in self.index.parts_roots_no_children:
                continue
            self._infer_parent_properties(_property, self.index.inferred_props)

        for property_key, _property in self.index.property_by_key.items():
            if len(_property.parent_prop_use_by_key) == 0:
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

            parent_property.part_node = parent_part
            # parent_part.property_by_key[parent_property_key] = parent_property

            _property.parent_prop_use_by_key[parent_property_key] = parent_property
            parent_property.child_prop_use_by_key[property_key] = _property

            self._infer_parent_properties(parent_property, inferred_props)
