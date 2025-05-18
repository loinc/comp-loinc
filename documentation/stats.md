# *CompLOINC Statistics*




# Entities and axioms
## Entities and axiom counts
| Metric | Value |
| ------ | ----- |
| Annotation properties | 13 |
| Axioms | 2171244 |
| Logical axioms | 965973 |
| Classes | 241874 |
| Object properties | 57 |
| Data properties | 0 |
| Individuals | 0 |

## Axiom types
| Metric | Value |
| ------ | ----- |
| AnnotationAssertion | 963329 |
| EquivalentClasses | 218286 |
| SubObjectPropertyOf | 55 |
| Declaration | 241942 |
| SubClassOf | 747632 |


## Entity namespaces counts
| Metric | Value |
| ------ | ----- |
| owl | 1 |
| rdf | 1 |
| LOINC_PART_GRP_CMP | 2462 |
| LOINC_PART_GRP_SYS | 1697 |
| SNOMED | 1 |
| rdfs | 1 |
| LOINC_PART | 116185 |
| LOINC_PROP | 48 |
| LOINC_PART_GRP_CMP_SYS | 18116 |
| LOINC_TERM | 103424 |
| COMPLOINC_AXIOM | 9 |


## Axiom namespaces counts
| Metric | Value |
| ------ | ----- |
| owl | 1020 |
| LOINC_PART_GRP_CMP | 24720 |
| LOINC_PART_GRP_SYS | 38643 |
| rdfs | 241867 |
| SNOMED | 5890 |
| LOINC_PROP | 1440019 |
| LOINC_PART | 1808312 |
| LOINC_PART_GRP_CMP_SYS | 335370 |
| LOINC_TERM | 1890586 |
| COMPLOINC_AXIOM | 72 |


# Subclass axiom analysis
This analysis shows set totals, intersections, and differences for direct subclass axioms in LOINC, CompLOINC, and 
LOINC-SNOMED Ontology. "Direct" means a direct parent/child relationship, as opposed to "indirect", meaning 2+ degree 
ancestor relationship.  

## Total subclass axioms
|              | n       |
|:-------------|:--------|
| LOINC        | 120,449 |
| LOINC-SNOMED | 11,376  |
| CompLOINC    | 747,632 |

## Merged comparison table
Cell formatting: (%intersection/a) / (n intersection) / (%intersection/b)  
Where 'a' is the ontology represented by the row, and 'b' is the ontology represented by the column. 'n intersection' is 
the total number of subclass axioms in the intersection of the two ontologies. '%intersection/' is the percentage of 
subclass axioms in the intersection of the two ontologies, relative to the total number of subclass axioms in the 
ontology. 

|              | LOINC                   | LOINC-SNOMED          | CompLOINC               |
|:-------------|:------------------------|:----------------------|:------------------------|
| LOINC        | -                       | 0.0% / 0 / 0.0%       | 99.1% / 119,409 / 16.0% |
| LOINC-SNOMED | 0.0% / 0 / 0.0%         | -                     | 96.1% / 10,936 / 1.5%   |
| CompLOINC    | 16.0% / 119,409 / 99.1% | 1.5% / 10,936 / 96.1% | -                       |

## Individual comparison tables
Meaning of table headers:  
"a vs b": 'a' is the ontology on the left side of the comparison, and 'b' is the one on the right side.
- **tot a**: Total number of subclass axioms for ontology on left side of the comparison.
- **% (a-b)**: The percentage of "a - b" (the set difference of a and b) over the total number of axioms in a.
- **n (a-b)**: Total number of subclass axioms in the set difference of a and b.
- **intersection**: The length of the intersection
- **tot b**: Total number of subclass axioms for ontology on left side of the comparison.
- **n (b-a)**: Total number of subclass axioms in the set difference of b and a.
- **% (b-a)**: The percentage of "b - a" (the set difference of b and a) over the total number of axioms in b.


### LOINC

#### vs LOINC-SNOMED

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 100.0%    |    120449 |  120449 |              0 |   11376 |     11376 | 100.0%    |


#### vs CompLOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 0.9%      |      1040 |  120449 |         119409 |  747632 |    628223 | 84.0%     |



### LOINC-SNOMED

#### vs LOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 100.0%    |     11376 |   11376 |              0 |  120449 |    120449 | 100.0%    |


#### vs CompLOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 3.9%      |       440 |   11376 |          10936 |  747632 |    736696 | 98.5%     |



### CompLOINC

#### vs LOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 84.0%     |    628223 |  747632 |         119409 |  120449 |      1040 | 0.9%      |


#### vs LOINC-SNOMED

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 98.5%     |    736696 |  747632 |          10936 |   11376 |       440 | 3.9%      |



# Dangling part terms
These are parts that do not fall in the hierarchy in LOINC, but for which CompLOINC attempts to incorporate.

Similarity threshold: 0.5

| Part | n | Percentage |
|----------|-------|------------|
| All parts | 72740 | 100% |
| Non-dangling | 38951 | 53.5% |
| Dangling | 33789 | 46.5% |
| (Dangling >= threshold) / dangling | 17955 | 53.1% |
| (Dangling >= threshold) / all | 17955 | 24.7% |

# Additional statistics
## Expressivity
| Metric | Value |
| ------ | ----- |
| Expressivity | ALEH |
| OWL2 | True |
| OWL2 DL | True |
| OWL2 EL | True |
| OWL2 QL | False |
| OWL2 RL | False |

## Class expressions used
| Metric | Value |
| ------ | ----- |
| Class | 3383067 |
| ObjectSomeValuesFrom | 1515211 |
| ObjectIntersectionOf | 208040 |

