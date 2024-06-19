from __future__ import annotations

import logging
import re
import typing as t
from enum import Enum


def _split_colon_1(self, loinc_string: str):
    parts = loinc_string.split(':')
    if len(parts) == 1:
        logging.warning(f'Identifier: {loinc_string} for system: {self.base_url} did not have an expected prefix')
        return parts[0]
    elif len(parts) == 2:
        return parts[1]
    else:
        logging.warning(f'Identifier {loinc_string} for system: {self.base_url} had more than two parts')
        raise ValueError(f'Identifier {loinc_string} for system: {self.base_url} had more than two parts')


# Enum with attributes:
# https://stackoverflow.com/questions/12680080/python-enums-with-attributes#19300424
class NameSpace(Enum):
    # enum id = name, base_url, code_prefix, curie_prefix, url_regex_string
    loinc_code = 'LoincCode', 'https://loinc.org', None, 'loinc', r'https://loinc.org/\d+-\d'
    loinc_part = 'LoincPart', 'https://loinc.org', None, 'loinc', r'https://loinc.org/LP\d+-\d'

    fdasis = 'fdasis', 'http://fdasis.nlm.nih.gov', None, 'fdasis', r'http://fdasis.nlm.nih.gov/.+'
    pubchem = 'pubchem', 'http://pubchem.ncbi.nlm.nih.gov', None, 'pubchem', r'http://pubchem.ncbi.nlm.nih.gov/.+'
    snomed = 'snomed', 'http://snomed.info/sct', None, 'snomed', r'http://snomed.info/sct/.+'
    chebi_class_base = 'chebi', 'http://purl.obolibrary.org/obo', 'CHEBI_', 'chebi', r'http://purl.obolibrary.org/obo/CHEBI_.+'
    ncbi_clinvar = 'ncbi_clinvar', 'https://www.ncbi.nlm.nih.gov/clinvar', None, 'ncbi_clinvar', r'https://www.ncbi.nlm.nih.gov/clinvar/.+'
    ncbi_gene = 'ncbi_gene', 'https://www.ncbi.nlm.nih.gov/gene', None, 'ncbi_gene', r'https://www.ncbi.nlm.nih.gov/gene/.+'
    ncbi_taxonomy = 'ncbi_taxonomy', 'https://www.ncbi.nlm.nih.gov/taxonomy', None, 'ncbi_taxonomy', r'https://www.ncbi.nlm.nih.gov/taxonomy/.+'
    genenames = 'genenames', 'http://www.genenames.org/', None, 'genenames', r'http://www.genenames.org/.+'
    rxnorm = 'rxnorm', 'http://www.nlm.nih.gov/research/umls/rxnorm', None, 'rxnorm', r'http://www.nlm.nih.gov/research/umls/rxnorm/.+'
    radlex = 'radlex', 'http://www.radlex.org/', None, 'radlex', r'http://www.radlex.org/.+'

    loinclib_part = 'LoincLibPart', 'http://example.com/loinclib/part', None, 'LoincLibPart', r'http://example.com/loinclib/part/.+'
    loinclib_code = 'c', 'http://example.com/loinclib/code', None, 'LoincLibCode', r'http://example.com/loinclib/code/.+'
    loinclib_special = 'LoincLibSpecial', 'http://example.com/loinclib/special', None, 'LoincLibSpecial', r'http://example.com/loinclib/special/.+'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name: str, base_url: str, code_prefix: t.Optional[str], curie_prefix: str,
                 url_regex_string: str):
        self.namespace_name = name
        self.base_url = base_url
        self.curie_prefix = curie_prefix
        self.code_prefix: t.Optional[str] = code_prefix
        self.url_regex_string = url_regex_string
        self.url_regex_pattern: re.Pattern = re.compile(url_regex_string, re.IGNORECASE)

    def get_url_from_code(self, code: str) -> str:
        return f'{self.base_url}/{self.code_prefix if self.code_prefix else ""}{code}'

    def get_code_from_url(self, url: str) -> str:
        code = url.removeprefix(f'{self.base_url}/')
        if self.code_prefix:
            code = code.removeprefix(self.code_prefix)
        return code

    def is_valid_url(self, url: str) -> bool:
        return self.url_regex_pattern.fullmatch(url) is not None

    def is_valid_code(self, code: str) -> bool:
        return self.is_valid_url(self.get_code_from_url(code)) is not None

    @classmethod
    def namespace_for_url(cls, url: str) -> NameSpace:
        for ns in NameSpace:
            if ns.url_regex_pattern.fullmatch(url):
                return ns
        raise ValueError(f'No NameSpace for url {url}')

    @classmethod
    def namespace_for_curie(cls, curie: str) -> t.Optional[NameSpace]:
        parts = curie.split(':')
        if len(parts) != 2:
            logging.warning(f'CURIE: {curie} is not formatted properly.')
            return None
        for ns in NameSpace:
            if ns.curie_prefix == parts[0]:
                url = f'{ns.base_url}/{ns.code_prefix if ns.code_prefix else ""}{parts[1]}'

                if ns.url_regex_pattern.fullmatch(url):
                    return ns

        logging.warning(f'CURIE: {curie} did not match any namespace.')

    # todo: older below
    # def clean_loinc_string(self, loinc_string: str):
    #     return loinc_string
    #
    # def owl_url(self, loinc_string):
    #     return f'{self.owl_url_prefix}{self.clean_loinc_string(loinc_string)}'
    #
    # @classmethod
    # def namespace_for_prefix(cls, node_id_prefix: str) -> NameSpace:
    #     for ns in NameSpace:
    #         if ns.node_id_prefix == node_id_prefix:
    #             return ns
    #     raise ValueError(f'No NameSpace for prefix {node_id_prefix}')
    #
    # @classmethod
    # def namespace_for_loinc_identifier(cls, identifier: str) -> NameSpace:
    #     if re.match(r'^LP\d+-\d$', identifier):
    #         return NameSpace.loinclib_part
    #     elif re.search(r'^\d+-\d$', identifier):
    #         return NameSpace.loinclib_code
    #     else:
    #         raise ValueError(f'Loinc identifier: {identifier} did not match NameSpace.')


