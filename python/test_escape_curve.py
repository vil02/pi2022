"""tests for the module escape_curve"""
import itertools
import numpy
import pytest

import escape_curve
import convex_shapes


def _get_example_curves():
    res_list = []
    angle_curve_class_list = [
        escape_curve.LogoCurve, escape_curve.AzimuthCurve]
    for initial_angle, segment_size, curve_class in itertools.product(
            numpy.linspace(0, 2*numpy.pi, 5),
            numpy.linspace(0.1, 5, 5),
            angle_curve_class_list):
        res_list.append(curve_class([initial_angle], segment_size))

    for _ in itertools.product(
            numpy.linspace(-0.3, 0.7, 5), repeat=2):
        res_list.append(escape_curve.PointCurve([numpy.array(_)]))
        res_list.append(escape_curve.ShiftCurve([numpy.array(_)]))
    return res_list


@pytest.mark.parametrize("example_curve", _get_example_curves())
@pytest.mark.parametrize("radius", numpy.linspace(0.2, 5, 5))
def test_with_wheel_and_line(example_curve, radius):
    """
    test the method get_max_len_inside in case of a straing line and a Wheel
    """
    unit_wheel = convex_shapes.Wheel([0, 0], radius)
    assert abs(example_curve.get_max_len_inside(unit_wheel, 20)-radius) < \
        0.00001


def test_calculate_dist_list():
    """test of the function calculate_dist_list"""
    point_list = [
        numpy.array([0, 0]),
        numpy.array([0, 1]),
        numpy.array([1, 1]),
        numpy.array([2, 1]),
        numpy.array([2, 10])]
    dist_list = [0, 1, 2, 3, 12]
    assert escape_curve.calculate_dist_list(point_list) == dist_list
