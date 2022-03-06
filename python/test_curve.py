"""contains tests for the curve module"""

import pytest
import numpy

import curve


@pytest.fixture(name='example_square_logo_curve')
def fixture_example_square_logo_curve():
    """
    returns a logo-Curve object representing a "counterclockwise unit square"
    """
    angle_deg_list = [0, 90, 90, 90]
    yield curve.get_curve_class(curve.angles_to_points_logo)(
        [numpy.radians(_) for _ in angle_deg_list], 1)


@pytest.fixture(name='example_square_azimuth_curve')
def fixture_example_square_azimuth_curve():
    """
    returns a azimuth-Curve object representing a
    "counterclockwise unit square"
    """
    angle_deg_list = [0, 90, 180, 270]
    yield curve.get_curve_class(curve.angles_to_points_azimuth)(
        [numpy.radians(_) for _ in angle_deg_list], 1)


@pytest.mark.parametrize(
    'example_square_curve_str',
    ['example_square_azimuth_curve',
     'example_square_logo_curve'])
def test_x_list(example_square_curve_str, request):
    """test of the x_list"""
    example_square_curve = request.getfixturevalue(example_square_curve_str)
    assert numpy.allclose(example_square_curve.x_list, [0, 1, 1, 0, 0])


@pytest.mark.parametrize(
    'example_square_curve_str',
    ['example_square_azimuth_curve',
     'example_square_logo_curve'])
def test_y_list(example_square_curve_str, request):
    """test of the y_list"""
    example_square_curve = request.getfixturevalue(example_square_curve_str)
    assert numpy.allclose(example_square_curve.y_list, [0, 0, 1, 1, 0])


@pytest.mark.parametrize(
    'in_logo_angles',
    [numpy.random.rand(20) for _ in range(5)])
def test_logo_agnles_to_azimuth_angles(in_logo_angles):
    """test of the function logo_angles_to_azimuth_angles"""
    segment_size = 3.2
    logo_curve = curve.get_curve_class(curve.angles_to_points_logo)(
        in_logo_angles, segment_size)
    azimuth_curve = curve.get_curve_class(curve.angles_to_points_azimuth)(
        curve.logo_agnles_to_azimuth_angles(in_logo_angles), segment_size)
    for _ in zip(logo_curve.point_list, azimuth_curve.point_list):
        numpy.allclose(*_)
