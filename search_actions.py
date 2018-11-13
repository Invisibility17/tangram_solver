import actions

def find_med_right(node):
    if node.points < 2:
        return False
    roots, units, others = group_edges(node)
    
def find_large_anchor(node):
    if node.points < 4:
        return False
    roots, units, others = group_edges(node)
    if (len(roots) < 2) or len(units) < 2:
        return False
    root_neighbors = get_neighbors(node, roots)
    unit_neighbors = get_neighbors(node, units)
    other_neighbors = get_neighbors(node, others)
    matches = match_between(root_neighbors, unit_neighbors)
    if len(matches) < 2:
        return False
    solns = []
    for i in range(len(matches)):
        for j in range(i+1, len(matches), 1):
            right_node =  connected_by_units(matches[i][0], matches[j][0], node)
            if right_node:
                for n in matches[i][1]:
                    if n not in matches[j][1]:
                        solns.append((node, matches[i][0], matches[j][0], right_node))

    if len(solns) > 0:
        return solns
    return False
    

def connected_by_units(node1, node2, excluded_node):
    roots1, units1, others1 = group_edges(node1)
    unit_neighbors1 = get_neighbors(node1, units1)
    roots2, units2, others2 = group_edges(node2)
    unit_neighbors2 = get_neighbors(node2, units2)
    for unit in unit_neighbors1:
        if (unit in unit_neighbors2) and unit != excluded_node:
            return unit
    return False


def group_edges(node):
    roots = []
    units = []
    others = []
    for edge in node.edges:
        e = actions.edges.get(edge)
        if e.is_root_multiple():
            roots.append(e)
        elif e.is_unit():
            units.append(e)
        else:
            others.append(e)
    return roots, units, others

def get_neighbors(node, edge_list):
    neighbors = []
    for edge in edge_list:
        neighbors.append(actions.nodes.get(edge.get_other_node(node.label)))
    return neighbors

def match_between(root_neighbors, unit_neighbors):
    neighbors_neighbor_dict = {}
    matches = []
    for root_neighbor in root_neighbors:
        roots, units, others = group_edges(root_neighbor)
        unit_neighbors_neighbors = get_neighbors(root_neighbor, units)
        for unit in unit_neighbors_neighbors:
            if unit.label not in neighbors_neighbor_dict:
                neighbors_neighbor_dict[unit.label] = [root_neighbor.label]
            else:
                neighbors_neighbor_dict[unit.label].append(root_neighbor.label)
    for unit_neighbor in unit_neighbors:
        if unit_neighbor.label in neighbors_neighbor_dict:
            matches.append((unit_neighbor, neighbors_neighbor_dict[unit_neighbor.label]))
    return matches
