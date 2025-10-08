import pickle
import sys

from comp_loinc import comploinc_cli


sys.argv = [
  "cli_run",
  "builder",
  "set-module",
  "-n",
  "snomed-parts",
  "sct-loinc-part-map-instances",
  "sct-close-isa",
  "sct-label",
  "save-owl"
]


comploinc_cli()
