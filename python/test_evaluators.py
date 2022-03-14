"""tests for the most cost_functions"""
import pytest

import evaluators as ev
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
def test_evaluate_data_in_single_shape(example_representation):
    """test of the method evaluate_data"""
    cur_evaluator = ev.get_single_shape_evaluator(
        example_representation, convex_shapes.Wheel((0, 0, ), 1), 20)
    cur_data = _get_trivial_data(example_representation)
    assert abs(cur_evaluator.evaluate_data(cur_data)-1) < 0.000001


def _get_example_shape_list():
    return [convex_shapes.Wheel((0, 0, ), 1), convex_shapes.Wheel((0, 0, ), 2)]


@pytest.mark.parametrize(
    "example_representation", _get_example_representations())
def test_evaluate_data_max_in_multiple_shape(example_representation):
    """test of the method evaluate_data"""
    cur_evaluator = ev.get_multiple_shape_evaluator(
        example_representation, _get_example_shape_list(), 20)
    cur_data = _get_trivial_data(example_representation)
    assert abs(cur_evaluator.evaluate_data_max(cur_data)-2) < 0.000001


@pytest.mark.parametrize(
    "example_representation", _get_example_representations())
def test_evaluate_data_sum_in_multiple_shape(example_representation):
    """test of the method evaluate_data"""
    cur_evaluator = ev.get_multiple_shape_evaluator(
        example_representation, _get_example_shape_list(), 20)
    cur_data = _get_trivial_data(example_representation)
    assert abs(cur_evaluator.evaluate_data_sum(cur_data)-3) < 0.000001
