def constrain(A, a, B, b):
    return non_overlapping(a, b) and non_overlapping(b, a)
    
def non_overlapping(shape1, shape2):
    if type(shape1) not in (Large_Triangle, Medium_Triangle) \
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
        
        Shape.__init__(self, [hypotenuse_node.label, r_acute.label, r_node.label, right_angle.label, l_acute.label, l_node.label])

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

        Shape.__init__(self, [hypotenuse_node.label, right_node.label,
                        r_acute.label, l_acute.label])

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

        Shape.__init__(self, [anchor.label, bottom.label, cross.label, top.label])

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
        Shape.__init__(self, [corner0.label, corner1.label, corner2.label, corner3.label])

    def __str__(self):
        return """{} {}
{} {}""".format(self.corner0.label, self.corner1.label,
                self.corner2.label, self.corner3.label)

class Small_Triangle(Shape):
    def __init__(self, right_corner, top_corner, bottom_corner):
        self.right_corner = right_corner
        self.top_corner = top_corner
        self.bottom_corner = bottom_corner

        Shape.__init__(self, [right_corner.label, top_corner.label, bottom_corner.label])

    def __str__(self):
        return """{}
{} {}""".format(self.top_corner.label,
                self.right_corner.label, self.bottom_corner.label)

