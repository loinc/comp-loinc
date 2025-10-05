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
  "--property",
  "primary_component",
  "--property",
  "primary_system",

  "part-parent-types",
  "--type",
  "loinc",

  "part-parent-edges",
  "--edge",
  "has-parent",
  "--edge",
  "mapped-to",

  "group-generate",
  "--parent-group",
  "--parent-rounds",
  "3",
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
