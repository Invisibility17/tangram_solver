import image_util

def constrain(A, a, B, b):
    val = not overlapping(a, b) and not overlapping(b, a)
    #print(val)
    return val
    
def overlapping(shape1, shape2):
    #print("Checking overlap")
    #print(shape1)
    #print(shape2)
    for small_triangle in shape1.triangles:
        if small_triangle in shape2.triangles:
            return True
        for other_small_triangle in shape2.triangles:
            if is_inside(small_triangle, shape1, other_small_triangle, shape2):
                return True
    return False
            
    #print("Calling non_overlapping \n{} \n ---- \n{}".format(shape1, shape2))
    #print("# triangles {}, {}".format(len(shape1.triangles), len(shape2.triangles)))
    """for small_triangle in shape1.triangles:
        #print("Examining {}".format(small_triangle))
        if small_triangle in shape2.triangles:
            #print("These conflict \n{} \n ---- \n{}".format(shape1, shape2))
            return False

        corner1 = small_triangle[0]
        corner2 = small_triangle[1][0]
        corner3 = small_triangle[1][1]

        orders = [small_overlap(corner1, corner2, corner3, shape1, shape2),
                  small_overlap(corner1, corner3, corner2, shape1, shape2),
                  small_overlap(corner2, corner1, corner3, shape1, shape2),
                  small_overlap(corner3, corner1, corner2, shape1, shape2)]
                  #small_overlap(corner2, corner3, corner1, shape1, shape2),
        #small_overlap(corner3, corner2, corner1, shape1, shape2)
        for order in orders:
            if order:
                #print("These conflict \n{} \n ---- \n{}".format(shape1, shape2))
                return False
        

    return True"""

def is_inside(small_triangle1, shape1, small_triangle2, shape2):
    labels = [small_triangle2[0], small_triangle2[1][0], small_triangle2[1][1]]
    x = 0
    y = 0
    for tri_node in shape2.class_nodes:
        if tri_node.label in labels:
            x += tri_node.coords[0]
            y += tri_node.coords[1]
    x = x/3
    y = y/3
    
    labels = [small_triangle1[0], small_triangle1[1][0], small_triangle1[1][1]]
    pts = []
    for tri_node in shape1.class_nodes:
        if tri_node.label in labels:
            pts.append(tri_node.coords)
    #print(pts, (x,y))
    short_side = min(image_util.distance_between(pts[0], pts[1]),
                     image_util.distance_between(pts[0], pts[2]),
                     image_util.distance_between(pts[1], pts[2]))
    area = 0.5 *(-pts[1][1]*pts[2][0] + pts[0][1]*(-pts[1][0] + pts[2][0]) + pts[0][0]*(pts[1][1] - pts[2][1]) + pts[1][0]*pts[2][1])
    s = 1/(2*area)*(pts[0][1]*pts[2][0] - pts[0][0]*pts[2][1]
                    + (pts[2][1] - pts[0][1])*x
                    + (pts[0][0] - pts[2][0])*y)
    """if s < -0.003:
        print("{} {} s: {}".format(pts, (x,y), s))
        return False"""
    t = 1/(2*area)*(pts[0][0]*pts[1][1] - pts[0][1]*pts[1][0]
                    + (pts[0][1] - pts[1][1])*x
                    + (pts[1][0] - pts[0][0])*y)
    """if t < -0.003:
        print("{} {} t: {}".format(pts, (x,y), t))
        return False
    if 1-s-t < -0.003: 
        print("{} {} 1-s-t: {}".format(pts, (x,y), 1-t-s))
        return False"""
    """if (abs(s) < 0.1 or abs(t) < 0.1 or abs(1-s-t) < 0.1):
        print(s, t, 1-s-t)
        print(small_triangle1, small_triangle2)"""
    if t >= -0.02 and s >= -0.02 and 1-s-t >= -0.02:
        return True
    #print(pts, (x,y), s, t, 1-s-t)
    return False
            

def small_overlap(corner1, corner2, corner3, shape1, shape2):
    if corner1 in shape2.triangle_dictionary:
        for shape2s_corner_triangle in shape2.triangle_dictionary[corner1]:
            #print(corner2, shape2s_corner_triangle)
            if corner2 in [shape2s_corner_triangle[0]] + list(shape2s_corner_triangle[1]):
                for other_corner in [shape2s_corner_triangle[0]] + list(shape2s_corner_triangle[1]):
                    if other_corner != corner1 and other_corner != corner2:
                        if are_neighbors(corner3, other_corner, shape1, shape2):
                            return True
    return False

