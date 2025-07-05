# Classification depth analysis 
This measures how deep into the hierarchy each class is. E.g. if the root of the hierarchy is TermA, and we have axioms
(TermC subClassOf TermB) and (TermB subClassOf TermA), then TermC is at depth 3, TermB is at depth 2, and TermA is at 
depth 1.

## Polyhierarchies
**Impact on class depths**  
CompLOINC and the LOINC and LOINC-SNOMED representations are all polyhierarchies. This means that classes can appear 
multiple times. For this analysis, we have decided to include every occurrence of a class in the counts. For example, if
a class appears in 3 subtrees, once at depth 3, and in two subtrees at depth 2, this class will be tallied twice at 
depth 2, and once at depth 3. 

**Disaggregating major subtrees**  
CompLOINC and LOINC have more than 1 top-level branches (AKA subhierachies or subtrees).

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
all grouping clases is http://comploinc/group/ ("GRP"), and the children of this class are all of the roots of each 
property axis, e.g. http://comploinc/group/component/ ("GRP_CMP"), http://comploinc/group/component-system/ ("GRP_SYS"),
and so on.

## LOINC representation
LOINC itself does not have an `.owl` representaiton, but for this analysis we constructed one. The following are some 
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
![Number of classes (terms)](plot-class-depth_terms_totals.png)

|   depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
|---------|---------|----------------|---------------------|---------------------------|
|       1 |       0 |              1 |                   2 |                         2 |
|       2 |       0 |             10 |                  14 |                        14 |
|       3 |       0 |             67 |                 216 |                       216 |
|       4 |       0 |            394 |               43085 |                     47815 |
|       5 |       0 |            815 |               40624 |                     37256 |
|       6 |       0 |           1649 |               15714 |                     12216 |
|       7 |       0 |           2033 |                7475 |                      4727 |
|       8 |       0 |           1955 |                4170 |                      2929 |
|       9 |       0 |           1998 |                2509 |                      2185 |
|      10 |       0 |           2289 |                2408 |                      2314 |
|      11 |       0 |           2632 |                2718 |                      2710 |
|      12 |       0 |           2180 |                2358 |                      2356 |
|      13 |       0 |           1191 |                1314 |                      1314 |
|      14 |       0 |           1226 |                1291 |                      1291 |
|      15 |       0 |            611 |                 610 |                       610 |
|      16 |       0 |            630 |                 651 |                       651 |
|      17 |       0 |            876 |                 895 |                       895 |
|      18 |       0 |           1506 |                1519 |                      1519 |
|      19 |       0 |           1291 |                1303 |                      1303 |
|      20 |       0 |            701 |                 705 |                       705 |
|      21 |       0 |            492 |                 492 |                       492 |
|      22 |       0 |             56 |                  56 |                        56 |
|      23 |       0 |              9 |                   9 |                         9 |
|      24 |       0 |              2 |                   2 |                         2 |
|      25 |       0 |              1 |                   1 |                         1 |



## % of classes (terms)
![% of classes (terms)](plot-class-depth_terms_percentages.png)

|   depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
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



## Number of classes (terms, groups)
![Number of classes (terms, groups)](plot-class-depth_terms-groups_totals.png)

|   depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
|---------|---------|----------------|---------------------|---------------------------|
|       1 |       2 |              1 |                   3 |                         3 |
|       2 |      61 |             10 |                  17 |                        17 |
|       3 |    7168 |             67 |               22409 |                     22403 |
|       4 |   30327 |            394 |              101331 |                     69073 |
|       5 |       0 |            815 |              109235 |                     58044 |
|       6 |       0 |           1649 |              104091 |                     32920 |
|       7 |       0 |           2033 |              101076 |                     24904 |
|       8 |       0 |           1955 |               95687 |                     21590 |
|       9 |       0 |           1998 |               86113 |                     17708 |
|      10 |       0 |           2289 |               72782 |                     14359 |
|      11 |       0 |           2632 |               62977 |                     11845 |
|      12 |       0 |           2180 |               52640 |                      9092 |
|      13 |       0 |           1191 |               43809 |                      6070 |
|      14 |       0 |           1226 |               33786 |                      4143 |
|      15 |       0 |            611 |               24311 |                      2060 |
|      16 |       0 |            630 |               16646 |                      1200 |
|      17 |       0 |            876 |               10378 |                      1066 |
|      18 |       0 |           1506 |                5434 |                      1534 |
|      19 |       0 |           1291 |                2715 |                      1304 |
|      20 |       0 |            701 |                 990 |                       705 |
|      21 |       0 |            492 |                 526 |                       492 |
|      22 |       0 |             56 |                  58 |                        56 |
|      23 |       0 |              9 |                   9 |                         9 |
|      24 |       0 |              2 |                   2 |                         2 |
|      25 |       0 |              1 |                   1 |                         1 |



