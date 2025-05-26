"""Utilities"""
import os
from pathlib import Path
from typing import Dict, Set, Tuple, Union

import pandas as pd

THIS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = THIS_DIR.parent.parent.parent
ONTOLOGIES = ('LOINC', 'LOINC-SNOMED', 'CompLOINC')


def _subclass_axioms_and_totals(indir: Union[Path, str]) -> Tuple[pd.DataFrame, Dict[str, Set[Tuple[str, str]]]]:
    """Read & return transformed inputs"""
    ont_paths = {k: PROJECT_ROOT / indir / f'subclass-rels-{k.lower()}.tsv' for k in ONTOLOGIES}
    ont_sets: Dict[str, Set[Tuple[str, str]]] = {}
    ont_dfs = {}

    # Totals
    tots_rows = []
    for ont, path in ont_paths.items():
        df = pd.read_csv(path, sep='\t')
        ont_dfs[ont] = df
        tots_rows.append({'': ont, 'n': f'{len(df):,}'})
        ont_sets[ont] = set(zip(df["?child"], df["?parent"]))
    tots_df = pd.DataFrame(tots_rows)
    return tots_df, ont_sets
