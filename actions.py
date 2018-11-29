from classes import *

#nodes = GraphElements([])
#edges = GraphElements([])
debug = True

""" Resolves any edges of length sqrt(2)"""
def resolve_root_two(edge, nodes, edges):
    #global nodes
    #global edges
    global debug
    if debug: print("Resolving {}".format(edge))

    # Get the nodes on each end
    edge.resolved = True
    node0 = nodes.get(edge.nodes[0])
    node1 = nodes.get(edge.nodes[1])

    # Check that neither of these nodes is totally resolved
    if node0.remaining_points == 0 or node1.remaining_points == 0:
        if debug: print("Error: node remaining points at 0")
        exit()

    # add an edge to both, if possible (also a new node)
    if node0.can_add_edge() and node1.can_add_edge():
        if debug: print("Adding edges to nodes {} and {}".format(node0.label, node1.label))

        # Create elements
        new_node = Node(8, [])
        new_edge0 = Edge((True, 1, 0), node0.label, new_node.label)
        new_edge1 = Edge((True, 1, 0), node1.label, new_node.label)

        # Connect them to each other
        node0.add_edge(new_edge0.label)
        node1.add_edge(new_edge1.label)
        new_node.add_edge(new_edge0.label)
        new_node.add_edge(new_edge1.label)

        # Update properties
        new_node.internal = True
        new_node.sub_remaining(2)
        node0.sub_remaining(1)
        node1.sub_remaining(1)

        # Register in list
        edges.add(new_edge0)
        edges.add(new_edge1)
        nodes.add(new_node)

        return new_node, nodes, edges
    # If both nodes cannot take a new edge, add an edge to one and identify another edge. No new node creation.
    elif node0.can_add_edge():
        opposite_node = connect_dissimilar_nodes_add_unit(node0, node1)
        node0.sub_remaining(1)
        node1.sub_remaining(1)
        return opposite_node, nodes, edges
    
    elif node1.can_add_edge():
        opposite_node = connect_dissimilar_nodes_add_unit(node1, node0)
        node0.sub_remaining(1)
        node1.sub_remaining(1)
        return opposite_node, nodes, edges
    
    else:
        if debug: print("Looking for overlapping neighbor between nodes {} and {}".format(node0, node1))
        # Collect unresolved eges from node0
        roots, units, others = group_unresolved_edges(node0)
        radial_edges_node0 = units+others
        neighbor_nodes_node0 = [nodes.get(get_far_node(node0, e)) for e in radial_edges_node0]
        
        # Collect unresolved edges for node1
        roots, units, others = group_unresolved_edges(node1)
        radial_edges_node1 = units+others
        neighbor_nodes_node1 = [nodes.get(get_far_node(node1, e)) for e in radial_edges_node1]
        
        # Check if any unresolved edges overlap (they shouldn't!)
        allnodes = [n.label for n in neighbor_nodes_node0] + [n.label for n in neighbor_nodes_node1]
        allnodes.sort()
        for n in range(len(allnodes)-1):
            if allnodes[n] == allnodes[n+1]:
                print("Error: nodes {} and {} already connected".format(node0, node1))
                exit()
                    
        # Check if there is a single subsumable neighbor (ie, an "internal" node)
        if len(neighbor_nodes_node0)==1 and len(neighbor_nodes_node1)==1:
            if debug: print("Attempting to merge {} and {}".format(
                neighbor_nodes_node0[0], neighbor_nodes_node1[0]))
            if neighbor_nodes_node0[0].label < neighbor_nodes_node1[0].label:
                #if neighbor_nodes_node1[0].internal:
                merge_nodes(neighbor_nodes_node0[0], neighbor_nodes_node1[0])
                neighbor_nodes_node0[0].sub_remaining(4)
                opposite_node = neighbor_nodes_node0[0]
            else : #if neighbor_nodes_node0[0].internal:
                merge_nodes(neighbor_nodes_node1[0], neighbor_nodes_node0[0])
                neighbor_nodes_node1[0].sub_remaining(4)
                opposite_node = neighbor_nodes_node1[0]

        # If there is one subsumable neighbor for one node but not the other,
        # cheat on the assumption that it's the last match.
        elif len(neighbor_nodes_node0) + len(neighbor_nodes_node1) == 1:
            if debug: print("FINAL RESOLUTION: Adding edge between {} and {}".format(
                node0, node1))
            far_node = Node(8, [])
            far_node.internal = True
            nodes.add(far_node)
            if len(neighbor_nodes_node0) == 0 and len(neighbor_nodes_node1) == 1:
                unit_edge = Edge((True, 1, 0), far_node.label, node0.label)
                edges.add(unit_edge)
                far_node.add_edge(unit_edge.label)
                node0.add_edge(unit_edge.label)
                merge_nodes(neighbor_nodes_node1[0], far_node)
                neighbor_nodes_node1[0].sub_remaining(2)
                opposite_node = neighbor_nodes_node1[0]
            else:
                unit_edge = Edge((True, 1, 0), far_node.label, node1.label)
                edges.add(unit_edge)
                far_node.add_edge(unit_edge.label)
                node1.add_edge(unit_edge.label)
                merge_nodes(neighbor_nodes_node0[0], far_node)
                neighbor_nodes_node0[0].sub_remaining(2)
                opposite_node = neighbor_nodes_node0[1]


        else:
            if debug: print("Error: multiple subsumable neighboring nodes; not implemented.")
            exit()

        # The nodes that the edge connect have had 45* resolved    
        node0.sub_remaining(1)
        node1.sub_remaining(1)
        return opposite_node, nodes, edges

