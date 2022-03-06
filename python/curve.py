"""contains the definition of the function get_curve_class"""

import copy
import numpy


def angles_to_points_logo(
        in_angle_list, in_segment_size, in_start_pos=numpy.array([0.0, 0.0])):
    """
    returns the list of points as in "logo-curve"
    """
    cur_angle = 0
    point_list = [copy.deepcopy(in_start_pos)]
    cur_pos = copy.deepcopy(in_start_pos)
    for _ in in_angle_list:
        cur_angle += _
        cur_pos += in_segment_size*numpy.array(
            [numpy.cos(cur_angle), numpy.sin(cur_angle)])
        point_list.append(copy.deepcopy(cur_pos))
    return point_list


def angles_to_points_azimuth(
        in_angle_list, in_segment_size, in_start_pos=numpy.array([0.0, 0.0])):
    """
    returns the list of points as in "azimuth-curve"
    """
    point_list = [copy.deepcopy(in_start_pos)]
    cur_pos = copy.deepcopy(in_start_pos)
    for cur_angle in in_angle_list:
        cur_pos += in_segment_size*numpy.array(
            [numpy.cos(cur_angle), numpy.sin(cur_angle)])
        point_list.append(copy.deepcopy(cur_pos))
    return point_list


def get_curve_class(in_to_point_list_fun):
    """returns a Curve class"""
    class Curve:
        """
        represents a curve
        """
        def __init__(self, in_angle_list, in_segment_size):
            self._angle_list = copy.deepcopy(in_angle_list)
            self._segment_size = in_segment_size
            self._point_list = in_to_point_list_fun(
                self._angle_list, self._segment_size)

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
            """returns the angle_list"""
            return self._angle_list

        @property
        def segment_size(self):
            """returns the segment_size"""
            return self._segment_size
    return Curve
