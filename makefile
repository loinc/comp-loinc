# todo: catalog-v001.xml needs to be moved from owl-files into output before merged. and perhaps more from there?
.PHONY=stats

# All ------------------------------------------------------------------------------------------------------------------
all: stats

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
