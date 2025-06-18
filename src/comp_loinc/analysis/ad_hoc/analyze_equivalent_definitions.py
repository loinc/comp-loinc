"""Analyze equivalent definitions in CompLOINC.

FYI: This script does an analysis of variations with and without included inferred subclass axioms, just to be safe. As
expected, though, this variation had no effect on the results.

------------------------------------------------------------------------------------------------------------------------

This script groups terms that share identical OWL equivalence definitions.  It
produces two TSV files:

1. ``equivalent_groups_defs.tsv`` – a row for each property/value pair in a
   group of terms that share the same definition.  This file now includes a
   ``label`` column which contains the ``rdfs:label`` for the class in the
   ``value`` column.
2. ``equivalent_groups_labels.tsv`` – a simple mapping of ``group_num`` to the
   labels of the terms in that group.

------------------------------------------------------------------------------------------------------------------------
PROMPTS
------------------------------------------------------------------------------------------------------------------------

https://chatgpt.com/codex/tasks/task_e_68508c866ff8832cb2646ccad9b71308

I want to analyze the supplementary part model in LOINC.

I want to analyze the file at this path (relative to the root of the repository):
`output/build-default/merged-and-reasoned/canonical/comploinc-merged-reasoned-all-supplementary.owl`

It is comprised of many classes that have EquivalentClass definitions like so:

```
    <owl:Class rdf:about="https://loinc.org/56561-4">
        <owl:equivalentClass>
            <owl:Class>
                <owl:intersectionOf rdf:parseType="Collection">
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/PROPERTY-supplementary"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP6827-2"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/SCALE_TYP-supplementary"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP7753-9"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/analyte"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP14695-8"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/analyte-core"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP14695-8"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/category"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP20461-7"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/category"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP7784-4"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/challenge"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP20502-8"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/class_"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP7784-4"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/system-core"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP7576-4"/>
                    </owl:Restriction>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://loinc.org/property/time-core"/>
                        <owl:someValuesFrom rdf:resource="https://loinc.org/LP6960-1"/>
                    </owl:Restriction>
                </owl:intersectionOf>
            </owl:Class>
        </owl:equivalentClass>
        <rdfs:subClassOf rdf:resource="https://loinc.org/CHAL"/>
        <rdfs:label>LT Somatotropin [Mass/volume] in Serum or Plasma --5.5 hours post XXX challenge</rdfs:label>
        <loinc:loinc_class>CHAL</loinc:loinc_class>
        <loinc:loinc_class_type>1</loinc:loinc_class_type>
        <loinc:loinc_number>56561-4</loinc:loinc_number>
        <loinc:long_common_name>Somatotropin [Mass/volume] in Serum or Plasma --5.5 hours post XXX challenge</loinc:
        long_common_name>
    </owl:Class>
```

I want to be able find out any / all terms that have the same exact equivalent class definitions.

I want this analysis to output a TSV with the following columns: group_num, property, value, terms

- group_num: An integer (like a new ID) simply representing this group of terms that have the same equivalence
definition.
- property: The "code" shown at the last part of the URL (after the last `/`) in the `onProperty` field, e.g.
"time-core".
- value: The corresponding value `someValuesFrom` for the given property, e.g. for "time-core" in the above example,
it'd be "LP6960-1".
- terms: | delimited list showing all terms that have this exact same definition.

Example, using the above snippet:
```
group_num   property    value   terms
1   PROPERTY-supplementary  LP6827-2    56561-4
1   SCALE_TYP-supplementary LP7753-9    56561-4
1   analyte LP14695-8   56561-4
1   analyte-core    LP14695-8   56561-4
1   category    LP20461-7   56561-4
1   category    LP7784-4    56561-4
1   challenge   LP20502-8   56561-4
1   class_  LP7784-4    56561-4
1   system-core LP7576-4    56561-4
1   time-core   LP6960-1    56561-4
```

But, I want this TSV to ONLY be populated by cases where there is more than 1 class with the same equivalent class
definition.

Feel free to solve this using SPARQL, Python, or a combination of the two.

You won't have access to the input file itself, so don't worry about running it. I'll run it after you've coded up a
solution.


------------------------------------------------------------------------------------------------------------------------


https://chatgpt.com/codex/tasks/task_e_6850b8dd7884832cbc2f2d9d32ab389b
Please update the script: `analyze_equivalent_definitions.py`

It should now output a 2nd file. For reference, here's what the first file looks like:

Fields:
- group_num: An integer (like a new ID) simply representing this group of terms that have the same equivalence
definition.
- property: The "code" shown at the last part of the URL (after the last `/`) in the `onProperty` field, e.g.
"time-core".
- value: The corresponding value `someValuesFrom` for the given property, e.g. for "time-core" in the above example,
it'd be "LP6960-1".
- terms: | delimited list showing all terms that have this exact same definition.


Example:
```
group_num   property    value   terms
1   PROPERTY-supplementary  LP6827-2    56561-4|56561-2
1   SCALE_TYP-supplementary LP7753-9    56561-4|56561-2
1   analyte LP14695-8   56561-4
1   analyte-core    LP14695-8   56561-4|56561-2
1   category    LP20461-7   56561-4|56561-2
1   category    LP7784-4    56561-4|56561-2
1   challenge   LP20502-8   56561-4|56561-2
1   class_  LP7784-4    56561-4|56561-2
1   system-core LP7576-4    56561-4|56561-2
1   time-core   LP6960-1    56561-4|56561-2
```

This 2nd file, you can call 'labels.tsv'. It will have the following fields:

- group_num: Uses the same `group_num` from the first file.
- term: Deconstructs the | delimited list from the `terms` column in the first file. So if the first file had 2 terms
for a given group_num, this file should have 2 rows for the given group_num
- label: The rdfs:label for that term.


------------------------------------------------------------------------------------------------------------------------


I'd like to update the script analyze_equivalent_definitions.py. I'd like to modify `equivalent_groups_defs.tsv`. It
should have a `label` column now. This should be for the rdfs:label for the class shown in the `property` column.
"""
import os
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Union

