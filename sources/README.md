This folder contains, by release version, original LOINC released or provided content. The following uses version `2.67`
as an example and all paths are from the root of the Git repository.

The tooling depends on the following content:

* The LOINC release from: https://loinc.org/downloads/
* The tree exports from: https://loinc.org/tree/

Perform the following steps to set up this directory for the tooling.

* Download the LOINC release zip file and unpack it into the `data/loinc_release/2.67` folder. After doing
  this, there should be a path
  like `data/loinc_release/2.67/loinc.xml`.
* Download all the exports from https://loinc.org/tree/ and use them to form the following file structure. It is not
  clear if the downloaded files' content could change from one download to the next even if it indicates the same LOINC
  version. To address this possibility, a dated folder name (the date the files were downloaded) is used in the
  following paths, and the folder name (as a string) is used as a parameter to the tooling.

    * Create a folder like `data/loinc_release/2.67/trees/2023-9-26` that will hold the unpacked tree files
      from that date.
    * For each exported tree, unpack the zip somewhere and copy the `LOINC_2.76_Export_*.csv` to
      the `data/loinc_release/2.67/trees/2023-9-26` and rename it according to its tree type. For example, you should
      have a file at
      this path `data/loinc_release/2.67/trees/2023-9-26/component.csv`.
    * The files needed in this folder
      are `class.csv`, `component.csv`, `compoent_by_system.csv`, `document_ontology.csv`, `method.csv`, `panels.csv`,
      and `system.csv`.
