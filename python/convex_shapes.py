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
        self._center = in_center

    def __contains__(self, in_pos):
        return norm_sq(in_pos-self.center) <= self._radius_sq

    @property
    def center(self):
        """returns the center of the circle"""
        return self._center
