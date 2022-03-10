"""contains definitions of the plotable convex shapes"""
import numpy
import matplotlib.pyplot as plt

import convex_shapes


class Wheel(convex_shapes.Wheel):
    """represents a plotable Wheel/2d-ball"""
    def __init__(self, in_center, in_radius):
        super().__init__(in_center, in_radius)
        self._radius = in_radius
        assert self._radius_sq**2 == self._radius

    def plot(self, **kwargs):
        """"plots the represented shape"""
        plt.gca().add_patch(
            plt.Circle(self.center, self.radius, **kwargs))

    @property
    def radius(self):
        """returns radius"""
        return self._radius


class Rectangle(convex_shapes.Rectangle):
    # pylint: disable=too-few-public-methods
    """represents a plotable horizontal rectanlge"""
    def plot(self, **kwargs):
        """"plots the represented shape"""
        corner = self.center-numpy.array([self.width, self.height])/2
        plt.gca().add_patch(
            plt.Rectangle(corner, self.width, self.height, **kwargs))
