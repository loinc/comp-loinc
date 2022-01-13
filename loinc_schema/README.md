# LOINC Information Schema
This folder is located here: https://github.com/loinc/comp-loinc/linkml

A schema/model to demonstrate use of LinkML using initial LOINC Hierarchy and LPL data. For more information, please visit (https://linkml.io/linkml/index.html)

Latest updates as of 1/13/2022
- Added comments, constraints(slot_uri, pattern), enums, and 5 classes 

Initial schema sketch using lucid
![initial_lucid_schema](lucid.png)

 * [loincinfo.yaml](loincinfo.yaml) -- schema source
 * [loincinfo.py](loincinfo.py) -- generated python datamodel 
 * [Hierarchy_and_LPL_data.xlsx](Hierarchy_and_LPL_data.xlsx) -- schema source 
 * [data.ttl](data.ttl) -- output data

## Schema Diagram

generated via `gen-yuml`:

![schema](32fa8d11.jpeg)
