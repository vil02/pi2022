"""tests for the most cost_functions"""
import pytest

import cost_functions as cf
import curve_representations as cr
import convex_shapes


def _get_example_representations():
    angle_data_size = 1
    segment_size = 0.31
    limits = (-1, 1, )
    return [
        cr.LogoRepresentation(angle_data_size, segment_size),
        cr.AzimuthRepresentation(angle_data_size, segment_size),
        cr.LogoRepresentationFix(angle_data_size, segment_size),
        cr.AzimuthRepresentationFix(angle_data_size, segment_size),
        cr.PointCurveRepresentation(2*angle_data_size, *limits),
        cr.ShiftCurveRepresentation(2*angle_data_size, *limits)]


def _get_trivial_data(in_curve_representation):
    return [0]*len(in_curve_representation.bounds)


@pytest.mark.parametrize(
    "example_representation", _get_example_representations())
def test_get_single_shape_cost(example_representation):
    """test of the function get_single_shape_cost"""
    example_shape = convex_shapes.Wheel((0, 0, ), 1)
    cur_cost_fun = cf.get_single_shape_cost(
        example_representation, example_shape, 20)
    cur_data = _get_trivial_data(example_representation)
    assert abs(cur_cost_fun(cur_data)-1) < 0.000001


def _get_example_shape_list():
    return [convex_shapes.Wheel((0, 0, ), 1), convex_shapes.Wheel((0, 0, ), 2)]


@pytest.mark.parametrize(
    "example_representation", _get_example_representations())
def test_get_cost_max(example_representation):
    """test of the function get_cost_max"""
    example_shape_list = _get_example_shape_list()
    cur_cost_fun = cf.get_cost_max(
        example_representation, example_shape_list, 20)
    cur_data = _get_trivial_data(example_representation)
    assert abs(cur_cost_fun(cur_data)-2) < 0.000001


@pytest.mark.parametrize(
    "example_representation", _get_example_representations())
def test_get_cost_sum(example_representation):
    """test of the function get_cost_sum"""
    example_shape_list = _get_example_shape_list()
    cur_cost_fun = cf.get_cost_sum(
        example_representation, example_shape_list, 20)
    cur_data = _get_trivial_data(example_representation)
    assert abs(cur_cost_fun(cur_data)-3) < 0.000001