""" Given node object, return list of adjacent unresolved edge objects """
def get_all_unresolved_edges(node):
    unresolved = []
    for x in node.edges:
        edge = edges.get(x)
        if not edge.resolved:
            unresolved.append(edge)
    return unresolved

""" Given adjacent node and edge objects, return the other adjacent node's label """
def get_far_node(node, edge):
    for n in edge.nodes:
        if node.label != n:
            return n

""" Attempts to find/create the 3rd point of a triangle where node0 can add an edge and node1 cannot """
def connect_dissimilar_nodes_add_unit(node0, node1, nodes, edges):
    #global nodes
    #global edges
    
    if debug: print("Adding edge to node {}; using existing edge for node {}".format(
        node0.label, node1.label))
    gather_resolutions(nodes, edges)

    # identify an unresolved candidate edge
    roots, units, others = group_unresolved_edges(node1)
    adjacent_edges_node1 = units+others
                
    if len(adjacent_edges_node1) != 1:
        print("Error: {} unresolved adjacent edges to {}".format(len(adjacent_edges_node1), node1))
        exit()
        
    connecting_edge = edges.get(adjacent_edges_node1[0].label)
    far_node = nodes.get(get_far_node(node1, connecting_edge))
    far_node.sub_remaining(2)  

    # Add a unit edge if the connecting edge is already length 1
    if connecting_edge.is_one():
        if debug: print("Found edge {} with length 1".format(connecting_edge))
        new_edge = Edge((True, 1, 0), node0.label, far_node.label)
        node0.add_edge(new_edge.label)
        far_node.add_edge(new_edge.label)
        edges.add(new_edge)
        return far_node, nodes, edges

    # If exact length is not known, split/create new edges
    elif not connecting_edge.is_known() and connecting_edge.lt_one():
        if debug: print("Found edge {} with irregular short length".format(connecting_edge))
        # Create 3rd node of triangle & connect it to node via constructed parallel edges
        farther_node = Node(4, []) 
        replacement_edge = Edge((True, 1, 0), farther_node.label, node1.label)
        splint_edge = Edge((False, 0, 0), far_node.label, farther_node.label)
        # new edge for node0 (which had space)
        new_edge = Edge((True, 1, 0), farther_node.label, node0.label)

        # Register new nodes, edges
        edges.add([replacement_edge, splint_edge, new_edge])
        nodes.add(farther_node)

        # Connect everything
        farther_node.add_edge(replacement_edge.label)
        farther_node.add_edge(new_edge.label)
        farther_node.add_edge(splint_edge.label)
        farther_node.sub_remaining(2)
        node0.add_edge(new_edge.label)
        node1.add_edge(replacement_edge.label)
        far_node.add_edge(splint_edge.label)

        # Modify node / edge properties
        far_node.sub_remaining(2)
        farther_node.internal = True
        connecting_edge.resolved = True
        splint_edge.resolved = True

        return farther_node, nodes, edges
    
    else:
        print("Error: unimplemented behavior required")
        exit()

""" Split long edges into sqrt(2)-length edge and other edge """
def split_edge_root(node, edge, nodes, edges):
    #global nodes
    #global edges
    # Get neighboring node, create new side node, non-root edge
    far_node = nodes.get(get_far_node(node, edge))
    side_node = Node(4, [edge.label])
    far_edge = Edge(edge.minus_root(), side_node.label,
                    far_node.label)

    # Connect everything
    side_node.add_edge(far_edge.label)
    far_node.replace_edge(edge.label, far_edge.label)
    
    # Update properties
    side_node.internal = False
    far_edge.length = edge.minus_root() #(True, 0, 1)
    far_edge.raw = edge.raw - sqrt(2)
    far_edge.nodes = [side_node.label, far_node.label]
    edge.nodes = [node.label, side_node.label]
    edge.length = (True, 0, 1) 
    edge.raw = sqrt(2)

    # Register new node, edge
    edges.add(far_edge)
    nodes.add(side_node)
    return side_node, nodes, edges

