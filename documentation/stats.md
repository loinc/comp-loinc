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
# Classification depth analysis 
This measures how deep into the hierarchy each class is. E.g. if the root of the hierarchy is TermA, and we have axioms
(TermC subClassOf TermB) and (TermB subClassOf TermA), then TermC is at depth 3, TermB is at depth 2, and TermA is at 
depth 1.

## Web application: https://comp-loinc.onrender.com/
Can take ~5 minutes to load when asleep. Sleeps when unused for 15 minutes. Contains interactive variations of these 
plots.

## Polyhierarchies
**Impact on class depths**  
CompLOINC and the LOINC and LOINC-SNOMED representations are all polyhierarchies. This means that classes can appear 
multiple times. For this analysis, we have decided to include every occurrence of a class in the counts. For example, if
a class appears in 3 subtrees, once at depth 3, and in two subtrees at depth 2, this class will be tallied twice at 
depth 2, and once at depth 3. 

**Disaggregating major subtrees**  
CompLOINC and LOINC have more than 1 top-level branches (AKA subhierarchies or subtrees).

| Terminology | Hierarchy name   | Root URI                        |
|-------------|------------------|---------------------------------|
| CompLOINC   | SNOMED-Inspired  | https://loinc.org/138875005     |
| CompLOINC   | LoincTerm        | https://loinc.org/LoincTerm     |
| CompLOINC   | CompLOINC Groups | http://comploinc/group          |
| CompLOINC   | LoincPart        | https://loinc.org/LoincPart     |
| LOINC       | LOINC Categories | https://loinc.org/LoincCategory |
| LOINC       | LOINC Groups     | https://loinc.org/LoincGroup    |
| LOINC       | LoincPart        | https://loinc.org/LoincPart     |

