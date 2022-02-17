"""test of rotations module"""
import numpy
import pytest
import rotations as rts


def test_zero_angle_rotation_is_identity():
    """
    checks if calculate_rotation_matrix_2d(0) is an identy matrix
    """
    assert (rts.calculate_rotation_matrix_2d(0) == numpy.identity(2)).all()


_TEST_SIZE = 7


@pytest.mark.parametrize(
    "cur_angle", numpy.linspace(0, 2*numpy.pi, _TEST_SIZE))
def test_rotation_matrix_has_determinant_1(cur_angle):
    """
    checks if calculate_rotation_matrix_2d()
    returns a matrix with determinant 1
    """
    assert numpy.linalg.det(rts.calculate_rotation_matrix_2d(cur_angle)) == 1


@pytest.mark.parametrize("angle_a", numpy.linspace(0, 2*numpy.pi, _TEST_SIZE))
@pytest.mark.parametrize("angle_b", numpy.linspace(0, 2*numpy.pi, _TEST_SIZE))
def test_composition_of_rotations(angle_a, angle_b):
    """
    rotation by sum of angles is a compositions of rotations
    """
    composition_of_rotations = \
        rts.calculate_rotation_matrix_2d(angle_a) @ \
        rts.calculate_rotation_matrix_2d(angle_b)
    rotation_by_sum = rts.calculate_rotation_matrix_2d(angle_a+angle_b)
    assert numpy.allclose(composition_of_rotations, rotation_by_sum)


@pytest.mark.parametrize(
    "cur_angle", numpy.linspace(0, 2*numpy.pi, _TEST_SIZE))
def test_rotate_by_negative_angle(cur_angle):
    """
    rotation by -angle is a rotation by 2*pi-angle
    """
    assert numpy.allclose(
        rts.calculate_rotation_matrix_2d(-cur_angle),
        rts.calculate_rotation_matrix_2d(2*numpy.pi-cur_angle))


def test_rotation_matrix_90_deg():
    """
    checks the result of calculate_rotation_matrix_2d(90 deg)
    """
    assert numpy.allclose(
        rts.calculate_rotation_matrix_2d(numpy.radians(90)),
        numpy.array([[0, -1], [1, 0]]))


def test_rotate_2d():
    """checks the result of rotate_2d([1, 0], numpy.radians(90))"""
    assert numpy.allclose(rts.rotate_2d([1, 0], numpy.radians(90)), [0, 1])
