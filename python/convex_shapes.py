"""
defines classes representing convex shapes in 2d
"""
import numpy


def norm_sq(in_vec):
    """returns the square of the Euclidean norm of in_vec"""
    return numpy.dot(in_vec, in_vec)


class Wheel:
    """represents a Wheel"""
    def __init__(self, in_center, in_radius):
        self._radius_sq = in_radius**2
        self.center = in_center

    def __contains__(self, in_pos):
        return norm_sq(in_pos-self.center) <= self._radius_sq


class Rectangle:
    """represents a rectangle"""
    def __init__(self, in_center, in_width, in_height):
        self.center = in_center
        self.width = in_width
        self.height = in_height

    def __contains__(self, in_pos):
        tmp_pos = in_pos-self.center
        return abs(tmp_pos[0]) <= self.width/2 and \
            abs(tmp_pos[1]) <= self.height/2
