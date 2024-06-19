from builtins import print
from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series

from loinclib.loinc_release import LoincGraph

release: LoincGraph = LoincGraph(release_path=Path('data/loinc_release/2.67'),
                                 trees_path=Path('data/loinc_release/2.67/trees/2023-09-26'), loinc_version='2.6.7')

index = ['PartNumber', 'PartName', 'PartTypeName', 'ExtCodeId', 'ExtCodeDisplayName', 'ExtCodeSystem', 'Equivalence',
         'ContentOrigin', 'ExtCodeSystemVersion', 'ExtCodeSystemCopyrightNotice']

out_frame: DataFrame = DataFrame(columns=index)
gene_parts: list = []

mapping_frame: DataFrame = release.read_AccessoryFiles_PartFile_PartRelatedCodeMapping_csv()
for tpl in mapping_frame.itertuples():
    (row_number,
     part_number,
     part_name,
     part_type_name,
     ext_code_id,
     ext_code_display,
     ext_code_system,
     equivalence,
     content_origin,
     ext_system_version,
     ext_system_copyright
     ) = tpl

    if ext_code_system in ['https://www.ncbi.nlm.nih.gov/gene', 'http://www.genenames.org']:
        if part_number not in gene_parts:
            gene_parts.append(part_number)

        series: Series = Series(data=tpl[1:], index=index)
        out_frame = pd.concat([out_frame, series.to_frame().T])
        # print(out_frame)

        # print(tpl)

parts_frame: DataFrame = release.read_AccessoryFiles_PartFile_Part_csv()

for tpl in parts_frame.itertuples():
    (row_number, part_number, part_type, part_name, part_display, status) = tpl

    if part_type == 'GENE' and part_number not in gene_parts:
        if part_number not in gene_parts:
            series: Series = Series(data=[part_number, part_name, part_type, '', '', '', '', '', '', ''], index=index)

            out_frame = pd.concat([out_frame, series.to_frame().T])

out: Path = Path('data') / 'misc-out' / 'part-to-gene.csv'
out.parent.mkdir(exist_ok=True, parents=True)
out_frame.to_csv(path_or_buf=out, index=False)
