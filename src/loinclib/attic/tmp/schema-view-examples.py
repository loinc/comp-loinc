import pathlib

import linkml_runtime
from linkml_runtime.linkml_model.meta import SchemaDefinition

schema_path = pathlib.Path('../../comp_loinc/schema/comp_loinc.yaml')
schema_view = linkml_runtime.SchemaView(schema_path, merge_imports=True)
schema: SchemaDefinition = schema_view.schema

schema.classes.get('LoincCodeClassIntersection').slot_usage.get('has_component').annotations['owl'] = 'Shahim Test'

slot_usage = schema.classes.get('LoincCodeClassIntersection').slot_usage.get('has_component')

print(schema_view)
print(schema)
