"""contains the definition of the Curve class"""

import copy
import numpy


class Curve:
    """
    represents a "logo-curve"
    """
    def __init__(self, in_angle_list, in_segment_size):
        cur_pos = numpy.array([0.0, 0.0])
        cur_angle = 0
        self._angle_list = copy.deepcopy(in_angle_list)
        self._point_list = [copy.deepcopy(cur_pos)]
        self._segment_size = in_segment_size
        for _ in in_angle_list:
            cur_angle += _
            cur_pos += in_segment_size*numpy.array(
                [numpy.cos(cur_angle), numpy.sin(cur_angle)])
            self._point_list.append(copy.deepcopy(cur_pos))

    @property
    def point_list(self):
        """returns potins of the curve in order"""
        return self._point_list

    @property
    def x_list(self):
        """returns the x-coordinates of point_list"""
        return tuple(_[0] for _ in self.point_list)

    @property
    def y_list(self):
        """returns the y-coordinates of point_list"""
        return tuple(_[1] for _ in self.point_list)

    @property
    def angle_list(self):
        return self._angle_list

    @property
    def segment_size(self):
        return self._segment_size
