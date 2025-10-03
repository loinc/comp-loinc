import pickle
import sys

from comp_loinc import comploinc_cli

sys.argv = [
  "cli_run",
  "builder",

  "set-module",
  "-n",
  "test",

  "group-properties",
  "--properties",
  "/component",
  "--properties",
  "/system",

  # "parent-types",

  # "--type",
  # "snomed",

  "group-parse-loincs",

  "part-ancestors",
  "--parent-type",
  "loinc",
  #
  "group-generate",
  "--parent-group",
  #
  "save-owl"
  # ,'--help'
]

# sys.argv = ['cli_run',
#
#             'builder',
#             'load-schema',
#             'set-module', '--name', 'test',
#             'lt-inst-all',
#             'load-schema', # '-f', 'comp_loinc_v2.yaml',
#              'save-owl',
#
#             '--help'
#             ]

comploinc_cli()