## % of classes (terms, groups)
![% of classes (terms, groups)](plot-class-depth_terms-groups_percentages.png)

|   depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
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



## Number of classes (terms, groups, parts)
![Number of classes (terms, groups, parts)](plot-class-depth_terms-groups-parts_totals.png)

|   depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
|---------|---------|----------------|---------------------|---------------------------|
|       1 |       3 |              1 |                   4 |                         4 |
|       2 |   29800 |             10 |               29605 |                     29605 |
|       3 |   10843 |             67 |               26303 |                     26297 |
|       4 |   38733 |            394 |              110854 |                     78596 |
|       5 |    3735 |            815 |              115845 |                     64654 |
|       6 |   11474 |           1649 |              123168 |                     51997 |
|       7 |   19887 |           2033 |              131840 |                     55668 |
|       8 |   24922 |           1955 |              129859 |                     55762 |
|       9 |   21787 |           1998 |              118213 |                     49808 |
|      10 |   12833 |           2289 |               99935 |                     41512 |
|      11 |    7702 |           2632 |               86235 |                     35103 |
|      12 |    3634 |           2180 |               72627 |                     29079 |
|      13 |    1191 |           1191 |               62086 |                     24347 |
|      14 |     134 |           1226 |               48980 |                     19337 |
|      15 |      10 |            611 |               37462 |                     15211 |
|      16 |       0 |            630 |               27250 |                     11804 |
|      17 |       0 |            876 |               18832 |                      9520 |
|      18 |       0 |           1506 |               12145 |                      8245 |
|      19 |       0 |           1291 |                8321 |                      6910 |
|      20 |       0 |            701 |                5176 |                      4891 |
|      21 |       0 |            492 |                3289 |                      3255 |
|      22 |       0 |             56 |                1275 |                      1273 |
|      23 |       0 |              9 |                 120 |                       120 |
|      24 |       0 |              2 |                  28 |                        28 |
|      25 |       0 |              1 |                   8 |                         8 |



## % of classes (terms, groups, parts)
![% of classes (terms, groups, parts)](plot-class-depth_terms-groups-parts_percentages.png)

|   depth |   LOINC |   LOINC-SNOMED |   CompLOINC-Primary |   CompLOINC-Supplementary |
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





## Number of classes (terms), by hierarchy
![Number of classes (terms), by hierarchy](plot-class-depth_by-hierarchy_terms_totals.png)

|   depth |   LOINC-SNOMED - SNOMED-Inspired |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Primary - LoincTerm |   CompLOINC-Supplementary - SNOMED-Inspired |   CompLOINC-Supplementary - LoincTerm |
|---------|----------------------------------|---------------------------------------|---------------------------------|---------------------------------------------|---------------------------------------|
|       1 |                                1 |                                     1 |                               1 |                                           1 |                                     1 |
|       2 |                               10 |                                    10 |                               4 |                                          10 |                                     4 |
|       3 |                               67 |                                    65 |                             151 |                                          65 |                                   151 |
|       4 |                              394 |                                   369 |                           42716 |                                         369 |                                 47446 |
|       5 |                              815 |                                   777 |                           39847 |                                         777 |                                 36479 |
|       6 |                             1649 |                                  1599 |                           14115 |                                        1599 |                                 10617 |
|       7 |                             2033 |                                  1971 |                            5504 |                                        1971 |                                  2756 |
|       8 |                             1955 |                                  1938 |                            2232 |                                        1938 |                                   991 |
|       9 |                             1998 |                                  2017 |                             492 |                                        2017 |                                   168 |
|      10 |                             2289 |                                  2302 |                             106 |                                        2302 |                                    12 |
|      11 |                             2632 |                                  2709 |                               9 |                                        2709 |                                     1 |
|      12 |                             2180 |                                  2356 |                               2 |                                        2356 |                                     0 |
|      13 |                             1191 |                                  1314 |                               0 |                                        1314 |                                     0 |
|      14 |                             1226 |                                  1291 |                               0 |                                        1291 |                                     0 |
|      15 |                              611 |                                   610 |                               0 |                                         610 |                                     0 |
|      16 |                              630 |                                   651 |                               0 |                                         651 |                                     0 |
|      17 |                              876 |                                   895 |                               0 |                                         895 |                                     0 |
|      18 |                             1506 |                                  1519 |                               0 |                                        1519 |                                     0 |
|      19 |                             1291 |                                  1303 |                               0 |                                        1303 |                                     0 |
|      20 |                              701 |                                   705 |                               0 |                                         705 |                                     0 |
|      21 |                              492 |                                   492 |                               0 |                                         492 |                                     0 |
|      22 |                               56 |                                    56 |                               0 |                                          56 |                                     0 |
|      23 |                                9 |                                     9 |                               0 |                                           9 |                                     0 |
|      24 |                                2 |                                     2 |                               0 |                                           2 |                                     0 |
|      25 |                                1 |                                     1 |                               0 |                                           1 |                                     0 |



