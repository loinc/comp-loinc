# *CompLOINC Statistics*




# Entities and axioms
## Entities and axiom counts
| Metric | Value |
| ------ | ----- |
| Annotation properties | 13 |
| Axioms | 1689913 |
| Logical axioms | 484643 |
| Classes | 241874 |
| Object properties | 56 |
| Data properties | 0 |
| Individuals | 0 |

## Axiom types
| Metric | Value |
| ------ | ----- |
| AnnotationAssertion | 963329 |
| EquivalentClasses | 123324 |
| SubObjectPropertyOf | 55 |
| Declaration | 241941 |
| SubClassOf | 361264 |


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
| LOINC_PROP | 47 |
| LOINC_PART_GRP_CMP_SYS | 18116 |
| LOINC_TERM | 103424 |
| COMPLOINC_AXIOM | 9 |


## Axiom namespaces counts
| Metric | Value |
| ------ | ----- |
| owl | 1020 |
| LOINC_PART_GRP_CMP | 20345 |
| LOINC_PART_GRP_SYS | 13868 |
| rdfs | 241867 |
| SNOMED | 5890 |
| LOINC_PART | 1227021 |
| LOINC_PROP | 858727 |
| LOINC_PART_GRP_CMP_SYS | 104012 |
| LOINC_TERM | 1283396 |
| COMPLOINC_AXIOM | 72 |


# Subclass axiom analysis
This analysis shows set totals, intersections, and differences for direct subclass axioms in LOINC, CompLOINC, and 
LOINC-SNOMED Ontology. "Direct" means a direct parent/child relationship, as opposed to "indirect", meaning 2+ degree 
ancestor relationship.  

## Total subclass axioms
|              | n       |
|:-------------|:--------|
| LOINC        | 120,334 |
| LOINC-SNOMED | 11,385  |
| CompLOINC    | 361,264 |

## Comparison: Upset plot
![Upset plot](upset.png)

In this upset plot, we observe both CompLOINC's large count of subclass axioms, and its nearly full inclusion of 
subclass axioms from sources. In the upset plot, horizontal bars represent the proportion of each terminology's subclass
axioms relative to the total number of unique subclass axioms across all three resources. Vertical bars represent the 
proportion of subclass axioms belonging to specific combinations of terminology resources, with each column showing a 
distinct intersection pattern as indicated by the connected dots below.

## Comparison: Merged table
Cell formatting: (%intersection/a) / (n intersection) / (%intersection/b)

Where 'a' is the ontology represented by the row, and 'b' is the ontology represented by the column. 'n intersection' is 
the total number of subclass axioms in the intersection of the two ontologies. '%intersection/' is the percentage of 
subclass axioms in the intersection of the two ontologies, relative to the total number of subclass axioms in the 
ontology. 

|              | LOINC                   | LOINC-SNOMED          | CompLOINC               |
|:-------------|:------------------------|:----------------------|:------------------------|
| LOINC        | -                       | 0.0% / 0 / 0.0%       | 99.2% / 119,410 / 33.1% |
| LOINC-SNOMED | 0.0% / 0 / 0.0%         | -                     | 96.1% / 10,937 / 3.0%   |
| CompLOINC    | 33.1% / 119,410 / 99.2% | 3.0% / 10,937 / 96.1% | -                       |

## Comparison: Individual tables
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
| 100.0%    |    120334 |  120334 |              0 |   11385 |     11385 | 100.0%    |


#### vs CompLOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 0.8%      |       924 |  120334 |         119410 |  361264 |    241854 | 66.9%     |



### LOINC-SNOMED

#### vs LOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 100.0%    |     11385 |   11385 |              0 |  120334 |    120334 | 100.0%    |


#### vs CompLOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 3.9%      |       448 |   11385 |          10937 |  361264 |    350327 | 97.0%     |



### CompLOINC

#### vs LOINC

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 66.9%     |    241854 |  361264 |         119410 |  120334 |       924 | 0.8%      |


#### vs LOINC-SNOMED

| % (a-b)   |   n (a-b) |   tot a |   intersection |   tot b |   n (b-a) | % (b-a)   |
|:----------|----------:|--------:|---------------:|--------:|----------:|:----------|
| 97.0%     |    350327 |  361264 |          10937 |   11385 |       448 | 3.9%      |



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
| Class | 1934078 |
| ObjectSomeValuesFrom | 933920 |
| ObjectIntersectionOf | 113078 |

