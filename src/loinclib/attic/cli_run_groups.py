import pickle
import sys

from comp_loinc import comploinc_cli

sys.argv = [
    "cli_run",
    "builder",
    "groups-index-props",
    # "--pickle",
    # ,'--supl'
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