## % of classes (terms), by hierarchy
![% of classes (terms), by hierarchy](plot-class-depth_by-hierarchy_terms_percentages.png)

|   depth |   LOINC-SNOMED - SNOMED-Inspired |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Primary - LoincTerm |   CompLOINC-Supplementary - SNOMED-Inspired |   CompLOINC-Supplementary - LoincTerm |
|---------|----------------------------------|---------------------------------------|---------------------------------|---------------------------------------------|---------------------------------------|
|       1 |                           0.0041 |                                 0.004 |                         0.00095 |                                       0.004 |                                0.001  |
|       2 |                           0.041  |                                 0.04  |                         0.0038  |                                       0.04  |                                0.0041 |
|       3 |                           0.27   |                                 0.26  |                         0.14    |                                       0.26  |                                0.15   |
|       4 |                           1.6    |                                 1.5   |                        41       |                                       1.5   |                               48      |
|       5 |                           3.3    |                                 3.1   |                        38       |                                       3.1   |                               37      |
|       6 |                           6.7    |                                 6.4   |                        13       |                                       6.4   |                               11      |
|       7 |                           8.3    |                                 7.9   |                         5.2     |                                       7.9   |                                2.8    |
|       8 |                           7.9    |                                 7.8   |                         2.1     |                                       7.8   |                                1      |
|       9 |                           8.1    |                                 8.1   |                         0.47    |                                       8.1   |                                0.17   |
|      10 |                           9.3    |                                 9.2   |                         0.1     |                                       9.2   |                                0.012  |
|      11 |                          11      |                                11     |                         0.0086  |                                      11     |                                0.001  |
|      12 |                           8.9    |                                 9.4   |                         0.0019  |                                       9.4   |                                0      |
|      13 |                           4.8    |                                 5.3   |                         0       |                                       5.3   |                                0      |
|      14 |                           5      |                                 5.2   |                         0       |                                       5.2   |                                0      |
|      15 |                           2.5    |                                 2.4   |                         0       |                                       2.4   |                                0      |
|      16 |                           2.6    |                                 2.6   |                         0       |                                       2.6   |                                0      |
|      17 |                           3.6    |                                 3.6   |                         0       |                                       3.6   |                                0      |
|      18 |                           6.1    |                                 6.1   |                         0       |                                       6.1   |                                0      |
|      19 |                           5.2    |                                 5.2   |                         0       |                                       5.2   |                                0      |
|      20 |                           2.8    |                                 2.8   |                         0       |                                       2.8   |                                0      |
|      21 |                           2      |                                 2     |                         0       |                                       2     |                                0      |
|      22 |                           0.23   |                                 0.22  |                         0       |                                       0.22  |                                0      |
|      23 |                           0.037  |                                 0.036 |                         0       |                                       0.036 |                                0      |
|      24 |                           0.0081 |                                 0.008 |                         0       |                                       0.008 |                                0      |
|      25 |                           0.0041 |                                 0.004 |                         0       |                                       0.004 |                                0      |



