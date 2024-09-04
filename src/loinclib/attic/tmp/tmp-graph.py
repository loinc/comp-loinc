import networkx as nx

import loinclib.loinc_schema

G: nx.Graph = nx.Graph()

sources = G.graph.setdefault('sources', {})

if 's1'in sources:
    print("source 1 loaded")
else:
    print("source 1 not loaded")

sources['s1'] = True



if G.graph.setdefault('sources', {}).get('s1', False):
    print("source 1 loaded")
else:
    print("source 1 not loaded")

################################

g = nx.MultiDiGraph()

# node= g.add_node('hello', one=1, two=2)
node= g.add_node('hello')
node_back = g.nodes['hello']

print(node_back)
someting = g.nodes.get('somging', None)

print(loinclib.loinc_schema_v2.LoincNodeType.LoincTerm)

get = g.nodes.get('notthere')


print('done')
