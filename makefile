# todo: catalog-v001.xml needs to be moved from owl-files into output before merged. and perhaps more from there?
.PHONY=all stats chebi-subsets

# All ------------------------------------------------------------------------------------------------------------------
all: stats chebi-subsets

# Analysis -------------------------------------------------------------------------------------------------------------
input/analysis/:
	mkdir -p $@

output/analysis/:
	mkdir -p $@

output/tmp/:
	mkdir -p $@

# Merging & reasoning --------------------------------------------------------------------------------------------------
output/build-default/merged-and-reasoned/comploinc-merged-reasoned.owl: output/build-default/merged-and-reasoned/comploinc-merged-unreasoned.owl
	robot reason --input $< --output $@

BUILD_DEFAULT_PATHS := $(wildcard output/build-default/*.owl)
output/build-default/merged-and-reasoned/comploinc-merged-unreasoned.owl: $(BUILD_DEFAULT_PATHS)
	robot merge $(patsubst %, --input %, $(BUILD_DEFAULT_PATHS)) --output $@

# Alternative hierarchies ----------------------------------------------------------------------------------------------
# - ChEBI subsets
PART_MAPPINGS=loinc_release/Loinc_2.78/AccessoryFiles/PartFile/PartRelatedCodeMapping.csv
CHEBI_OWL=input/analysis/chebi.owl
CHEBI_MODULE=output/analysis/chebi_module.txt
CHEBI_OUT_BOT=output/analysis/chebi-subset-BOT.owl
CHEBI_OUT_MIREOT=output/analysis/chebi-subset-MIREOT.owl

chebi-subsets: $(CHEBI_OUT_BOT) $(CHEBI_OUT_MIREOT)

input/analysis/chebi.owl.gz: | input/analysis/
	wget -O $@ ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl.gz

input/analysis/chebi.owl: input/analysis/chebi.owl.gz
	gunzip -c $< > $@
	rm $<

# todo: bug fix for label comment: Alwyas shows up as ' # ,'. Alternatively, I could just not include the label comment.
$(CHEBI_MODULE): $(PART_MAPPINGS) | output/analysis/
	awk -F'",' '/ebi\.ac\.uk\/chebi/ { \
		split($$0, parts, "\""); \
		for (i=1; i<=NF; i++) { \
			if (parts[i] ~ /CHEBI:/) { \
				id = parts[i]; \
				gsub(".*CHEBI:", "http://purl.obolibrary.org/obo/CHEBI_", id); \
				gsub(",.*", "", id); \
				print id " # " parts[i+1] \
			} \
		} \
	}' $< > $@

# BOT: use the SLME (Syntactic Locality Module Extractor) to extract a bottom module
# - Source: https://robot.obolibrary.org/extract
# - The BOT, or BOTTOM, -module contains mainly the terms in the seed, plus all their super-classes and the
# inter-relations between them. The module is called BOT (or BOTTOM) because it takes a view from the BOTTOM of the
# class-hierarchy upwards. Modules of this type are typically of a medium size and should be used if there is a need to
# include all super-classes in the module. This is the most widely used module type - when in doubt, use this one.
$(CHEBI_OUT_BOT): $(CHEBI_OWL) $(CHEBI_MODULE)
	robot extract --method BOT \
    --input $(CHEBI_OWL) \
    --term-file $(CHEBI_MODULE) \
    --output $@

# MIREOT: Minimum Information to Reference an External Ontology Term
# - Source: https://robot.obolibrary.org/extract
# - To specify upper and lower term files, use --upper-terms and --lower-terms. The upper terms are the upper boundaries
# of what will be extracted. If no upper term is specified, all terms up to the root (owl:Thing) will be returned. The
# lower term (or terms) is required; this is the limit to what will be extracted, e.g. no descendants of the lower term
# will be included in the result.
$(CHEBI_OUT_MIREOT): $(CHEBI_OWL) $(CHEBI_MODULE)
	robot extract --method MIREOT \
    --input $(CHEBI_OWL) \
    --lower-terms $(CHEBI_MODULE) \
    --output $@

# todo: SPARQL TSV subset: Just the classes themselves?
# - might require a jinja SPARQL or something like it, populated by the module
#output/analysis/chebi-terms.tsv: $(CHEBI_OWL) | output/analysis/
#	robot query -i $< -q src/sparql/mappings.sparql $@

# todo: Subset?
# - Source: https://robot.obolibrary.org/extract
# - The subset method extracts a sub-ontology that contains only the seed terms (that you specify with --term and
# --term-file options) and the relations between them. This method uses the relation-graph to materialize the
# existential relations among the seed terms. Procedurally, the subset method materializes the input ontology and adds
# the inferred axioms to the input ontology. Then filters the ontology with the given seed terms. Finally, it reduces
# the filtered ontology to remove redundant subClassOf axioms.
#output/analysis/chebi-subset-subsetOnly.owl: $(CHEBI_OWL) $(CHEBI_MODULE)
#	robot extract --method subset \
#	--input $(CHEBI_OWL) \
#	--term-file $(CHEBI_MODULE) \
#	--output $@

# Stats ----------------------------------------------------------------------------------------------------------------
stats: documentation/stats.md

SOURCE_METRICS_TEMPLATE=src/comp_loinc/analysis/stats.md.j2
PREFIXES_METRICS=--prefix 'LOINC_PART: https://loinc.org/LP' \
	--prefix 'LOINC_TERM: https://loinc.org/' \
	--prefix 'LOINC_PART_GRP_CMP: http://comploinc//group/component/LP' \
	--prefix 'LOINC_PART_GRP_SYS: http://comploinc//group/system/LP' \
	--prefix 'LOINC_PART_GRP_CMP_SYS: http://comploinc//group/component-system/LP' \

output/tmp/stats.json: output/build-default/merged-and-reasoned/comploinc-merged-reasoned.owl | output/tmp/
	robot measure $(PREFIXES_METRICS) -i $< --format json --metrics extended --output $@
.PRECIOUS: output/tmp/stats.json

documentation/stats.md: output/tmp/stats.json
	jinjanate "$(SOURCE_METRICS_TEMPLATE)" $< > $@