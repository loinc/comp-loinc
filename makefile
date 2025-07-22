# Default build, run: `make all -B`
# todo: Ideally would change pipeline to use `make all` instead of `make all -B`. Leaving -B out is preferred whenever possible, because it will theoretically only update targets and their prereqs that are outdated. But if the codebase changes, these files will be outdated but they will not appear so to make, which means we must execute using -B.

.PHONY: all build modules grouping dangling merge-reason stats additional-outputs alternative-hierarchies \
	chebi-subsets start-app test
DEFAULT_BUILD_DIR=output/build-default
DANGLING_DIR=output/analysis/dangling
LOINC_OWL_DIR=output/analysis/loinc
LOINC_SNOMED_OWL_DIR=output/analysis/loinc-snomed
SNOMED_OWL_DIR=output/analysis/snomed

# Resolve the directory name for the default LOINC release using the
# project's Python configuration.  This is required so that the
# analysis targets always reference the correct release directory.
LOINC_DEFAULT_DIR := $(shell python src/loinclib/config.py --method-names get_loinc_default_dir_name)
# STRICT:
#  - if true, sets '--equivalent-classes-allowed none' when reasoning.
#  - Usage: `make STRICT=true merge-reason`
# todo: STRICT: consider changing the goal where this is used to do '--equivalent-classes-allowed asserted-only' instead
STRICT ?= false

# All ------------------------------------------------------------------------------------------------------------------
# todo: remove 'all' and 'build' as is and replace with: 'all: documentation/stats.md'. Should be same result.
all: build additional-outputs

build: grouping dangling modules merge-reason stats

additional-outputs: alternative-hierarchies

# Functions ------------------------------------------------------------------------------------------------------------
# Remove subclass axioms
# 1: The input file; 2: the output file
define remove_subclass_axioms
robot remove --input $(1) --axioms "subclass" --output $(2)
endef

# Run a ROBOT SPARQL query
# 1: The input file; 2: the query; 3: the output file
define robot_query
robot query -i $(1) --query $(2) $(3)
endef

# Core modules ---------------------------------------------------------------------------------------------------------
MODULE_FILES = \
	$(DEFAULT_BUILD_DIR)/loinc-snomed-equiv.owl \
	$(DEFAULT_BUILD_DIR)/loinc-term-primary-def.owl \
	$(DEFAULT_BUILD_DIR)/loinc-term-supplementary-def.owl \
	$(DEFAULT_BUILD_DIR)/loinc-terms-list-all.owl \
	$(DEFAULT_BUILD_DIR)/loinc-part-hierarchy-all.owl \
	$(DEFAULT_BUILD_DIR)/loinc-part-list-all.owl \
	$(DEFAULT_BUILD_DIR)/snomed-parts.owl

$(MODULE_FILES): output/tmp/.main-modules-built

output/tmp/.main-modules-built: curation/nlp-matches.sssom.tsv | output/tmp/
	comploinc build
	touch $@

modules: output/tmp/.main-modules-built

# Grouping classes -----------------------------------------------------------------------------------------------------
# todo: eventually, grouping classes will be part of `comploinc build`, and this separate part of the makefile will no longer be necessary
# todo: group_components_systems.owl will probably be removed. When that is done, update this goal.
GROUPING_FILES = \
	$(DEFAULT_BUILD_DIR)/group_components.owl \
	$(DEFAULT_BUILD_DIR)/group_systems.owl \
	$(DEFAULT_BUILD_DIR)/group_components_systems.owl \
	$(DANGLING_DIR)/dangling.tsv

$(GROUPING_FILES): output/tmp/.grouping-modules-built

# todo: when the grouping classes put into the correct dir, can remove these mv steps
output/tmp/.grouping-modules-built: | output/tmp/
	python src/loinclib/attic/cli_run_groups.py
	mkdir -p $(DEFAULT_BUILD_DIR)
	mv -f output/group_components.owl $(DEFAULT_BUILD_DIR)/group_components.owl
	mv -f output/group_systems.owl $(DEFAULT_BUILD_DIR)/group_systems.owl
	mv -f output/group_components_systems.owl $(DEFAULT_BUILD_DIR)/group_components_systems.owl

