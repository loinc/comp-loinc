import sys

from comp_loinc import comploinc_cli

# sys.argv = [
#     "cli_run",
#     "--fast-run",
#     "build",
#     "lt-list-all",
#     # "--pickle",
#     # ,'--supl'
#     # ,'--help'
# ]

# sys.argv = [
#     "cli_run",
#     # "--fast-run",
#     "build",
#     "lt-primary-def",
#     # "--pickle",
#     # ,'--supl'
#     # ,'--help'
# ]

sys.argv = [
    "cli_run",
    "--fast-run",
    "build",
    "lt-supplementary-def",
    # "--pickle",
    # ,'--supl'
    # ,'--help'
]

# sys.argv = [
#     "cli_run",
#     "--fast-run",
#     "build",
#     "default",
#     # "--pickle",
#     # ,'--supl'
#     # ,'--help'
# ]


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