OWL = '{http://www.w3.org/2002/07/owl#}'
RDF = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
RDFS = '{http://www.w3.org/2000/01/rdf-schema#}'
THIS_FILE = Path(__file__)
PROJ_DIR = THIS_FILE.parent.parent.parent.parent.parent
OUTDIR = PROJ_DIR / 'output' / 'analysis' / 'equivalent_def_collisions'
PART_MODELS = ('primary', 'supplementary')
CONFIGS = {  # part model goes into {}
    'inferred_included': {
        'indir': PROJ_DIR / 'output/build-default/merged-and-reasoned/inferred-sc-axioms-included/',
        'outpath_defs_pattern': OUTDIR / '{}-inferred_included--defs.tsv',
        'outpath_labels_pattern': OUTDIR / '{}-inferred_included--labels.tsv',
    },
    'inferred_excluded': {
        'indir': PROJ_DIR / 'output/build-default/merged-and-reasoned/',
        'outpath_defs_pattern': '{}-inferred_excluded--defs.tsv',
        'outpath_labels_pattern': '{}-inferred_excluded--labels.tsv',
    },
}
if not os.path.exists(OUTDIR):
    os.mkdir(OUTDIR)


def extract_pairs(intersection: ET.Element) -> List[Tuple[str, str]]:
    """Extract key value pairs for definitions"""
    pairs = []
    for restriction in intersection.findall(f'{OWL}Restriction'):
        prop_elem = restriction.find(f'{OWL}onProperty')
        val_elem = restriction.find(f'{OWL}someValuesFrom')
        if prop_elem is None or val_elem is None:
            continue
        prop_uri = prop_elem.attrib.get(f'{RDF}resource')
        val_uri = val_elem.attrib.get(f'{RDF}resource')
        if not prop_uri or not val_uri:
            continue
        prop = prop_uri.rsplit('/', 1)[-1]
        val = val_uri.rsplit('/', 1)[-1]
        pairs.append((prop, val))
    return pairs


