

CREATE TABLE "ComponentClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	part_number TEXT, 
	part_type TEXT, 
	"subClassOf" TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "LoincCodeOntology" (
	component_class_set TEXT, 
	system_class_set TEXT, 
	code_class_set TEXT, 
	PRIMARY KEY (component_class_set, system_class_set, code_class_set)
);

CREATE TABLE "MethodClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	part_number TEXT, 
	part_type TEXT, 
	"subClassOf" TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "PartClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	part_number TEXT, 
	part_type TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "PropertyClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	part_number TEXT, 
	part_type TEXT, 
	"subClassOf" TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "ScaleClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	part_number TEXT, 
	part_type TEXT, 
	"subClassOf" TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "SystemClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	part_number TEXT, 
	part_type TEXT, 
	"subClassOf" TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "TimeClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	part_number TEXT, 
	part_type TEXT, 
	"subClassOf" TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "CodeByComponent" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	has_component TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_component) REFERENCES "ComponentClass" (id)
);

CREATE TABLE "CodeBySystem" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	has_system TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_system) REFERENCES "SystemClass" (id)
);

CREATE TABLE "LoincCodeClass" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	"subClassOf" TEXT NOT NULL, 
	formal_name TEXT, 
	loinc_number TEXT, 
	status TEXT, 
	short_name TEXT, 
	long_common_name TEXT, 
	has_component TEXT, 
	has_property TEXT, 
	has_system TEXT, 
	has_method TEXT, 
	has_scale TEXT, 
	has_time TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_component) REFERENCES "ComponentClass" (id), 
	FOREIGN KEY(has_property) REFERENCES "PropertyClass" (id), 
	FOREIGN KEY(has_system) REFERENCES "SystemClass" (id), 
	FOREIGN KEY(has_method) REFERENCES "MethodClass" (id), 
	FOREIGN KEY(has_scale) REFERENCES "ScaleClass" (id), 
	FOREIGN KEY(has_time) REFERENCES "TimeClass" (id)
);

CREATE TABLE "Thing" (
	id TEXT NOT NULL, 
	label TEXT, 
	description TEXT, 
	"PartClass_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("PartClass_id") REFERENCES "PartClass" (id)
);
