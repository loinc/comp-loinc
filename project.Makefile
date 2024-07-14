CLI=$(RUN) python -m src.comp_loinc

.PHONY:
build:
	$(CLI) generate-all
