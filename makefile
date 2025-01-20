# TODO: catalog-v001.xml needs to be moved from owl-files into output before merged. and perhaps more from there?
.PHONY=metrics

# All ------------------------------------------------------------------------------------------------------------------
all: metrics temp-reasoned-extras

# Analysis -------------------------------------------------------------------------------------------------------------
input/analysis/:
	mkdir -p $@

output/analysis/:
	mkdir -p $@

metrics: output/groups.owl

# Grouping classes -----------------------------------------------------------------------------------------------------
######## todo temp
temp-reasoned-extras: output/temp/ output/temp/group_components_reasoned_temp.owl output/temp/group_components_systems_reasoned_temp.owl output/temp/group_systems_reasoned_temp.owl
output/temp/:
	mkdir -p $@
output/temp/group_components_reasoned_temp.owl: output/group_components.owl
	robot reason --input $< --output $@
output/temp/group_components_systems_reasoned_temp.owl:  output/group_components_systems.owl
	robot reason --input $< --output $@
output/temp/group_systems_reasoned_temp.owl: output/group_systems.owl
	robot reason --input $< --output $@
#########

output/groups-unreasoned.owl: output/group_components.owl output/group_components_systems.owl output/group_systems.owl
	robot merge --input output/group_components.owl --input output/group_components_systems.owl \
	--input output/group_systems.owl --output $@

output/groups.owl: output/groups-unreasoned.owl
	robot reason --input $< --output $@