class NodeType(Enum):
    loinc_code = NameSpace.loinc_code
    loinc_part = NameSpace.loinc_part
    loinclib_part = NameSpace.loinclib_part
    loinclib_code = NameSpace.loinclib_code
    special = NameSpace.loinclib_special

    fdasis = NameSpace.fdasis
    pubchem = NameSpace.pubchem
    snomed = NameSpace.snomed
    chebi = NameSpace.chebi_class_base
    ncbi_clinvar = NameSpace.ncbi_clinvar
    ncbi_gene = NameSpace.ncbi_gene
    ncbi_taxonomy = NameSpace.ncbi_taxonomy
    genenames = NameSpace.genenames
    rxnorm = NameSpace.rxnorm
    radlex = NameSpace.radlex

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, namespace):
        self.namespace: NameSpace = namespace

    @classmethod
    def nodetype_for_namespace(cls, namespace: NameSpace) -> NodeType:
        for nodetype in NodeType:
            if nodetype.namespace == namespace:
                return nodetype
        raise ValueError(f'Unable to find NodeType for NameSpace: {namespace} ')

    def nodeid_of_identifier(self, identifier: str) -> str:
        return f'{self.namespace.node_id_prefix}{{{identifier}}}'

    def identifier_of_nodeid(self, node_id) -> str:
        match = re.match(f'{self.namespace.node_id_prefix}{{(.+)}}', node_id)
        if match:
            return match.group(1)
        else:
            raise ValueError(f'Failed to extract identifier from node id: {node_id}')

    def is_type_of_nodeid(self, node_id: str) -> bool:
        if re.match(f'{self.namespace.node_id_prefix}{{.+}}', node_id):
            return True
        return False

    @classmethod
    def type_for_identifier(cls, identifier: str, namespace: NameSpace) -> NodeType:
        for t in NodeType:
            if t.namespace == namespace:
                return t
        raise ValueError(f'Unable to find node type for identifier {identifier} and namespace  {namespace}')

    @classmethod
    def type_for_node_id(cls, nodeid: str) -> NodeType:
        match = re.match(f'(.+){{(.+)}}', nodeid)
        if match:
            prefix = match.group(1)
            namespace = NameSpace.namespace_for_prefix(prefix)
            return NodeType.nodetype_for_namespace(namespace)
        raise ValueError(f'Unable to find NodeType for node id: {nodeid}.')


