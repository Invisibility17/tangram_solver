## beginnings of the tangram solver code

from math import sqrt
from classes import Node, Edge, GraphElements
import actions, search_actions, shape_classes, tangram_class
import csp2

"""actions.nodes.add([Node(1, [1, 14]),  Node(3, [1, 2]),    Node(2, [2, 3]),
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
"""
def add_crossbars(nodes, edges):
    for edge in edges.all():
        if len(edge.across) == 2:
            edge.crossbar = True
            nodes, edges = actions.add_crossbar(*edge.across, nodes, edges)
        elif len(edge.across) > 2:
            print("Error: why so many crossbars? {}".format(edge))
    return nodes, edges

def split_long_edges(nodes, edges):
    # split long edges up
    action_last_round = True
    while action_last_round:
        action_last_round = False
        for edge in edges.all():
            if edge.contains_one() and not edge.is_one():
                side_node, nodes, edges = actions.split_edge_one(nodes.get(edge.nodes[0]), edge, nodes, edges)
                action_last_round = True
            if edge.contains_root() and not edge.is_root():
                side_node, nodes, edges = actions.split_edge_root(nodes.get(edge.nodes[0]), edge, nodes, edges)
                action_last_round = True
    return nodes, edges

def resolve_overlapping_edges(nodes, edges):
    # resolve overlapping edges 
    for edge in edges.all():
        if edge.is_overlapped():
            nodes, edges = actions.resolve_overlapped_edge(edge, nodes, edges)
    return nodes, edges
        

def resolve_root_edges(nodes, edges):
    # compile and resolve root edges        
    edges_to_resolve = []
    for edge in edges.all():
        if edge.is_root():
            edges_to_resolve.append(edge.label)
   
    for edge in edges_to_resolve:
        node, nodes, edges = actions.resolve_root_two(edges.get(edge), nodes, edges)
    return nodes, edges
def resolve_right_angles(nodes, edges):
    resolved_something = 1
    resolve_count = 0
    while resolved_something > 0:
        resolved_something = 0
        for node in nodes.all():
            if node.remaining_points == 2:
                resolved, nodes, edges = actions.resolve_right_angle(node, nodes, edges)
                resolved_something += resolved
                resolve_count += resolved
    return resolve_count, nodes, edges
    
            
# update resolutions / do not print

def fold_root_edges(nodes, edges):
    folded_something = 1
    fold_count = 0
    while folded_something > 0:
        folded_something = 0
        for edge in edges.all():
            if edge.is_root() and not edge.resolved:
                folded, nodes, edges = actions.fold_root_edge(edge, nodes, edges)
                folded_something += folded
                fold_count += folded
    return fold_count, nodes, edges
                
# compile and resolve pointy nodes
def resolve_pointy_nodes(nodes, edges):
    resolved_something = 1
    resolve_count = 0
    while resolved_something > 0:
        resolved_something = 0
        for node in nodes.all():
            if node.remaining_points == 1:
                resolved, nodes, edges = actions.resolve_pointy_node(node, nodes, edges)
                resolved_something += resolved
                resolve_count += resolved

    return resolve_count, nodes, edges

def resolve_squares(nodes, edges):
    # identify squares
    squares = actions.identify_squares(nodes, edges)
    for sq in squares:
        nodes, edges = actions.resolve_square(sq, nodes, edges)
    return nodes, edges
