"""tests for the module escape_curve"""
import numpy
import pytest

import escape_curve
import convex_shapes


@pytest.mark.parametrize('initial_angle', numpy.linspace(0, 2*numpy.pi, 5))
@pytest.mark.parametrize('radius', numpy.linspace(0.2, 5, 5))
@pytest.mark.parametrize('segment_size', numpy.linspace(0.1, 5, 5))
def test_with_wheel_and_line(initial_angle, radius, segment_size):
    """
    test the method get_max_len_inside in case of a straing line and a Wheel
    """
    unit_wheel = convex_shapes.Wheel([0, 0], radius)
    cur_curve = escape_curve.Curve([initial_angle], segment_size)
    assert abs(cur_curve.get_max_len_inside(unit_wheel, 20)-radius) < 0.00001