grouping: output/tmp/.grouping-modules-built

# Dangling part terms --------------------------------------------------------------------------------------------------
DANGLING_FILES = \
	curation/nlp-matches.sssom.tsv \
	$(DANGLING_DIR)/nlp-matches.sssom_prop_analysis.tsv \
	$(DANGLING_DIR)/confidence_histogram.png

$(DANGLING_FILES): output/tmp/.dangling-outputs-built

output/tmp/.dangling-outputs-built: $(DANGLING_DIR)/dangling.tsv | output/tmp/
	python src/loinclib/nlp_taxonomification.py
	touch $@

dangling: output/tmp/.dangling-outputs-built

# Merging & reasoning --------------------------------------------------------------------------------------------------
STATIC_DIR = owl-files/comploinc-default
SOURCES := LOINC LOINCSNOMED all
MODELS := primary supplementary
FLAVORS := $(foreach source,$(SOURCES),$(foreach model,$(MODELS),$(source)-$(model)))

.SILENT: $(DEFAULT_BUILD_DIR)/catalog-v001-%.xml
$(DEFAULT_BUILD_DIR)/catalog-v001-%.xml: $(STATIC_DIR)/catalog-v001-%.xml
	@cp $< $@

.SILENT: $(DEFAULT_BUILD_DIR)/comploinc-%.owl
$(DEFAULT_BUILD_DIR)/comploinc-%.owl: $(STATIC_DIR)/comploinc-%.owl
	@cp $< $@

$(DEFAULT_BUILD_DIR)/comploinc-axioms.owl: $(STATIC_DIR)/comploinc-axioms.owl
	cp $< $@

# canonical build
$(DEFAULT_BUILD_DIR)/merged-and-reasoned/canonical/comploinc-merged-reasoned-all-supplementary.owl: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-all-supplementary.owl | $(DEFAULT_BUILD_DIR)/merged-and-reasoned/canonical/
	cp $< $@