def _get(cls):
    """Get class ID"""
    return cls.get(f'{RDF}about') or cls.get(f'{RDF}ID')


def parse_rdf_xml_owl(path: Union[Path, str]) -> Tuple[Dict[Tuple[Tuple[str, str], ...], List[str]], Dict[str, str]]:
    """Parse the OWL file and group terms by their equivalence definitions.

    Returns a mapping of property/value pairs to a list of terms (``groups``) and
    a mapping from term identifier to its ``rdfs:label`` (``labels``).
    """

    tree = ET.parse(path)
    root = tree.getroot()

    groups: Dict[Tuple[Tuple[str, str], ...], List[str]] = defaultdict(list)
    labels: Dict[str, str] = {}

    for cls in root.findall(f'.//{OWL}Class'):
        # noinspection DuplicatedCode
        term_uri = _get(cls)
        if not term_uri:
            continue
        term = term_uri.rsplit('/', 1)[-1]

        label_elem = cls.find(f'{RDFS}label')
        if label_elem is not None and label_elem.text:
            labels[term] = label_elem.text.strip()

        eq_elem = cls.find(f'{OWL}equivalentClass')
        if eq_elem is None:
            continue
        anon_class = eq_elem.find(f'{OWL}Class')
        if anon_class is None:
            continue
        intersection = anon_class.find(f'{OWL}intersectionOf')
        if intersection is None:
            continue
        pairs = extract_pairs(intersection)
        if not pairs:
            continue
        key = tuple(sorted(pairs))
        groups[key].append(term)

    # capture labels for properties as well
    for prop_elem in (root.findall(f'.//{OWL}ObjectProperty') + root.findall(f'.//{OWL}DatatypeProperty') +
                      root.findall(f'.//{OWL}AnnotationProperty')):
        # noinspection DuplicatedCode
        uri = _get(prop_elem)
        if not uri:
            continue
        prop_id = uri.rsplit('/', 1)[-1]

        label_elem = prop_elem.find(f'{RDFS}label')
        if label_elem is not None and label_elem.text:
            labels[prop_id] = label_elem.text.strip()

    return groups, labels


def generate_rows(groups: Dict[Tuple[Tuple[str, str], ...], List[str]], labels: Dict[str, str]):
    """Generate rows for the TSV outputs.

    Returns a list of rows for ``equivalent_groups_defs.tsv`` and a mapping from
    ``group_num`` to the list of terms in that group for use when writing the
    labels file.
    """

    rows = []
    group_terms: Dict[int, List[str]] = {}
    group_num = 0

    for key, terms in groups.items():
        if len(terms) < 2:
            continue
        group_num += 1
        sorted_terms = sorted(terms)
        term_str = '|'.join(sorted_terms)
        for prop, val in key:
            label = labels.get(val, '')
            rows.append((group_num, prop, val, label, term_str))
        group_terms[group_num] = sorted_terms

    return rows, group_terms


def main():
    """CLI entry point."""
    for paths in CONFIGS.values():
        for mdl in PART_MODELS:
            inpath = paths['indir'] / f'comploinc-merged-reasoned-all-{mdl}.owl'
            outpath_defs = str(paths['outpath_defs_pattern']).format(mdl)
            outpath_labels = str(paths['outpath_labels_pattern']).format(mdl)

            groups, labels = parse_rdf_xml_owl(inpath)
            rows, group_terms = generate_rows(groups, labels)

            with open(outpath_defs, 'w', encoding='utf-8') as f:
                f.write('group_num\tproperty\tvalue\tlabel\tterms\n')
                for g, p, v, lbl, t in rows:
                    f.write(f"{g}\t{p}\t{v}\t{lbl}\t{t}\n")

            with open(outpath_labels, 'w', encoding='utf-8') as f:
                f.write('group_num\tterm\tlabel\n')
                for g, terms in group_terms.items():
                    for term in terms:
                        f.write(f"{g}\t{term}\t{labels.get(term, '')}\n")


if __name__ == '__main__':
    main()
