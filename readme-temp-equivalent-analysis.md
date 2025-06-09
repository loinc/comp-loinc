# Setup
Before running, create the log files:

For each MODE `none`, `asserted-only`
1) Ensure STRICT=true at the top of the makefile.
2) In the makefile, go to the goal for `$(DEFAULT_BUILD_DIR)/merged-and-reasoned/comploinc-merged-reasoned-%.owl`, and in the body, update `--equivalent-classes-allowed MODE` for this given mode.
3) Update the following snippet with the `MODE`, and run it to create the log files.

```
make output/build-default/merged-and-reasoned/comploinc-merged-reasoned-all-primary.owl > MODE--all-primary.txt 2>&1
make output/build-default/merged-and-reasoned/comploinc-merged-reasoned-all-supplementary.owl > MODE--all-supplementary.txt 2>&1
make output/build-default/merged-and-reasoned/comploinc-merged-reasoned-LOINC-primary.owl > MODE--LOINC-primary.txt 2>&1
make output/build-default/merged-and-reasoned/comploinc-merged-reasoned-LOINC-supplementary.owl > MODE--LOINC-supplementary.txt 2>&1
make output/build-default/merged-and-reasoned/comploinc-merged-reasoned-LOINCSNOMED-primary.owl > MODE--LOINCSNOMED-primary.txt 2>&1
make output/build-default/merged-and-reasoned/comploinc-merged-reasoned-LOINCSNOMED-supplementary.owl > MODE--LOINCSNOMED-supplementary.txt 2>&1
```

# Prompt
## Overview
We want to make a file in the root of the repo called `temp_equivalence_analysis.py`.

We will be reading log files, parsing out certain lines, then creating an xlsx where each tab contains data that was extracted and transformed from each log file, as well as some summary statistics.

## Packages
Note that your setup instructions include a step to install Python packages: `pip install -r codex-requirements.txt`. Only `pandas` is listed there, but you will need a package to write .xlsx. I want to let you pick that package, along with any other packages you might need, adding to `codex-requirements.txt`, and then install the resulting packages you added.

## Running, committing, and pull request
When you finish coding, run the `temp_equivalence_analysis.py`, commit any outputs, and open a pull request.

## Reading & parsing
The files to be read are all in the root of the repository and have the following filename pattern: `MODE--FLAVOR.txt`.

All log files look similar to this:
```
robot --catalog output/build-default/catalog-v001-LOINCSNOMED-supplementary.xml merge -i output/build-default/comploinc-LOINCSNOMED-supplementary.owl reason --equivalent-classes-allowed none --output output/build-default/merged-and-reasoned/comploinc-merged-reasoned-LOINCSNOMED-supplementary.owl
ERROR No equivalent class axioms are allowed
ERROR Equivalence: <https://loinc.org/39500-4> == <https://loinc.org/44235-0>
...
ERROR Equivalence: <https://loinc.org/LP15163-6> == <https://loinc.org/372831009>
make: *** [output/build-default/merged-and-reasoned/comploinc-merged-reasoned-LOINCSNOMED-primary.owl] Error 1
rm output/build-default/catalog-v001-LOINCSNOMED-primary.xml
```

From each of these log files, we're only interested in these lines: `ERROR Equivalence: <https://loinc.org/LP15163-6> == <https://loinc.org/372831009>`. Your Python script should include a step where you create pandas dataframes for each of these log files, with the columns `cls1` and `cls2`. `cls` means "class code", FYI. So for this example line, `cls1` would be `LP15163-6`, and `cls2` would be `372831009`. 

Next, you'll want to add class labels. There is a file called `labels.tsv`. This file is currently empty except for the headers, which have fields `cls` and `label`. `cls` contains the same "class codes" that you see in the log files. Modify your data frame to add new columns: `cls1_lab` and `cls2_lab` to add these labels. If you find the label for a given code, that's OK, you can leave the cell empty. Indeed, currently this file is empty; I'll be filling it in later.

Output: Summary stats
One of the outputs of this script will be `stats.tsv`. It should have 3 columns: `mode`, `flavor`, and `count`. `mode` and `flavor` come from the log's filename. `count` should simply be the number of rows in the dataframe for the given log.

Output: XLSX
The dataframes you just created with `cls1`, `cls1_lab`, `cls2`, and `cls2_lab` should go into an XLSX file, each with its own sheet tab. Please name the tabs corresponding to the `MODE--FLAVOR` for the given log.

---

Do you have any questions or requests of me before you begin?
