from networkx import MultiDiGraph

g = MultiDiGraph()

g.add_node('from')
g.add_node('to')

print(g)
print(g.nodes)
print(g.nodes())

g.add_edge('from', 'to', first='true')
g.add_edge('from', 'to', second='true')
g.add_edge('from_another', 'to', first_another='true')


print(g.out_edges)
print(g.out_edges())
print(g.out_edges(keys=True, data=True))
print(g.out_edges( keys=True, data=True))
print(g.out_edges( nbunch='from', keys=True, data=True))

print('-------------')