class PropertyType(Enum):
    # enum_id = friendly/official name, uri, group name, description
    edge_type = 'graph-edge-type'

    """Attribute keys/names for LOINC values"""

    loinc_code = 'code'
    """The actual LOINC code (any code), or the identifier for what this node is about"""

    loinc_display = 'display'
    """
    This is the main label for a LOINC entity.

    For parts: an alternate display name for the Part, which is often used to create the LOINC Long Common Name
    """

    loinc_status = 'status'
    """The status of the entity."""

    # parts file based attributes
    loinc_part_name = 'part name'
    loinc_part_display_name = 'part display name'
    loinc_part_type = 'part type'

    # Tree file attributes
    loinc_tree_code_text = 'tree code text'

    # loinc attributes
    loinc_long_common_name = 'loinc long common name'
    loinc_short_name = 'loinc short name'
    loinc_definition = 'loinc definition'
    loinc_component = 'loinc component'
    loinc_property = 'loinc property'
    loinc_time_aspect = 'loinc time aspect'
    loinc_system = 'loinc system'
    loinc_scale_type = 'loinc scale type'
    loinc_method_type = 'loinc method type'
    loinc_class = 'loinc class'
    loinc_class_type = 'loinc class type'
    loinc_version_first_released = 'loinc version first released'
    loinc_version_last_changed = 'loinc version last changed'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name=None, uri=None, group=None, description=None):
        self.attr_name = name
        self.attr_uri = uri
        self.attr_group = group
        self.attr_description = description