## Number of classes (terms, groups), by hierarchy
![Number of classes (terms, groups), by hierarchy](plot-class-depth_by-hierarchy_terms-groups_totals.png)

|   depth |   LOINC - LOINC Categories |   LOINC - LOINC Groups |   LOINC-SNOMED - SNOMED-Inspired |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Primary - LoincTerm |   CompLOINC-Primary - CompLOINC Groups |   CompLOINC-Supplementary - SNOMED-Inspired |   CompLOINC-Supplementary - LoincTerm |   CompLOINC-Supplementary - CompLOINC Groups |
|---------|----------------------------|------------------------|----------------------------------|---------------------------------------|---------------------------------|----------------------------------------|---------------------------------------------|---------------------------------------|----------------------------------------------|
|       1 |                          1 |                      1 |                                1 |                                     1 |                               1 |                                      1 |                                           1 |                                     1 |                                            1 |
|       2 |                         16 |                     45 |                               10 |                                    10 |                               4 |                                      3 |                                          10 |                                     4 |                                            3 |
|       3 |                       7130 |                   7168 |                               67 |                                    65 |                             151 |                                  22193 |                                          65 |                                   151 |                                        22187 |
|       4 |                      30327 |                  30327 |                              394 |                                   369 |                           79704 |                                 100519 |                                         369 |                                 47446 |                                        21258 |
|       5 |                          0 |                      0 |                              815 |                                   777 |                           87670 |                                 107919 |                                         777 |                                 36479 |                                        20788 |
|       6 |                          0 |                      0 |                             1649 |                                  1599 |                           81788 |                                 102254 |                                        1599 |                                 10617 |                                        20704 |
|       7 |                          0 |                      0 |                             2033 |                                  1971 |                           78928 |                                  99103 |                                        1971 |                                  2756 |                                        20177 |
|       8 |                          0 |                      0 |                             1955 |                                  1938 |                           75088 |                                  93749 |                                        1938 |                                   991 |                                        18661 |
|       9 |                          0 |                      0 |                             1998 |                                  2017 |                           68573 |                                  84096 |                                        2017 |                                   168 |                                        15523 |
|      10 |                          0 |                      0 |                             2289 |                                  2302 |                           58435 |                                  70480 |                                        2302 |                                    12 |                                        12045 |
|      11 |                          0 |                      0 |                             2632 |                                  2709 |                           51133 |                                  60268 |                                        2709 |                                     1 |                                         9135 |
|      12 |                          0 |                      0 |                             2180 |                                  2356 |                           43548 |                                  50284 |                                        2356 |                                     0 |                                         6736 |
|      13 |                          0 |                      0 |                             1191 |                                  1314 |                           37739 |                                  42495 |                                        1314 |                                     0 |                                         4756 |
|      14 |                          0 |                      0 |                             1226 |                                  1291 |                           29643 |                                  32495 |                                        1291 |                                     0 |                                         2852 |
|      15 |                          0 |                      0 |                              611 |                                   610 |                           22251 |                                  23701 |                                         610 |                                     0 |                                         1450 |
|      16 |                          0 |                      0 |                              630 |                                   651 |                           15446 |                                  15995 |                                         651 |                                     0 |                                          549 |
|      17 |                          0 |                      0 |                              876 |                                   895 |                            9312 |                                   9483 |                                         895 |                                     0 |                                          171 |
|      18 |                          0 |                      0 |                             1506 |                                  1519 |                            3900 |                                   3915 |                                        1519 |                                     0 |                                           15 |
|      19 |                          0 |                      0 |                             1291 |                                  1303 |                            1411 |                                   1412 |                                        1303 |                                     0 |                                            1 |
|      20 |                          0 |                      0 |                              701 |                                   705 |                             285 |                                    285 |                                         705 |                                     0 |                                            0 |
|      21 |                          0 |                      0 |                              492 |                                   492 |                              34 |                                     34 |                                         492 |                                     0 |                                            0 |
|      22 |                          0 |                      0 |                               56 |                                    56 |                               2 |                                      2 |                                          56 |                                     0 |                                            0 |
|      23 |                          0 |                      0 |                                9 |                                     9 |                               0 |                                      0 |                                           9 |                                     0 |                                            0 |
|      24 |                          0 |                      0 |                                2 |                                     2 |                               0 |                                      0 |                                           2 |                                     0 |                                            0 |
|      25 |                          0 |                      0 |                                1 |                                     1 |                               0 |                                      0 |                                           1 |                                     0 |                                            0 |



