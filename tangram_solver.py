import image_processing
import graph_resolution
import actions
import search_actions
import csp2
import shape_classes
import image_util

def print_all(nodes, edges):
    for node in nodes.all():
        print(node)
    for edge in edges.all():
        print(edge)
 
filename = "tangram14.png"
unit_length = image_processing.get_unit_length(filename)
corners, lines = image_processing.detect_corners(filename, unit_length)
print("{} corners {} lines".format(corners.size(), lines.size()))
print_all(corners, lines)
corners, lines = image_processing.split_lines(corners, lines, filename, unit_length)
print("{} corners {} lines".format(corners.size(), lines.size()))
print_all(corners, lines)
for x in range(10):
    corners, lines = image_util.match_corners(corners, lines, filename, unit_length)
    print("{} corners {} lines".format(corners.size(), lines.size()))
    corners, lines = image_processing.split_lines(corners, lines, filename, unit_length)
    print("{} corners {} lines".format(corners.size(), lines.size()))
    print(len(list(set(lines.all()))))
"""
corners, lines = image_util.match_corners(corners, lines, filename, unit_length)
print("{} corners {} lines".format(corners.size(), lines.size()))
corners, lines = image_processing.split_lines(corners, lines, filename, unit_length)
print("{} corners {} lines".format(corners.size(), lines.size()))
corners, lines = image_util.match_corners(corners, lines, filename, unit_length)
print("{} corners {} lines".format(corners.size(), lines.size()))
corners, lines = image_processing.split_lines(corners, lines, filename, unit_length)
print("{} corners {} lines".format(corners.size(), lines.size()))"""
image_processing.visualize(filename, "corners_and_edges.jpg", corners, lines)
#print_all(corners, lines)
nodes, edges = image_processing.create_nodes_edges(corners, lines, unit_length)
print_all(nodes, edges)
print("Found {} corners in image".format(corners.size()))
print("Unit length is {}".format(unit_length))
#nodes, edges = image_processing.detect_edges(corners, unit_length)
#nodes, edges = graph_resolution.resolve_overlapping_edges(nodes, edges)
#nodes, edges = graph_resolution.split_long_edges(nodes, edges)
#nodes, edges = graph_resolution.resolve_root_edges(nodes, edges)
#actions.gather_resolutions(nodes, edges)

resolved_or_folded_this_round = (0, 0, 1)
while sum(resolved_or_folded_this_round) > 0:
    did_resolve, nodes, edges = graph_resolution.resolve_pointy_nodes(nodes, edges)
    if did_resolve: print_all(nodes, edges)

    did_fold, nodes, edges = graph_resolution.fold_root_edges(nodes, edges)
    if did_fold: print_all(nodes, edges)
    
    did_resolve_right, nodes, edges = graph_resolution.resolve_right_angles(nodes, edges)
    if did_resolve_right: print_all(nodes, edges)
    
    resolved_or_folded_this_round = (did_resolve, did_fold, did_resolve_right)

#nodes, edges = graph_resolution.add_crossbars(nodes, edges)


image_processing.visualize(filename, "resolved.jpg", nodes, edges)
large_triangles = []
medium_triangles = []
small_triangles = []
parallelograms = []
squares = []
for node in nodes.all():
    large_triangles += search_actions.find_large_triangle(node, nodes, edges)
    medium_triangles += search_actions.find_medium_triangle(node, nodes, edges)
    small_triangles += search_actions.find_small_triangle(node, nodes, edges)
    parallelograms += search_actions.find_parallelogram(node, nodes, edges)
    squares += search_actions.find_square(node, nodes, edges)
    
large_triangles = list(set(large_triangles))
medium_triangles = list(set(medium_triangles))
small_triangles = list(set(small_triangles))
parallelograms = list(set(parallelograms))
squares = list(set(squares))

print(len(large_triangles))
print(len(medium_triangles))
print(len(parallelograms))
for p in parallelograms:
    print(p)
print(len(squares))
print(len(small_triangles))

variables = ['LT1', 'LT2', 'MT', 'SQ', 'PA', 'ST1', 'ST2']
domains = {'LT1':large_triangles, 'LT2':large_triangles, 'MT':medium_triangles,
           'SQ':squares, 'PA':parallelograms, 'ST1':small_triangles, 'ST2':small_triangles}

neighbors = {}
for i in range(len(variables)):
    neighbors[variables[i]] = variables[:i] + variables[i+1:]

prob = csp2.CSP(variables, domains, neighbors, shape_classes.constrain)
result = csp2.backtracking_search(prob)

polygons = []
for var in result:
    poly = []
    shape = result[var]
    for node in shape.nodes:
        poly.append(nodes.get(node).coords)
    polygons.append(tuple(poly))
image_processing.fill_in_solution(filename, "solved.jpg", polygons)

