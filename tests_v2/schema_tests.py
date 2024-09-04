import unittest

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import Annotation

from comp_loinc import Runtime


class SchemaTests(unittest.TestCase):

  def test_read_schema(self):
    runtime = Runtime()
    runtime.load_linkml_schema('comp_loinc_v2.yaml')
    schema: SchemaView = runtime.schema_views.get('comp_loinc_v2', None)
    self.assertIsNotNone(schema)

    loinc_term_class = schema.schema.classes['LoincTerm']
    primary_property = loinc_term_class.attributes['primary_property']
    annotations = primary_property.annotations
    owl_annotation: Annotation = annotations['owl']
    owl_annotation.value = 'changed'
    print(owl_annotation)
