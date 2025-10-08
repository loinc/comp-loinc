import csv
import json
import pathlib
from csv import DictWriter

file_path_string = "tmp/loinc-snomed-conceptmap"
file = pathlib.Path(f"{file_path_string}.json")
with open(file, encoding="utf-8") as f:
  cm = json.load(f)

groups = cm["entry"][0]["resource"]["group"]

mappings = {}

def do_groups(groups):
  for group in groups:
    elements = group["element"]
    for element in elements:
      map = mappings.setdefault(element["code"], {})
      map["code"] = element["code"]
      map["display"] = element["display"]
      map["tcode"] = element["target"][0]["code"]
      map["tdisplay"] = element["target"][0]["display"]

  with open(f"{file_path_string}.csv", "w", encoding="utf-8") as f:
    writer:DictWriter = csv.DictWriter(f, fieldnames=["code", "display", "tcode", "tdisplay"])
    writer.writeheader()
    for mapping in mappings.values():
      writer.writerow(mapping)


do_groups(groups)

print(mappings)



