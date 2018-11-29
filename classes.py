## Node & Edge classes for the tangram solver.
# points = value from 1 to 8, with each representing 45* of filled in space
# 1 is a point, 8 is an entirely internal point.
# length tuple = (known, i, j) where if length is determined, known = True
# and length = i + sqrt(2)*j. If length not determined,
# known = False and i, j = 0

from math import sqrt
import image_util

# "equality" computation with a margin of error
#def close_enough(num1, num2):
#    return abs(num1-num2)/num1 < 0.011
    
class Node:
    new_label = 1
    def __init__(self, points, edges=[]):
        self.label = Node.new_label
        Node.new_label += 1
        self.points = points
        self.remaining_points = points
        self.externals = edges.copy()
        self.edges = edges.copy()
        self.resolved = False
        self.internal = False

    def __str__(self):
        return "N{0}: {1} {2} {3} Resolved: {4}".format(
            self.label, self.edges, self.points, self.remaining_points, self.resolved)

    def can_add_edge(self):
        return self.remaining_points >= 2 # len(self.edges)

    def gt_90(self):
        return self.remaining_points > 2

    def add_edge(self, edge):
        self.edges.append(edge)

    def replace_edge(self, current_edge, future_edge):
        self.edges.remove(current_edge)
        self.edges.append(future_edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def __gt__(self, other):
        return self.label > other.label

    def sub_remaining(self, count):
        if self.remaining_points >= count:
            self.remaining_points -= count
            if self.remaining_points == 0:
                self.resolved = True
            return True
        else:
            print("Error: node {} does not have {} remaining points".format(self, count))
            return False

class Edge:
    new_label = 1
    # it might  be better to pass a raw length and let Edge determine the "length"
    def __init__(self, length, node1, node2, raw=False):
        self.label = Edge.new_label
        Edge.new_label += 1
        self.nodes = [node1, node2]
        self.resolved = False
        if raw:
            self.length = self.process_raw(raw)
            self.raw = raw
        else:
            self.length = length
            self.raw = False

    def get_other_node(self, node):
        if self.nodes[0] == node:
            return self.nodes[1]
        elif self.nodes[1] == node:
            return self.nodes[0]
        else:
            print("Error: node {} not connected to edge {}".format(node, self.label))
            exit()
        
    # try to determine the closest fit between units/root two
    def process_raw(self, length):
        progression = [(0, 0), (-1, 1), (2, -1), (-2, 2), (1, 0), (0, 1), (-1, 2), (2, 0), (1, 1), (0, 2), (3, 0), (-1, 3), (2, 1), (4, 0)]
        for n in range(1, len(progression), 1):
            combo = progression[n]
            tlen = combo[0] + 2**(1/2)*combo[1]
            if image_util.close_enough(tlen, length):
                return (True,) + combo
            elif tlen > length:
                return (False,) + progression[n-1]

            
                
    def is_root(self):
        return self.length[0] and self.length[1] == 0 and self.length[2] == 1

    def contains_one(self):
        return self.length[0] and self.length[1] > 0 and self.length[2] >= 0

    def contains_root(self):
        return self.length[0] and self.length[1] >= 0 and self.length[2] > 0

    def is_one(self):
        return self.length[0] and self.length[1] == 1 and self.length[2] == 0

    def is_unit(self):
        return self.length[0] and self.length[1] >= 1 and self.length[2] == 0

    def is_root_multiple(self):
        return self.length[0] and self.length[1] == 0 and self.length[2] >= 1

    def is_known(self):
        return self.length[0]

    def minus_one(self):
        if self.contains_one():
            return (self.length[0], self.length[1]-1, self.length[2])

    def minus_root(self):
        if self.contains_root() or self.length[2]>0:
            return (self.length[0], self.length[1], self.length[2]-1)
        elif self.raw and self.raw >= sqrt(2):
            return self.process_raw(self.raw - sqrt(2))
        else:
            print("Error: too short to subtract root from edge")

    def is_overlapped(self):
        return self.length == (True, -1, 1)
        

    def gteq_root(self):
        return (self.length[2] >= 1 and self.length[1] >= 0) or (self.length[1] >= 2)

    def gteq_one(self):
        return self.length[1] >= 1

    def lt_one(self):
        return self.length[1] + sqrt(2)*self.length[2] < 1
    
    def __str__(self):
        return "E{0}: {1} {2}. Resolved: {3}".format(self.label, self.nodes, self.length, self.resolved)

    def __hash__(self):
        return hash(set(*self.nodes))

class GraphElements:
    def __init__(self, elements=[]):
        self.elements = elements

    def add(self, element):
        if type(element) == list:
            self.elements += element
        else:
            self.elements.append(element)

    def get(self, label):
        for element in self.elements:
            if element.label == label:
                return element
        print("Error: {} not found".format(label))
    def size(self):
        return len(self.elements)
            
    def all(self):
        return self.elements
    
    def remove(self, label):
        for element in []+self.elements:
            if element.label == label:
                self.elements.remove(element)
