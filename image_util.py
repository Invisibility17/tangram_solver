from math import sqrt, acos, pi, sin, cos
import cv2
#import numpy as np
threshold = 8
progression = [(1, 0), (0, 1), (2, 0), (1, 1), (0, 2), (3, 0), (2, 1), (1, 2), (4, 0), (3, 1), (2,2), (5, 0),(0,4)]

def match_corners(corners, lines, filename, unit_length):
    bw_img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    for i, corner1 in enumerate(corners.all()):
        #corners.get(corner1).points = image_util.find_convexity(corner1, bw_img)
        for j in range(i+1, corners.size(), 1):
            corner2 = corners.all()[j]
            if legal_edge(corner1.coords, corner2.coords, bw_img):
                if is_regular_length(corner1.coords, corner2.coords, unit_length):
                    if at_45_degree_multiple(corner1.coords, corner2.coords):
                        line = [corner1.coords, corner2.coords]
                        line.sort()
                        line = tuple(line)

                        if outside_edge(corner1.coords, corner2.coords, bw_img):
                            lines.add( Line(line, 2))
                        elif inside_edge(corner1.coords, corner2.coords, bw_img):
                            lines.add( Line(line, 1))
                        else:
                            lines.add(Line(line, 3))
                        corners.get(corner1.coords).add_neighbor(corner2.coords)
                        corners.get(corner2.coords).add_neighbor(corner1.coords)
    return corners, lines
def split_line(line, corners, lines, unit_length, img):
    progression = [(2, 0), (0, 2), (3, 0), (0, 3), (4, 0), (5, 0), (0, 4)]
    for length in progression:
        if close_enough( distance_between(*line.coords), unit_length*(length[0] + sqrt(2)*length[1]), 4):
            print("Splitting line length {}".format(length))

            #print("Split {}".format(line))
            # split in half
            if sum(length)%2 == 0:
                if sum(length) %2 == 0:
                    midpoint = find_midpoint(*line.coords)
                    existing = False
                    for corner in corners.all():
                        if points_are_close(midpoint, corner.coords):
                            print("Found close points {} {}".format(corner.coords, midpoint))
                            existing = True
                            corner.add_neighbor(line.coords[0])
                            corner.add_neighbor(line.coords[1])
                            midpoint = corner.coords
                    if not existing:
                        new_corner = Corner(midpoint)
                        new_corner.add_neighbor(line.coords[0])
                        new_corner.add_neighbor(line.coords[1])
                        print("Adding new corner {}".format(new_corner))
                        corners.add(new_corner)
                        new_corner.points = find_convexity(new_corner.coords, img)
                    new_lines = [[line.coords[0], midpoint], [line.coords[1], midpoint]]
                    for new_line in new_lines:
                        new_line.sort()
                        new_line = tuple(new_line)
                        lines = add_new_line(new_line, lines, img)
                    print("Getting {}".format(line.coords[0]))
                    corners.get(line.coords[0]).add_neighbor(midpoint)
                    corners.get(line.coords[0]).remove_neighbor(line.coords[1])
                    corners.get(line.coords[1]).add_neighbor(midpoint)
                    corners.get(line.coords[1]).remove_neighbor(line.coords[0])


            else:
                if length[0] > 0:
                    segment_length = unit_length
                else:
                    segment_length = sqrt(2)*unit_length
                new_corner = point_along_line(line.coords, segment_length)
                existing = False
                for corner in corners.all():
                    if points_are_close(corner.coords, new_corner.coords):
                        #print("Existing {} {}".format(corner, new_corner))
                        corner.add_neighbor(line.coords[0])
                        corner.add_neighbor(line.coords[1])
                        new_lines = [[line.coords[0], new_corner.coords], [new_corner.coords, line.coords[1]]]
                        for new_line in new_lines:
                            new_line.sort()
                            new_line = tuple(new_line)
                            lines = add_new_line(new_line, lines, img)
                        corners.get(line.coords[0]).add_neighbor(corner.coords)
                        corners.get(line.coords[0]).remove_neighbor(line.coords[1])
                        corners.get(line.coords[1]).add_neighbor(corner.coords)
                        corners.get(line.coords[1]).remove_neighbor(line.coords[0])
                        existing = True
                if not existing:
                    #print("New corner {}".format(new_corner))
                    new_corner.add_neighbor(line.coords[0])
                    new_corner.add_neighbor(line.coords[1])
                    new_corner.points = find_convexity(new_corner.coords, img)
                    #print("Adding new corner {}".format( new_corner))
                    corners.add(new_corner)
                    new_lines = [[line.coords[0], new_corner.coords], [new_corner.coords, line.coords[1]]]
                    for new_line in new_lines:
                        new_line.sort()
                        new_line = tuple(new_line)
                        lines = add_new_line(new_line, lines, img)
                    print(corners.get(line.coords[0]), corners.get(line.coords[1]))
                    corners.get(line.coords[0]).add_neighbor(new_corner.coords)
                    corners.get(line.coords[0]).remove_neighbor(line.coords[1])
                    corners.get(line.coords[1]).add_neighbor(new_corner.coords)
                    corners.get(line.coords[1]).remove_neighbor(line.coords[0])


                    
            """elif sum(length) == 3:
                tri1, tri2 = find_trisections(*line.coords)
                existing = [False, False]
                for corner in corners.all():
                    if points_are_close(tri1, corner.coords):
                        corner.add_neighbor(line.coords[0])
                        corner.add_neighbor(line.coords[1])
                        existing[0] = True
                        tri1 = corner.coords
                    if points_are_close(tri2, corner.coords):
                        corner.add_neighbor(line.coords[0])
                        corner.add_neighbor(line.coords[1])
                        existing[1] = True
                        tri2 = corner.coords
                        
                if not existing[0]:
                    new_corner = Corner(tri1)
                    new_corner.add_neighbor(line.coords[0])
                    new_corner.add_neighbor(tri2)
                    new_corner.points = find_convexity(new_corner.coords, img)
                    corners.add(new_corner)
                    new_lines = [[line.coords[0], tri1], [tri1, tri2]]
                    for new_line in new_lines:
                        new_line.sort()
                        new_line = tuple(new_line)
                        lines = add_new_line(new_line, lines, img)
                        
                if not existing[1]:
                    new_corner = Corner(tri2)
                    new_corner.add_neighbor(line.coords[1])
                    corners.get(line.coords[1]).add_neighbor(tri2)
                    new_corner.add_neighbor(tri1)
                    corners.get(tri1).add_neighbor(tri2)
                    new_corner.points = find_convexity(new_corner.coords, img)
                    corners.add(new_corner)
                    new_lines = [[tri1, tri2], [line.coords[1], tri2]]
                    for new_line in new_lines:
                        new_line.sort()
                        new_line = tuple(new_line)
                        lines = add_new_line(new_line, lines, img)"""

            
                        
            lines.remove(line.coords)
            return 1, corners, lines
            
    return 0, corners, lines
