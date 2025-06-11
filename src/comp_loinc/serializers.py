import typing as t
from pathlib import Path

import linkml_runtime
import pyhornedowl
from jsonasobj import JsonObj
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.namespaces import Namespaces
from pyhornedowl.model import DeclareClass, Class, SimpleLiteral, Annotation, AnnotationAssertion, AnnotationSubject, \
  IRI
from pyhornedowl.pyhornedowl import PyIndexedOntology

from comp_loinc import Runtime
from comp_loinc.datamodel import Entity


class OwlSerializer:
  def __init__(self,
      runtime: Runtime,
      file_path: Path
  ):
    self.runtime = runtime
    self.file_path = file_path
    self.schema: t.Optional[SchemaDefinition] = None

    from comp_loinc import schemas_path
    self.schema = linkml_runtime.SchemaView(schemas_path / "comp_loinc.yaml").materialize_derived_schema()
    self.namespaces = Namespaces()
    self.ontology: t.Optional[PyIndexedOntology] = None

  def as_tbox_equivalent_axioms(self):
    print("RUNNING PY HORNED OWL")

    self._create_ontology()

    for entity in self.runtime.current_module.get_all_entities():
      class_name = type(entity).class_name
      entity_class = self.schema.classes.get(class_name, None)

      if entity_class:
        uri = entity.class_class_uri
        model_uri = entity.class_model_uri
        curie = entity.class_class_curie

        entity_id = entity.id
        iri = self.ontology.iri(entity_id, absolute=None)
        clazz: Class = self.ontology.clazz(str(iri))

        declare_class = DeclareClass(clazz)
        self.ontology.add_axiom(declare_class, None)
        self._add_class_annotations(iri, entity)

    print(self.file_path)
    self.ontology.save_to_file(str(self.file_path), serialization="ofn")

    # generator = LinkmlGenerator(self.runtime.current_schema_view.schema)
    # generator.materialize_classes()
    #
    # loinc_term_class = self.runtime.current_schema_view.schema.classes.get("LoincTerm", None)
    # # loinc_term_class = self.runtime.current_schema_view.get_class("LoincTerm")
    # slots = loinc_term_class.slots
    # for slot in slots:
    #   print(slot)
    #
    # materialized = self.runtime.current_schema_view.materialize_derived_schema()

    print("materialized")

  def _create_ontology(self):
    self.ontology = pyhornedowl.PyIndexedOntology()

    # ontology.add_prefix_mapping("", schema.default_prefix)
    for prefix_name, prefix in self.schema.prefixes.items():
      reference = prefix.prefix_reference
      self.ontology.add_prefix_mapping(prefix_name, reference)

    self.ontology.add_prefix_mapping("", self.schema.prefixes[self.schema.default_prefix].prefix_reference)

  def _add_class_annotations(self, iri: IRI, entity: Entity):

    for prop in dir(entity):
      prop_value = getattr(entity, prop, None)
      if prop_value is None:
        continue

      class_name = type(entity).class_name
      schema_class = self.schema.classes.get(class_name, None)

      schema_prop = schema_class.attributes.get(prop, None)
      if schema_prop is None:
        continue

      annotations: JsonObj = schema_prop.annotations
      owl_annotation = getattr(annotations, "owl", None)
      if owl_annotation is None:
        continue

      if "AnnotationAssertion" in owl_annotation.value:
        if isinstance(prop_value, str):
          string_literal = SimpleLiteral(prop_value)
          ann_prop = self.ontology.annotation_property(schema_prop.slot_uri)
          ann = Annotation(ann_prop, string_literal)
          ann_assertion = AnnotationAssertion(iri, ann)
          self.ontology.add_axiom(ann_assertion, None)

