import typing as t
from pathlib import Path

import linkml_runtime
import pyhornedowl
from linkml_runtime.linkml_model import SchemaDefinition, Annotatable
from linkml_runtime.utils.namespaces import Namespaces
from numpy.ma.core import absolute
from pyhornedowl.model import (
  DeclareClass,
  SimpleLiteral,
  Annotation,
  AnnotationAssertion,
  ObjectSomeValuesFrom,
  ObjectIntersectionOf,
  EquivalentClasses,
  SubClassOf,
  OntologyID,
)
from pyhornedowl.pyhornedowl import PyIndexedOntology

from comp_loinc import Runtime
from comp_loinc.datamodel import Entity, LoincTerm


def _has_owl_annotation(annotatable: dict | Annotatable, value: str) -> bool:
  annotation = getattr(annotatable.annotations, "owl", None)
  if annotation is None:
    return False
  return value in annotation.value


class OwlSerializer:
  def __init__(self, runtime: Runtime, file_path: Path):
    self.runtime = runtime
    self.file_path = file_path
    self.schema: t.Optional[SchemaDefinition] = None

    from comp_loinc import schemas_path

    self.schema = linkml_runtime.SchemaView(
        schemas_path / "comp_loinc.yaml"
    ).materialize_derived_schema()
    self.namespaces = Namespaces()
    self.ontology: t.Optional[PyIndexedOntology] = None

  def as_tbox(self):
    print("RUNNING PY HORNED OWL")

    self._create_ontology()

    for entity in self.runtime.current_module.get_all_entities():
      entity_class = self.schema.classes.get(type(entity).class_name, None)

      if entity_class:
        self._add_class_declaration(entity)
        self._add_annotations(entity)
        self._add_subs_and_equivalents(entity)

        if isinstance(entity, LoincTerm):
          try:
            self._add_equivalent_definition_axiom(entity)
          except Exception as e:
            print(e)

    ontology_id = OntologyID(
        self.ontology.iri(
            f"comploinc:{self.runtime.current_module.name}", absolute=None
        ),
        None,
    )
    self.ontology.add_axiom(ontology_id, None)

    self.ontology.save_to_file(str(self.file_path), serialization="ofn")

  def _create_ontology(self):
    self.ontology = pyhornedowl.PyIndexedOntology()

    for prefix_name, prefix in self.schema.prefixes.items():
      reference = prefix.prefix_reference
      self.ontology.add_prefix_mapping(prefix_name, reference)

    # self.ontology.add_prefix_mapping(
    #     "", self.schema.prefixes[self.schema.default_prefix].prefix_reference
    # )

  def _add_class_declaration(self, entity: Entity):
    clazz = self.ontology.clazz(entity.id)
    declare_class = DeclareClass(clazz)
    self.ontology.add_axiom(declare_class, None)

  def _add_annotations(self, entity: Entity):
    iri = self.ontology.iri(entity.id, absolute=None)
    for prop in dir(entity):
      prop_value = getattr(entity, prop, None)
      if prop_value is None:
        continue

      schema_class = self.schema.classes.get(type(entity).class_name, None)

      schema_prop = schema_class.attributes.get(prop, None)
      if schema_prop is None:
        continue

      if _has_owl_annotation(schema_prop, "AnnotationAssertion"):
        if isinstance(prop_value, list):
          prop_value = ", ".join(prop_value)
        if isinstance(prop_value, str):
          string_literal = SimpleLiteral(prop_value)
          ann_prop = self.ontology.annotation_property(schema_prop.slot_uri)
          ann = Annotation(ann_prop, string_literal)
          ann_assertion = AnnotationAssertion(iri, ann)
          self.ontology.add_axiom(ann_assertion, None)


  def _add_subs_and_equivalents(self, entity: Entity):
    clazz = self.ontology.clazz(entity.id)
    for super_entity in entity.sub_class_of or []:
      self.ontology.add_axiom(
          SubClassOf(
              clazz,
              self.ontology.clazz(
                  super_entity.id
                  if isinstance(super_entity, Entity)
                  else super_entity
              ),
          ),
          None,
      )
    bce = [clazz]
    for equiv_entity in entity.equivalent_class or []:
      bce.append(
          self.ontology.clazz(
              equiv_entity.id
              if isinstance(equiv_entity, Entity)
              else equiv_entity
          )
      )

    if len(bce) > 1:
      self.ontology.add_axiom(EquivalentClasses(bce), None)

  def _add_equivalent_definition_axiom(self, entity: Entity):
    iri = self.ontology.iri(entity.id, absolute=None)
    ob_expressions: t.List[ObjectSomeValuesFrom] = list()
    for prop in dir(entity):
      prop_value: Entity = getattr(entity, prop, None)
      if prop_value is None:
        continue

      schema_class = self.schema.classes.get(type(entity).class_name, None)

      schema_prop = schema_class.attributes.get(prop, None)
      if schema_prop is None:
        continue


      if _has_owl_annotation(schema_prop, "ObjectSomeValuesFrom"):
        ob_expressions.append(
            ObjectSomeValuesFrom(
                self.ontology.object_property(schema_prop.slot_uri),
                self.ontology.clazz(
                    prop_value.id
                    if isinstance(prop_value, Entity)
                    else prop_value
                ),
            )
        )

    size = len(ob_expressions)
    if size == 0:
      return

    bce = [self.ontology.clazz(entity.id)]
    if size == 1:
      bce.append(ob_expressions[0])
    else:
      bce.append(ObjectIntersectionOf(ob_expressions))

    self.ontology.add_axiom(EquivalentClasses(bce), None)