def point_along_line(line, distance):
    x0, y0 = line[0]
    x1, y1 = line[1]
    if close_enough(x0, x1, 8):
        corner = Corner((x0, min(y0, y1)+int(distance)))
        return corner
    elif close_enough(y0, y1, 8):
        return Corner((int(min(x0,x1)+round(distance)), y0))
    else:
        m = (y1-y0)/(x1-x0)
        x = min(x0, x1) + distance*sqrt(1+m**2)
        y = m*(x-x0)+y0
        return Corner((int(round(x)), int(round(y))))
def add_new_line(line, lines, img):
    if inside_edge(*line, img):
        new_line = Line(line, 1)
        lines.add(new_line)
    elif outside_edge(*line, img):
        new_line = Line(line, 2)
        lines.add(new_line)
    else:
        new_line = Line(line, 3)
        lines.add(new_line)
    return lines

def find_midpoint(point1, point2):
    new_x = int(round((point1[0] + point2[0])/2))
    new_y = int(round((point1[1] + point2[1])/2))
    return (new_x, new_y)

def find_trisections(point1, point2):
    dif_x = point1[0] - point2[0]
    dif_y = point1[1] - point2[1]
    pt1x = int(round(point1[0] - dif_x/3))
    pt1y = int(round(point1[1] - dif_y/3))
    pt2x = int(round(point1[0] - 2*dif_x/3))
    pt2y = int(round(point1[1] - 2*dif_y/3))
    return (pt1x, pt1y), (pt2x, pt2y)
    
def point_on_line(point, line):
    if point.coords in line.coords:
        return False
    line1 = (point.coords, line.coords[0])
    line2 = (point.coords, line.coords[1])
    return close_enough(distance_between(*line1) + distance_between(*line2), distance_between(*line.coords), 3)

def lines_connect(line1, line2):
    if line1.coords[0] in line2.coords:
        return True
    if line1.coords[1] in line2.coords:
        return True
    return False