# build flavors
# todo: consider: '--equivalent-classes-allowed asserted-only' instead
# todo: Drop the 'merged' from the name? shouldn't it be obvious by the fact that it says 'comploinc'? though i guess there is a comploinc.owl in owl-files/
$(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-%.owl: $(DEFAULT_BUILD_DIR)/catalog-v001-%.xml $(DEFAULT_BUILD_DIR)/comploinc-%.owl $(DEFAULT_BUILD_DIR)/comploinc-axioms.owl output/tmp/.main-modules-built output/tmp/.grouping-modules-built | $(DEFAULT_BUILD_DIR)/merged-and-reasoned/
	$(eval EQUIV_FLAG := $(if $(filter true,$(STRICT)),--equivalent-classes-allowed none,))
	robot --catalog $(DEFAULT_BUILD_DIR)/catalog-v001-$*.xml merge -i $(DEFAULT_BUILD_DIR)/comploinc-$*.owl reason $(EQUIV_FLAG) --output $@

# build flavors: including inferred subclass axioms
$(DEFAULT_BUILD_DIR)/merged-and-reasoned/inferred-sc-axioms-included/comploinc-merged-reasoned-%.owl: $(DEFAULT_BUILD_DIR)/catalog-v001-%.xml $(DEFAULT_BUILD_DIR)/comploinc-%.owl $(DEFAULT_BUILD_DIR)/comploinc-axioms.owl output/tmp/.main-modules-built output/tmp/.grouping-modules-built | $(DEFAULT_BUILD_DIR)/merged-and-reasoned/inferred-sc-axioms-included/
	$(eval EQUIV_FLAG := $(if $(filter true,$(STRICT)),--equivalent-classes-allowed asserted-only,))
	robot --catalog $(DEFAULT_BUILD_DIR)/catalog-v001-$*.xml merge -i $(DEFAULT_BUILD_DIR)/comploinc-$*.owl reason $(EQUIV_FLAG) --include-indirect true --output $@

merge-reason: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/canonical/comploinc-merged-reasoned-all-supplementary.owl $(foreach flavor,$(FLAVORS),$(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-$(flavor).owl) $(foreach flavor,$(FLAVORS),$(DEFAULT_BUILD_DIR)/merged-and-reasoned/inferred-sc-axioms-included/comploinc-merged-reasoned-$(flavor).owl)

# Analysis / Stats  ----------------------------------------------------------------------------------------------------
# - defs & dirs
TEMPLATE_AXIOMS_ENTITIES=src/comp_loinc/analysis/stats-main-axioms-entities.md.j2
TEMPLATE_MISC=src/comp_loinc/analysis/stats-misc.md.j2
# todo: for https://loinc.org/category/, maybe it'd be better to add a CompLOINC URI since even though this is part of LOINC and not CompLOINC the ontology, it is CompLOINC the project that ontologises these classes
PREFIXES_METRICS=\
	--prefix 'LOINC_CATEGORY: https://loinc.org/category/' \
	--prefix 'LOINC_GROUP: https://loinc.org/LG' \
	--prefix 'LOINC_PART: https://loinc.org/LP' \
	--prefix 'LOINC_TERM: https://loinc.org/' \
	--prefix 'LOINC_PART_GRP_CMP: http://comploinc//group/component/LP' \
	--prefix 'LOINC_PART_GRP_SYS: http://comploinc//group/system/LP' \
	--prefix 'LOINC_PART_GRP_CMP_SYS: http://comploinc//group/component-system/LP' \
	--prefix 'LOINC_PROP: http://loinc.org/property/' \
	--prefix 'COMPLOINC_AXIOM: https://comploinc-axioms\#' \
	--prefix 'SNOMED: http://snomed.info/id/'

input/analysis/:
	mkdir -p $@

output/analysis/:
	mkdir -p $@

$(LOINC_OWL_DIR):
	mkdir -p $@

$(LOINC_SNOMED_OWL_DIR):
	mkdir -p $@

$(SNOMED_OWL_DIR):
	mkdir -p $@

output/tmp/:
	mkdir -p $@

$(DEFAULT_BUILD_DIR)/merged-and-reasoned/:
	mkdir -p $@

$(DEFAULT_BUILD_DIR)/merged-and-reasoned/canonical/:
	mkdir -p $@

$(DEFAULT_BUILD_DIR)/merged-and-reasoned/inferred-sc-axioms-included/:
	mkdir -p $@

documentation/analyses/class-depth/:
	mkdir -p $@

# - robot stats & markdown files
output/tmp/stats.json: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/canonical/comploinc-merged-reasoned-all-supplementary.owl | output/tmp/
	robot measure $(PREFIXES_METRICS) -i $< --format json --metrics extended --output $@
.PRECIOUS: output/tmp/stats.json

documentation/stats-main-axioms-entities.md: output/tmp/stats.json
	jinjanate src/comp_loinc/analysis/stats-main-axioms-entities.md.j2 $< > $@

documentation/stats-misc.md: output/tmp/stats.json
	jinjanate src/comp_loinc/analysis/stats-misc.md.j2 $< > $@

documentation/stats-dangling.md: curation/nlp-matches.sssom.tsv
	python src/loinclib/nlp_taxonomification.py --stats-only

# - Comparisons: LOINC-SNOMED Ontology
# -- SNOMED representation
# ROBOT_JAVA_ARGS='-Xmx...G': for some reason runs out of memory even on simple query: Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
$(SNOMED_OWL_DIR)/snomed-unreasoned.ofn: | $(SNOMED_OWL_DIR)
	python src/comp_loinc/analysis/snomed_rf2_parser.py --by-module-name snomed --outpath $@.tmp
	ROBOT_JAVA_ARGS='-Xmx16G' robot query --input $@.tmp --update src/comp_loinc/analysis/remove-jellyfish-sting.sparql --output $@
	rm -f $@.tmp

# todo: consider if there is value in using this to extract in place of -unreasoned for building LOINC-SNOMED Ontology
# FYI: if not .ofn, get: https://robot.obolibrary.org/errors#invalid-element-error due to :-namespace and inlining of annotation prop refs. So if we want RDF/XML, we should use a SNOMED prefix rather than:.
#$(SNOMED_OWL_DIR)/snomed-reasoned.ofn: $(SNOMED_OWL_DIR)/snomed-unreasoned.ofn
	#robot reason --input $< --output $@

# Extract ancestors: See https://robot.obolibrary.org/extract (ChEBI goal in this makefile also has more info)
$(LOINC_SNOMED_OWL_DIR)/related-snomed-ancestor-closure.owl: $(LOINC_SNOMED_OWL_DIR)/snomed-with-loinc-snomed-full-unreasoned.ofn $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module-classes-and-props.txt
	robot extract --method BOT \
	--input $(LOINC_SNOMED_OWL_DIR)/snomed-with-loinc-snomed-full-unreasoned.ofn \
	--term-file $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module-classes-and-props.txt --output $@

# -- LOINC-SNOMED representation
# Intermediate file: We don't actually care about full SNOMED enhanced by LOINC-SNOMED Ontology. This is just a temporary step to be used in `robot extract`
$(LOINC_SNOMED_OWL_DIR)/snomed-with-loinc-snomed-full-unreasoned.ofn: $(SNOMED_OWL_DIR)/snomed-unreasoned.ofn $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module.ofn
	robot merge --input $(SNOMED_OWL_DIR)/snomed-unreasoned.ofn --input $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module.ofn --output $@

# Representation of LOINC-SNOMED Ontology module (lacks ancestors from SNOMED)
$(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module.ofn: | $(LOINC_SNOMED_OWL_DIR)
	python src/comp_loinc/analysis/snomed_rf2_parser.py --by-module-name loinc-snomed --outpath $@

$(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module-classes-and-props.txt: $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module.ofn
	$(call robot_query,$<,src/comp_loinc/analysis/classes-and-props.sparql,$@.tmp)
	grep '^http' $@.tmp | sort > $@
	rm -f $@.tmp

# Full representation of LOINC-SNOMED Ontology: combines the LOINC-SNOMED module with ancestor classes from SNOMED proper
$(LOINC_SNOMED_OWL_DIR)/loinc-snomed-unreasoned.owl: $(LOINC_SNOMED_OWL_DIR)/related-snomed-ancestor-closure.owl $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module.ofn
	robot merge --input $(LOINC_SNOMED_OWL_DIR)/related-snomed-ancestor-closure.owl --input $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-module.ofn --output $@

$(LOINC_SNOMED_OWL_DIR)/loinc-snomed-reasoned.owl: $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-unreasoned.owl
	robot reason --input $< --output $@

$(LOINC_SNOMED_OWL_DIR)/loinc-snomed-reasoned-indirect-sc-axioms-included.owl: $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-unreasoned.owl
	robot reason --input $< --include-indirect true --output $@

# uses `subsumption.sparql` instead of `subclass-rels.sparql` SNOMED uses data property hierarchies, not just subClassOf as is the case with our constructed LOINC representation of the part hierarchy obtained from the tree browser (and improted into CompLOINC)
# todo: use reasoned or unreasoned?
output/tmp/subclass-rels-loinc-snomed.tsv: $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-reasoned.owl
	$(call robot_query,$<,src/comp_loinc/analysis/subsumption.sparql,$@)

# TODO temp: Keep this goal? maybe i won't end up using. or if i don't end up using the one above, remove that instead
output/tmp/subclass-rels-loinc-snomed-indirect-sc-axioms-included.tsv: $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-reasoned-indirect-sc-axioms-included.owl
	$(call robot_query,$<,src/comp_loinc/analysis/subsumption.sparql,$@)

# querying unreasoned also fine
output/tmp/labels-loinc-snomed.tsv: $(LOINC_SNOMED_OWL_DIR)/loinc-snomed-reasoned.owl
	$(call robot_query,$<,src/comp_loinc/analysis/labels.sparql,$@)

# - Comparisons: LOINC
$(LOINC_OWL_DIR)/loinc-groups.owl: output/tmp/loinc-groups.robot.tsv | $(LOINC_OWL_DIR)
	robot template --template $< \
	--prefix 'LOINC_CATEGORY: https://loinc.org/category/' \
	--prefix 'LOINC_GROUP: https://loinc.org/LG' \
	--prefix 'LOINC_TERM: https://loinc.org/' \
  	--ontology-iri "https://github.com/loinc/comploinc/source-representations/loinc/loing-groups.owl" \
  	--output $@

output/tmp/loinc-groups.robot.tsv: | output/tmp/
	python src/comp_loinc/analysis/loinc_groups.py \
	--group-path loinc_release/$(LOINC_DEFAULT_DIR)/AccessoryFiles/GroupFile/Group.csv\
	--parent-group-path loinc_release/$(LOINC_DEFAULT_DIR)/AccessoryFiles/GroupFile/ParentGroup.csv\
    --group-loinc-terms-path loinc_release/$(LOINC_DEFAULT_DIR)/AccessoryFiles/GroupFile/GroupLoincTerms.csv\
	--outpath $@

$(LOINC_OWL_DIR)/loinc-terms-list-all-sans-sc-axioms.owl: $(DEFAULT_BUILD_DIR)/loinc-terms-list-all.owl | $(LOINC_OWL_DIR)
	$(call remove_subclass_axioms,$<,$@)

# loinc-unreasoned.owl: This representation includes (i) group defs, (ii) term defs, (iii) part defs, (iv) subclass axioms (groups::groups, terms::groups; part::part; no term::term exist). Doesn't include: equivalent class axioms for temrs (for neither part model)
$(LOINC_OWL_DIR)/loinc-unreasoned.owl: $(DEFAULT_BUILD_DIR)/loinc-part-list-all.owl $(DEFAULT_BUILD_DIR)/loinc-part-hierarchy-all.owl $(LOINC_OWL_DIR)/loinc-terms-list-all-sans-sc-axioms.owl $(LOINC_OWL_DIR)/loinc-groups.owl | $(LOINC_OWL_DIR)
	robot merge --input $(DEFAULT_BUILD_DIR)/loinc-part-hierarchy-all.owl --input $(DEFAULT_BUILD_DIR)/loinc-part-hierarchy-all.owl --input $(LOINC_OWL_DIR)/loinc-terms-list-all-sans-sc-axioms.owl --input $(LOINC_OWL_DIR)/loinc-groups.owl --output $@

# loinc-reasoned.owl: Not including, because the LOINC release is not reasoned, so it doesn't make sense for us to use this for our comparisons.
#$(LOINC_OWL_DIR)/loinc-reasoned.owl: $(LOINC_OWL_DIR)/loinc-unreasoned.owl | $(LOINC_OWL_DIR)
#	robot reason --input $< --output $@

output/tmp/subclass-rels-loinc.tsv: $(LOINC_OWL_DIR)/loinc-unreasoned.owl
	$(call robot_query,$<,src/comp_loinc/analysis/subclass-rels.sparql,$@)

output/tmp/labels-loinc.tsv: $(LOINC_OWL_DIR)/loinc-unreasoned.owl
	$(call robot_query,$<,src/comp_loinc/analysis/labels.sparql,$@)

# - Comparisons: CompLOINC
output/tmp/subclass-rels-comploinc-primary.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-all-primary.owl
	$(call robot_query,$<,src/comp_loinc/analysis/subclass-rels.sparql,$@)

output/tmp/subclass-rels-comploinc-supplementary.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-all-supplementary.owl
	$(call robot_query,$<,src/comp_loinc/analysis/subclass-rels.sparql,$@)

output/tmp/subclass-rels-comploinc-inferred-included-primary.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/inferred-sc-axioms-included/comploinc-merged-reasoned-all-primary.owl
	$(call robot_query,$<,src/comp_loinc/analysis/subclass-rels.sparql,$@)

output/tmp/subclass-rels-comploinc-inferred-included-supplementary.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/inferred-sc-axioms-included/comploinc-merged-reasoned-all-supplementary.owl
	$(call robot_query,$<,src/comp_loinc/analysis/subclass-rels.sparql,$@)

output/tmp/labels-comploinc-primary.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-all-primary.owl
	$(call robot_query,$<,src/comp_loinc/analysis/labels.sparql,$@)

output/tmp/labels-comploinc-supplementary.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-all-supplementary.owl
	$(call robot_query,$<,src/comp_loinc/analysis/labels.sparql,$@)

# - Comparisons: all
output/tmp/labels-all-terminologies.tsv: output/tmp/labels-loinc.tsv output/tmp/labels-loinc-snomed.tsv output/tmp/labels-comploinc-primary.tsv output/tmp/labels-comploinc-supplementary.tsv
	cat $^ > $@

documentation/subclass-analysis.md documentation/upset.png output/tmp/missing_comploinc_axioms.tsv: output/tmp/subclass-rels-loinc.tsv output/tmp/subclass-rels-loinc-snomed.tsv output/tmp/subclass-rels-comploinc-inferred-included-primary.tsv output/tmp/subclass-rels-comploinc-inferred-included-supplementary.tsv
	python src/comp_loinc/analysis/subclass_rels.py \
	--loinc-path output/tmp/subclass-rels-loinc.tsv \
	--loinc-snomed-path output/tmp/subclass-rels-loinc-snomed.tsv \
	--comploinc-primary-path output/tmp/subclass-rels-comploinc-inferred-included-primary.tsv \
	--comploinc-supplementary-path output/tmp/subclass-rels-comploinc-inferred-included-supplementary.tsv \
	--outpath-md documentation/subclass-analysis.md \
	--outpath-upset-plot documentation/upset.png

documentation/analyses/class-depth/depth.md: output/tmp/subclass-rels-loinc.tsv output/tmp/subclass-rels-loinc-snomed.tsv output/tmp/subclass-rels-comploinc-primary.tsv output/tmp/subclass-rels-comploinc-supplementary.tsv output/tmp/labels-all-terminologies.tsv | documentation/analyses/class-depth/
	python src/comp_loinc/analysis/depth.py \
	--loinc-path output/tmp/subclass-rels-loinc.tsv \
	--loinc-snomed-path output/tmp/subclass-rels-loinc-snomed.tsv \
	--comploinc-primary-path output/tmp/subclass-rels-comploinc-primary.tsv \
	--comploinc-supplementary-path output/tmp/subclass-rels-comploinc-supplementary.tsv \
	--labels-path output/tmp/labels-all-terminologies.tsv \
	--outpath-md documentation/analyses/class-depth/depth.md \
	--outdir-plots documentation/analyses/class-depth

# - Build final outputs & main command
documentation/stats.md: documentation/stats-main-axioms-entities.md documentation/stats-dangling.md documentation/subclass-analysis.md documentation/analyses/class-depth/depth.md documentation/stats-misc.md
	cat documentation/stats-main-axioms-entities.md documentation/subclass-analysis.md documentation/stats-dangling.md documentation/analyses/class-depth/depth.md documentation/stats-misc.md > $@

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

# Ad hoc analyses: not connected to the main pipeline
output/tmp/cl-parts.tsv: $(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned.owl
	$(call robot_query,$<,src/comp_loinc/analysis/ad_hoc/cl-parts.sparql,$@)

start-app-debug:
	python src/comp_loinc/analysis/app.py

start-app:
	#gunicorn comp_loinc.analysis.app:server --bind 0.0.0.0:$PORT  # this is the version of the command used on render.com
	gunicorn src.comp_loinc.analysis.app:server

# - Testing -------------------------------------------------------------------------------------------------------------
test:
	python -m unittest discover
