import image_processing
import graph_resolution

filename = "tangram1.png"
unit_length = image_processing.get_unit_length(filename)
corners = image_processing.detect_corners(filename, unit_length)
print("Found {} corners in image".format(corners.size()))
print("Unit length is {}".format(unit_length))
nodes, edges = image_processing.detect_edges(corners, unit_length)
nodes, edges = graph_resolution.split_long_edges(nodes, edges)
for node in nodes.all():
    print(node)
for edge in edges.all():
    print(edge)
nodes, edges = graph_resolution.resolve_overlapping_edges(nodes, edges)
for node in nodes.all():
    print(node)
for edge in edges.all():
    print(edge)