def third_line(line1, line2, lines):
    line1 = line1.coords
    line2 = line2.coords
    if line1[0] == line2[0]:
        third = [line1[1], line2[1]]
    elif line1[1] == line2[0]:
        third = [line1[0], line2[1]]
    elif line1[0] == line2[1]:
        third = [line1[1], line2[0]]
    elif line1[1] == line2[1]:
        third = [line1[0], line2[0]]
    third.sort()
    if lines.contains(tuple(third)):
        if close_enough(distance_between(*line2) + distance_between(*third), distance_between(*line1)):
            return line1
    return False
    
def at_45_degree_multiple(point1, point2):
    if close_enough(point1[0], point2[0]):
        return True
    if close_enough(point1[1], point2[1]):
        return True
    pt = (point1[0], point2[1])
    angle = angle_between(point1, point2, pt)
    if close_enough(angle, 45, 5) or close_enough(angle, 135, 5) or close_enough(angle, 225, 5) or close_enough(angle, 315, 5):
        return True
    return False
    
def is_regular_length(point1, point2, unit_length):
    global progression
    distance = distance_between(point1, point2)
    for lengths in progression:
        if close_enough((lengths[0]+sqrt(2)*lengths[1])*unit_length, distance, 8):
            return True
    return False

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

def legal_edge(point1, point2, img):
    if not close_enough(point1[0], point2[0]):
        up1 = (point1[0], point1[1]-threshold)
        down1 = (point1[0], point1[1]+threshold)
        up2 = (point2[0], point2[1]-threshold)
        down2 = (point2[0], point2[1]+threshold)
        if points_between_are_inside(up1, up2, img) == 1 or points_between_are_inside(down1, down2, img) == 1:
            return True
    else:
        right1 = (point1[0]+threshold, point1[1])
        left1 = (point1[0]-threshold, point1[1])
        right2 = (point2[0]+threshold, point2[1])
        left2 = (point2[0]-threshold, point2[1])
        if points_between_are_inside(right1, right2, img) == 1 or points_between_are_inside(left1, left2, img) == 1:
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

def close_enough(int1, int2, threshold=8):
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
                
def angle_between(center_point, point1, point2):
    a = (center_point[0]-point1[0])**2 + (center_point[1]-point1[1])**2
    b = (center_point[0]-point2[0])**2 + (center_point[1]-point2[1])**2
    c = (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2
    return round(180* acos((a+b-c)/ sqrt(4*a*b)) / pi)

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
        #print("Increment distance {} from {} to {}".format(max(pm_one, pm_one * x_dist // check), lower, upper ))
        for x in range(lower, upper, max(pm_one, pm_one * x_dist // check )):
            y = int(round(slope*(x-x1)+y1))
            #print("At {}, {} {}".format(x,y, img[y][x]))
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
    #print(point1, point2)
    if black+white == 0:
        return -1
    elif (black / (black+white)) > 0.93:
        return 1
    elif (white / (black+white)) > 0.93:
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

def lines_are_close(line1, line2):
    return points_are_close(line1[0], line2[0]) and points_are_close(line1[1], line2[1])


class Corner():
    def __init__(self, pt):
        self.coords = pt
        self.neighbors = set()
        self.convex = None
        self.points = 0

    def add_neighbor(self, neighbor):
        assert type(neighbor) == tuple
        self.neighbors.add(neighbor)
        

    def remove_neighbor(self, neighbor):
        #if neighbor in self.neighbors:
        for other_neighbor in list(self.neighbors):
            if points_are_close(other_neighbor, neighbor):
                self.neighbors.remove(other_neighbor)
                return
        print("Error: {} does not neighbor {}".format(self.coords, neighbor))
        exit()

    def __hash__(self):
        return hash(self.coords)

    def __str__(self):
        return """{}: points: {}, {}""".format(self.coords, self.points, self.neighbors)

inside = 1
edge = 2
mixed = 3
class Line():
    ref = {1:"internal", 2:"edge", 3:"mixed", 0:"undefined"}
    def __init__(self, coords, line_type=0):
        self.coords = coords
        self.line_type = line_type

    def __hash__(self):
        return hash(self.coords)

    def __eq__(self, other):
        if points_are_close(self.coords[0], other.coords[0]) and points_are_close(self.coords[1], other.coords[1]):
            return True
        if points_are_close(self.coords[1], other.coords[0]) and points_are_close(self.coords[0], other.coords[1]):
            return True
        return False

    def __str__(self):
        return """{}: line type {}""".format(self.coords, self.ref[self.line_type])
