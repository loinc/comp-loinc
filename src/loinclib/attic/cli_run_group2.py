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
    "-p",
    "http://loinc.org/property/COMPONENT",
    "-p",
    "TIME_ASPCt",
    "-p",
    "document-subject-matter-domain",
    "group-parse-loincs"
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
