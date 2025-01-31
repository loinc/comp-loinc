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
    "primary_component",
    "--properties",
    "primary_system",
    "group-parents",
    "--parents",
    "parent_comp_by_system",
    "--parents",
    "tree_parent",
    "group-parse-loincs",
    "group-roots",
    "group2-hello"
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
