from random import random

class Polygon(object):
    def __init__(self, vertices):
        if len(vertices) < 2:
            raise Exception("Polygon by definition must have more than 2 verticies")

        self.segments = []
        i = 0
        for i in range(len(vertices)-1):
            self.segments.append((vertices[i], vertices[i+1]))

        # last segmenet wraps around index
        self.segments.append((vertices[-1], vertices[0]))

    def point_inside(self, pt):
        """ Use the Raycasting algorithm to determine if the point is inside our
        polygon

        See: 
        http://en.wikipedia.org/wiki/Point_in_polygon
        http://rosettacode.org/wiki/Ray-casting_algorithm
        """
        intersections = 0
        for segment in self.segments:
            if self.ray_intersects_segment(pt, segment):
                intersections += 1

        # point is outside polygon if # of intersection is odd
        # point is inside polygon if # of intersection is even
        return False if (intersections % 2 == 0) else True

    def ray_intersects_segment(self, ray_origin, segment):
        xPt, yPt = ray_origin

        p1,p2 = segment
        x1,y1 = p1
        x2,y2 = p2

        # let pA be lowest y-point and pB be highest y-point
        if y1 < y2:
            pA = (x1,y1)
            pB = (x2,y2)
        else:
            pA = (x2,y2)
            pB = (x1,y1)
        xa,ya = pA
        xb,yb = pB

        # ray will intersect on a vertices, so we shift it up a bit
        EPSILON = 0.01
        if yPt == ya or yPt == yb:
            yPt += EPSILON
        
        if yPt < ya or yPt > yb:
            # point lies too low or too high for line segment
            return False
        elif xPt > max(xa,xb):
            # point lies past segment
            return False
        elif xPt < min(xa,xb):
            # point lies before segment
            return True
        else:
            # pt is boxed by segment; we want to know which side of the segment pt is on
            # if pt on left side then intersect, otherwise no intersect on right side
            # we compare alpha = angle(pB, pA) and beta = angle(pt, pA)
            # if beta > alpha then point is on left side of segmenet
            # we can use slopes rather than calc. angle
            m_alpha = Infinity if xa == xb else float(yb - ya) / float(xb - xa)
            m_beta = Infinity if xPt == xa else float(yPt - ya) / float(xPt - xa)
            return (m_beta >= m_alpha)



def random_point_in_bbox(x1, y1, x2, y2):
    x_len = abs(x2 - x1)
    y_len = abs(y2 - y1)

    # generate random point on [0, x_len] then shift by x1 to be inside bbox
    x_pos = random() * x_len + x1
    y_pos = random() * y_len + y1

    return (x_pos, y_pos)

def random_point_in_polygon(polygon_verts, polygon_bbox):
    poly = Polygon(polygon_verts)
    while True:
        pt = random_point_in_bbox(polygon_bbox)
        if poly.point_inside(pt):
            return pt

def test_point_in_polygon():
    polygon_verts = [
        (0,0),
        (5,5),
        (10,0),
        (5,-5)
    ]
    polygon_bbox = [0,-5, 10, 10]

    poly = Polygon(polygon_verts)
    test_pt0 = (3,0)
    test_pt1 = (1,1)
    test_pt2 = (11,1)
    test_pt3 = (7,3)

    assert poly.point_inside(test_pt0) == True
    assert poly.point_inside(test_pt1) == False # on boundary; make judgement call false
    assert poly.point_inside(test_pt2) == False
    assert poly.point_inside(test_pt3) == True


if __name__ == "__main__":
    test_point_in_polygon()
