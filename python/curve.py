"""
contains the definition of the functions returing classes representing curves
starting at the point (0, 0)
"""

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


def logo_agnles_to_azimuth_angles(in_logo_angles):
    """
    returns the list of azimuth angles based on in_logo_angles
    """
    res = []
    cur_angle = 0
    for _ in in_logo_angles:
        cur_angle += _
        res.append(cur_angle)
    return res


class _AbstractCurve:
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


def get_angle_curve_class(in_to_point_list_fun):
    """returns an AngleCurve class"""
    class AngleCurve(_AbstractCurve):
        """
        represents a curve
        """
        def __init__(self, in_angle_list, in_segment_size):
            self._angle_list = copy.deepcopy(in_angle_list)
            self._point_list = in_to_point_list_fun(
                self._angle_list, in_segment_size)

    return AngleCurve


class PointCurve(_AbstractCurve):
    """represetns a zig-zag-curvestarting at the point (0, 0)"""
    def __init__(self, in_point_list):
        self._point_list = [(0, 0)]+in_point_list