def are_neighbors(corner1, corner2, shape1, shape2):
    """print("____")
    print(shape1)
    print(shape2)
    print("----")
    print(corner1, corner2)"""
    for node in shape1.class_nodes:
        if node.label == corner1:
            node1 = node
    for node in shape2.class_nodes:
        if node.label == corner2:
            node2 = node
    for edge in node1.edges:
        if edge in node2.edges:
            return True
    return False
    
    
    """if type(shape1) not in (Large_Triangle, Medium_Triangle) \
       or type(shape2)  not in (Large_Triangle, Medium_Triangle):
            for i in range(len(shape2.nodes)):
                if shape2.nodes[i] in shape1.nodes:
                    for j in range(i+1, len(shape2.nodes), 1):
                        if shape2.nodes[j] in shape1.nodes:
                            for k in range(j+1, len(shape2.nodes), 1):
                                if shape2.nodes[k] in shape1.nodes:
                                    return False
            return True
    else:
        if type(shape1) is Medium_Triangle:
            if (shape1.hypotenuse_node.label in shape2.nodes) and (shape1.right_node.label in shape2.nodes):
                return False
            return True
        elif type(shape2) is Medium_Triangle:
            if (shape2.hypotenuse_node.label in shape1.nodes) and (shape2.right_node.label in shape1.nodes):
                return False
            return True
        elif type(shape1) is Large_Triangle:
            if shape1.hypotenuse_node.label in shape2.nodes:
                if shape1.r_node.label in shape2.nodes:
                    return False
                elif shape1.l_node.label in shape2.nodes:
                    return False
                elif shape1.right_angle.label in shape2.nodes:
                    return False
            elif shape1.l_node.label in shape2.nodes and shape1.r_node.label in shape2.nodes:
                return False
            return True
        else:
            print("Error: Type not recognized")
            exit()
        """
class Shape:
    def __init__(self, nodes):
        self.nodes = nodes
        self.nodes.sort()
        self.nodes = tuple(self.nodes)

    

    def __eq__(self, other):
        return hash(self.nodes) == hash(other.nodes)

    def __hash__(self):
        return hash(self.nodes)
    
    def overlaps(self, other):
        for i in range(len(other.nodes)):
            if other.nodes[i] in self.nodes:
                for j in range(i+1, len(other.nodes), 1):
                    if other.nodes[j] in self.nodes:
                        for k in range(j+1, len(other.nodes), 1):
                            if other.nodes[k] in self.nodes:
                                return True
        return False

class Large_Triangle(Shape):
    def __init__(self, hypotenuse_node, r_acute, r_node, right_angle, l_acute, l_node):
        self.hypotenuse_node = hypotenuse_node
        self.r_acute = r_acute
        self.r_node = r_node
        self.right_angle = right_angle
        self.l_acute = l_acute
        self.l_node = l_node
        self.class_nodes = [hypotenuse_node, r_acute, r_node, right_angle, l_acute, l_node]
        Shape.__init__(self, [hypotenuse_node.label, r_acute.label, r_node.label, right_angle.label, l_acute.label, l_node.label])
        tris = [(self.r_node.label, self.hypotenuse_node.label, self.r_acute.label),
                (self.l_node.label, self.hypotenuse_node.label, self.l_acute.label),
                (self.hypotenuse_node.label, self.l_node.label, self.r_node.label),
                (self.r_node.label, self.hypotenuse_node.label, self.right_angle.label),
                (self.l_node.label, self.hypotenuse_node.label, self.right_angle.label),
                (self.right_angle.label, self.l_node.label, self.r_node.label)]
        self.triangles = []
        self.triangle_dictionary = {}
        for tri in tris:
            sorted_tri = tuple([tri[0], tuple(sorted([tri[1], tri[2]]))])
            self.triangles.append(sorted_tri)
            for t in tri:
                if t not in self.triangle_dictionary:
                    self.triangle_dictionary[t] = [sorted_tri]
                else:
                    self.triangle_dictionary[t].append(sorted_tri)
        #self.triangles.append( tuple(sorted((self.hypotenuse_node.label, self.r_acute.label)), self.r_node.label), 
    def __str__(self):
        return """{} 
{} {}
{} {} {}""".format(self.r_acute.label,
                   self.r_node.label, self.hypotenuse_node.label,
                   self.right_angle.label, self.l_node.label, self.l_acute.label)
    
    def overlaps(self, other):
        if type(other) is Medium_Triangle:
            if (other.hypotenuse_node.label in self.nodes) and (other.right_node.label in self.nodes):
                return True
            else:
                return False
        else:
            for i in range(len(other.nodes)):
                if other.nodes[i] in self.nodes:
                    for j in range(i+1, len(other.nodes), 1):
                        if other.nodes[j] in self.nodes:
                            for k in range(j+1, len(other.nodes), 1):
                                if other.nodes[k] in self.nodes:
                                    return True
            return False

