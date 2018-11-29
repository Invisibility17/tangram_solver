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

def get_unit_length(filename):
    black_area = image_util.black_area(filename)
    return int(round(sqrt(black_area/8)))

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
        cv2.circle(color_img, (x, y), 10, 25*i, -1)

    for i, corner1 in enumerate(simple_corners):
        corners.get(corner1).points = image_util.find_convexity(corner1, bw_img)
        for j in range(i+1, len(simple_corners), 1):
            if image_util.outside_edge(corner1, simple_corners[j], bw_img):
                corners.get(corner1).add_neighbor(simple_corners[j])
                corners.get(simple_corners[j]).add_neighbor(corner1)

    cv2.imwrite('all_corners.jpg',color_img)

    return corners
            
        
    