""" Two nodes have been identified as actually the same; combine them."""
def merge_nodes(destination, source):
    global nodes
    global edges
    if debug: print("Merging {} into {}".format(source, destination))
    if not source.internal:
        print("Error: trying to merge non-internal node {} into node {}".format(source.label, destination.label))
        exit()
        
    for edge in source.edges:
        if edge not in destination.edges:
            destination.add_edge(edge)
            e = edges.get(edge)
            n = get_far_node(source, e)
            e.nodes = [n, destination.label]

    nodes.remove(source.label)



def group_unresolved_edges(node):
    global edges
    roots = []
    units = []
    others = []
    for edge in node.edges:
        e = edges.get(edge)
        if not e.resolved:
            if e.is_root_multiple():
                roots.append(e)
            elif e.is_unit():
                units.append(e)
            else:
                others.append(e)
    return roots, units, others

def resolve_pointy_node(node, nodes, edges):
    #global edges
    if debug: print("Resolving node {}".format(node))
    roots, units, others = group_unresolved_edges(node)
   
    if len(units) + len(roots) == 0:
        if debug: print("Error: cannot determine edge")
    elif (len(units) + len(roots) + len(others)) > 2:
        if debug: print("Error: which edges to use is indeterminate")
    elif len(units) == 1 and len(roots) == 1:
        if debug: print("Best of all worlds... implement later.")
    elif len(units) == 1 and len(others) == 1:
        if debug: print("Found irregular edge")
        unit_edge = units[0]
        other_edge = others[0]
        if unit_edge.is_one():
            far_unit_node = nodes.get(get_far_node(node, unit_edge))
        else:
            far_unit_node, nodes, edges = split_edge_one(node, unit_edge, nodes, edges)
            
        # we know other_edge cannot be a root multiple, but it might be known
        if other_edge.is_known():
            if debug: print("other edge is known, please implement")
        elif other_edge.gteq_root():
            side_node = split_edge_root(node, other_edge)
            connecting_edge = Edge((True, 1, 0),
                                   side_node.label, far_unit_node.label)
            side_node.add_edge(connecting_edge.label)
            side_node.sub_remaining(1)
            if far_unit_node.can_add_edge():
                far_unit_node.add_edge(connecting_edge.label)
                far_unit_node.sub_remaining(2)
                other_edge.resolved = True
                unit_edge.resolved = True
                node.resolved = True
                edges.add(connecting_edge)
                node.sub_remaining(1)
            else:
                if debug: print("Error: far_unit_node cannot add edge, resolution not implemented.")
            
            
        else:
            # far_unit_node = node on other side of unit edge
            # node = current node, it's pointy
            # unit_edge = the actual unit edge
            # other_edge = shorter than sqrt(2) other edge
            far_root_node = Node(8, [])
            far_root_node.sub_remaining(4)
            far_root_node.internal = True
            root_edge = Edge((True, 0, 1), node.label, far_root_node.label)
            far_root_node.add_edge(root_edge.label)
            node.add_edge(root_edge.label)
            edges.add(root_edge)

            near_node = nodes.get(get_far_node(node, other_edge))
            near_node.sub_remaining(4)
            splint_edge = Edge((False, 0, 0), near_node.label, far_root_node.label)
            near_node.add_edge(splint_edge.label)
            far_root_node.add_edge(splint_edge.label)
            edges.add(splint_edge)
            
            # we'd best be checkin' whether we can actually add a new edge
            if far_unit_node.gt_90():
                if debug: print("Error: Pointy adding edges not yet implemented.")
                if debug: print(far_unit_node)
            else:
                roots, candidates, units = group_unresolved_edges(far_unit_node)
                candidates.remove(unit_edge)
                if len(candidates) != 1:
                    if debug: print("Error: {} candidates in point resolution".format(len(candidates)))
                else:
                    far_node = nodes.get(get_far_node(far_unit_node, candidates[0]))
                    if far_node.label < far_root_node.label:
                        merge_nodes(far_node, far_root_node)
                        far_node.sub_remaining(5)
                    else:
                        merge_nodes(far_root_node, far_node)
                        far_root_node.sub_remaining(5)                        
                far_unit_node.sub_remaining(2)
                node.sub_remaining(1)

                
                


