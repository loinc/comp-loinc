import typing

import networkx as nx

g = nx.MultiDiGraph()


def add(node: str, name: str, value: typing.Any):
    if node not in g.nodes:
        g.add_node(node)

    node = g.nodes[node]
    node[name] = value


add('node1', 'name', 'some name')

print(g.nodes(data=False, default={'1': 'one'})['node1']['1'])


