"""contains definitions of the plotable convex shapes"""
import numpy
import matplotlib.pyplot as plt

import convex_shapes


class Wheel(convex_shapes.Wheel):
    def __init__(self, in_center, in_radius):
        super().__init__(in_center, in_radius)
        self._radius = in_radius
        assert self._radius_sq**2 == self._radius

    def plot(self, **kwargs):
        plt.gca().add_patch(
            plt.Circle(self.center, self.radius, **kwargs))

    @property
    def radius(self):
        return self._radius


class Rectangle(convex_shapes.Rectangle):
    def plot(self, **kwargs):
        corner = self.center-numpy.array([self.width, self.height])/2
        plt.gca().add_patch(
            plt.Rectangle(corner, self.width, self.height, **kwargs))
