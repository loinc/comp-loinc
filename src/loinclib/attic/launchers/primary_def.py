import pickle
import sys

from comp_loinc import comploinc_cli


sys.argv = [
  "cli_run",
  "builder",
  "set-module",
  "-n",
  "loinc-term-primary-def",
  "lt-inst-all",
  "--active",
  "lt-primary-def",


  # "l-label",
  # "l-annotate",
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
