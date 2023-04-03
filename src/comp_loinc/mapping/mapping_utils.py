import yaml
import textwrap


def build_context(prefix_set=None):
    """Build context for SSSOM files."""
    cmap = {
        "curie_map": {
            "linkml": "https://w3id.org/linkml/",
            "sempav": "https://w3id.org/sempav",
            "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
            "skos": "http://www.w3.org/2004/02/skos/core#"},
        "license": "https://github.com/mapping-commons/mapping-commons.github.io/blob/main/docs/original_license_applies.md",
        "mapping_date": '2022-02-23',
        "mapping_set_id": "http://w3id.org/mapping_commons/disease-mappings/onto-icd10",
        "mapping_tool": "https://github.com/mapping-commons/sssom-py"
    }

    if prefix_set is not None:
        cmap['curie_map'].update(prefix_set)
    cmap_yml = yaml.dump(cmap)
    return "".join([f"#{x}" for x in cmap_yml.splitlines(True)])