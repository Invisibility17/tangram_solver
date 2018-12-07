'''
 * Python script to demonstrate Sobel edge detection.
 * combo of
 * https://mmeysenburg.github.io/image-processing/08-edge-detection/ (sobel) 
 * https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html (hough lines)
 * and
 * https://www.youtube.com/watch?v=6e6NbNegChU (corners)
'''
import cv2
import numpy as np
from random import randint
import image_util
from math import sqrt
from classes import GraphElements, Node, Edge

def split_lines(corners, lines, filename, unit_length):
    bw_img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    processed_count = 1
    while processed_count > 0:
        #print(lines.size())
        processed_count = 0
        for line in lines.all():
            #print(line)
            if not image_util.close_enough(image_util.distance_between(*line.coords), unit_length) \
               and not image_util.close_enough(image_util.distance_between(*line.coords), sqrt(2)*unit_length):
                processed, corners, lines = image_util.split_line(line, corners, lines, unit_length, bw_img)
                processed_count += processed
            
        #processed = 0
    return corners, lines    
            
def get_unit_length(filename):
    black_area = image_util.black_area(filename)
    return sqrt(black_area/8)

def detect_edges(corners, unit_length):
    print("Detecting edges")
    nodes = GraphElements([])
    edges = GraphElements([])
    corner = corners.all()[0]
    first_corner = corner
    new_node = Node(corner.points)
    first_node = new_node
    nodes.add(new_node)
    complete = False
    while complete==False:
        # get a neighbor of the corner; create & register a node for it
        #next_corner = tuple(corner.neighbors)[0]
        #if len(tuple(corner.neighbors)) > 0:
        next_corner = corners.get(tuple(corner.neighbors)[0])

        if len(tuple(next_corner.neighbors)) > 1:
            next_node = Node(next_corner.points)
            nodes.add(next_node)

            # find distance between the nodes
            dist = image_util.distance_between(corner.label, next_corner.label)
            dist = dist/unit_length

            # create & register an edge; use it to connect the nodes
            new_edge = Edge("", next_node.label, new_node.label, raw=dist)
            edges.add(new_edge)
            new_node.add_edge(new_edge.label)
            next_node.add_edge(new_edge.label)
            
            # remove the neighbor from the "to-do" list / the corner from the neighbor's "to-do"
            corner.remove_neighbor(next_corner.label)
            next_corner.remove_neighbor(corner.label)

            # update corner
            corner = next_corner
            new_node = next_node
        else:
            # find distance between the nodes
            dist = image_util.distance_between(corner.label, first_corner.label)
            dist = dist/unit_length

            # create and register an edge
            new_edge = Edge("", first_node.label, new_node.label, raw=dist)
            edges.add(new_edge)
            first_node.add_edge(new_edge.label)
            new_node.add_edge(new_edge.label)

            complete = True
            
    return nodes, edges
        
def detect_corners(filename, unit_length):
    # Load Image
    bw_img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    gray = np.float32(bw_img)
    color_img = cv2.imread(filename)

    min_line_length = unit_length//4

    ### CORNER DETECTION
    raw_corners = cv2.goodFeaturesToTrack(gray, 23, 0.17, min_line_length)
    raw_corners = np.int0(raw_corners)

    simple_corners = []
    corners = GraphElements()
    for i, corner in enumerate(raw_corners):
        x, y = corner.ravel()
        simple_corners.append((x,y))
        corners.add(image_util.Corner((x,y)))
        cv2.circle(color_img, (x, y), 5, (255, 0, 0), -1)

    # Add lines (internal and external; none across empty space)
    lines = set()
    for i, corner1 in enumerate(simple_corners):
        corners.get(corner1).points = image_util.find_convexity(corner1, bw_img)
        for j in range(i+1, len(simple_corners), 1):
            if image_util.legal_edge(corner1, simple_corners[j], bw_img):
                if image_util.is_regular_length(corner1, simple_corners[j], unit_length):
                    if image_util.at_45_degree_multiple(corner1, simple_corners[j]):
                        line = [corner1, simple_corners[j]]
                        line.sort()
                        line = tuple(line)

                        if image_util.outside_edge(corner1, simple_corners[j], bw_img):
                            lines.add( image_util.Line(line, 2))
                        elif image_util.inside_edge(corner1, simple_corners[j], bw_img):
                            lines.add( image_util.Line(line, 1))
                        else:
                            lines.add(image_util.Line(line, 3))
                        corners.get(corner1).add_neighbor(simple_corners[j])
                        corners.get(simple_corners[j]).add_neighbor(corner1)
                        cv2.line(color_img,corner1,simple_corners[j],(0,255,0),2)
    lines = GraphElements(list(lines))
        
    
    cv2.imwrite('raw_corners.jpg',color_img)

    return corners, lines

def visualize(in_name, out_name, corners, edges):
    color_img = cv2.imread(in_name)
    for edge in edges.all():
        cv2.line(color_img,edge.coords[0],edge.coords[1],(randint(100, 200),randint(100, 200),randint(100, 200)),2)
    for corner in corners.all():
        cv2.circle(color_img, corner.coords, 5, (255, 0, 0), -1)
    cv2.imwrite(out_name,color_img)

def fill_in_solution(in_name, out_name, polygons):
    img = cv2.imread(in_name)
    for poly in polygons:
        #poly = np.array(poly)
        colors = (randint(100, 200), randint(100, 200), randint(100, 200))
        
        for i, p1 in enumerate(poly):
            for j in range(i+1, len(poly), 1):
                for k in range(j+1, len(poly), 1):
                    cv2.fillPoly(img, pts=[np.array([poly[i], poly[j], poly[k]])], color=colors)
    cv2.imwrite(out_name, img)        
        
def create_nodes_edges(corners, lines, unit_length):
    nodes = GraphElements([])
    edges = GraphElements([])

    # Get rid of unnecessary edges
    superfluous_lines = set()
    for line in lines.all():
        #if line.line_type == 3:
        for smaller_line in lines.all():
            if smaller_line != line and image_util.lines_connect(line, smaller_line):
                completion = image_util.third_line(line, smaller_line, lines)
                if completion:
                    print("Found completion: {}".format(completion))
                    superfluous_lines.add(line)
    for line in list(superfluous_lines):
        lines.remove(line.coords)

    # Handle corners at odd intersections
    for corner in corners.all():
        for line in lines.all():
            if corner.points > 4: #and line.line_type == 3:
                if image_util.point_on_line(corner, line):
                    print("Subtracting {} {}".format(corner, line))
                    corner.points -= 4

    for corner in corners.all():
        new_node = Node(corner.points, coords=corner.coords)
        new_node.internal = False
        nodes.add(new_node)

    for line in lines.all():
        node1 = nodes.get(line.coords[0])
        node2 = nodes.get(line.coords[1])
        dist = image_util.distance_between(*line.coords)
        dist = dist/unit_length
        new_edge = Edge("", node1.label, node2.label, dist, line.coords)
        edges.add(new_edge)

    for corner in corners.all():
        node = nodes.get(corner.coords)
        for neighbor in corner.neighbors:
            edge_coords = [corner.coords, neighbor]
            edge_coords.sort()
            if edges.contains(tuple(edge_coords)):
                edge = edges.get(tuple(edge_coords))
                node.add_edge(edge.label)

    return nodes, edges
    
