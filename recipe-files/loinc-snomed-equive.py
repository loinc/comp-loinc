from sys import argv, orig_argv

from comp_loinc.cli import comploinc_file_cli

argv.append('recipe-files/loinc-snomed-equiv.txt')

comploinc_file_cli()
