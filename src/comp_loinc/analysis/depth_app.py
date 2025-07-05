from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from . import depth

# Convenience mappings for UI -> data keys
FILTER_OPTIONS = {
    "terms": ("terms",),
    "terms, groups": ("terms", "groups"),
    "terms, groups, parts": ("terms", "groups", "parts"),
}
STAT_OPTIONS = {"Numbers": "totals", "Percentages": "percentages"}
VIEW_OPTIONS = {"Full ontology": False, "By subhierarchy": True}

DATA_DIR = Path(depth.DEFAULTS["outdir-plots"])


def _expected_tsvs() -> Iterable[Path]:
    for filt in FILTER_OPTIONS.values():
        filt_str = "-".join(filt)
        for stat in STAT_OPTIONS.values():
            for by_sub in VIEW_OPTIONS.values():
                suffix = "_by-hierarchy" if by_sub else ""
                yield DATA_DIR / f"plot-class-depth{suffix}_{filt_str}_{stat}.tsv"


def ensure_data() -> None:
    missing = [p for p in _expected_tsvs() if not p.exists()]
    if missing:
        print("Missing depth analysis TSVs. Running analyze_class_depth()...")
        depth.analyze_class_depth()
        missing = [p for p in _expected_tsvs() if not p.exists()]
        if missing:
            raise FileNotFoundError("Missing expected TSVs: " + ", ".join(str(p) for p in missing))


def load_data() -> Dict[Tuple[bool, Tuple[str, ...], str], pd.DataFrame]:
    data: Dict[Tuple[bool, Tuple[str, ...], str], pd.DataFrame] = {}
    for filt in FILTER_OPTIONS.values():
        filt_str = "-".join(filt)
        for stat in STAT_OPTIONS.values():
            for by_sub in VIEW_OPTIONS.values():
                suffix = "_by-hierarchy" if by_sub else ""
                path = DATA_DIR / f"plot-class-depth{suffix}_{filt_str}_{stat}.tsv"
                df = pd.read_csv(path, sep="\t", index_col=0)
                data[(by_sub, filt, stat)] = df
    return data


def create_app(data: Dict[Tuple[bool, Tuple[str, ...], str], pd.DataFrame]) -> Dash:
    app = Dash(__name__)
    app.layout = html.Div([
        html.H3("CompLOINC Classification Depth"),
        html.Div([
            html.Label("Filter:"),
            dcc.RadioItems(list(FILTER_OPTIONS.keys()), list(FILTER_OPTIONS.keys())[0], id="filter-radio")
        ]),
        html.Div([
            html.Label("View:"),
            dcc.RadioItems(list(VIEW_OPTIONS.keys()), list(VIEW_OPTIONS.keys())[0], id="view-radio")
        ]),
        html.Div([
            html.Label("Display:"),
            dcc.RadioItems(list(STAT_OPTIONS.keys()), list(STAT_OPTIONS.keys())[0], id="stat-radio")
        ]),
        html.Div([
            html.Label("Terminologies:"),
            dcc.Checklist(id="ont-checklist")
        ]),
        dcc.Graph(id="depth-graph")
    ])

    @app.callback(
        Output("ont-checklist", "options"),
        Output("ont-checklist", "value"),
        Input("filter-radio", "value"),
        Input("view-radio", "value"),
    )
    def update_checklist(filter_val, view_val):
        filt = FILTER_OPTIONS[filter_val]
        by_sub = VIEW_OPTIONS[view_val]
        df = data[(by_sub, filt, "totals")]
        options = [{"label": c, "value": c} for c in df.columns]
        values = [c for c in df.columns]
        return options, values

    @app.callback(
        Output("depth-graph", "figure"),
        Input("filter-radio", "value"),
        Input("view-radio", "value"),
        Input("stat-radio", "value"),
        Input("ont-checklist", "value"),
    )
    def update_graph(filter_val, view_val, stat_val, ont_values):
        filt = FILTER_OPTIONS[filter_val]
        by_sub = VIEW_OPTIONS[view_val]
        stat = STAT_OPTIONS[stat_val]
        df = data[(by_sub, filt, stat)]
        if ont_values:
            df = df[ont_values]
        fig = px.bar(df, x=df.index, y=df.columns, barmode="group")
        fig.update_layout(
            xaxis_title="Depth",
            yaxis_title="Number of classes" if stat == "totals" else "% of classes",
        )
        return fig

    return app


def main() -> None:
    ensure_data()
    data = load_data()
    app = create_app(data)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
