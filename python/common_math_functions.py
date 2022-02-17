"""some common functions"""
import numpy


def calculate_rotation_matrix_2d(in_angle):
    """
    returns 2d rotation matrix of the given in_angle
    """
    cos_val = numpy.cos(in_angle)
    sin_val = numpy.sin(in_angle)
    return numpy.array([
        [cos_val, -sin_val],
        [sin_val, cos_val]])


def rotate_2d(in_vec, in_angle):
    """
    rreturns in_vec rotated by in_angle
    """
    assert len(in_vec) == 2
    return calculate_rotation_matrix_2d(in_angle)@in_vec
