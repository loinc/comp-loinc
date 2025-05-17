.PHONY: all build modules grouping dangling merge-reason stats additional-outputs alternative-hierarchies \
	chebi-subsets
DEFAULT_BUILD_DIR=output/build-default
DANGLING_DIR=output/analysis/dangling
# STRICT:
#  - if true, sets '--equivalent-classes-allowed none' when reasoning.
#  - Usage: `make STRICT=true merge-reason`
# todo: STRICT: consider changing the goal where this is used to do '--equivalent-classes-allowed asserted-only' instead
STRICT ?= false

# All ------------------------------------------------------------------------------------------------------------------
all: build additional-outputs

build: grouping dangling modules merge-reason stats

additional-outputs: alternative-hierarchies

# Core modules ---------------------------------------------------------------------------------------------------------
MODULE_FILES = \
	$(DEFAULT_BUILD_DIR)/loinc-snomed-equiv.owl \
	$(DEFAULT_BUILD_DIR)/loinc-term-primary-def.owl \
	$(DEFAULT_BUILD_DIR)/loinc-term-supplementary-def.owl \
	$(DEFAULT_BUILD_DIR)/loinc-terms-list-all.owl \
	$(DEFAULT_BUILD_DIR)/loinc-part-hierarchy-all.owl \
	$(DEFAULT_BUILD_DIR)/loinc-part-list-all.owl \
	$(DEFAULT_BUILD_DIR)/snomed-parts.owl

modules: $(MODULE_FILES)

$(MODULE_FILES): curation/nlp-matches.sssom.tsv
	comploinc build

# Grouping classes -----------------------------------------------------------------------------------------------------
# todo: eventually, grouping classes will be part of `comploinc build`, and this separate part of the makefile will no longer be necessary
# todo: group_components_systems.owl will probably be removed. When that is done, update this goal.
GROUPING_FILES = \
	$(DEFAULT_BUILD_DIR)/group_components.owl \
	$(DEFAULT_BUILD_DIR)/group_systems.owl \
	$(DEFAULT_BUILD_DIR)/group_components_systems.owl \
	$(DANGLING_DIR)/dangling.tsv

grouping: $(GROUPING_FILES)

# todo: when the grouping classes put into the correct dir, can remove these mv steps
$(GROUPING_FILES):
	python src/loinclib/attic/cli_run_groups.py
	mv -f output/group_components.owl $(DEFAULT_BUILD_DIR)/group_components.owl
	mv -f output/group_systems.owl $(DEFAULT_BUILD_DIR)/group_systems.owl
	mv -f output/group_components_systems.owl $(DEFAULT_BUILD_DIR)/group_components_systems.owl

# Dangling part terms --------------------------------------------------------------------------------------------------
DANGLING_FILES = \
	curation/nlp-matches.sssom.tsv \
	$(DANGLING_DIR)/nlp-matches.sssom_prop_analysis.tsv \
	$(DANGLING_DIR)/confidence_histogram.png

$(DANGLING_FILES): $(DANGLING_DIR)/dangling.tsv
	python src/loinclib/nlp_taxonomification.py

dangling: $(DANGLING_FILES)

# Merging & reasoning --------------------------------------------------------------------------------------------------
STATIC_DIR = owl-files/comploinc-default
STATIC_MERGE_FILES = \
	$(DEFAULT_BUILD_DIR)/catalog-v001.xml \
	$(DEFAULT_BUILD_DIR)/comploinc.owl \
	$(DEFAULT_BUILD_DIR)/comploinc-axioms.owl

$(DEFAULT_BUILD_DIR)/catalog-v001.xml: $(STATIC_DIR)/catalog-v001.xml
	cp $< $@

$(DEFAULT_BUILD_DIR)/comploinc.owl: $(STATIC_DIR)/comploinc.owl
	cp $< $@

$(DEFAULT_BUILD_DIR)/comploinc-axioms.owl: $(STATIC_DIR)/comploinc-axioms.owl
	cp $< $@

