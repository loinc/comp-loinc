"""Analyze supplemental equivalent class defs

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
"""
import argparse
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


OWL = '{http://www.w3.org/2002/07/owl#}'
RDF = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
THIS_FILE = Path(__file__)
PROJ_DIR = THIS_FILE.parent.parent
INPATH = PROJ_DIR / 'output/build-default/merged-and-reasoned/canonical/comploinc-merged-reasoned-all-supplementary.owl'
OUTPATH = PROJ_DIR / 'equivalent_groups.tsv'


def extract_pairs(intersection: ET.Element) -> List[Tuple[str, str]]:
    """todo"""
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


def parse_file(path: str) -> Dict[Tuple[Tuple[str, str], ...], List[str]]:
    """todo"""
    tree = ET.parse(path)
    root = tree.getroot()
    groups: Dict[Tuple[Tuple[str, str], ...], List[str]] = defaultdict(list)
    for cls in root.findall(f'.//{OWL}Class'):
        term_uri = cls.get(f'{RDF}about') or cls.get(f'{RDF}ID')
        if not term_uri:
            continue
        term = term_uri.rsplit('/', 1)[-1]
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
    return groups


def generate_rows(groups: Dict[Tuple[Tuple[str, str], ...], List[str]]):
    """todo"""
    rows = []
    group_num = 0
    for key, terms in groups.items():
        if len(terms) < 2:
            continue
        group_num += 1
        term_str = '|'.join(sorted(terms))
        for prop, val in key:
            rows.append((group_num, prop, val, term_str))
    return rows


def main():
    """todo"""
    parser = argparse.ArgumentParser(description='Group LOINC terms by equivalent class definitions.')
    parser.add_argument(
        '-i', '--inpath', help='Path to comploinc-merged-reasoned-all-supplementary.owl', default=INPATH)
    parser.add_argument('-o', '--outpath', default=OUTPATH, help='Output TSV file')
    args = parser.parse_args()

    groups = parse_file(args.inpath)
    rows = generate_rows(groups)

    with open(args.outpath, 'w', encoding='utf-8') as f:
        f.write('group_num\tproperty\tvalue\tterms\n')
        for g, p, v, t in rows:
            f.write(f"{g}\t{p}\t{v}\t{t}\n")


if __name__ == '__main__':
    main()
