import funowl
from linkml_owl.dumpers import owl_dumper

from loinclib.tmp.tmp_linkml_eq_1.EQ1_model import EQ1Thing, SomethingId
import linkml_runtime as rt


entities = []
eq1 = EQ1Thing(id='eq1')
st1 = SomethingId('st1')
st2 = SomethingId('st2')
st3 = SomethingId('st3')

eq1.rel1 = st1
eq1.rel2 = st2
eq1.rel3 = st3

entities.extend([eq1])

schema_view: rt.SchemaView = rt.SchemaView('schema.yaml')

dumper = owl_dumper.OWLDumper()

document: funowl.ontology_document.OntologyDocument = \
    dumper.to_ontology_document(element=entities, schema=schema_view.schema)

with open('eq1.owl', 'w') as f:
    f.write(str(document))