## % of classes (terms, groups), by hierarchy
![% of classes (terms, groups), by hierarchy](plot-class-depth_by-hierarchy_terms-groups_percentages.png)

|   depth |   LOINC - LOINC Categories |   LOINC - LOINC Groups |   LOINC-SNOMED - SNOMED-Inspired |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Primary - LoincTerm |   CompLOINC-Primary - CompLOINC Groups |   CompLOINC-Supplementary - SNOMED-Inspired |   CompLOINC-Supplementary - LoincTerm |   CompLOINC-Supplementary - CompLOINC Groups |
|---------|----------------------------|------------------------|----------------------------------|---------------------------------------|---------------------------------|----------------------------------------|---------------------------------------------|---------------------------------------|----------------------------------------------|
|       1 |                     0.0027 |                 0.0027 |                           0.0041 |                                 0.004 |                         0.00013 |                                0.00011 |                                       0.004 |                                0.001  |                                      0.00056 |
|       2 |                     0.043  |                 0.12   |                           0.041  |                                 0.04  |                         0.00054 |                                0.00033 |                                       0.04  |                                0.0041 |                                      0.0017  |
|       3 |                    19      |                19      |                           0.27   |                                 0.26  |                         0.02    |                                2.4     |                                       0.26  |                                0.15   |                                     13       |
|       4 |                    81      |                81      |                           1.6    |                                 1.5   |                        11       |                               11       |                                       1.5   |                               48      |                                     12       |
|       5 |                     0      |                 0      |                           3.3    |                                 3.1   |                        12       |                               12       |                                       3.1   |                               37      |                                     12       |
|       6 |                     0      |                 0      |                           6.7    |                                 6.4   |                        11       |                               11       |                                       6.4   |                               11      |                                     12       |
|       7 |                     0      |                 0      |                           8.3    |                                 7.9   |                        11       |                               11       |                                       7.9   |                                2.8    |                                     11       |
|       8 |                     0      |                 0      |                           7.9    |                                 7.8   |                        10       |                               10       |                                       7.8   |                                1      |                                     11       |
|       9 |                     0      |                 0      |                           8.1    |                                 8.1   |                         9.2     |                                9.1     |                                       8.1   |                                0.17   |                                      8.8     |
|      10 |                     0      |                 0      |                           9.3    |                                 9.2   |                         7.8     |                                7.7     |                                       9.2   |                                0.012  |                                      6.8     |
|      11 |                     0      |                 0      |                          11      |                                11     |                         6.9     |                                6.5     |                                      11     |                                0.001  |                                      5.2     |
|      12 |                     0      |                 0      |                           8.9    |                                 9.4   |                         5.8     |                                5.5     |                                       9.4   |                                0      |                                      3.8     |
|      13 |                     0      |                 0      |                           4.8    |                                 5.3   |                         5.1     |                                4.6     |                                       5.3   |                                0      |                                      2.7     |
|      14 |                     0      |                 0      |                           5      |                                 5.2   |                         4       |                                3.5     |                                       5.2   |                                0      |                                      1.6     |
|      15 |                     0      |                 0      |                           2.5    |                                 2.4   |                         3       |                                2.6     |                                       2.4   |                                0      |                                      0.82    |
|      16 |                     0      |                 0      |                           2.6    |                                 2.6   |                         2.1     |                                1.7     |                                       2.6   |                                0      |                                      0.31    |
|      17 |                     0      |                 0      |                           3.6    |                                 3.6   |                         1.2     |                                1       |                                       3.6   |                                0      |                                      0.097   |
|      18 |                     0      |                 0      |                           6.1    |                                 6.1   |                         0.52    |                                0.43    |                                       6.1   |                                0      |                                      0.0085  |
|      19 |                     0      |                 0      |                           5.2    |                                 5.2   |                         0.19    |                                0.15    |                                       5.2   |                                0      |                                      0.00056 |
|      20 |                     0      |                 0      |                           2.8    |                                 2.8   |                         0.038   |                                0.031   |                                       2.8   |                                0      |                                      0       |
|      21 |                     0      |                 0      |                           2      |                                 2     |                         0.0046  |                                0.0037  |                                       2     |                                0      |                                      0       |
|      22 |                     0      |                 0      |                           0.23   |                                 0.22  |                         0.00027 |                                0.00022 |                                       0.22  |                                0      |                                      0       |
|      23 |                     0      |                 0      |                           0.037  |                                 0.036 |                         0       |                                0       |                                       0.036 |                                0      |                                      0       |
|      24 |                     0      |                 0      |                           0.0081 |                                 0.008 |                         0       |                                0       |                                       0.008 |                                0      |                                      0       |
|      25 |                     0      |                 0      |                           0.0041 |                                 0.004 |                         0       |                                0       |                                       0.004 |                                0      |                                      0       |



