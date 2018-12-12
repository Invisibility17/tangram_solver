import actions
from shape_classes import *

def find_small_triangle(node, nodes, edges):
    if node.points < 2:
        return []
    roots, units, others = group_edges(node, edges)
    if len(units) < 2:
        return []
    unit_neighbors = get_neighbors(node, units, nodes)
    matches, all_neighboring = get_pairs_with_root_edges_between(unit_neighbors, nodes, edges)
    triangles = []
    for pair in matches:
        triangles.append(Small_Triangle(node, *pair))
    return triangles
                         
def find_square(node, nodes, edges):
    if node.points < 2:
        return []
    roots, units, others = group_edges(node, edges)
    if len(units) < 2:
        return []
    if len(roots) < 1:
        return []
    root_neighbors = get_neighbors(node, roots, nodes)
    unit_neighbors = get_neighbors(node, units, nodes)
    matches = match_between(root_neighbors, unit_neighbors, nodes, edges)
    if len(matches) < 2:
        return []
    squares = []
    for i in range(len(matches)):
        for j in range(i+1, len(matches), 1):
            for cross in matches[i][1]:
                if cross in matches[j][1]:
                    squares.append(Square(node, matches[i][0],
                                          matches[j][0], nodes.get(cross)))
            
    return squares    
def find_medium_triangle(node, nodes, edges):
    if node.points < 2:
        return []
    roots, units, others = group_edges(node, edges)
    if len(units) < 3:
        return []
    unit_neighbors = get_neighbors(node, units, nodes)
    matches, all_neighboring = get_pairs_with_root_edges_between(unit_neighbors, nodes, edges)
    tris = []
    for right_node in all_neighboring:
        paired = []
        for pair in matches:
            if right_node in pair:
                paired.append(pair)
        if len(paired) == 2:
            tris.append(paired)
    triangles = []
    for tri in tris:
        pair0 = list(tri[0])
        pair1 = list(tri[1])
        right_node = list(set(tri[0]) & set(tri[1]))[0]
        pair0.remove(right_node)
        pair1.remove(right_node)
        triangles.append(Medium_Triangle( node, right_node, pair0[0], pair1[0]))

    return triangles

def find_parallelogram(node, nodes, edges):
    if node.points < 3:
        return []
    roots, units, others = group_edges(node, edges)
    if len(units) < 2:
        return []
    if len(roots) < 1:
        return []
    root_neighbors = get_neighbors(node, roots, nodes)
    unit_neighbors = get_neighbors(node, units, nodes)
    matches, found_neighbors = get_pairs_with_root_edges_between(unit_neighbors, nodes, edges)
    parallels = []
    for match in matches:
        fourth_nodes = get_unmutual_neighbors(root_neighbors, match[0], match[1], nodes, edges)
        for corner in fourth_nodes:
            parallels.append(Parallelogram(node, corner, *fourth_nodes[corner]))
    return parallels

def get_unmutual_neighbors(unit_nodes, spoke0, spoke1, nodes, edges):
    r0, u0, o0 = group_edges(spoke0, edges)
    r1, u1, o1 = group_edges(spoke1, edges)
    unit_neighbors0 = get_neighbors(spoke0, u0, nodes)
    unit_neighbors1 = get_neighbors(spoke1, u1, nodes)
    acceptable_nodes = {}
    for node in unit_nodes:
        if (node in unit_neighbors0) and (node not in unit_neighbors1):
            acceptable_nodes[node] = (spoke0, spoke1)
        elif node in unit_neighbors1 and node not in unit_neighbors0:
            acceptable_nodes[node] = (spoke1, spoke0)
    return acceptable_nodes                
                
        
def get_pairs_with_root_edges_between(potential_bordering_nodes, nodes, edges):
    matches = set()
    found_neighbors = set()
    for node in potential_bordering_nodes:
        roots, units, others = group_edges(node, edges)
        root_neighbors = get_neighbors(node, roots, nodes)
        for root_neighbor in root_neighbors:
            if root_neighbor in potential_bordering_nodes:
                temp = [root_neighbor, node]
                temp.sort()
                matches.add(tuple(temp))
                found_neighbors.add(node)
                found_neighbors.add(root_neighbor)
    return matches, found_neighbors
                
    
def find_large_triangle(node, nodes, edges):
    if node.points < 4:
        return []
    roots, units, others = group_edges(node, edges)
    if (len(roots) < 3) or len(units) < 2:
        return []
    root_neighbors = get_neighbors(node, roots, nodes)
    unit_neighbors = get_neighbors(node, units, nodes)
    matches = match_between(root_neighbors, unit_neighbors, nodes, edges)
    if len(matches) < 2:
        return []
    solns = []
    for i in range(len(matches)):
        for j in range(i+1, len(matches), 1):
            right_node =  connected_by_units(matches[i][0], matches[j][0], node, nodes, edges)
            if right_node:
                for n in matches[i][1]:
                    if n not in matches[j][1]:
                        for m in matches[j][1]:
                            if m not in matches[i][1]:
                                solns.append(Large_Triangle(node, nodes.get(n),
                                            matches[i][0], right_node,
                                            nodes.get(m), matches[j][0]))
    return solns
    

def connected_by_units(node1, node2, excluded_node, nodes, edges):
    roots1, units1, others1 = group_edges(node1, edges)
    unit_neighbors1 = get_neighbors(node1, units1, nodes)
    roots2, units2, others2 = group_edges(node2, edges)
    unit_neighbors2 = get_neighbors(node2, units2, nodes)
    
    for unit in unit_neighbors1:
        #roots, units, others = group_edges(unit, edges)
        #root_neighbors = get_neighbors(unit, roots, nodes)
        #if (excluded_node.label not in root_neighbors) and
        if (unit in unit_neighbors2) and unit != excluded_node:
            return unit
    return False


def group_edges(node, edges):
    roots = []
    units = []
    others = []
    for edge in node.edges:
        e = edges.get(edge)
        if e.is_root_multiple():
            roots.append(e)
        elif e.is_unit():
            units.append(e)
        else:
            others.append(e)
    return roots, units, others

def get_neighbors(node, edge_list, nodes):
    neighbors = []
    for edge in edge_list:
        neighbors.append(nodes.get(edge.get_other_node(node.label)))
    return neighbors

def match_between(root_neighbors, unit_neighbors, nodes, edges):
    neighbors_neighbor_dict = {}
    matches = []
    for root_neighbor in root_neighbors:
        roots, units, others = group_edges(root_neighbor, edges)
        unit_neighbors_neighbors = get_neighbors(root_neighbor, units, nodes)
        for unit in unit_neighbors_neighbors:
            if unit.label not in neighbors_neighbor_dict:
                neighbors_neighbor_dict[unit.label] = [root_neighbor.label]
            else:
                neighbors_neighbor_dict[unit.label].append(root_neighbor.label)
    for unit_neighbor in unit_neighbors:
        if unit_neighbor.label in neighbors_neighbor_dict:
            matches.append((unit_neighbor, neighbors_neighbor_dict[unit_neighbor.label]))
    return matches


