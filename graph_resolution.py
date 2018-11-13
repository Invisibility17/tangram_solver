## beginnings of the tangram solver code

from math import sqrt
from classes import Node, Edge, GraphElements
import actions, search_actions

actions.nodes.add([Node(1, [1, 14]),  Node(3, [1, 2]),    Node(2, [2, 3]),
         Node(6, [3, 4]),   Node(2, [4, 5]),    Node(6, [5, 6]),
         Node(5, [6, 7]),   Node(2, [7, 8]),    Node(1, [8, 9]),
         Node(5, [9, 10]), Node(3, [10, 11]), Node(5, [11, 12]),
         Node(1, [12, 13]),Node(6, [13, 14])])

actions.edges.add([Edge((True, 2, 0), 1, 2),  Edge((True, 0, 1), 2, 3),
         Edge((False, 0, 0), 3, 4, 12/29), Edge((True, 1, 0), 4, 5),
         Edge((True, 1, 0), 5, 6),  Edge((False, 0, 0), 6, 7),
         Edge((True, 0, 1), 7, 8),  Edge((True, 0, 1), 8, 9),
         Edge((True, 1, 0), 9, 10), Edge((True, 0, 1), 10, 11),
         Edge((True, 1, 0), 11, 12), Edge((True, 0, 1), 12, 13),
         Edge((True, 2, 0), 13, 14), Edge((False, 2, 0), 14, 1, 65/29)])


# split long edges up
action_last_round = True
while action_last_round:
    action_last_round = False
    for edge in actions.edges.all():
        if edge.contains_one() and not edge.is_one():
            actions.split_edge_one(actions.nodes.get(edge.nodes[0]), edge)
            action_last_round = True
        if edge.contains_root() and not edge.is_root():
            actions.split_edge_root(actions.nodes.get(edge.nodes[0]), edge)
            action_last_round = True

# resolve overlapping edges 
for edge in actions.edges.all():
    if edge.is_overlapped():
        actions.resolve_overlapped_edge(edge)
        
actions.gather_resolutions()

# compile and resolve root edges        
edges_to_resolve = []
for edge in actions.edges.all():
    if edge.is_root():
        edges_to_resolve.append(edge.label)
   
for edge in edges_to_resolve:
    actions.resolve_root_two(actions.edges.get(edge))

# update resolutions / do not print
actions.gather_resolutions()

# compile and resolve pointy nodes
nodes_to_resolve = []
for node in actions.nodes.all():
    if node.remaining_points == 1:
        nodes_to_resolve.append(node)
for node in nodes_to_resolve:
    actions.resolve_pointy_node(node)
    
# update resolutions 
actions.gather_resolutions()

# identify squares
squares = actions.identify_squares()
while squares:
    for sq in squares:
        actions.resolve_square(sq)

    actions.gather_resolutions()

    # compile and resolve pointy nodes
    nodes_to_resolve = []
    for node in actions.nodes.all():
        if node.remaining_points == 1:
            actions.resolve_pointy_node(node)

    actions.gather_resolutions()
    squares = actions.identify_squares()

actions.gather_resolutions(True)

large_triangles = []
for node in actions.nodes.all():
    triangle = search_actions.find_large_anchor(node)
    if triangle:
        large_triangles.append(triangle)


