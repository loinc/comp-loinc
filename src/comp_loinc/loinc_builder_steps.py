import typing as t
from pathlib import Path

import funowl
import typer
from linkml_owl.dumpers.owl_dumper import OWLDumper
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition, Annotation

from comp_loinc import Runtime
from comp_loinc.datamodel import LoincPart, LoincPartId
from comp_loinc.datamodel.comp_loinc import LoincTerm, SnomedConcept
from loinclib import Configuration, SnomedEdges, Node, SnomedProperteis, Edge
from loinclib import LoincLoader
from loinclib import LoincNodeType, LoincTermProps
from loinclib.loinc_schema import LoincPartProps, LoincPartEdge, LoincTermPrimaryEdges, LoincTermSupplementaryEdges
from loinclib.loinc_snomed_loader import LoincSnomedLoader
from loinclib.loinc_tree_loader import LoincTreeLoader
from loinclib.loinc_tree_schema import LoincTreeProps


class LoincBuilderSteps:

  def __init__(self, *,
      configuration: Configuration):
    self.configuration = configuration
    self.runtime: t.Optional[Runtime] = None

  def setup_builder(self, builder):

    builder.cli.command('lt-inst-all', help='Instantiate all LOINC terms into current module.')(
        self.loinc_terms_all)

    builder.cli.command('lt-parent', help='Make LOINC terms a child of a grouper LoincTerm class.')(
        self.loinc_terms_root_parent)

    builder.cli.command('lt-primary-def',
                        help='Populate primary def slots.')(self.loinc_term_primary_def)

    builder.cli.command('lt-supplementary-def',
                        help='Populate supplementary def slots.')(self.loinc_term_supplementary_def)

    builder.cli.command('lp-inst-all', help='Instantiate all LOINC parts into current module.')(
        self.loinc_parts_all)

    builder.cli.command('lp-parent', help='Make LOINC parts a child of a grouper LoincPart class.')(
        self.loinc_parts_root_parent)

    builder.cli.command('lp-sct-equiv',
                        help='Asserts LOINC part to SNOMED equivalence axioms for all available mappings..')(
        self.loinc_part_to_snomed_quivalence)

    builder.cli.command('lp-part-hierarchy-all',
                        help='Asserts part hierarchy for all parts based on component hierarchy file.')(
        self.loinc_part_hierarchy_all)

    # builder.cli.command('lp-part-tree-hierarchy-all',
    #                     help='Asserts part hierarchy for all parts based on tree files.')(
    #     self.part_tree_hierarchy_all)

    builder.cli.command('l-label', help='Add rdfs:label to current entities.')(self.entity_labels)
    builder.cli.command('l-annotate', help='Add annotations to current entities.')(self.entity_annotations)

    builder.cli.command('load-schema', help='Loads a LinkML schema file and gives it a name. '
                                            'It also makes it the "current" schema to operate on with schema related builder steps.')(
        self.load_schema)
    builder.cli.command('save-owl', help='Saves the current module to an owl file.')(self.save_to_owl)

  def loinc_terms_all(self,
      active_only: t.Annotated[
        bool, typer.Option('--active', help='Use active concepts only. Defaults to true.')] = False,
  ):
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_loinc_table__loinc_csv()
    count = 0
    for node in self.runtime.graph.get_nodes(LoincNodeType.LoincTerm):
      count = count + 1
      if self.configuration.fast_run and count > 100:
        break

      status = node.get_property(LoincTermProps.status)
      if active_only and status != 'ACTIVE':
        continue

      loinc_number = node.get_property(LoincTermProps.loinc_number)

      # add if not already instantiated, to not override an existing one
      if self.runtime.current_module.get_entity(loinc_number, LoincTerm) is None:
        loinc_term = LoincTerm(id=loinc_number)
        self.runtime.current_module.add_entity(loinc_term)

  def loinc_parts_all(self,
      active_only: t.Annotated[
        bool, typer.Option('--active', help='Use active concepts only. Defaults to true.')] = False,
  ):
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_accessory_files__part_file__part_csv()
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    loinc_tree_loader = LoincTreeLoader(config=self.configuration, graph=graph)
    loinc_tree_loader.load_class_tree()
    loinc_tree_loader.load_component_tree()
    loinc_tree_loader.load_component_by_system_tree()
    loinc_tree_loader.load_panel_tree()
    loinc_tree_loader.load_system_tree()
    loinc_tree_loader.load_method_tree()
    loinc_tree_loader.load_document_tree()

    count = 0
    for node in self.runtime.graph.get_nodes(LoincNodeType.LoincPart):
      count = count + 1
      if self.configuration.fast_run and count > 100:
        break
      status = node.get_property(LoincPartProps.status)
      if active_only and status != 'ACTIVE':
        continue

      number = node.get_property(LoincPartProps.part_number)

      # add if not already instantiated, to not override an existing one
      if self.runtime.current_module.get_entity(number, LoincPart) is None:
        part = LoincPart(id=number)
        self.runtime.current_module.add_entity(part)

  def entity_labels(self):
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_loinc_table__loinc_csv()
    loinc_loader.load_accessory_files__part_file__part_csv()
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

    loinc_tree_loader = LoincTreeLoader(config=self.configuration, graph=graph)
    loinc_tree_loader.load_class_tree()
    loinc_tree_loader.load_component_tree()
    loinc_tree_loader.load_component_by_system_tree()
    loinc_tree_loader.load_panel_tree()
    loinc_tree_loader.load_system_tree()
    loinc_tree_loader.load_method_tree()
    loinc_tree_loader.load_document_tree()

    loinc_term: LoincTerm
    for loinc_term in self.runtime.current_module.get_entities_of_type(LoincTerm):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code=loinc_term.id)
      if node is None:
        continue
      long_name = node.get_property(LoincTermProps.long_common_name)
      class_ = node.get_property(LoincTermProps.class_)
      loinc_term.entity_label = f'LT   {class_}   {long_name}'

    loinc_part: LoincPart
    for loinc_part in self.runtime.current_module.get_entities_of_type(LoincPart):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincPart, code=loinc_part.id)
      if node is None:
        continue

      final_name = node.get_property(LoincPartProps.part_display_name)
      if final_name is None:
        final_name = node.get_property(LoincPartProps.code_text__from_comp_hierarch)
      if final_name is None:
        final_name = node.get_property(LoincTreeProps.code_text)
      if final_name is None:
        final_name = f'NONAME:{loinc_part.id}'
      part_type_name = node.get_property(LoincPartProps.part_type_name)
      if part_type_name is None:
        part_type_name = f'NOTYPENAME'

      prefix = 'LP'
      if node.get_property(LoincPartProps.from_hierarchy):
        prefix = 'LHP'
      if node.get_property(LoincTreeProps.from_trees):
        prefix = 'LTP'

      loinc_part.entity_label = f'{prefix}   {part_type_name}   {final_name}'

  def entity_annotations(self):
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_loinc_table__loinc_csv()
    loinc_loader.load_accessory_files__part_file__part_csv()
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()

    loinc_tree_loader = LoincTreeLoader(config=self.configuration, graph=graph)
    loinc_tree_loader.load_class_tree()
    loinc_tree_loader.load_component_tree()
    loinc_tree_loader.load_component_by_system_tree()
    loinc_tree_loader.load_panel_tree()
    loinc_tree_loader.load_system_tree()
    loinc_tree_loader.load_method_tree()
    loinc_tree_loader.load_document_tree()

    loinc_term: LoincTerm
    for loinc_term in self.runtime.current_module.get_entities_of_type(LoincTerm):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code=loinc_term.id)
      if node is None:
        continue
      number = node.get_property(LoincTermProps.loinc_number)
      long_name = node.get_property(LoincTermProps.long_common_name)
      class_type = node.get_property(LoincTermProps.class_type)
      class_ = node.get_property(LoincTermProps.class_)

      loinc_term.long_common_name = long_name
      loinc_term.loinc_number = number
      loinc_term.loinc_class = class_
      loinc_term.loinc_class_type = class_type

    loinc_part: LoincPart
    for loinc_part in self.runtime.current_module.get_entities_of_type(LoincPart):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincPart, code=loinc_part.id)
      if node is None:
        continue

      part_number = node.get_property(LoincPartProps.part_number)
      part_name = node.get_property(LoincPartProps.part_name)
      part_type = node.get_property(LoincPartProps.part_type_name)
      part_display = node.get_property(LoincPartProps.part_display_name)

      loinc_part.part_number = part_number
      loinc_part.part_name = part_name
      loinc_part.part_type_name = part_type
      loinc_part.part_display_name = part_display

  def loinc_terms_root_parent(self):
    term: LoincTerm
    loinc_term_parent = self.runtime.current_module.get_entity(entity_class=LoincTerm, entity_id='LoincTerm')
    if loinc_term_parent is None:
      loinc_term_parent = LoincTerm(id='LoincTerm')
      self.runtime.current_module.add_entity(loinc_term_parent)
    for term in self.runtime.current_module.get_entities_of_type(entity_class=LoincTerm):
      if term == loinc_term_parent:
        continue
      if not term.sub_class_of:
        term.sub_class_of.append(loinc_term_parent)

  def loinc_parts_root_parent(self):
    loinc_part_parent = self.runtime.current_module.get_entity(entity_class=LoincPart, entity_id='LoincPart')
    if loinc_part_parent is None:
      loinc_part_parent = LoincPart(id='LoincPart')
      self.runtime.current_module.add_entity(loinc_part_parent)

    example = self.runtime.current_module.get_entity(entity_class=LoincPart, entity_id='LP20608-3')

    part: LoincPart
    for part in self.runtime.current_module.get_entities_of_type(entity_class=LoincPart):
      if part == loinc_part_parent:
        continue

      if len(part.sub_class_of) == 0 :
        part.sub_class_of.append(loinc_part_parent)

  def loinc_part_to_snomed_quivalence(self):
    graph = self.runtime.graph
    loader = LoincSnomedLoader(config=self.configuration, graph=self.runtime.graph)
    loader.load_part_mapping()

    part: LoincPart
    part_node: Node
    snomed_concept: SnomedConcept
    snomed_node: Node

    for part_node in graph.get_nodes(type_=LoincNodeType.LoincPart):
      for edge in part_node.get_all_out_edges():
        if edge.edge_type.type_ is SnomedEdges.maps_to:
          snomed_node: Node = edge.to_node

          part_id = part_node.get_property(type_=LoincPartProps.part_number)
          snomed_id = snomed_node.get_property(type_=SnomedProperteis.concept_id)

          part = self.runtime.current_module.get_entity(entity_class=LoincPart, entity_id=part_id)
          if part is None:
            part = LoincPart(id=part_id)
            self.runtime.current_module.add_entity(part)

          snomed_concept = self.runtime.current_module.get_entity(entity_class=SnomedConcept, entity_id=snomed_id)
          if snomed_concept is None:
            snomed_concept = SnomedConcept(id=snomed_id)
            self.runtime.current_module.add_entity(snomed_concept)

          part.equivalent_class.append(snomed_concept.id)

  def loinc_part_hierarchy_all(self):
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_accessory_files__part_file__part_csv()
    loinc_loader.load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    loinc_tree_loader = LoincTreeLoader(config=self.configuration, graph=graph)
    loinc_tree_loader.load_class_tree()
    loinc_tree_loader.load_component_tree()
    loinc_tree_loader.load_component_by_system_tree()
    loinc_tree_loader.load_panel_tree()
    loinc_tree_loader.load_system_tree()
    loinc_tree_loader.load_method_tree()
    loinc_tree_loader.load_document_tree()

    for child_part_node in graph.get_nodes(type_=LoincNodeType.LoincPart):
      child_part_number = child_part_node.get_property(type_=LoincPartProps.part_number)

      child_part = self.runtime.current_module.get_entity(entity_id=child_part_number, entity_class=LoincPart)
      if child_part is None:
        child_part = LoincPart(id=child_part_number)
        self.runtime.current_module.add_entity(child_part)

      edge: Edge
      for edge in child_part_node.get_all_out_edges():
        if edge.edge_type.type_ is LoincPartEdge.parent_comp_by_system:
          parent_part_node = edge.to_node
          parent_part_number = parent_part_node.get_property(type_=LoincPartProps.part_number)

          parent_part = self.runtime.current_module.get_entity(entity_id=parent_part_number, entity_class=LoincPart)
          if parent_part is None:
            parent_part = LoincPart(id=parent_part_number)
            self.runtime.current_module.add_entity(parent_part)

          if parent_part.id not in child_part.sub_class_of:
            child_part.sub_class_of.append(parent_part.id)

  # def part_tree_hierarchy_all(self):
  #   pass

  def loinc_term_primary_def(self):
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()

    loinc_term: LoincTerm
    for loinc_term in self.runtime.current_module.get_entities_of_type(entity_class=LoincTerm):
      loinc_term_id = loinc_term.id
      loinc_term_node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code=loinc_term_id)
      edge: Edge
      for edge in loinc_term_node.get_all_out_edges():
        edge_type = edge.edge_type.type_
        part_number = edge.to_node.get_property(type_=LoincPartProps.part_number)
        if part_number is None:
          continue
        loinc_part_id = LoincPartId(part_number)

        match edge_type:
          case LoincTermPrimaryEdges.primary_component:
            loinc_term.primary_component = loinc_part_id
          case LoincTermPrimaryEdges.primary_property:
            loinc_term.primary_property = loinc_part_id
          case LoincTermPrimaryEdges.primary_time_aspect:
            loinc_term.primary_time_aspect = loinc_part_id
          case LoincTermPrimaryEdges.primary_system:
            loinc_term.primary_system = loinc_part_id
          case LoincTermPrimaryEdges.primary_scale_type:
            loinc_term.primary_scale_typ = loinc_part_id
          case LoincTermPrimaryEdges.primary_method_type:
            loinc_term.primary_method_typ = loinc_part_id

          case LoincTermPrimaryEdges.primary_document_kind:
            loinc_term.primary_document_kind = loinc_part_id
          case LoincTermPrimaryEdges.primary_document_role:
            loinc_term.primary_document_role = loinc_part_id
          case LoincTermPrimaryEdges.primary_document_subject_matter_domain:
            loinc_term.primary_document_subject_matter_domain = loinc_part_id
          case LoincTermPrimaryEdges.primary_document_type_of_service:
            loinc_term.primary_document_type_of_service = loinc_part_id

          case LoincTermPrimaryEdges.primary_rad_anatomic_location_imaging_focus:
            loinc_term.primary_rad_anatomic_location_imaging_focus = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_anatomic_location_laterality:
            loinc_term.primary_rad_anatomic_location_laterality = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_anatomic_location_laterality_presence:
            loinc_term.primary_rad_anatomic_location_laterality_presence = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_anatomic_location_region_imaged:
            loinc_term.primary_rad_anatomic_location_region_imaged = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_guidance_for_action:
            loinc_term.primary_rad_guidance_for_action = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_guidance_for_approach:
            loinc_term.primary_rad_guidance_for_approach = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_guidance_for_object:
            loinc_term.primary_rad_guidance_for_object = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_guidance_for_presence:
            loinc_term.primary_rad_guidance_for_presence = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_maneuver_maneuver_type:
            loinc_term.primary_rad_maneuver_maneuver_type = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_modality_subtype:
            loinc_term.primary_rad_modality_subtype = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_modality_type:
            loinc_term.primary_rad_modality_type = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_pharmaceutical_route:
            loinc_term.primary_rad_pharmaceutical_route = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_pharmaceutical_substance_given:
            loinc_term.primary_rad_pharmaceutical_substance_given = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_reason_for_exam:
            loinc_term.primary_rad_reason_for_exam = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_subject:
            loinc_term.primary_rad_subject = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_timing:
            loinc_term.primary_rad_timing = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_view_aggregation:
            loinc_term.primary_rad_view_aggregation = loinc_part_id
          case LoincTermPrimaryEdges.primary_rad_view_view_type:
            loinc_term.primary_rad_view_view_type = loinc_part_id

  def loinc_term_supplementary_def(self):
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    loinc_term: LoincTerm
    for loinc_term in self.runtime.current_module.get_entities_of_type(entity_class=LoincTerm):
      loinc_term_id = loinc_term.id
      loinc_term_node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code=loinc_term_id)
      edge: Edge
      for edge in loinc_term_node.get_all_out_edges():
        edge_type = edge.edge_type.type_
        part_number = edge.to_node.get_property(type_=LoincPartProps.part_number)
        if part_number is None:
          continue
        loinc_part_id = LoincPartId(part_number)

        match edge_type:
          case LoincTermSupplementaryEdges.supplementary_adjustment:
            loinc_term.supplementary_adjustment = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_analyte:
            loinc_term.supplementary_analyte = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_analyte_core:
            loinc_term.supplementary_analyte_core = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_analyte_divisor:
            loinc_term.supplementary_analyte_divisor = loinc_part_id

          case LoincTermSupplementaryEdges.supplementary_analyte_divisor_suffix:
            loinc_term.supplementary_analyte_divisor_suffix = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_analyte_gene:
            loinc_term.supplementary_analyte_gene = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_analyte_numerator:
            loinc_term.supplementary_analyte_numerator = loinc_part_id

          case LoincTermSupplementaryEdges.supplementary_analyte_suffix:
            loinc_term.supplementary_analyte_suffix = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_category:
            loinc_term.supplementary_category = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_challenge:
            loinc_term.supplementary_challenge = loinc_part_id

          case LoincTermSupplementaryEdges.supplementary_CLASS:
            loinc_term.supplementary_class = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_count:
            loinc_term.supplementary_count = loinc_part_id

          case LoincTermSupplementaryEdges.supplementary_METHOD_TYP:
            loinc_term.supplementary_method_typ = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_PROPERTY:
            loinc_term.supplementary_property = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_SCALE_TYP:
            loinc_term.supplementary_scale_typ = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_search:
            loinc_term.supplementary_search = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_super_system:
            loinc_term.supplementary_super_system = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_system_core:
            loinc_term.supplementary_system_core = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_time_core:
            loinc_term.supplementary_time_core = loinc_part_id
          case LoincTermSupplementaryEdges.supplementary_time_modifier:
            loinc_term.supplementary_time_modifier = loinc_part_id

  def load_schema(self, filename: t.Annotated[str, typer.Option('--file-name', '-f',
                                                                help='The LinkML schema file name in the schema directory. For example: "comp_loinc.yaml"')],
      schema_name: t.Annotated[str, typer.Option('--schema-name', '-n',
                                                 help='A name to hold the loaded schema under. Defaults to the file name without the .yaml suffix')] = None,
      reload: t.Annotated[bool, typer.Option('--reload', '-r',
                                             help='A previously loaded schema under the same name will be reloaded if true.')] = False,
      equivalent_term: t.Annotated[bool, typer.Option('--equivalent-term',
                                                      help='Modifies the LoincTerm OWL annotations from "ObjectSomeValuesFrom" to '
                                                           '"EquivalentClasses, IntersectionOf"')] = False
  ) -> SchemaView:
    typer.echo(f'Running load_linkml_schema')
    schema_view = self.runtime.load_linkml_schema(filename, schema_name, reload)
    if equivalent_term:
      class_def: ClassDefinition = schema_view.get_class(class_name='LoincTerm')
      attribute: SlotDefinition
      for attribute in class_def.attributes.values():
        owl_annotation: Annotation = attribute.annotations.get('owl', None)
        if owl_annotation and 'ObjectSomeValuesFrom' in owl_annotation.value:
          attribute.annotations['owl'] = Annotation(value='ObjectSomeValuesFrom, IntersectionOf, EquivalentClasses',
                                                    tag='owl')

    self.runtime.current_schema_view = schema_view
    return schema_view

  def save_to_owl(self, file_path: t.Annotated[Path, typer.Option('--file', '-f',
                                                                  help='The output file path. If relative, it will be saved under the "output" directory in the runtime directory. '
                                                                       'If not given, it will be saved after the modul\'s name in the output directory.')] = None,
      schema_name: t.Annotated[str, typer.Option('--schema-name', '-s',
                                                 help='A loaded schema name to use while saving. If not provided, the "current schema" will be used.')] = None):

    typer.echo(f'Running save_to_owl')
    owl_dumper = OWLDumper()
    document = owl_dumper.to_ontology_document(schema=self.runtime.current_schema_view.schema,
                                               element=list(self.runtime.current_module.get_all_entities()))
    document.ontology.iri = funowl.identifiers.IRI(f'https://comploinc/{self.runtime.current_module.name}')
    owl_file_path = file_path
    if owl_file_path is None:
      owl_file_path = Path(self.runtime.current_module.name + '.owl')
    if not owl_file_path.is_absolute():
      owl_file_path = self.configuration.output / owl_file_path

    owl_file_path.parent.mkdir(parents=True, exist_ok=True)
    typer.echo(f'Writing file: {owl_file_path}')
    with open(owl_file_path, 'w') as f:
      f.write(str(document))
