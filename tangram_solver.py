import image_processing
import graph_resolution
import actions

filename = "tangram4.png"
unit_length = image_processing.get_unit_length(filename)
corners, lines = image_processing.detect_corners(filename, unit_length)
nodes, edges = image_processing.create_nodes_edges(corners, lines, unit_length)
for node in nodes.all():
    print(node)
for edge in edges.all():
    print(edge)
print("Found {} corners in image".format(corners.size()))
print("Unit length is {}".format(unit_length))
#nodes, edges = image_processing.detect_edges(corners, unit_length)
#nodes, edges = graph_resolution.resolve_overlapping_edges(nodes, edges)
nodes, edges = graph_resolution.split_long_edges(nodes, edges)
"""nodes, edges = graph_resolution.resolve_root_edges(nodes, edges)
actions.gather_resolutions(nodes, edges)"""

nodes, edges = graph_resolution.resolve_pointy_nodes(nodes, edges)
for node in nodes.all():
    print(node)
for edge in edges.all():
    print(edge)

