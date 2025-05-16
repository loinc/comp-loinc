#!/usr/bin/env python3

import subprocess
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict
import pandas as pd

def get_comploinc_relationships():
    """Extract subclass relationships from CompLOINC using ROBOT and SPARQL"""
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?parent ?child
    WHERE {
        ?child rdfs:subClassOf ?parent .
    }
    """
    
    # Write query to temporary file
    with open('temp_query.rq', 'w') as f:
        f.write(query)
    
    # Run ROBOT query
    cmd = ['robot', 'query',
           '--input', 'output/build-default/merged-and-reasoned/comploinc-merged-reasoned.owl',
           '--query', 'temp_query.rq',
           '--format', 'tsv']
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse results
    relationships = set()
    for line in result.stdout.strip().split('\n')[1:]:  # Skip header
        if line.strip():
            parent, child = line.strip().split('\t')
            relationships.add((parent, child))
    
    return relationships

def get_loinc_relationships():
    """Extract hierarchical relationships from LOINC XML"""
    tree = ET.parse('loinc_release/Loinc_2.80/loinc.xml')
    root = tree.getroot()
    
    relationships = set()
    for part in root.findall('.//PART'):
        parent = part.find('PARENT')
        code = part.find('CODE')
        if parent is not None and code is not None:
            relationships.add((parent.text, code.text))
    
    return relationships

def get_loinc_snomed_relationships():
    """Extract relationships from LOINC-SNOMED mappings"""
    relationships = set()
    with open('loinc_snomed_release/part-mappings_0.0.3.tsv', 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            # Assuming the file has columns for LOINC part and SNOMED concept
            if 'loinc_part' in row and 'snomed_concept' in row:
                relationships.add((row['loinc_part'], row['snomed_concept']))
    
    return relationships

def calculate_overlap(set1, set2):
    """Calculate the number of overlapping relationships between two sets"""
    return len(set1.intersection(set2))

def main():
    # Get relationships from each source
    comploinc_rels = get_comploinc_relationships()
    loinc_rels = get_loinc_relationships()
    loinc_snomed_rels = get_loinc_snomed_relationships()
    
    # Create overlap matrix
    sources = ['LOINC', 'LOINC-SNOMED', 'CompLOINC']
    relationships = [loinc_rels, loinc_snomed_rels, comploinc_rels]
    
    matrix = []
    for i, source1 in enumerate(sources):
        row = []
        for j, source2 in enumerate(sources):
            if i == j:
                row.append(len(relationships[i]))  # Total relationships in source
            else:
                row.append(calculate_overlap(relationships[i], relationships[j]))
        matrix.append(row)
    
    # Create DataFrame and save to TSV
    df = pd.DataFrame(matrix, index=sources, columns=sources)
    df.to_csv('output/relationship_overlap.tsv', sep='\t')

if __name__ == '__main__':
    main() 