class EdgeType(Enum):
    # enum_id = friendly/official name, uri, group name, description

    # Component part
    #  https://loinc.org/kb/enriched-linkages-between-loinc-terms-and-loinc-parts/#primary
    # https://loinc.org/kb/users-guide/major-parts-of-a-loinc-term/#componentanalyte-1st-part
    # https://loinc.org/kb/users-guide/major-parts-of-a-loinc-term/#distinguishing-multiple-values-for-any-test-via-the-test-name-4th-subpart
    # https://loinc.org/kb/enriched-linkages-between-loinc-terms-and-loinc-parts/#detailedmodel
    loinc_Primary_COMPONENT = 'COMPONENT', 'http://loinc.org/property/COMPONENT', 'Primary'
    loinc_DetailedModel_COMPONENT_analyte = 'COMPONENT', 'http://loinc.org/property/analyte', 'DetailedModel'
    loinc_DetailedModel_CHALLENGE_challenge = 'CHALLENGE', 'http://loinc.org/property/challenge', 'DetailedModel'
    loinc_DetailedModel_ADJUSTMENT_adjustment = 'ADJUSTMENT', 'http://loinc.org/property/adjustment', 'DetailedModel'
    loinc_DetailedModel_COUNT_count = 'COUNT', 'http://loinc.org/property/count', 'DetailedModel'

    # Property part
    # ==========
    loinc_Primary_PROPERTY = 'PROPERTY', 'http://loinc.org/property/PROPERTY', 'Primary'
    loinc_DetailedModel_PROPERTY_PROPERTY = 'PROPERTY', 'http://loinc.org/property/PROPERTY', 'DetailedModel'

    # Time part:
    # ==========
    loinc_Primary_TIME = 'TIME', 'http://loinc.org/property/TIME_ASPCT', 'Primary'
    loinc_DetailedModel_TIME_time_core = 'TIME', 'http://loinc.org/property/time-core', 'DetailedModel'
    loinc_DetailedModel_TIME_MODIFIER_time_modifier = 'TIME MODIFIER', 'http://loinc.org/property/time-modifier', 'DetailedModel'

    # System part:
    # ==========
    loinc_Primary_SYSTEM = 'SYSTEM', 'http://loinc.org/property/SYSTEM', 'Primary'
    loinc_DetailedModel_SYSTEM_system_core = 'SYSTEM', 'http://loinc.org/property/system-core', 'DetailedModel'
    loinc_DetailedModel_SUPER_SYSTEM_super_system = 'SUPER SYSTEM', 'http://loinc.org/property/super-system', 'DetailedModel'

    # Scale part:
    # ==========
    loinc_Primary_SCALE = 'SCALE', 'http://loinc.org/property/SCALE_TYP', 'Primary'
    loinc_DetailedModel_SCALE_SCALE_TYP = 'SCALE', 'http://loinc.org/property/SCALE_TYP', 'DetailedModel'

    # Method part:
    # ==========
    loinc_Primary_METHOD = 'METHOD', 'http://loinc.org/property/METHOD_TYP', 'Primary'
    loinc_DetailedModel_METHOD_METHOD_TYP = 'METHOD', 'http://loinc.org/property/METHOD_TYP', 'DetailedModel'

    # Document
    loinc_DocumentOntology_Document_Kind = 'Document.Kind', 'http://loinc.org/property/document-kind', 'DocumentOntology'
    loinc_DocumentOntology_Document_Role = 'Document.Role', 'http://loinc.org/property/document-role', 'DocumentOntology'
    loinc_DocumentOntology_Document_Setting = 'Document.Setting', 'http://loinc.org/property/document-setting', 'DocumentOntology'
    loinc_DocumentOntology_Document_SubjectMatterDomain = 'Document.SubjectMatterDomain', 'http://loinc.org/property/document-subject-matter-domain', 'DocumentOntology'
    loinc_DocumentOntology_Document_TypeOfService = 'Document.TypeOfService', 'http://loinc.org/property/document-type-of-service', 'DocumentOntology'

    # Radiology
    loinc_Radiology_Rad_Anatomic_Location_Imaging_Focus = 'Rad.Anatomic Location.Imaging Focus', 'http://loinc.org/property/rad-anatomic-location-imaging-focus', 'Radiology'
    loinc_Radiology_Rad_Anatomic_Location_Laterality = 'Rad.Anatomic Location.Laterality', 'http://loinc.org/property/rad-anatomic-location-laterality', 'Radiology'
    loinc_Radiology_Rad_Anatomic_Location_Laterality_Presence = 'Rad.Anatomic Location.Laterality.Presence', 'http://loinc.org/property/rad-anatomic-location-laterality-presence', 'Radiology'
    loinc_Radiology_Rad_Anatomic_Location_Region_Imaged = 'Rad.Anatomic Location.Region Imaged', 'http://loinc.org/property/rad-anatomic-location-region-imaged', 'Radiology'
    loinc_Radiology_Rad_Guidance_for_Action = 'Rad.Guidance for.Action', 'http://loinc.org/property/rad-guidance-for-action', 'Radiology'
    loinc_Radiology_Rad_Guidance_for_Approach = 'Rad.Guidance for.Approach', 'http://loinc.org/property/rad-guidance-for-approach', 'Radiology'
    loinc_Radiology_Rad_Guidance_for_Object = 'Rad.Guidance for.Object', 'http://loinc.org/property/rad-guidance-for-object', 'Radiology'
    loinc_Radiology_Rad_Guidance_for_Presence = 'Rad.Guidance for.Presence', 'http://loinc.org/property/rad-guidance-for-presence', 'Radiology'
    loinc_Radiology_Rad_Maneuver_Maneuver_Type = 'Rad.Maneuver.Maneuver Type', 'http://loinc.org/property/rad-maneuver-maneuver-type', 'Radiology'
    loinc_Radiology_Rad_Modality_Modality_Subtype = 'Rad.Modality.Modality Subtype', 'http://loinc.org/property/rad-modality-subtype', 'Radiology'
    loinc_Radiology_Rad_Modality_Modality_Type = 'Rad.Modality.Modality Type', 'http://loinc.org/property/rad-modality-type', 'Radiology'
    loinc_Radiology_Rad_Pharmaceutical_Route = 'Rad.Pharmaceutical.Route', 'http://loinc.org/property/rad-pharmaceutical-route', 'Radiology'
    loinc_Radiology_Rad_Pharmaceutical_Substance_Given = 'Rad.Pharmaceutical.Substance Given', 'http://loinc.org/property/rad-pharmaceutical-substance-given', 'Radiology'
    loinc_Radiology_Rad_Reason_for_Exam = 'Rad.Reason for Exam', 'http://loinc.org/property/rad-reason-for-exam', 'Radiology'
    loinc_Radiology_Rad_Subject = 'Rad.Subject', 'http://loinc.org/property/rad-subject', 'Radiology'
    loinc_Radiology_Rad_Timing = 'Rad.Timing', 'http://loinc.org/property/rad-timing', 'Radiology'
    loinc_Radiology_Rad_View_Aggregation = 'Rad.View.Aggregation', 'http://loinc.org/property/rad-view-aggregation', 'Radiology'
    loinc_Radiology_Rad_View_View_Type = 'Rad.View.View Type', 'http://loinc.org/property/rad-view-view-type', 'Radiology'

    # Other
    loinc_Metadata_CLASS_CLASS = 'CLASS', 'http://loinc.org/property/CLASS', 'Metadata'
    loinc_Metadata_CLASS_category = 'CLASS', 'http://loinc.org/property/category', 'Metadata'
    loinc_Search_CHALLENGE_search = 'CHALLENGE', 'http://loinc.org/property/search', 'Search'
    loinc_Search_COMPONENT_search = 'COMPONENT', 'http://loinc.org/property/search', 'Search'
    loinc_Search_METHOD_search = 'METHOD', 'http://loinc.org/property/search', 'Search'
    loinc_Search_SUPER_SYSTEM_search = 'SUPER SYSTEM', 'http://loinc.org/property/search', 'Search'
    loinc_Search_SYSTEM_search = 'SYSTEM', 'http://loinc.org/property/search', 'Search'

    loinc_SemanticEnhancement_GENE_analyte_gene = 'GENE', 'http://loinc.org/property/analyte-gene', 'SemanticEnhancement'

    loinc_SyntaxEnhancement_COMPONENT_analyte_core = 'COMPONENT', 'http://loinc.org/property/analyte-core', 'SemanticEnhancement'
    loinc_SyntaxEnhancement_DIVISOR_analyte_divisor = 'DIVISOR', 'http://loinc.org/property/analyte-divisor', 'SemanticEnhancement'
    loinc_SyntaxEnhancement_NUMERATOR_analyte_numerator = 'NUMERATOR', 'http://loinc.org/property/analyte-numerator', 'SemanticEnhancement'
    loinc_SyntaxEnhancement_SUFFIX_analyte_divisor_suffix = 'SUFFIX', 'http://loinc.org/property/analyte-divisor-suffix', 'SemanticEnhancement'
    loinc_SyntaxEnhancement_SUFFIX_analyte_suffix = 'SUFFIX', 'http://loinc.org/property/analyte-suffix', 'SemanticEnhancement'

    loinc_Equivalence_equivalent_equivalent = 'equivalent', 'equivalent', 'Equivalence'
    loinc_Equivalence_relatedto_relatedto = 'relatedto', 'relatedto', 'Equivalence'
    loinc_Equivalence_narrower_narrower = 'narrower', 'narrower', 'Equivalence'
    loinc_Equivalence_wider_wider = 'wider', 'wider', 'Equivalence'

    loinc_LoincTree_has_parent = 'has_parent', 'has_parent', 'LoincTree'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name=None, uri=None, group=None, description=None):
        self.edge_name = name
        self.edge_uri = uri
        self.edge_group = group
        self.edge_description = description

    def __repr__(self):
        return f'Edge:{{name:{self.edge_name}, group:{self.edge_group}, uri:{self.edge_uri}}}'

    def __str__(self):
        return self.__repr__()

    @classmethod
    def type_of(cls, /, *, group, name, uri):
        for edgeType in EdgeType:
            if edgeType.edge_group == group and edgeType.edge_name == name and edgeType.edge_uri == uri:
                return edgeType
        raise ValueError(f'Unable to find EdgeType for group: {{{group}}}, name: {{{name}}}, uri: {{{uri}}}')


