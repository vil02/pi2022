"""contains tests for the curve module"""

import pytest
import numpy

import curve


@pytest.fixture(name='example_square_curve')
def fixture_example_square_curve():
    """
    returns a Curve object representing a "counterclockwise unit square"
    """
    angle_deg_list = [0, 90, 90, 90]
    yield curve.Curve(
        [numpy.radians(_) for _ in angle_deg_list], 1)


def test_x_list(example_square_curve):
    """test of the x_list"""
    assert numpy.allclose(example_square_curve.x_list, [0, 1, 1, 0, 0])


def test_y_list(example_square_curve):
    """test of the y_list"""
    assert numpy.allclose(example_square_curve.y_list, [0, 0, 1, 1, 0])