class Medium_Triangle(Shape):
    def __init__(self, hypotenuse_node, right_node, r_acute,  l_acute):
        self.hypotenuse_node = hypotenuse_node
        self.right_node = right_node
        self.l_acute = l_acute
        self.r_acute = r_acute
        self.class_nodes = [hypotenuse_node, right_node, r_acute, l_acute]
        Shape.__init__(self, [hypotenuse_node.label, right_node.label,
                        r_acute.label, l_acute.label])

        tris = [(self.hypotenuse_node.label, self.r_acute.label, self.right_node.label),
                (self.hypotenuse_node.label, self.l_acute.label, self.right_node.label)]
        self.triangles = []
        self.triangle_dictionary = {}
        for tri in tris:
            sorted_tri = tuple([tri[0], tuple(sorted([tri[1], tri[2]]))])
            self.triangles.append(sorted_tri)
            for t in tri:
                if t not in self.triangle_dictionary:
                    self.triangle_dictionary[t] = [sorted_tri]
                else:
                    self.triangle_dictionary[t].append(sorted_tri)

    def __str__(self):
        return """{}
{} {}
{}""".format(self.l_acute.label,
             self.hypotenuse_node.label, self.right_node.label,
             self.r_acute.label)

class Parallelogram(Shape):
    def __init__(self, anchor, bottom, cross, top):
        self.anchor = anchor
        self.bottom = bottom
        self.cross = cross
        self.top = top
        self.class_nodes = [anchor, bottom, cross, top]
        Shape.__init__(self, [anchor.label, bottom.label, cross.label, top.label])
        tris =[(self.anchor.label, self.cross.label, self.top.label),
               (self.cross.label, self.bottom.label, self.anchor.label)]
        #[(self.anchor.label, self.bottom.label, self.cross.label),
        #(self.cross.label, self.anchor.label, self.top.label)]
        # (self.anchor.label, self.cross.label, self.top.label)
        # (self.cross.label, self.bottom.label, self.anchor.label)
        self.triangles = []
        self.triangle_dictionary = {}
        for tri in tris:
            sorted_tri = tuple([tri[0], tuple(sorted([tri[1], tri[2]]))])
            self.triangles.append(sorted_tri)
            for t in tri:
                if t not in self.triangle_dictionary:
                    self.triangle_dictionary[t] = [sorted_tri]
                else:
                    self.triangle_dictionary[t].append(sorted_tri)

    def __str__(self):
        return """{}
{} {}
   {}""".format(self.top.label, self.anchor.label, self.cross.label, self.bottom.label)


class Square(Shape):
    def __init__(self, corner0, corner1, corner2, corner3):
        self.corner0 = corner0
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.class_nodes = [corner0, corner1, corner2, corner3]
        Shape.__init__(self, [corner0.label, corner1.label, corner2.label, corner3.label])

        tris = [(self.corner0.label, self.corner1.label, self.corner2.label),
                (self.corner3.label, self.corner1.label, self.corner2.label),
                (self.corner1.label, self.corner0.label, self.corner3.label),
                (self.corner2.label, self.corner0.label, self.corner3.label)]
        self.triangles = []
        self.triangle_dictionary = {}
        for tri in tris:
            sorted_tri = tuple([tri[0], tuple(sorted([tri[1], tri[2]]))])
            self.triangles.append(sorted_tri)
            for t in tri:
                if t not in self.triangle_dictionary:
                    self.triangle_dictionary[t] = [sorted_tri]
                else:
                    self.triangle_dictionary[t].append(sorted_tri)

    def __str__(self):
        return """{} {}
{} {}""".format(self.corner0.label, self.corner1.label,
                self.corner2.label, self.corner3.label)

class Small_Triangle(Shape):
    def __init__(self, right_corner, top_corner, bottom_corner):
        self.right_corner = right_corner
        self.top_corner = top_corner
        self.bottom_corner = bottom_corner
        self.class_nodes = [right_corner, top_corner, bottom_corner]
        Shape.__init__(self, [right_corner.label, top_corner.label, bottom_corner.label])
        self.triangles = [tuple([self.right_corner.label, tuple(sorted([self.top_corner.label, self.bottom_corner.label]))])]
        self.triangle_dictionary = {self.right_corner.label:[self.triangles[0]],
                                    self.top_corner.label:[self.triangles[0]],
                                    self.bottom_corner.label:[self.triangles[0]]}

    def __str__(self):
        return """{}
{} {}""".format(self.top_corner.label,
                self.right_corner.label, self.bottom_corner.label)