# class EdgeAttributeKey(str, Enum):
#     pass
#     # edge_type = 'edge type'


# class EdgeType(Enum):
#
#     def __new__(cls, *args, **kwds):
#         value = len(cls.__members__) + 1
#         obj = object.__new__(cls)
#         obj._value_ = value
#         return obj
#
#     def __init__(self, group, name, uri):
#         self.rel_group = group
#         self.rel_name = name
#         self.rel_uri = uri
#
#     def __repr__(self):
#         return f'{self.name}{{group:{self.rel_group}, name:{self.rel_name}, uri:{self.rel_uri}}}'
#
#     def __str__(self):
#         return self.__repr__()


# class LoincEdgeType(Enum):
# First part: Component/Analyte
# ==========

# #  https://loinc.org/kb/enriched-linkages-between-loinc-terms-and-loinc-parts/#primary
# loinc_Primary_COMPONENT = 'Primary', 'COMPONENT', 'http://loinc.org/property/COMPONENT'
#
# # Sub parts:
# # https://loinc.org/kb/users-guide/major-parts-of-a-loinc-term/#componentanalyte-1st-part
# # https://loinc.org/kb/users-guide/major-parts-of-a-loinc-term/#distinguishing-multiple-values-for-any-test-via-the-test-name-4th-subpart
# # https://loinc.org/kb/enriched-linkages-between-loinc-terms-and-loinc-parts/#detailedmodel
# loinc_DetailedModel_COMPONENT_analyte = 'DetailedModel', 'COMPONENT', 'http://loinc.org/property/analyte'
# loinc_DetailedModel_CHALLENGE_challenge = 'DetailedModel', 'CHALLENGE', 'http://loinc.org/property/challenge'
# loinc_DetailedModel_ADJUSTMENT_adjustment = 'DetailedModel', 'ADJUSTMENT', 'http://loinc.org/property/adjustment'
# loinc_DetailedModel_COUNT_count = 'DetailedModel', 'COUNT', 'http://loinc.org/property/count'
#
# # Second part: Property
# # ==========
#
# loinc_Primary_PROPERTY = 'Primary', 'PROPERTY', 'http://loinc.org/property/PROPERTY'
#
# loinc_DetailedModel_PROPERTY_PROPERTY = 'DetailedModel', 'PROPERTY', 'http://loinc.org/property/PROPERTY'
#
# # Time part:
# # ==========
#
# loinc_Primary_TIME = 'Primary', 'TIME', 'http://loinc.org/property/TIME_ASPCT'
#
# loinc_DetailedModel_TIME_time_core = 'DetailedModel', 'TIME', 'http://loinc.org/property/time-core'
# loinc_DetailedModel_TIME_MODIFIER_time_modifier = 'DetailedModel', 'TIME MODIFIER', 'http://loinc.org/property/time-modifier'
#
# # System part:
# # ==========
#
# loinc_Primary_SYSTEM = 'Primary', 'SYSTEM', 'http://loinc.org/property/SYSTEM'
#
# loinc_DetailedModel_SYSTEM_system_core = 'DetailedModel', 'SYSTEM', 'http://loinc.org/property/system-core'
# loinc_DetailedModel_SUPER_SYSTEM_super_system = 'DetailedModel', 'SUPER SYSTEM', 'http://loinc.org/property/super-system'
#
# # Scale part:
# # ==========
#
# loinc_Primary_SCALE = 'Primary', 'SCALE', 'http://loinc.org/property/SCALE_TYP'
# loinc_DetailedModel_SCALE_SCALE_TYP = 'DetailedModel', 'SCALE', 'http://loinc.org/property/SCALE_TYP'
#
# # Method part:
# # ==========
#
# loinc_Primary_METHOD = 'Primary', 'METHOD', 'http://loinc.org/property/METHOD_TYP'
#
# loinc_DetailedModel_METHOD_METHOD_TYP = 'DetailedModel', 'METHOD', 'http://loinc.org/property/METHOD_TYP'
#
# # Document
# loinc_DocumentOntology_Document_Kind = 'DocumentOntology', 'Document.Kind', 'http://loinc.org/property/document-kind'
# loinc_DocumentOntology_Document_Role = 'DocumentOntology', 'Document.Role', 'http://loinc.org/property/document-role'
# loinc_DocumentOntology_Document_Setting = 'DocumentOntology', 'Document.Setting', 'http://loinc.org/property/document-setting'
# loinc_DocumentOntology_Document_SubjectMatterDomain = 'DocumentOntology', 'Document.SubjectMatterDomain', 'http://loinc.org/property/document-subject-matter-domain'
# loinc_DocumentOntology_Document_TypeOfService = 'DocumentOntology', 'Document.TypeOfService', 'http://loinc.org/property/document-type-of-service'
#
# # Radiology
# loinc_Radiology_Rad_Anatomic_Location_Imaging_Focus = 'Radiology', 'Rad.Anatomic Location.Imaging Focus', 'http://loinc.org/property/rad-anatomic-location-imaging-focus'
# loinc_Radiology_Rad_Anatomic_Location_Laterality = 'Radiology', 'Rad.Anatomic Location.Laterality', 'http://loinc.org/property/rad-anatomic-location-laterality'
# loinc_Radiology_Rad_Anatomic_Location_Laterality_Presence = 'Radiology', 'Rad.Anatomic Location.Laterality.Presence', 'http://loinc.org/property/rad-anatomic-location-laterality-presence'
# loinc_Radiology_Rad_Anatomic_Location_Region_Imaged = 'Radiology', 'Rad.Anatomic Location.Region Imaged', 'http://loinc.org/property/rad-anatomic-location-region-imaged'
# loinc_Radiology_Rad_Guidance_for_Action = 'Radiology', 'Rad.Guidance for.Action', 'http://loinc.org/property/rad-guidance-for-action'
# loinc_Radiology_Rad_Guidance_for_Approach = 'Radiology', 'Rad.Guidance for.Approach', 'http://loinc.org/property/rad-guidance-for-approach'
# loinc_Radiology_Rad_Guidance_for_Object = 'Radiology', 'Rad.Guidance for.Object', 'http://loinc.org/property/rad-guidance-for-object'
# loinc_Radiology_Rad_Guidance_for_Presence = 'Radiology', 'Rad.Guidance for.Presence', 'http://loinc.org/property/rad-guidance-for-presence'
# loinc_Radiology_Rad_Maneuver_Maneuver_Type = 'Radiology', 'Rad.Maneuver.Maneuver Type', 'http://loinc.org/property/rad-maneuver-maneuver-type'
# loinc_Radiology_Rad_Modality_Modality_Subtype = 'Radiology', 'Rad.Modality.Modality Subtype', 'http://loinc.org/property/rad-modality-subtype'
# loinc_Radiology_Rad_Modality_Modality_Type = 'Radiology', 'Rad.Modality.Modality Type', 'http://loinc.org/property/rad-modality-type'
# loinc_Radiology_Rad_Pharmaceutical_Route = 'Radiology', 'Rad.Pharmaceutical.Route', 'http://loinc.org/property/rad-pharmaceutical-route'
# loinc_Radiology_Rad_Pharmaceutical_Substance_Given = 'Radiology', 'Rad.Pharmaceutical.Substance Given', 'http://loinc.org/property/rad-pharmaceutical-substance-given'
# loinc_Radiology_Rad_Reason_for_Exam = 'Radiology', 'Rad.Reason for Exam', 'http://loinc.org/property/rad-reason-for-exam'
# loinc_Radiology_Rad_Subject = 'Radiology', 'Rad.Subject', 'http://loinc.org/property/rad-subject'
# loinc_Radiology_Rad_Timing = 'Radiology', 'Rad.Timing', 'http://loinc.org/property/rad-timing'
# loinc_Radiology_Rad_View_Aggregation = 'Radiology', 'Rad.View.Aggregation', 'http://loinc.org/property/rad-view-aggregation'
# loinc_Radiology_Rad_View_View_Type = 'Radiology', 'Rad.View.View Type', 'http://loinc.org/property/rad-view-view-type'
#
# # Other
# loinc_Metadata_CLASS_CLASS = 'Metadata', 'CLASS', 'http://loinc.org/property/CLASS'
# loinc_Metadata_CLASS_category = 'Metadata', 'CLASS', 'http://loinc.org/property/category'
# loinc_Search_CHALLENGE_search = 'Search', 'CHALLENGE', 'http://loinc.org/property/search'
# loinc_Search_COMPONENT_search = 'Search', 'COMPONENT', 'http://loinc.org/property/search'
# loinc_Search_METHOD_search = 'Search', 'METHOD', 'http://loinc.org/property/search'
# loinc_Search_SUPER_SYSTEM_search = 'Search', 'SUPER SYSTEM', 'http://loinc.org/property/search'
# loinc_Search_SYSTEM_search = 'Search', 'SYSTEM', 'http://loinc.org/property/search'
#
# loinc_SemanticEnhancement_GENE_analyte_gene = 'SemanticEnhancement', 'GENE', 'http://loinc.org/property/analyte-gene'
#
# loinc_SyntaxEnhancement_COMPONENT_analyte_core = 'SyntaxEnhancement', 'COMPONENT', 'http://loinc.org/property/analyte-core'
# loinc_SyntaxEnhancement_DIVISOR_analyte_divisor = 'SyntaxEnhancement', 'DIVISOR', 'http://loinc.org/property/analyte-divisor'
# loinc_SyntaxEnhancement_NUMERATOR_analyte_numerator = 'SyntaxEnhancement', 'NUMERATOR', 'http://loinc.org/property/analyte-numerator'
# loinc_SyntaxEnhancement_SUFFIX_analyte_divisor_suffix = 'SyntaxEnhancement', 'SUFFIX', 'http://loinc.org/property/analyte-divisor-suffix'
# loinc_SyntaxEnhancement_SUFFIX_analyte_suffix = 'SyntaxEnhancement', 'SUFFIX', 'http://loinc.org/property/analyte-suffix'
#
# loinc_Equivalence_equivalent_equivalent = 'Equivalence', 'equivalent', 'equivalent'
# loinc_Equivalence_relatedto_relatedto = 'Equivalence', 'relatedto', 'relatedto'
# loinc_Equivalence_narrower_narrower = 'Equivalence', 'narrower', 'narrower'
# loinc_Equivalence_wider_wider = 'Equivalence', 'wider', 'wider'
#
# loinc_LoincTree_has_parent_has_parent = 'LoincTree', 'has_parent', 'has_parent'

