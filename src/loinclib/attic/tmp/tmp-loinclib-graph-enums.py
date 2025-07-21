import re

import loinclib

print(loinclib.NodeHandler.type_for_identifier("4-4"))

node_id = "LP{LP78-8}"
pattern = f"^LP{{(.+)}}$"

match = re.match(pattern, node_id)

if match:
    print(f"Pattern {pattern} matched: {match.group(1)}")

node_type = loinclib.NodeHandler

print(node_type)
