# Auto generated from schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-08-10T02:53:10
# Schema: eq-1
#
# id: http://loinclib/eq-1
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
EQ1 = CurieNamespace('eq1', 'http://loinclib/eq-1')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDFS = CurieNamespace('rdfs', 'http://example.org/UNKNOWN/rdfs/')
DEFAULT_ = EQ1


# Types

# Class references
class ThingId(URIorCURIE):
    pass


class EQ1ThingId(ThingId):
    pass


class SomethingId(ThingId):
    pass


@dataclass
class Thing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EQ1.Thing
    class_class_curie: ClassVar[str] = "eq1:Thing"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = EQ1.Thing

    id: Union[str, ThingId] = None
    label: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ThingId):
            self.id = ThingId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass
class EQ1Thing(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EQ1.EQ1Thing
    class_class_curie: ClassVar[str] = "eq1:EQ1Thing"
    class_name: ClassVar[str] = "EQ1Thing"
    class_model_uri: ClassVar[URIRef] = EQ1.EQ1Thing

    id: Union[str, EQ1ThingId] = None
    rel1: Optional[Union[str, ThingId]] = None
    rel2: Optional[Union[str, ThingId]] = None
    rel3: Optional[Union[str, ThingId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EQ1ThingId):
            self.id = EQ1ThingId(self.id)

        if self.rel1 is not None and not isinstance(self.rel1, ThingId):
            self.rel1 = ThingId(self.rel1)

        if self.rel2 is not None and not isinstance(self.rel2, ThingId):
            self.rel2 = ThingId(self.rel2)

        if self.rel3 is not None and not isinstance(self.rel3, ThingId):
            self.rel3 = ThingId(self.rel3)

        super().__post_init__(**kwargs)


@dataclass
class Something(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EQ1.Something
    class_class_curie: ClassVar[str] = "eq1:Something"
    class_name: ClassVar[str] = "Something"
    class_model_uri: ClassVar[URIRef] = EQ1.Something

    id: Union[str, SomethingId] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SomethingId):
            self.id = SomethingId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.rel1 = Slot(uri=EQ1.rel1, name="rel1", curie=EQ1.curie('rel1'),
                   model_uri=EQ1.rel1, domain=None, range=Optional[Union[str, ThingId]])

slots.rel2 = Slot(uri=EQ1.rel1, name="rel2", curie=EQ1.curie('rel1'),
                   model_uri=EQ1.rel2, domain=None, range=Optional[Union[str, ThingId]])

slots.rel3 = Slot(uri=EQ1.rel1, name="rel3", curie=EQ1.curie('rel1'),
                   model_uri=EQ1.rel3, domain=None, range=Optional[Union[str, ThingId]])

slots.thing__id = Slot(uri=EQ1.id, name="thing__id", curie=EQ1.curie('id'),
                   model_uri=EQ1.thing__id, domain=None, range=URIRef)

slots.thing__label = Slot(uri=RDFS.label, name="thing__label", curie=RDFS.curie('label'),
                   model_uri=EQ1.thing__label, domain=None, range=Optional[str])

slots.something__name = Slot(uri=EQ1.name, name="something__name", curie=EQ1.curie('name'),
                   model_uri=EQ1.something__name, domain=None, range=Optional[str])

slots.EQ1Thing_rel1 = Slot(uri=EQ1.rel1, name="EQ1Thing_rel1", curie=EQ1.curie('rel1'),
                   model_uri=EQ1.EQ1Thing_rel1, domain=EQ1Thing, range=Optional[Union[str, ThingId]])

slots.EQ1Thing_rel2 = Slot(uri=EQ1.rel1, name="EQ1Thing_rel2", curie=EQ1.curie('rel1'),
                   model_uri=EQ1.EQ1Thing_rel2, domain=EQ1Thing, range=Optional[Union[str, ThingId]])

slots.EQ1Thing_rel3 = Slot(uri=EQ1.rel1, name="EQ1Thing_rel3", curie=EQ1.curie('rel1'),
                   model_uri=EQ1.EQ1Thing_rel3, domain=EQ1Thing, range=Optional[Union[str, ThingId]])