## Number of classes (terms, groups, parts), by hierarchy
![Number of classes (terms, groups, parts), by hierarchy](plot-class-depth_by-hierarchy_terms-groups-parts_totals.png)

|   depth |   LOINC - LOINC Categories |   LOINC - LoincPart |   LOINC - LOINC Groups |   LOINC-SNOMED - SNOMED-Inspired |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Primary - LoincPart |   CompLOINC-Primary - LoincTerm |   CompLOINC-Primary - CompLOINC Groups |   CompLOINC-Supplementary - SNOMED-Inspired |   CompLOINC-Supplementary - LoincPart |   CompLOINC-Supplementary - LoincTerm |   CompLOINC-Supplementary - CompLOINC Groups |
|---------|----------------------------|---------------------|------------------------|----------------------------------|---------------------------------------|---------------------------------|---------------------------------|----------------------------------------|---------------------------------------------|---------------------------------------|---------------------------------------|----------------------------------------------|
|       1 |                          1 |                   1 |                      1 |                                1 |                                     1 |                               1 |                               1 |                                      1 |                                           1 |                                     1 |                                     1 |                                            1 |
|       2 |                         16 |               29739 |                     45 |                               10 |                                   412 |                           29590 |                               4 |                                      3 |                                         412 |                                 29590 |                                     4 |                                            3 |
|       3 |                       7130 |                3675 |                   7168 |                               67 |                                   458 |                            3930 |                             151 |                                  22193 |                                         458 |                                  3930 |                                   151 |                                        22187 |
|       4 |                      30327 |                8406 |                  30327 |                              394 |                                  2405 |                            9749 |                           79704 |                                 100519 |                                        2405 |                                  9749 |                                 47446 |                                        21258 |
|       5 |                          0 |                3735 |                      0 |                              815 |                                  4823 |                            7139 |                           87670 |                                 107919 |                                        4823 |                                  7139 |                                 36479 |                                        20788 |
|       6 |                          0 |               11474 |                      0 |                             1649 |                                 12019 |                           20365 |                           81788 |                                 102254 |                                       12019 |                                 20365 |                                 10617 |                                        20704 |
|       7 |                          0 |               19887 |                      0 |                             2033 |                                 20546 |                           32465 |                           78928 |                                  99103 |                                       20546 |                                 32465 |                                  2756 |                                        20177 |
|       8 |                          0 |               24922 |                      0 |                             1955 |                                 25564 |                           35857 |                           75088 |                                  93749 |                                       25564 |                                 35857 |                                   991 |                                        18661 |
|       9 |                          0 |               21787 |                      0 |                             1998 |                                 27540 |                           33913 |                           68573 |                                  84096 |                                       27540 |                                 33913 |                                   168 |                                        15523 |
|      10 |                          0 |               12833 |                      0 |                             2289 |                                 27363 |                           29305 |                           58435 |                                  70480 |                                       27363 |                                 29305 |                                    12 |                                        12045 |
|      11 |                          0 |                7702 |                      0 |                             2632 |                                 25470 |                           25875 |                           51133 |                                  60268 |                                       25470 |                                 25875 |                                     1 |                                         9135 |
|      12 |                          0 |                3634 |                      0 |                             2180 |                                 22282 |                           22276 |                           43548 |                                  50284 |                                       22282 |                                 22276 |                                     0 |                                         6736 |
|      13 |                          0 |                1191 |                      0 |                             1191 |                                 19582 |                           19552 |                           37739 |                                  42495 |                                       19582 |                                 19552 |                                     0 |                                         4756 |
|      14 |                          0 |                 134 |                      0 |                             1226 |                                 16485 |                           16469 |                           29643 |                                  32495 |                                       16485 |                                 16469 |                                     0 |                                         2852 |
|      15 |                          0 |                  10 |                      0 |                              611 |                                 13761 |                           13750 |                           22251 |                                  23701 |                                       13761 |                                 13750 |                                     0 |                                         1450 |
|      16 |                          0 |                   0 |                      0 |                              630 |                                 11255 |                           11245 |                           15446 |                                  15995 |                                       11255 |                                 11245 |                                     0 |                                          549 |
|      17 |                          0 |                   0 |                      0 |                              876 |                                  9349 |                            9340 |                            9312 |                                   9483 |                                        9349 |                                  9340 |                                     0 |                                          171 |
|      18 |                          0 |                   0 |                      0 |                             1506 |                                  8230 |                            8222 |                            3900 |                                   3915 |                                        8230 |                                  8222 |                                     0 |                                           15 |
|      19 |                          0 |                   0 |                      0 |                             1291 |                                  6909 |                            6902 |                            1411 |                                   1412 |                                        6909 |                                  6902 |                                     0 |                                            1 |
|      20 |                          0 |                   0 |                      0 |                              701 |                                  4891 |                            4885 |                             285 |                                    285 |                                        4891 |                                  4885 |                                     0 |                                            0 |
|      21 |                          0 |                   0 |                      0 |                              492 |                                  3255 |                            3250 |                              34 |                                     34 |                                        3255 |                                  3250 |                                     0 |                                            0 |
|      22 |                          0 |                   0 |                      0 |                               56 |                                  1273 |                            1270 |                               2 |                                      2 |                                        1273 |                                  1270 |                                     0 |                                            0 |
|      23 |                          0 |                   0 |                      0 |                                9 |                                   120 |                             118 |                               0 |                                      0 |                                         120 |                                   118 |                                     0 |                                            0 |
|      24 |                          0 |                   0 |                      0 |                                2 |                                    28 |                              27 |                               0 |                                      0 |                                          28 |                                    27 |                                     0 |                                            0 |
|      25 |                          0 |                   0 |                      0 |                                1 |                                     8 |                               8 |                               0 |                                      0 |                                           8 |                                     8 |                                     0 |                                            0 |



