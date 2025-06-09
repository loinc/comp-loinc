Place the default modular output files in this directory and then open a `comploinc.owl`  in Protégé to get what is 
considered to be the default content of CompLOINC (still WIP).

## Variations
For a given set of modular output files, there are several standard ways to combine the modules into singular merged 
artefacts.

For each variation, there is a set of 2 files: 
- `catalog-v001-SOURCES-PART_MODEL.xml`
- `comploinc-SOURCES-PART_MODEL.owl`

Where `SOURCES` represents the source terminology content included, and is one of:
- LOINC: Includes the LOINC release & LOINC tree browser outputs
- LOINCSNOMED: For the LOINC-SNOMED Ontology
- all: Includes all sources.

And `MODEL` represents the part model chosen, and is one of:
- primary   
- supplemental

## Canonical version
The canonical version is "all-supplemental". That is, all sources (LOINC, LOINC-SNOMED Ontology), using just the 
supplementary part model.
- `catalog-v001-all-supplementary.xml`
- `comploinc-all-supplementary.owl`