Note, by subtree:
- *SNOMED-Inspired*: This is inspired largely by the LOINC-SNOMED Ontology.
- *LoincTerm*: LOINC has no Term hierarchy. It has a part hierarchy in the tree browser (https://loinc.org/tree/), which 
has parts as leaves. CompLOINC has a term hierarchy based on inference, combining the part hierarchy from the tree 
browser with supplementary or primary part model definitions.
- *LoincPart*: Exists in the LOINC tree browser, but not the official LOINC release. CompLOINC includes it as an 
optional subtree, largely obtained.
- *LOINC Groups*: Part of the LOINC release. See more: https://loinc.org/groups/. Terms are grouped, and some groups 
have groups. Also just for this analysis, we have added a single, novel https://loinc.org/LoincGroup root as a parent of
the otherwise top level groups in the LOINC release.
- *LOINC Categories*: Part of  the LOINC release, but not as formal as LOINC groups. These categories have no URIs, just 
labels. They are parents only of groups, not terms. From https://loinc.org/groups/: 'Category: A short description that 
identifies the general purpose of the group, such as "Flowsheet", "Reportable microbiology" or "Document ontology 
grouped by role and subject matter domain".'
- *CompLOINC Groups*: CompLOINC has a novel grouping class hierarchy. It does not utilize LOINC groups or categories in 
the LOINC release. The top level class is "http://comploinc/group", followed by a major group branch for each "property 
axis" (that is, a single part property or combination thereof), e.g. "http://comploinc/group/component/". Then, groups 
which are defined via these properties descend from there. 

**Two sets of outputs**  
In many cases, the best way to use each of these is not to use the entire polyhierarchy, but individual major subtrees. 
As such, we have produced a set of "by hierarchy" outputs, where these major subtrees have been disaggregated. The other
set of outputs aggregates all of the subtrees together in its counts. 

## Class types
We consider the following 3 types of classes: terms, parts, and groups. There are 3 sets of outputs with respect to 
class types: terms only, terms+groups, and terms+groups+parts.

There are also different kinds of possible axioms in CompLOINC, LOINC, and LOINC-SNOMED Ontology, with respect to class 
types.  

Homogeneous
- term --> term
- part --> part
- group --> group

Heterogeneous
- term --> part
- part --> term
- term --> group
- group --> term
- part --> group
- group --> part 

For a given filter of class type, we discard any subclass axioms where either the parent or child is not included. So, 
for example if we are only looking at 'terms', we only consider the term-->term axioms. If we are looking at 
'terms+groups', we retain axioms for term-->term, group-->group, term-->group, and group-->term.

## Dangling classes  
Dangling classes are not represented here in this class depth analysis.

**Ramifications for CompLOINC**  
The only dangling classes in CompLOINC are dangling parts from the LOINC release, specifically the ones which CompLOINC 
was not able to find matches. Those classes are not represented here.

**Ramifications for LOINC representation**  
Note that this results in LOINC showing that it has 0 terms at any depths, as LOINC has no term hierarchy. The only 
hierarchies that exist in LOINC are a shallow grouping hierarchy (represented by CSVs in `AccessoryFiles/GroupFile/` in 
the LOINC release, and the part hierarchy, which is not represented in the release, but only exists in the LOINC tree 
browser (https://loinc.org/tree/). Regarding parts, there are also a large number of those that are dangling even after 
when considering all of the tree browser hierarchies, and those as well are not represented here. 

**Dangling subtrees**  
There is also the case where, as a result of filtering class types, there end up being dangling sub-trees. For example, 
it could be that somewhere in a hierarchy, there is a term-group axiom, which is the root of its own subtree. If we are 
filtering to show terms only, then this axiom gets removed, leaving its descendants (subtree) dangling. This subtree may
contain term-term axioms, which would otherwise be kept, but since they are part of a dangling subtree, they are 
removed. 

## CompLOINC representation
**Grouping class depths adjusted via synthetic "master grouping classes"**  
This particular analysis makes small modifications to the CompLOINC representation with respect to groups. In the 
CompLOINC .owl artefacts, there are many top-level grouping classes at the root of the ontology. These top level 
grouping classes come in various sets, one for each LOINC property or combination of properties used to construct the 
groups. For example, the grouping class http://comploinc/group/component/LP16066-0 falls under the "component" property 
axis, while the grouping class http://comploinc/group/component-system/LP7795-0-LP310005-6 falls under the 
"component+system" property (combination) axis. If these parts for these properties have no parents, then these grouping
classes will reside at the root of CompLOINC. However, for these classification depth analyses, we are comparing against 
other subtrees that have a single root, e.g. LoincPart or LoincTerm. Therefore, for the depths to be consistent along 
class types (terms, parts, groups), we have included "master grouping classes" just for this analysis. The top level for
all grouping classes is http://comploinc/group/ ("GRP"), and the children of this class are all of the roots of each 
property axis, e.g. http://comploinc/group/component/ ("GRP_CMP"), http://comploinc/group/component-system/ ("GRP_SYS"),
and so on.

## LOINC representation
LOINC itself does not have an `.owl` representation, but for this analysis we constructed one. The following are some 
caveats about the representation, by class type.

**Terms**  
LOINC defines no term-term subclass relationships. It only defines term-group relationships. Therefore, for the analyses 
where we consider only terms, the term-group subclass axioms are intentionally dropped, resulting in no axioms at all, 
and therefore rendering LOINC to show 0 classes at any depth.  

**Parts**  
Some variations of the outputs include part classes. The LOINC release does not establish part-part subclass 
relationships. These relationships are obtained by exports from the LOINC tree browser: https://loinc.org/tree/.

**Groups**  
Some variations of the outputs include parts group classes. While the LOINC release does not have term-term or part-part
subclass axioms, it does have such "axioms" for group-group and term-group. `Group.csv`: Defines relationships between 
groups and parent groups. `GroupLoincTerms.csv`: Defines relationships between terms (`LoincNumber` column) and groups 
(`GroupId` column). Also defines relationships between categories (`Category` column) and groups/terms. For this 
analysis, we consider categories to be just another kind of group. This results in our representation of LOINC groups 
being a polyhierarchy, as terms and groups can fall under other groups, but also can fall under categories. Thus, such 
terms and groups will be counted multiple times in the depths counts. 

More information about LOINC groups can be found here: https://loinc.org/groups/

---



## Number of classes (terms)
![Number of classes (terms)](analyses/class-depth/plot-class-depth_terms_totals.png)

|   Depth |   LOINC | LOINC-SNOMED   | CompLOINC-Primary   | CompLOINC-Supplementary   |
|---------|---------|----------------|---------------------|---------------------------|
|       1 |       0 | 1              | 2                   | 2                         |
|       2 |       0 | 10             | 14                  | 14                        |
|       3 |       0 | 67             | 216                 | 216                       |
|       4 |       0 | 394            | 43,085              | 47,815                    |
|       5 |       0 | 815            | 40,624              | 37,256                    |
|       6 |       0 | 1,649          | 15,714              | 12,216                    |
|       7 |       0 | 2,033          | 7,475               | 4,727                     |
|       8 |       0 | 1,955          | 4,170               | 2,929                     |
|       9 |       0 | 1,998          | 2,509               | 2,185                     |
|      10 |       0 | 2,289          | 2,408               | 2,314                     |
|      11 |       0 | 2,632          | 2,718               | 2,710                     |
|      12 |       0 | 2,180          | 2,358               | 2,356                     |
|      13 |       0 | 1,191          | 1,314               | 1,314                     |
|      14 |       0 | 1,226          | 1,291               | 1,291                     |
|      15 |       0 | 611            | 610                 | 610                       |
|      16 |       0 | 630            | 651                 | 651                       |
|      17 |       0 | 876            | 895                 | 895                       |
|      18 |       0 | 1,506          | 1,519               | 1,519                     |
|      19 |       0 | 1,291          | 1,303               | 1,303                     |
|      20 |       0 | 701            | 705                 | 705                       |
|      21 |       0 | 492            | 492                 | 492                       |
|      22 |       0 | 56             | 56                  | 56                        |
|      23 |       0 | 9              | 9                   | 9                         |
|      24 |       0 | 2              | 2                   | 2                         |
|      25 |       0 | 1              | 1                   | 1                         |



## % of classes (terms)
![% of classes (terms)](analyses/class-depth/plot-class-depth_terms_percentages.png)

|   Depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
|---------|---------|----------------|---------------------|---------------------------|
|       1 |       0 |         0.0041 |             0.0015  |                   0.0016  |
|       2 |       0 |         0.041  |             0.011   |                   0.011   |
|       3 |       0 |         0.27   |             0.17    |                   0.17    |
|       4 |       0 |         1.6    |            33       |                  39       |
|       5 |       0 |         3.3    |            31       |                  30       |
|       6 |       0 |         6.7    |            12       |                   9.9     |
|       7 |       0 |         8.3    |             5.7     |                   3.8     |
|       8 |       0 |         7.9    |             3.2     |                   2.4     |
|       9 |       0 |         8.1    |             1.9     |                   1.8     |
|      10 |       0 |         9.3    |             1.9     |                   1.9     |
|      11 |       0 |        11      |             2.1     |                   2.2     |
|      12 |       0 |         8.9    |             1.8     |                   1.9     |
|      13 |       0 |         4.8    |             1       |                   1.1     |
|      14 |       0 |         5      |             0.99    |                   1       |
|      15 |       0 |         2.5    |             0.47    |                   0.49    |
|      16 |       0 |         2.6    |             0.5     |                   0.53    |
|      17 |       0 |         3.6    |             0.69    |                   0.72    |
|      18 |       0 |         6.1    |             1.2     |                   1.2     |
|      19 |       0 |         5.2    |             1       |                   1.1     |
|      20 |       0 |         2.8    |             0.54    |                   0.57    |
|      21 |       0 |         2      |             0.38    |                   0.4     |
|      22 |       0 |         0.23   |             0.043   |                   0.045   |
|      23 |       0 |         0.037  |             0.0069  |                   0.0073  |
|      24 |       0 |         0.0081 |             0.0015  |                   0.0016  |
|      25 |       0 |         0.0041 |             0.00077 |                   0.00081 |



## Number of classes (terms), by hierarchy
![Number of classes (terms), by hierarchy](analyses/class-depth/plot-class-depth_by-hierarchy_terms_totals.png)

|   Depth |   LOINC | LOINC-SNOMED   | CompLOINC-Primary - LoincTerm   | CompLOINC-Primary - SNOMED-Inspired   | CompLOINC-Supplementary - LoincTerm   | CompLOINC-Supplementary - SNOMED-Inspired   |
|---------|---------|----------------|---------------------------------|---------------------------------------|---------------------------------------|---------------------------------------------|
|       1 |       0 | 1              | 1                               | 1                                     | 1                                     | 1                                           |
|       2 |       0 | 10             | 4                               | 10                                    | 4                                     | 10                                          |
|       3 |       0 | 67             | 151                             | 65                                    | 151                                   | 65                                          |
|       4 |       0 | 394            | 42,716                          | 369                                   | 47,446                                | 369                                         |
|       5 |       0 | 815            | 39,847                          | 777                                   | 36,479                                | 777                                         |
|       6 |       0 | 1,649          | 14,115                          | 1,599                                 | 10,617                                | 1,599                                       |
|       7 |       0 | 2,033          | 5,504                           | 1,971                                 | 2,756                                 | 1,971                                       |
|       8 |       0 | 1,955          | 2,232                           | 1,938                                 | 991                                   | 1,938                                       |
|       9 |       0 | 1,998          | 492                             | 2,017                                 | 168                                   | 2,017                                       |
|      10 |       0 | 2,289          | 106                             | 2,302                                 | 12                                    | 2,302                                       |
|      11 |       0 | 2,632          | 9                               | 2,709                                 | 1                                     | 2,709                                       |
|      12 |       0 | 2,180          | 2                               | 2,356                                 | 0                                     | 2,356                                       |
|      13 |       0 | 1,191          | 0                               | 1,314                                 | 0                                     | 1,314                                       |
|      14 |       0 | 1,226          | 0                               | 1,291                                 | 0                                     | 1,291                                       |
|      15 |       0 | 611            | 0                               | 610                                   | 0                                     | 610                                         |
|      16 |       0 | 630            | 0                               | 651                                   | 0                                     | 651                                         |
|      17 |       0 | 876            | 0                               | 895                                   | 0                                     | 895                                         |
|      18 |       0 | 1,506          | 0                               | 1,519                                 | 0                                     | 1,519                                       |
|      19 |       0 | 1,291          | 0                               | 1,303                                 | 0                                     | 1,303                                       |
|      20 |       0 | 701            | 0                               | 705                                   | 0                                     | 705                                         |
|      21 |       0 | 492            | 0                               | 492                                   | 0                                     | 492                                         |
|      22 |       0 | 56             | 0                               | 56                                    | 0                                     | 56                                          |
|      23 |       0 | 9              | 0                               | 9                                     | 0                                     | 9                                           |
|      24 |       0 | 2              | 0                               | 2                                     | 0                                     | 2                                           |
|      25 |       0 | 1              | 0                               | 1                                     | 0                                     | 1                                           |



## % of classes (terms), by hierarchy
![% of classes (terms), by hierarchy](analyses/class-depth/plot-class-depth_by-hierarchy_terms_percentages.png)

|   Depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary - LoincTerm |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Supplementary - LoincTerm |   CompLOINC-Supplementary - SNOMED-Inspired |
|---------|---------|----------------|---------------------------------|---------------------------------------|---------------------------------------|---------------------------------------------|
|       1 |       0 |         0.0041 |                         0.00095 |                                 0.004 |                                0.001  |                                       0.004 |
|       2 |       0 |         0.041  |                         0.0038  |                                 0.04  |                                0.0041 |                                       0.04  |
|       3 |       0 |         0.27   |                         0.14    |                                 0.26  |                                0.15   |                                       0.26  |
|       4 |       0 |         1.6    |                        41       |                                 1.5   |                               48      |                                       1.5   |
|       5 |       0 |         3.3    |                        38       |                                 3.1   |                               37      |                                       3.1   |
|       6 |       0 |         6.7    |                        13       |                                 6.4   |                               11      |                                       6.4   |
|       7 |       0 |         8.3    |                         5.2     |                                 7.9   |                                2.8    |                                       7.9   |
|       8 |       0 |         7.9    |                         2.1     |                                 7.8   |                                1      |                                       7.8   |
|       9 |       0 |         8.1    |                         0.47    |                                 8.1   |                                0.17   |                                       8.1   |
|      10 |       0 |         9.3    |                         0.1     |                                 9.2   |                                0.012  |                                       9.2   |
|      11 |       0 |        11      |                         0.0086  |                                11     |                                0.001  |                                      11     |
|      12 |       0 |         8.9    |                         0.0019  |                                 9.4   |                                0      |                                       9.4   |
|      13 |       0 |         4.8    |                         0       |                                 5.3   |                                0      |                                       5.3   |
|      14 |       0 |         5      |                         0       |                                 5.2   |                                0      |                                       5.2   |
|      15 |       0 |         2.5    |                         0       |                                 2.4   |                                0      |                                       2.4   |
|      16 |       0 |         2.6    |                         0       |                                 2.6   |                                0      |                                       2.6   |
|      17 |       0 |         3.6    |                         0       |                                 3.6   |                                0      |                                       3.6   |
|      18 |       0 |         6.1    |                         0       |                                 6.1   |                                0      |                                       6.1   |
|      19 |       0 |         5.2    |                         0       |                                 5.2   |                                0      |                                       5.2   |
|      20 |       0 |         2.8    |                         0       |                                 2.8   |                                0      |                                       2.8   |
|      21 |       0 |         2      |                         0       |                                 2     |                                0      |                                       2     |
|      22 |       0 |         0.23   |                         0       |                                 0.22  |                                0      |                                       0.22  |
|      23 |       0 |         0.037  |                         0       |                                 0.036 |                                0      |                                       0.036 |
|      24 |       0 |         0.0081 |                         0       |                                 0.008 |                                0      |                                       0.008 |
|      25 |       0 |         0.0041 |                         0       |                                 0.004 |                                0      |                                       0.004 |



## Number of classes (terms, groups)
![Number of classes (terms, groups)](analyses/class-depth/plot-class-depth_terms-groups_totals.png)

|   Depth | LOINC   | LOINC-SNOMED   | CompLOINC-Primary   | CompLOINC-Supplementary   |
|---------|---------|----------------|---------------------|---------------------------|
|       1 | 2       | 1              | 3                   | 3                         |
|       2 | 61      | 10             | 17                  | 17                        |
|       3 | 7,168   | 67             | 22,409              | 22,403                    |
|       4 | 30,327  | 394            | 101,331             | 69,073                    |
|       5 | 0       | 815            | 109,235             | 58,044                    |
|       6 | 0       | 1,649          | 104,091             | 32,920                    |
|       7 | 0       | 2,033          | 101,076             | 24,904                    |
|       8 | 0       | 1,955          | 95,687              | 21,590                    |
|       9 | 0       | 1,998          | 86,113              | 17,708                    |
|      10 | 0       | 2,289          | 72,782              | 14,359                    |
|      11 | 0       | 2,632          | 62,977              | 11,845                    |
|      12 | 0       | 2,180          | 52,640              | 9,092                     |
|      13 | 0       | 1,191          | 43,809              | 6,070                     |
|      14 | 0       | 1,226          | 33,786              | 4,143                     |
|      15 | 0       | 611            | 24,311              | 2,060                     |
|      16 | 0       | 630            | 16,646              | 1,200                     |
|      17 | 0       | 876            | 10,378              | 1,066                     |
|      18 | 0       | 1,506          | 5,434               | 1,534                     |
|      19 | 0       | 1,291          | 2,715               | 1,304                     |
|      20 | 0       | 701            | 990                 | 705                       |
|      21 | 0       | 492            | 526                 | 492                       |
|      22 | 0       | 56             | 58                  | 56                        |
|      23 | 0       | 9              | 9                   | 9                         |
|      24 | 0       | 2              | 2                   | 2                         |
|      25 | 0       | 1              | 1                   | 1                         |



## % of classes (terms, groups)
![% of classes (terms, groups)](analyses/class-depth/plot-class-depth_terms-groups_percentages.png)

|   Depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
|---------|---------|----------------|---------------------|---------------------------|
|       1 |  0.0053 |         0.0041 |             0.00032 |                   0.001   |
|       2 |  0.16   |         0.041  |             0.0018  |                   0.0057  |
|       3 | 19      |         0.27   |             2.4     |                   7.5     |
|       4 | 81      |         1.6    |            11       |                  23       |
|       5 |  0      |         3.3    |            12       |                  19       |
|       6 |  0      |         6.7    |            11       |                  11       |
|       7 |  0      |         8.3    |            11       |                   8.3     |
|       8 |  0      |         7.9    |            10       |                   7.2     |
|       9 |  0      |         8.1    |             9.1     |                   5.9     |
|      10 |  0      |         9.3    |             7.7     |                   4.8     |
|      11 |  0      |        11      |             6.6     |                   3.9     |
|      12 |  0      |         8.9    |             5.6     |                   3       |
|      13 |  0      |         4.8    |             4.6     |                   2       |
|      14 |  0      |         5      |             3.6     |                   1.4     |
|      15 |  0      |         2.5    |             2.6     |                   0.69    |
|      16 |  0      |         2.6    |             1.8     |                   0.4     |
|      17 |  0      |         3.6    |             1.1     |                   0.35    |
|      18 |  0      |         6.1    |             0.57    |                   0.51    |
|      19 |  0      |         5.2    |             0.29    |                   0.43    |
|      20 |  0      |         2.8    |             0.1     |                   0.23    |
|      21 |  0      |         2      |             0.056   |                   0.16    |
|      22 |  0      |         0.23   |             0.0061  |                   0.019   |
|      23 |  0      |         0.037  |             0.00095 |                   0.003   |
|      24 |  0      |         0.0081 |             0.00021 |                   0.00067 |
|      25 |  0      |         0.0041 |             0.00011 |                   0.00033 |



## Number of classes (terms, groups), by hierarchy
![Number of classes (terms, groups), by hierarchy](analyses/class-depth/plot-class-depth_by-hierarchy_terms-groups_totals.png)

|   Depth | LOINC - LOINC Categories   | LOINC - LOINC Groups   | LOINC-SNOMED   | CompLOINC-Primary - CompLOINC Groups   | CompLOINC-Primary - LoincTerm   | CompLOINC-Primary - SNOMED-Inspired   | CompLOINC-Supplementary - CompLOINC Groups   | CompLOINC-Supplementary - LoincTerm   | CompLOINC-Supplementary - SNOMED-Inspired   |
|---------|----------------------------|------------------------|----------------|----------------------------------------|---------------------------------|---------------------------------------|----------------------------------------------|---------------------------------------|---------------------------------------------|
|       1 | 1                          | 1                      | 1              | 1                                      | 1                               | 1                                     | 1                                            | 1                                     | 1                                           |
|       2 | 16                         | 45                     | 10             | 3                                      | 4                               | 10                                    | 3                                            | 4                                     | 10                                          |
|       3 | 7,130                      | 7,168                  | 67             | 22,193                                 | 151                             | 65                                    | 22,187                                       | 151                                   | 65                                          |
|       4 | 30,327                     | 30,327                 | 394            | 100,519                                | 79,704                          | 369                                   | 21,258                                       | 47,446                                | 369                                         |
|       5 | 0                          | 0                      | 815            | 107,919                                | 87,670                          | 777                                   | 20,788                                       | 36,479                                | 777                                         |
|       6 | 0                          | 0                      | 1,649          | 102,254                                | 81,788                          | 1,599                                 | 20,704                                       | 10,617                                | 1,599                                       |
|       7 | 0                          | 0                      | 2,033          | 99,103                                 | 78,928                          | 1,971                                 | 20,177                                       | 2,756                                 | 1,971                                       |
|       8 | 0                          | 0                      | 1,955          | 93,749                                 | 75,088                          | 1,938                                 | 18,661                                       | 991                                   | 1,938                                       |
|       9 | 0                          | 0                      | 1,998          | 84,096                                 | 68,573                          | 2,017                                 | 15,523                                       | 168                                   | 2,017                                       |
|      10 | 0                          | 0                      | 2,289          | 70,480                                 | 58,435                          | 2,302                                 | 12,045                                       | 12                                    | 2,302                                       |
|      11 | 0                          | 0                      | 2,632          | 60,268                                 | 51,133                          | 2,709                                 | 9,135                                        | 1                                     | 2,709                                       |
|      12 | 0                          | 0                      | 2,180          | 50,284                                 | 43,548                          | 2,356                                 | 6,736                                        | 0                                     | 2,356                                       |
|      13 | 0                          | 0                      | 1,191          | 42,495                                 | 37,739                          | 1,314                                 | 4,756                                        | 0                                     | 1,314                                       |
|      14 | 0                          | 0                      | 1,226          | 32,495                                 | 29,643                          | 1,291                                 | 2,852                                        | 0                                     | 1,291                                       |
|      15 | 0                          | 0                      | 611            | 23,701                                 | 22,251                          | 610                                   | 1,450                                        | 0                                     | 610                                         |
|      16 | 0                          | 0                      | 630            | 15,995                                 | 15,446                          | 651                                   | 549                                          | 0                                     | 651                                         |
|      17 | 0                          | 0                      | 876            | 9,483                                  | 9,312                           | 895                                   | 171                                          | 0                                     | 895                                         |
|      18 | 0                          | 0                      | 1,506          | 3,915                                  | 3,900                           | 1,519                                 | 15                                           | 0                                     | 1,519                                       |
|      19 | 0                          | 0                      | 1,291          | 1,412                                  | 1,411                           | 1,303                                 | 1                                            | 0                                     | 1,303                                       |
|      20 | 0                          | 0                      | 701            | 285                                    | 285                             | 705                                   | 0                                            | 0                                     | 705                                         |
|      21 | 0                          | 0                      | 492            | 34                                     | 34                              | 492                                   | 0                                            | 0                                     | 492                                         |
|      22 | 0                          | 0                      | 56             | 2                                      | 2                               | 56                                    | 0                                            | 0                                     | 56                                          |
|      23 | 0                          | 0                      | 9              | 0                                      | 0                               | 9                                     | 0                                            | 0                                     | 9                                           |
|      24 | 0                          | 0                      | 2              | 0                                      | 0                               | 2                                     | 0                                            | 0                                     | 2                                           |
|      25 | 0                          | 0                      | 1              | 0                                      | 0                               | 1                                     | 0                                            | 0                                     | 1                                           |



## % of classes (terms, groups), by hierarchy
![% of classes (terms, groups), by hierarchy](analyses/class-depth/plot-class-depth_by-hierarchy_terms-groups_percentages.png)

|   Depth |   LOINC - LOINC Categories |   LOINC - LOINC Groups |   LOINC-SNOMED |   CompLOINC-Primary - CompLOINC Groups |   CompLOINC-Primary - LoincTerm |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Supplementary - CompLOINC Groups |   CompLOINC-Supplementary - LoincTerm |   CompLOINC-Supplementary - SNOMED-Inspired |
|---------|----------------------------|------------------------|----------------|----------------------------------------|---------------------------------|---------------------------------------|----------------------------------------------|---------------------------------------|---------------------------------------------|
|       1 |                     0.0027 |                 0.0027 |         0.0041 |                                0.00011 |                         0.00013 |                                 0.004 |                                      0.00056 |                                0.001  |                                       0.004 |
|       2 |                     0.043  |                 0.12   |         0.041  |                                0.00033 |                         0.00054 |                                 0.04  |                                      0.0017  |                                0.0041 |                                       0.04  |
|       3 |                    19      |                19      |         0.27   |                                2.4     |                         0.02    |                                 0.26  |                                     13       |                                0.15   |                                       0.26  |
|       4 |                    81      |                81      |         1.6    |                               11       |                        11       |                                 1.5   |                                     12       |                               48      |                                       1.5   |
|       5 |                     0      |                 0      |         3.3    |                               12       |                        12       |                                 3.1   |                                     12       |                               37      |                                       3.1   |
|       6 |                     0      |                 0      |         6.7    |                               11       |                        11       |                                 6.4   |                                     12       |                               11      |                                       6.4   |
|       7 |                     0      |                 0      |         8.3    |                               11       |                        11       |                                 7.9   |                                     11       |                                2.8    |                                       7.9   |
|       8 |                     0      |                 0      |         7.9    |                               10       |                        10       |                                 7.8   |                                     11       |                                1      |                                       7.8   |
|       9 |                     0      |                 0      |         8.1    |                                9.1     |                         9.2     |                                 8.1   |                                      8.8     |                                0.17   |                                       8.1   |
|      10 |                     0      |                 0      |         9.3    |                                7.7     |                         7.8     |                                 9.2   |                                      6.8     |                                0.012  |                                       9.2   |
|      11 |                     0      |                 0      |        11      |                                6.5     |                         6.9     |                                11     |                                      5.2     |                                0.001  |                                      11     |
|      12 |                     0      |                 0      |         8.9    |                                5.5     |                         5.8     |                                 9.4   |                                      3.8     |                                0      |                                       9.4   |
|      13 |                     0      |                 0      |         4.8    |                                4.6     |                         5.1     |                                 5.3   |                                      2.7     |                                0      |                                       5.3   |
|      14 |                     0      |                 0      |         5      |                                3.5     |                         4       |                                 5.2   |                                      1.6     |                                0      |                                       5.2   |
|      15 |                     0      |                 0      |         2.5    |                                2.6     |                         3       |                                 2.4   |                                      0.82    |                                0      |                                       2.4   |
|      16 |                     0      |                 0      |         2.6    |                                1.7     |                         2.1     |                                 2.6   |                                      0.31    |                                0      |                                       2.6   |
|      17 |                     0      |                 0      |         3.6    |                                1       |                         1.2     |                                 3.6   |                                      0.097   |                                0      |                                       3.6   |
|      18 |                     0      |                 0      |         6.1    |                                0.43    |                         0.52    |                                 6.1   |                                      0.0085  |                                0      |                                       6.1   |
|      19 |                     0      |                 0      |         5.2    |                                0.15    |                         0.19    |                                 5.2   |                                      0.00056 |                                0      |                                       5.2   |
|      20 |                     0      |                 0      |         2.8    |                                0.031   |                         0.038   |                                 2.8   |                                      0       |                                0      |                                       2.8   |
|      21 |                     0      |                 0      |         2      |                                0.0037  |                         0.0046  |                                 2     |                                      0       |                                0      |                                       2     |
|      22 |                     0      |                 0      |         0.23   |                                0.00022 |                         0.00027 |                                 0.22  |                                      0       |                                0      |                                       0.22  |
|      23 |                     0      |                 0      |         0.037  |                                0       |                         0       |                                 0.036 |                                      0       |                                0      |                                       0.036 |
|      24 |                     0      |                 0      |         0.0081 |                                0       |                         0       |                                 0.008 |                                      0       |                                0      |                                       0.008 |
|      25 |                     0      |                 0      |         0.0041 |                                0       |                         0       |                                 0.004 |                                      0       |                                0      |                                       0.004 |



## Number of classes (terms, groups, parts)
![Number of classes (terms, groups, parts)](analyses/class-depth/plot-class-depth_terms-groups-parts_totals.png)

|   Depth | LOINC   | LOINC-SNOMED   | CompLOINC-Primary   | CompLOINC-Supplementary   |
|---------|---------|----------------|---------------------|---------------------------|
|       1 | 3       | 1              | 4                   | 4                         |
|       2 | 29,800  | 10             | 29,605              | 29,605                    |
|       3 | 10,843  | 67             | 26,303              | 26,297                    |
|       4 | 38,733  | 394            | 110,854             | 78,596                    |
|       5 | 3,735   | 815            | 115,845             | 64,654                    |
|       6 | 11,474  | 1,649          | 123,168             | 51,997                    |
|       7 | 19,887  | 2,033          | 131,840             | 55,668                    |
|       8 | 24,922  | 1,955          | 129,859             | 55,762                    |
|       9 | 21,787  | 1,998          | 118,213             | 49,808                    |
|      10 | 12,833  | 2,289          | 99,935              | 41,512                    |
|      11 | 7,702   | 2,632          | 86,235              | 35,103                    |
|      12 | 3,634   | 2,180          | 72,627              | 29,079                    |
|      13 | 1,191   | 1,191          | 62,086              | 24,347                    |
|      14 | 134     | 1,226          | 48,980              | 19,337                    |
|      15 | 10      | 611            | 37,462              | 15,211                    |
|      16 | 0       | 630            | 27,250              | 11,804                    |
|      17 | 0       | 876            | 18,832              | 9,520                     |
|      18 | 0       | 1,506          | 12,145              | 8,245                     |
|      19 | 0       | 1,291          | 8,321               | 6,910                     |
|      20 | 0       | 701            | 5,176               | 4,891                     |
|      21 | 0       | 492            | 3,289               | 3,255                     |
|      22 | 0       | 56             | 1,275               | 1,273                     |
|      23 | 0       | 9              | 120                 | 120                       |
|      24 | 0       | 2              | 28                  | 28                        |
|      25 | 0       | 1              | 8                   | 8                         |



## % of classes (terms, groups, parts)
![% of classes (terms, groups, parts)](analyses/class-depth/plot-class-depth_terms-groups-parts_percentages.png)

|   Depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
|---------|---------|----------------|---------------------|---------------------------|
|       1 |  0.0016 |         0.0041 |             0.00032 |                   0.00064 |
|       2 | 16      |         0.041  |             2.3     |                   4.8     |
|       3 |  5.8    |         0.27   |             2.1     |                   4.2     |
|       4 | 21      |         1.6    |             8.7     |                  13       |
|       5 |  2      |         3.3    |             9.1     |                  10       |
|       6 |  6.1    |         6.7    |             9.7     |                   8.3     |
|       7 | 11      |         8.3    |            10       |                   8.9     |
|       8 | 13      |         7.9    |            10       |                   9       |
|       9 | 12      |         8.1    |             9.3     |                   8       |
|      10 |  6.9    |         9.3    |             7.9     |                   6.7     |
|      11 |  4.1    |        11      |             6.8     |                   5.6     |
|      12 |  1.9    |         8.9    |             5.7     |                   4.7     |
|      13 |  0.64   |         4.8    |             4.9     |                   3.9     |
|      14 |  0.072  |         5      |             3.9     |                   3.1     |
|      15 |  0.0054 |         2.5    |             3       |                   2.4     |
|      16 |  0      |         2.6    |             2.1     |                   1.9     |
|      17 |  0      |         3.6    |             1.5     |                   1.5     |
|      18 |  0      |         6.1    |             0.96    |                   1.3     |
|      19 |  0      |         5.2    |             0.66    |                   1.1     |
|      20 |  0      |         2.8    |             0.41    |                   0.79    |
|      21 |  0      |         2      |             0.26    |                   0.52    |
|      22 |  0      |         0.23   |             0.1     |                   0.2     |
|      23 |  0      |         0.037  |             0.0095  |                   0.019   |
|      24 |  0      |         0.0081 |             0.0022  |                   0.0045  |
|      25 |  0      |         0.0041 |             0.00063 |                   0.0013  |



## Number of classes (terms, groups, parts), by hierarchy
![Number of classes (terms, groups, parts), by hierarchy](analyses/class-depth/plot-class-depth_by-hierarchy_terms-groups-parts_totals.png)

|   Depth | LOINC - LOINC Categories   | LOINC - LOINC Groups   | LOINC - LoincPart   | LOINC-SNOMED   | CompLOINC-Primary - CompLOINC Groups   | CompLOINC-Primary - LoincPart   | CompLOINC-Primary - LoincTerm   | CompLOINC-Primary - SNOMED-Inspired   | CompLOINC-Supplementary - CompLOINC Groups   | CompLOINC-Supplementary - LoincPart   | CompLOINC-Supplementary - LoincTerm   | CompLOINC-Supplementary - SNOMED-Inspired   |
|---------|----------------------------|------------------------|---------------------|----------------|----------------------------------------|---------------------------------|---------------------------------|---------------------------------------|----------------------------------------------|---------------------------------------|---------------------------------------|---------------------------------------------|
|       1 | 1                          | 1                      | 1                   | 1              | 1                                      | 1                               | 1                               | 1                                     | 1                                            | 1                                     | 1                                     | 1                                           |
|       2 | 16                         | 45                     | 29,739              | 10             | 3                                      | 29,590                          | 4                               | 412                                   | 3                                            | 29,590                                | 4                                     | 412                                         |
|       3 | 7,130                      | 7,168                  | 3,675               | 67             | 22,193                                 | 3,930                           | 151                             | 458                                   | 22,187                                       | 3,930                                 | 151                                   | 458                                         |
|       4 | 30,327                     | 30,327                 | 8,406               | 394            | 100,519                                | 9,749                           | 79,704                          | 2,405                                 | 21,258                                       | 9,749                                 | 47,446                                | 2,405                                       |
|       5 | 0                          | 0                      | 3,735               | 815            | 107,919                                | 7,139                           | 87,670                          | 4,823                                 | 20,788                                       | 7,139                                 | 36,479                                | 4,823                                       |
|       6 | 0                          | 0                      | 11,474              | 1,649          | 102,254                                | 20,365                          | 81,788                          | 12,019                                | 20,704                                       | 20,365                                | 10,617                                | 12,019                                      |
|       7 | 0                          | 0                      | 19,887              | 2,033          | 99,103                                 | 32,465                          | 78,928                          | 20,546                                | 20,177                                       | 32,465                                | 2,756                                 | 20,546                                      |
|       8 | 0                          | 0                      | 24,922              | 1,955          | 93,749                                 | 35,857                          | 75,088                          | 25,564                                | 18,661                                       | 35,857                                | 991                                   | 25,564                                      |
|       9 | 0                          | 0                      | 21,787              | 1,998          | 84,096                                 | 33,913                          | 68,573                          | 27,540                                | 15,523                                       | 33,913                                | 168                                   | 27,540                                      |
|      10 | 0                          | 0                      | 12,833              | 2,289          | 70,480                                 | 29,305                          | 58,435                          | 27,363                                | 12,045                                       | 29,305                                | 12                                    | 27,363                                      |
|      11 | 0                          | 0                      | 7,702               | 2,632          | 60,268                                 | 25,875                          | 51,133                          | 25,470                                | 9,135                                        | 25,875                                | 1                                     | 25,470                                      |
|      12 | 0                          | 0                      | 3,634               | 2,180          | 50,284                                 | 22,276                          | 43,548                          | 22,282                                | 6,736                                        | 22,276                                | 0                                     | 22,282                                      |
|      13 | 0                          | 0                      | 1,191               | 1,191          | 42,495                                 | 19,552                          | 37,739                          | 19,582                                | 4,756                                        | 19,552                                | 0                                     | 19,582                                      |
|      14 | 0                          | 0                      | 134                 | 1,226          | 32,495                                 | 16,469                          | 29,643                          | 16,485                                | 2,852                                        | 16,469                                | 0                                     | 16,485                                      |
|      15 | 0                          | 0                      | 10                  | 611            | 23,701                                 | 13,750                          | 22,251                          | 13,761                                | 1,450                                        | 13,750                                | 0                                     | 13,761                                      |
|      16 | 0                          | 0                      | 0                   | 630            | 15,995                                 | 11,245                          | 15,446                          | 11,255                                | 549                                          | 11,245                                | 0                                     | 11,255                                      |
|      17 | 0                          | 0                      | 0                   | 876            | 9,483                                  | 9,340                           | 9,312                           | 9,349                                 | 171                                          | 9,340                                 | 0                                     | 9,349                                       |
|      18 | 0                          | 0                      | 0                   | 1,506          | 3,915                                  | 8,222                           | 3,900                           | 8,230                                 | 15                                           | 8,222                                 | 0                                     | 8,230                                       |
|      19 | 0                          | 0                      | 0                   | 1,291          | 1,412                                  | 6,902                           | 1,411                           | 6,909                                 | 1                                            | 6,902                                 | 0                                     | 6,909                                       |
|      20 | 0                          | 0                      | 0                   | 701            | 285                                    | 4,885                           | 285                             | 4,891                                 | 0                                            | 4,885                                 | 0                                     | 4,891                                       |
|      21 | 0                          | 0                      | 0                   | 492            | 34                                     | 3,250                           | 34                              | 3,255                                 | 0                                            | 3,250                                 | 0                                     | 3,255                                       |
|      22 | 0                          | 0                      | 0                   | 56             | 2                                      | 1,270                           | 2                               | 1,273                                 | 0                                            | 1,270                                 | 0                                     | 1,273                                       |
|      23 | 0                          | 0                      | 0                   | 9              | 0                                      | 118                             | 0                               | 120                                   | 0                                            | 118                                   | 0                                     | 120                                         |
|      24 | 0                          | 0                      | 0                   | 2              | 0                                      | 27                              | 0                               | 28                                    | 0                                            | 27                                    | 0                                     | 28                                          |
|      25 | 0                          | 0                      | 0                   | 1              | 0                                      | 8                               | 0                               | 8                                     | 0                                            | 8                                     | 0                                     | 8                                           |



## % of classes (terms, groups, parts), by hierarchy
![% of classes (terms, groups, parts), by hierarchy](analyses/class-depth/plot-class-depth_by-hierarchy_terms-groups-parts_percentages.png)

|   Depth |   LOINC - LOINC Categories |   LOINC - LOINC Groups |   LOINC - LoincPart |   LOINC-SNOMED |   CompLOINC-Primary - CompLOINC Groups |   CompLOINC-Primary - LoincPart |   CompLOINC-Primary - LoincTerm |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Supplementary - CompLOINC Groups |   CompLOINC-Supplementary - LoincPart |   CompLOINC-Supplementary - LoincTerm |   CompLOINC-Supplementary - SNOMED-Inspired |
|---------|----------------------------|------------------------|---------------------|----------------|----------------------------------------|---------------------------------|---------------------------------|---------------------------------------|----------------------------------------------|---------------------------------------|---------------------------------------|---------------------------------------------|
|       1 |                     0.0027 |                 0.0027 |             0.00067 |         0.0041 |                                0.00011 |                         0.00029 |                         0.00013 |                               0.00038 |                                      0.00056 |                               0.00029 |                                0.001  |                                     0.00038 |
|       2 |                     0.043  |                 0.12   |            20       |         0.041  |                                0.00033 |                         8.6     |                         0.00054 |                               0.16    |                                      0.0017  |                               8.6     |                                0.0041 |                                     0.16    |
|       3 |                    19      |                19      |             2.5     |         0.27   |                                2.4     |                         1.1     |                         0.02    |                               0.17    |                                     13       |                               1.1     |                                0.15   |                                     0.17    |
|       4 |                    81      |                81      |             5.6     |         1.6    |                               11       |                         2.8     |                        11       |                               0.91    |                                     12       |                               2.8     |                               48      |                                     0.91    |
|       5 |                     0      |                 0      |             2.5     |         3.3    |                               12       |                         2.1     |                        12       |                               1.8     |                                     12       |                               2.1     |                               37      |                                     1.8     |
|       6 |                     0      |                 0      |             7.7     |         6.7    |                               11       |                         5.9     |                        11       |                               4.6     |                                     12       |                               5.9     |                               11      |                                     4.6     |
|       7 |                     0      |                 0      |            13       |         8.3    |                               11       |                         9.4     |                        11       |                               7.8     |                                     11       |                               9.4     |                                2.8    |                                     7.8     |
|       8 |                     0      |                 0      |            17       |         7.9    |                               10       |                        10       |                        10       |                               9.7     |                                     11       |                              10       |                                1      |                                     9.7     |
|       9 |                     0      |                 0      |            15       |         8.1    |                                9.1     |                         9.8     |                         9.2     |                              10       |                                      8.8     |                               9.8     |                                0.17   |                                    10       |
|      10 |                     0      |                 0      |             8.6     |         9.3    |                                7.7     |                         8.5     |                         7.8     |                              10       |                                      6.8     |                               8.5     |                                0.012  |                                    10       |
|      11 |                     0      |                 0      |             5.2     |        11      |                                6.5     |                         7.5     |                         6.9     |                               9.6     |                                      5.2     |                               7.5     |                                0.001  |                                     9.6     |
|      12 |                     0      |                 0      |             2.4     |         8.9    |                                5.5     |                         6.4     |                         5.8     |                               8.4     |                                      3.8     |                               6.4     |                                0      |                                     8.4     |
|      13 |                     0      |                 0      |             0.8     |         4.8    |                                4.6     |                         5.7     |                         5.1     |                               7.4     |                                      2.7     |                               5.7     |                                0      |                                     7.4     |
|      14 |                     0      |                 0      |             0.09    |         5      |                                3.5     |                         4.8     |                         4       |                               6.2     |                                      1.6     |                               4.8     |                                0      |                                     6.2     |
|      15 |                     0      |                 0      |             0.0067  |         2.5    |                                2.6     |                         4       |                         3       |                               5.2     |                                      0.82    |                               4       |                                0      |                                     5.2     |
|      16 |                     0      |                 0      |             0       |         2.6    |                                1.7     |                         3.3     |                         2.1     |                               4.3     |                                      0.31    |                               3.3     |                                0      |                                     4.3     |
|      17 |                     0      |                 0      |             0       |         3.6    |                                1       |                         2.7     |                         1.2     |                               3.5     |                                      0.097   |                               2.7     |                                0      |                                     3.5     |
|      18 |                     0      |                 0      |             0       |         6.1    |                                0.43    |                         2.4     |                         0.52    |                               3.1     |                                      0.0085  |                               2.4     |                                0      |                                     3.1     |
|      19 |                     0      |                 0      |             0       |         5.2    |                                0.15    |                         2       |                         0.19    |                               2.6     |                                      0.00056 |                               2       |                                0      |                                     2.6     |
|      20 |                     0      |                 0      |             0       |         2.8    |                                0.031   |                         1.4     |                         0.038   |                               1.9     |                                      0       |                               1.4     |                                0      |                                     1.9     |
|      21 |                     0      |                 0      |             0       |         2      |                                0.0037  |                         0.94    |                         0.0046  |                               1.2     |                                      0       |                               0.94    |                                0      |                                     1.2     |
|      22 |                     0      |                 0      |             0       |         0.23   |                                0.00022 |                         0.37    |                         0.00027 |                               0.48    |                                      0       |                               0.37    |                                0      |                                     0.48    |
|      23 |                     0      |                 0      |             0       |         0.037  |                                0       |                         0.034   |                         0       |                               0.045   |                                      0       |                               0.034   |                                0      |                                     0.045   |
|      24 |                     0      |                 0      |             0       |         0.0081 |                                0       |                         0.0078  |                         0       |                               0.011   |                                      0       |                               0.0078  |                                0      |                                     0.011   |
|      25 |                     0      |                 0      |             0       |         0.0041 |                                0       |                         0.0023  |                         0       |                               0.003   |                                      0       |                               0.0023  |                                0      |                                     0.003   |



---

## Changes, by data processing stage
The following tables shows details in regards to total counts and percentages remaining of classes, subclass axioms, and
roots at various sequential stages of data preparation. The We start with the raw inputs queried by the ontology, 
including all class types. Then, a few transient grouping classes just for this analysis were added to LOINC and 
CompLOINC. Next, we filter out the classes types that are not needed for one of the sub-analyses. The filter is some 
combination of terms, parts, and/or groups. Finally, we remove any dangling classes, as well as any dangling subtrees 
that were caused by the previous filtration step.  

### Counts
| filter               | stage                 | metric         | CompLOINC-Primary   | CompLOINC-Supplementary   | LOINC   | LOINC-SNOMED   |
|----------------------|-----------------------|----------------|---------------------|---------------------------|---------|----------------|
| terms                | 1: raw_input          | classes        | 241,791             | 241,785                   | 153,742 | 7,963          |
| terms                | 1: raw_input          | roots          | 938                 | 932                       | 62      | 1              |
| terms                | 1: raw_input          | subclass pairs | 422,349             | 360,244                   | 177,265 | 11,376         |
| terms                | 2: post_new_groupings | classes        | 241,791             | 241,785                   | 153,742 | 7,963          |
| terms                | 2: post_new_groupings | roots          | 938                 | 932                       | 62      | 1              |
| terms                | 2: post_new_groupings | subclass pairs | 422,349             | 360,244                   | 177,265 | 11,376         |
| terms                | 3: post_filters       | classes        | 103,412             | 103,412                   | 30,327  | 7,963          |
| terms                | 3: post_filters       | roots          | 71                  | 71                        | 30,327  | 1              |
| terms                | 3: post_filters       | subclass pairs | 120,819             | 147,034                   | 0       | 11,376         |
| terms                | 4: post_pruning       | classes        | 103,104             | 103,104                   | 0       | 7,963          |
| terms                | 4: post_pruning       | roots          | 2                   | 2                         | 0       | 1              |
| terms                | 4: post_pruning       | subclass pairs | 120,387             | 146,602                   | 0       | 11,376         |
| terms, groups        | 1: raw_input          | classes        | 241,791             | 241,785                   | 153,742 | 7,963          |
| terms, groups        | 1: raw_input          | roots          | 938                 | 932                       | 62      | 1              |
| terms, groups        | 1: raw_input          | subclass pairs | 422,349             | 360,244                   | 177,265 | 11,376         |
| terms, groups        | 2: post_new_groupings | classes        | 241,795             | 241,789                   | 153,744 | 7,963          |
| terms, groups        | 2: post_new_groupings | roots          | 4                   | 4                         | 3       | 1              |
| terms, groups        | 2: post_new_groupings | subclass pairs | 444,545             | 382,434                   | 177,326 | 11,376         |
| terms, groups        | 3: post_filters       | classes        | 125,609             | 125,603                   | 37,558  | 7,963          |
| terms, groups        | 3: post_filters       | roots          | 72                  | 72                        | 2       | 1              |
| terms, groups        | 3: post_filters       | subclass pairs | 277,664             | 215,553                   | 56,877  | 11,376         |
| terms, groups        | 4: post_pruning       | classes        | 125,301             | 125,295                   | 37,558  | 7,963          |
| terms, groups        | 4: post_pruning       | roots          | 3                   | 3                         | 2       | 1              |
| terms, groups        | 4: post_pruning       | subclass pairs | 277,232             | 215,121                   | 56,877  | 11,376         |
| terms, groups, parts | 1: raw_input          | classes        | 241,791             | 241,785                   | 153,742 | 7,963          |
| terms, groups, parts | 1: raw_input          | roots          | 938                 | 932                       | 62      | 1              |
| terms, groups, parts | 1: raw_input          | subclass pairs | 422,349             | 360,244                   | 177,265 | 11,376         |
| terms, groups, parts | 2: post_new_groupings | classes        | 241,795             | 241,789                   | 153,744 | 7,963          |
| terms, groups, parts | 2: post_new_groupings | roots          | 4                   | 4                         | 3       | 1              |
| terms, groups, parts | 2: post_new_groupings | subclass pairs | 444,545             | 382,434                   | 177,326 | 11,376         |
| terms, groups, parts | 3: post_filters       | classes        | 241,795             | 241,789                   | 153,744 | 7,963          |
| terms, groups, parts | 3: post_filters       | roots          | 4                   | 4                         | 3       | 1              |
| terms, groups, parts | 3: post_filters       | subclass pairs | 444,545             | 382,434                   | 177,326 | 11,376         |
| terms, groups, parts | 4: post_pruning       | classes        | 241,795             | 241,789                   | 153,744 | 7,963          |
| terms, groups, parts | 4: post_pruning       | roots          | 4                   | 4                         | 3       | 1              |
| terms, groups, parts | 4: post_pruning       | subclass pairs | 444,545             | 382,434                   | 177,326 | 11,376         |

### Percentages
| filter               | stage                 | metric         |   CompLOINC-Primary |   CompLOINC-Supplementary |    LOINC |   LOINC-SNOMED |
|----------------------|-----------------------|----------------|---------------------|---------------------------|----------|----------------|
| terms                | 1: raw_input          | classes        |             100     |                   100     |   100    |            100 |
| terms                | 1: raw_input          | roots          |             100     |                   100     |   100    |            100 |
| terms                | 1: raw_input          | subclass pairs |             100     |                   100     |   100    |            100 |
| terms                | 2: post_new_groupings | classes        |             100     |                   100     |   100    |            100 |
| terms                | 2: post_new_groupings | roots          |             100     |                   100     |   100    |            100 |
| terms                | 2: post_new_groupings | subclass pairs |             100     |                   100     |   100    |            100 |
| terms                | 3: post_filters       | classes        |              42.8   |                    42.8   |    19.7  |            100 |
| terms                | 3: post_filters       | roots          |               7.57  |                     7.62  | 48900    |            100 |
| terms                | 3: post_filters       | subclass pairs |              28.6   |                    40.8   |     0    |            100 |
| terms                | 4: post_pruning       | classes        |              42.6   |                    42.6   |     0    |            100 |
| terms                | 4: post_pruning       | roots          |               0.213 |                     0.215 |     0    |            100 |
| terms                | 4: post_pruning       | subclass pairs |              28.5   |                    40.7   |     0    |            100 |
| terms, groups        | 1: raw_input          | classes        |             100     |                   100     |   100    |            100 |
| terms, groups        | 1: raw_input          | roots          |             100     |                   100     |   100    |            100 |
| terms, groups        | 1: raw_input          | subclass pairs |             100     |                   100     |   100    |            100 |
| terms, groups        | 2: post_new_groupings | classes        |             100     |                   100     |   100    |            100 |
| terms, groups        | 2: post_new_groupings | roots          |               0.426 |                     0.429 |     4.84 |            100 |
| terms, groups        | 2: post_new_groupings | subclass pairs |             105     |                   106     |   100    |            100 |
| terms, groups        | 3: post_filters       | classes        |              51.9   |                    51.9   |    24.4  |            100 |
| terms, groups        | 3: post_filters       | roots          |               7.68  |                     7.73  |     3.23 |            100 |
| terms, groups        | 3: post_filters       | subclass pairs |              65.7   |                    59.8   |    32.1  |            100 |
| terms, groups        | 4: post_pruning       | classes        |              51.8   |                    51.8   |    24.4  |            100 |
| terms, groups        | 4: post_pruning       | roots          |               0.32  |                     0.322 |     3.23 |            100 |
| terms, groups        | 4: post_pruning       | subclass pairs |              65.6   |                    59.7   |    32.1  |            100 |
| terms, groups, parts | 1: raw_input          | classes        |             100     |                   100     |   100    |            100 |
| terms, groups, parts | 1: raw_input          | roots          |             100     |                   100     |   100    |            100 |
| terms, groups, parts | 1: raw_input          | subclass pairs |             100     |                   100     |   100    |            100 |
| terms, groups, parts | 2: post_new_groupings | classes        |             100     |                   100     |   100    |            100 |
| terms, groups, parts | 2: post_new_groupings | roots          |               0.426 |                     0.429 |     4.84 |            100 |
| terms, groups, parts | 2: post_new_groupings | subclass pairs |             105     |                   106     |   100    |            100 |
| terms, groups, parts | 3: post_filters       | classes        |             100     |                   100     |   100    |            100 |
| terms, groups, parts | 3: post_filters       | roots          |               0.426 |                     0.429 |     4.84 |            100 |
| terms, groups, parts | 3: post_filters       | subclass pairs |             105     |                   106     |   100    |            100 |
| terms, groups, parts | 4: post_pruning       | classes        |             100     |                   100     |   100    |            100 |
| terms, groups, parts | 4: post_pruning       | roots          |               0.426 |                     0.429 |     4.84 |            100 |
| terms, groups, parts | 4: post_pruning       | subclass pairs |             105     |                   106     |   100    |            100 |
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

