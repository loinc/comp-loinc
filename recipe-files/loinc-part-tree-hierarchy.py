from sys import argv, orig_argv

from comp_loinc.cli import comploinc_file_cli

argv.append('recipe-files/loinc-part-tree-hierarchy.txt')

comploinc_file_cli()