def split_edge_one(node, edge, nodes, edges):
    #global nodes
    #global edges
    far_node = nodes.get(get_far_node(node, edge))
    side_node = Node(4, [edge.label])
    far_edge = Edge(edge.minus_one(), side_node.label,
                    far_node.label)
    side_node.add_edge(far_edge.label)
    side_node.internal = False
    far_node.replace_edge(edge.label, far_edge.label)
    far_edge.length = edge.minus_one() #(True, 1, 0)
    far_edge.nodes = [side_node.label, far_node.label]
    
    edge.nodes = [node.label, side_node.label]
    edge.length = (True, 1, 0) #edge.minus_one()
    edges.add(far_edge)
    nodes.add(side_node)
    return side_node, nodes, edges

def resolve_overlapped_edge(edge, nodes, edges):
    #global edges
    #global nodes

    # for now, we're assuming that one of these is < 180* and the other one is
    # greater than 180*.
    if nodes.get(edge.nodes[0]).points > 4 and nodes.get(
        edge.nodes[1]).points < 4:
        concave_node = nodes.get(edge.nodes[0])
        convex_node = nodes.get(edge.nodes[1])
    elif nodes.get(edge.nodes[1]).points > 4 and nodes.get(
        edge.nodes[0]).points < 4:
        concave_node = nodes.get(edge.nodes[1])
        convex_node = nodes.get(edge.nodes[0])
    else:
        if debug: print("Error: node properties do not match assumptions.")
        if debug: print("{}, {} {}".format(
            edge, nodes.get(edge.nodes[0]), nodes.get(edge.nodes[1])))
        return nodes, edges

    interior_node = Node(8, [])
    root_edge = Edge((True, 0, 1), convex_node.label,
                     interior_node.label)
    unit_edge = Edge((True, 1, 0), concave_node.label,
                     interior_node.label)
    interior_node.add_edge(root_edge.label)
    interior_node.add_edge(unit_edge.label)
    interior_node.internal = True
    convex_node.add_edge(root_edge.label)
    concave_node.add_edge(unit_edge.label)
    concave_node.sub_remaining(4)
    edge.resolved = True
    edges.add([root_edge, unit_edge])
    nodes.add(interior_node)
    return nodes, edges
    
def identify_squares(nodes, edges):
    if debug: print("Identifying squares")

    square_quads = []
    for corner0 in nodes.all():
        if corner0.remaining_points == 2: # 90* angles only
            roots, units, others = group_unresolved_edges(corner0)
            if len(units)+len(others) == 2:
                for connecting_edge in units:
                    corner1 = nodes.get(get_far_node(corner0, connecting_edge))
                    if corner1.remaining_points == 2:
                        c1_edges = GraphElements(get_all_unresolved_edges(corner1))
                        c1_edges.remove(connecting_edge.label)
                        if c1_edges.size() == 1:
                            if c1_edges.all()[0].is_unit():
                                square_quads.append((
                                    corner0, corner1, connecting_edge, c1_edges.all()[0]))
                                
                    
    return square_quads                    
                
def gather_resolutions(nodes, edges, p=False):
    if p: print("--------------")
    for node in nodes.all():
        if p: print(node)
    for edge in edges.all():
        if nodes.get(edge.nodes[0]).resolved or \
           nodes.get(edge.nodes[1]).resolved:
            edge.resolved = True
        if p: print(edge)
        
def resolve_square(square, nodes, edges):
    #global nodes
    #global edges
    base_corner = square[0]
    right_corner = square[1]
    base_edge = square[2]
    tall_edge = square[3]
    tall_corner = nodes.get(get_far_node(right_corner, tall_edge))
    if debug: print("Resolving square {} {} {}".format(base_corner, right_corner, tall_corner))
    if not base_corner.resolved and not right_corner.resolved and not tall_corner.resolved:
        # Create & register square diagonal
        hypotenuse = Edge((True, 0, 1), tall_corner.label, base_corner.label)
        edges.add(hypotenuse)
        # Connect everything
        base_corner.add_edge(hypotenuse.label)
        tall_corner.add_edge(hypotenuse.label)
        # Modify properties
        right_corner.sub_remaining(2)
        base_corner.sub_remaining(1)
        tall_corner.sub_remaining(1)
        gather_resolutions(nodes, edges)
        final_corner = resolve_root_two(hypotenuse)
        gather_resolutions(nodes, edges)

        # Create cross bar diagonal
        cross_bar = Edge((True, 0, 1), right_corner.label, final_corner.label)
        edges.add(cross_bar)
        # Connect everything
        right_corner.add_edge(cross_bar.label)
        final_corner.add_edge(cross_bar.label)
        # Modify properties
        cross_bar.resolved = True
        
    else:
        if debug: print("Square already resolved.")
    return nodes, edges