# def __new__(cls, *args, **kwds):
#     value = len(cls.__members__) + 1
#     obj = object.__new__(cls)
#     obj._value_ = value
#     return obj
#
# def __init__(self, group, name, uri):
#     self.edge_group = group
#     self.edge_name = name
#     self.edge_uri = uri
#
# def __repr__(self):
#     return f'LoincEdge:{{group:{self.edge_group}, name:{self.edge_name}, uri:{self.edge_uri}}}'
#
# def __str__(self):
#     return self.__repr__()
#
# @classmethod
# def type_of(cls, /, *, group, name, uri):
#     for edgeType in LoincEdgeType:
#         if edgeType.edge_group == group and edgeType.edge_name == name and edgeType.edge_uri == uri:
#             return edgeType
#     raise ValueError(f'Unable to find LoincEdgeType for group: {{{group}}}, name: {{{name}}}, uri: {{{uri}}}')


if __name__ == '__main__':
    print(NameSpace.loinc_part.url_regex_pattern.match(f'{NameSpace.loinc_part.base_url}/LP123-1'))
    print(NameSpace.namespace_for_url(f'{NameSpace.loinc_part.base_url}/LP123-1'))
    print(NameSpace.namespace_for_curie(f'loinc:LP123-1'))

    print(NameSpace.loinc_part.get_url_from_code('LP123-1'))
    print(NameSpace.loinc_part.get_code_from_url('https://loinc.org/LP123-1'))

    print(NameSpace.loinc_part.is_valid_code('LP123-1'))