# todo: consider: '--equivalent-classes-allowed asserted-only' instead
$(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned.owl: $(STATIC_MERGE_FILES) $(MODULE_FILES) $(GROUPING_FILES)
	$(eval EQUIV_FLAG := $(if $(filter true,$(STRICT)),--equivalent-classes-allowed none,))
	robot --catalog $(DEFAULT_BUILD_DIR)/catalog-v001.xml merge -i $(DEFAULT_BUILD_DIR)/comploinc.owl reason $(EQUIV_FLAG) --output $@

merge-reason: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned.owl

# Analysis / Stats  ----------------------------------------------------------------------------------------------------
TEMPLATE_AXIOMS_ENTITIES=src/comp_loinc/analysis/stats-main-axioms-entities.md.j2
TEMPLATE_MISC=src/comp_loinc/analysis/stats-misc.md.j2
PREFIXES_METRICS=\
	--prefix 'LOINC_PART: https://loinc.org/LP' \
	--prefix 'LOINC_TERM: https://loinc.org/' \
	--prefix 'LOINC_PART_GRP_CMP: http://comploinc//group/component/LP' \
	--prefix 'LOINC_PART_GRP_SYS: http://comploinc//group/system/LP' \
	--prefix 'LOINC_PART_GRP_CMP_SYS: http://comploinc//group/component-system/LP' \
	--prefix 'LOINC_PROP: http://loinc.org/property/' \
	--prefix 'COMPLOINC_AXIOM: https://comploinc-axioms\#' \
	--prefix 'SNOMED: http://snomed.info/'

input/analysis/:
	mkdir -p $@

output/analysis/:
	mkdir -p $@

output/tmp/:
	mkdir -p $@

output/tmp/stats.json: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned.owl | output/tmp/
	robot measure $(PREFIXES_METRICS) -i $< --format json --metrics extended --output $@
.PRECIOUS: output/tmp/stats.json

documentation/stats-axioms-entities.md: output/tmp/stats.json
	jinjanate "$(SOURCE_METRICS_TEMPLATE)" $< > $@

documentation/stats-misc.md: output/tmp/stats.json
	jinjanate "$(SOURCE_METRICS_TEMPLATE)" $< > $@

documentation/stats-dangling.md: curation/nlp-matches.sssom.tsv
	python src/loinclib/nlp_taxonomification.py --stats-only

output/tmp/subclass-rels-loinc-snomed.tsv: $(DEFAULT_BUILD_DIR)/snomed-parts.owl
	robot query -i $< --query src/comp_loinc/analysis/subclass-rels.sparql $@

output/tmp/subclass-rels-loinc.tsv: $(DEFAULT_BUILD_DIR)/loinc-part-hierarchy-all.owl
	robot query -i $< --query src/comp_loinc/analysis/subclass-rels.sparql $@

output/tmp/subclass-rels-comploinc.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned.owl
	robot query -i $< --query src/comp_loinc/analysis/subclass-rels.sparql $@

documentation/subclass-analysis.md: output/tmp/subclass-rels-loinc.tsv output/tmp/subclass-rels-loinc-snomed.tsv output/tmp/subclass-rels-comploinc.tsv
	python src/comp_loinc/analysis/subclass_rels.py --indir output/tmp/ --outpath $@

documentation/stats.md: documentation/stats-axioms-entities.md documentation/stats-dangling.md documentation/subclass-analysis.md documentation/stats-misc.md
	cat documentation/stats-axioms-entities.md documentation/subclass-analysis.md documentation/stats-dangling.md documentation/stats-misc.md > $@

stats: documentation/stats.md

# Additional outputs ---------------------------------------------------------------------------------------------------
# - Alternative hierarchies --------------------------------------------------------------------------------------------
# - ChEBI subsets
PART_MAPPINGS=loinc_release/Loinc_2.78/AccessoryFiles/PartFile/PartRelatedCodeMapping.csv
CHEBI_URI=http://purl.obolibrary.org/obo/chebi/chebi.owl.gz
CHEBI_OWL=input/analysis/chebi.owl
CHEBI_MODULE=output/analysis/chebi_module.txt
CHEBI_OUT_BOT=output/analysis/chebi-subset-BOT.owl
CHEBI_OUT_MIREOT=output/analysis/chebi-subset-MIREOT.owl

chebi-subsets: $(CHEBI_OUT_BOT) $(CHEBI_OUT_MIREOT)

input/analysis/chebi.owl.gz: | input/analysis/
	wget -O $@ $(CHEBI_URI)

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

alternative-hierarchies: chebi-subsets
