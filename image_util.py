from math import sqrt, acos, pi, sin, cos
import cv2
#import numpy as np
threshold = 8

def find_convexity(point, img):
    theta = 30
    directions = [pi/6, pi/6 + pi/4, pi/6 + pi/2, pi/6 + 3*pi/4, pi/6 + pi, pi/6 + 5*pi/4, pi/6 + 3*pi/2, pi/6 + 7*pi/4 ]
    black = 0
    for theta in directions:
        x = point[0]+int(round(cos(theta)*threshold))
        y = point[1]+int(round(sin(theta)*threshold))
        if img[y][x] == 0:
            black += 1
    return black
        
def inside_edge(point1, point2, img):
    if not close_enough(point1[0], point2[0]):
        up1 = (point1[0], point1[1]-threshold)
        down1 = (point1[0], point1[1]+threshold)
        up2 = (point2[0], point2[1]-threshold)
        down2 = (point2[0], point2[1]+threshold)
        if points_between_are_inside(up1, up2, img) == 1 and points_between_are_inside(down1, down2, img) == 1:
            return True
    else:
        right1 = (point1[0]+threshold, point1[1])
        left1 = (point1[0]-threshold, point1[1])
        right2 = (point2[0]+threshold, point2[1])
        left2 = (point2[0]-threshold, point2[1])
        if points_between_are_inside(right1, right2, img) == 1 and points_between_are_inside(left1, left2, img) == 1:
            return True

    return False
def outside_edge(point1, point2, img):
    if not close_enough(point1[0], point2[0]):
        up1 = (point1[0], point1[1]-threshold)
        down1 = (point1[0], point1[1]+threshold)
        up2 = (point2[0], point2[1]-threshold)
        down2 = (point2[0], point2[1]+threshold)
        if points_between_are_inside(up1, up2, img) == 1 and points_between_are_inside(down1, down2, img) == 0:
            return True
        elif points_between_are_inside(up1, up2, img) == 0 and points_between_are_inside(down1, down2, img) == 1:
            return True
    else:
        right1 = (point1[0]+threshold, point1[1])
        left1 = (point1[0]-threshold, point1[1])
        right2 = (point2[0]+threshold, point2[1])
        left2 = (point2[0]-threshold, point2[1])
        if points_between_are_inside(right1, right2, img) == 1 and points_between_are_inside(left1, left2, img) == 0:
            return True
        elif points_between_are_inside(right1, right2, img) == 0 and points_between_are_inside(left1, left2, img) == 1:
            return True
    return False

def close_enough(int1, int2):
    return abs((int1-int2)*100/max(int1, int2)) < threshold

def distance_is(point1, point2, unit_len):
    return close_enough(distance_between(point1, point2), unit_len)

def distance_between(point1, point2):
    return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def black_area(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    black = 0
    for x in range(w):
        for y in range(h):
            if img[y][x] == 0:
                black += 1
    return black
                
"""def angle_between(center_point, point1, point2):
    a = (center_point[0]-point1[0])**2 + (center_point[1]-point1[1])**2
    b = (center_point[0]-point2[0])**2 + (center_point[1]-point2[1])**2
    c = (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2
    return round(4* acos((a+b-c)/ sqrt(4*a*b)) / pi)"""

def points_between_are_inside(point1, point2, img, check=30):
    x1, y1 = point1
    x2, y2 = point2
    black = 0
    white = 0
    #print(point1, point2)
    if abs(x1 -x2) > threshold:
        slope = (y1-y2)/(x1-x2)
        pm_one = int((x2-x1)/abs(x2-x1))
        x_dist = abs(int(x2-x1))
        lower= int(x1) + threshold*pm_one
        upper = int(x2) - threshold*pm_one
        for x in range(lower, upper, max(pm_one, pm_one * x_dist // check )):
            y = int(round(slope*(x-x1)+y1))
            #print(x, y, img[y][x])
            if img[y][x] == 0:
                black += 1
            else:
                white += 1
    else:
        slope = (x1-x2)/(y1-y2)
        pm_one = int((y2 - y1)/abs(y2-y1))
        y_dist = abs(int(y2-y1))
        lower = int(y1)+threshold*pm_one
        upper = int(y2)-threshold*pm_one
        for y in range(lower, upper, max(pm_one, pm_one * y_dist // check)):
            x = int(round(slope*(y-y1)+x1))
            #print(x, y, img[y][x])
            if img[y][x] == 0:
                black += 1
            else:
                white += 1
    if (black / (black+white)) > 0.85:
        return 1
    elif (white / (black+white)) > 0.85:
        return 0
    else:
        return -1


"""def edge_connects_points(edge, points):
    end1 = edge[0]
    end2 = edge[1]
    connected = []
    for point in points:
        if points_are_close(end1, point):
            connected.append(point)
        elif points_are_close(end2, point):
            connected.append(point)
    if len(connected) == 2:
        return tuple(connected)
    return False"""

def points_are_close(point1, point2):
    return distance_between(point1, point2) <= threshold


class Corner():
    def __init__(self, pt):
        self.label = pt
        self.neighbors = set()
        self.convex = None
        self.points = 0

    def add_neighbor(self, neighbor):
        assert type(neighbor) == tuple
        self.neighbors.add(neighbor)
        if len(self.neighbors) > 2:
            print("Error: too many neighbors")
            exit()

    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
        else:
            print("Error: {} does not neighbor {}".format(self.label, neighbor))
            exit()

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return """{}: points: {}, {}""".format(self.label, self.points, self.neighbors)
