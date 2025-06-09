import re
import pandas as pd
from pathlib import Path

EQ_PATTERN = re.compile(r"ERROR Equivalence: <([^>]+)> == <([^>]+)>")

ROOT = Path(__file__).resolve().parent

# Load labels
labels_path = ROOT / "labels.tsv"
if labels_path.exists():
    labels_df = pd.read_csv(labels_path, sep="\t")
else:
    labels_df = pd.DataFrame(columns=["cls", "label"])
labels_map = dict(zip(labels_df["cls"], labels_df["label"]))

# Gather log files
log_files = sorted(p for p in ROOT.glob("*--*.txt") if p.is_file())

stats_rows = []
frames = {}
for log_path in log_files:
    # Use the filename to get mode and flavor; split on the first '--'
    parts = log_path.stem.split("--", 1)
    if len(parts) != 2:
        continue
    mode, flavor = parts

    rows = []
    with log_path.open() as f:
        for line in f:
            m = EQ_PATTERN.search(line)
            if m:
                url1, url2 = m.groups()
                cls1 = url1.rsplit("/", 1)[-1]
                cls2 = url2.rsplit("/", 1)[-1]
                rows.append({
                    "cls1": cls1,
                    "cls2": cls2,
                    "cls1_lab": labels_map.get(cls1, ""),
                    "cls2_lab": labels_map.get(cls2, "")
                })
    df = pd.DataFrame(rows, columns=["cls1", "cls1_lab", "cls2", "cls2_lab"])
    frames[f"{mode}--{flavor}"] = df
    stats_rows.append({"mode": mode, "flavor": flavor, "count": len(df)})

# Write stats.tsv
stats_df = pd.DataFrame(stats_rows)
stats_df.to_csv(ROOT / "stats.tsv", sep="\t", index=False)

# Write Excel workbook
with pd.ExcelWriter(ROOT / "equivalence_analysis.xlsx", engine="openpyxl") as writer:
    for sheet_name, frame in frames.items():
        frame.to_excel(writer, sheet_name=sheet_name, index=False)