## % of classes (terms, groups, parts), by hierarchy
![% of classes (terms, groups, parts), by hierarchy](plot-class-depth_by-hierarchy_terms-groups-parts_percentages.png)

|   depth |   LOINC - LOINC Categories |   LOINC - LoincPart |   LOINC - LOINC Groups |   LOINC-SNOMED - SNOMED-Inspired |   CompLOINC-Primary - SNOMED-Inspired |   CompLOINC-Primary - LoincPart |   CompLOINC-Primary - LoincTerm |   CompLOINC-Primary - CompLOINC Groups |   CompLOINC-Supplementary - SNOMED-Inspired |   CompLOINC-Supplementary - LoincPart |   CompLOINC-Supplementary - LoincTerm |   CompLOINC-Supplementary - CompLOINC Groups |
|---------|----------------------------|---------------------|------------------------|----------------------------------|---------------------------------------|---------------------------------|---------------------------------|----------------------------------------|---------------------------------------------|---------------------------------------|---------------------------------------|----------------------------------------------|
|       1 |                     0.0027 |             0.00067 |                 0.0027 |                           0.0041 |                               0.00038 |                         0.00029 |                         0.00013 |                                0.00011 |                                     0.00038 |                               0.00029 |                                0.001  |                                      0.00056 |
|       2 |                     0.043  |            20       |                 0.12   |                           0.041  |                               0.16    |                         8.6     |                         0.00054 |                                0.00033 |                                     0.16    |                               8.6     |                                0.0041 |                                      0.0017  |
|       3 |                    19      |             2.5     |                19      |                           0.27   |                               0.17    |                         1.1     |                         0.02    |                                2.4     |                                     0.17    |                               1.1     |                                0.15   |                                     13       |
|       4 |                    81      |             5.6     |                81      |                           1.6    |                               0.91    |                         2.8     |                        11       |                               11       |                                     0.91    |                               2.8     |                               48      |                                     12       |
|       5 |                     0      |             2.5     |                 0      |                           3.3    |                               1.8     |                         2.1     |                        12       |                               12       |                                     1.8     |                               2.1     |                               37      |                                     12       |
|       6 |                     0      |             7.7     |                 0      |                           6.7    |                               4.6     |                         5.9     |                        11       |                               11       |                                     4.6     |                               5.9     |                               11      |                                     12       |
|       7 |                     0      |            13       |                 0      |                           8.3    |                               7.8     |                         9.4     |                        11       |                               11       |                                     7.8     |                               9.4     |                                2.8    |                                     11       |
|       8 |                     0      |            17       |                 0      |                           7.9    |                               9.7     |                        10       |                        10       |                               10       |                                     9.7     |                              10       |                                1      |                                     11       |
|       9 |                     0      |            15       |                 0      |                           8.1    |                              10       |                         9.8     |                         9.2     |                                9.1     |                                    10       |                               9.8     |                                0.17   |                                      8.8     |
|      10 |                     0      |             8.6     |                 0      |                           9.3    |                              10       |                         8.5     |                         7.8     |                                7.7     |                                    10       |                               8.5     |                                0.012  |                                      6.8     |
|      11 |                     0      |             5.2     |                 0      |                          11      |                               9.6     |                         7.5     |                         6.9     |                                6.5     |                                     9.6     |                               7.5     |                                0.001  |                                      5.2     |
|      12 |                     0      |             2.4     |                 0      |                           8.9    |                               8.4     |                         6.4     |                         5.8     |                                5.5     |                                     8.4     |                               6.4     |                                0      |                                      3.8     |
|      13 |                     0      |             0.8     |                 0      |                           4.8    |                               7.4     |                         5.7     |                         5.1     |                                4.6     |                                     7.4     |                               5.7     |                                0      |                                      2.7     |
|      14 |                     0      |             0.09    |                 0      |                           5      |                               6.2     |                         4.8     |                         4       |                                3.5     |                                     6.2     |                               4.8     |                                0      |                                      1.6     |
|      15 |                     0      |             0.0067  |                 0      |                           2.5    |                               5.2     |                         4       |                         3       |                                2.6     |                                     5.2     |                               4       |                                0      |                                      0.82    |
|      16 |                     0      |             0       |                 0      |                           2.6    |                               4.3     |                         3.3     |                         2.1     |                                1.7     |                                     4.3     |                               3.3     |                                0      |                                      0.31    |
|      17 |                     0      |             0       |                 0      |                           3.6    |                               3.5     |                         2.7     |                         1.2     |                                1       |                                     3.5     |                               2.7     |                                0      |                                      0.097   |
|      18 |                     0      |             0       |                 0      |                           6.1    |                               3.1     |                         2.4     |                         0.52    |                                0.43    |                                     3.1     |                               2.4     |                                0      |                                      0.0085  |
|      19 |                     0      |             0       |                 0      |                           5.2    |                               2.6     |                         2       |                         0.19    |                                0.15    |                                     2.6     |                               2       |                                0      |                                      0.00056 |
|      20 |                     0      |             0       |                 0      |                           2.8    |                               1.9     |                         1.4     |                         0.038   |                                0.031   |                                     1.9     |                               1.4     |                                0      |                                      0       |
|      21 |                     0      |             0       |                 0      |                           2      |                               1.2     |                         0.94    |                         0.0046  |                                0.0037  |                                     1.2     |                               0.94    |                                0      |                                      0       |
|      22 |                     0      |             0       |                 0      |                           0.23   |                               0.48    |                         0.37    |                         0.00027 |                                0.00022 |                                     0.48    |                               0.37    |                                0      |                                      0       |
|      23 |                     0      |             0       |                 0      |                           0.037  |                               0.045   |                         0.034   |                         0       |                                0       |                                     0.045   |                               0.034   |                                0      |                                      0       |
|      24 |                     0      |             0       |                 0      |                           0.0081 |                               0.011   |                         0.0078  |                         0       |                                0       |                                     0.011   |                               0.0078  |                                0      |                                      0       |
|      25 |                     0      |             0       |                 0      |                           0.0041 |                               0.003   |                         0.0023  |                         0       |                                0       |                                     0.003   |                               0.0023  |                                0      |                                      0       |

