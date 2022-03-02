"""tests for the module convex_shapes"""

import collections
import numpy
import pytest
import convex_shapes as cs

Example = collections.namedtuple("Example", ["shape", "point"])


@pytest.mark.parametrize(
    "in_data",
    [
        Example(cs.Wheel([0, 0], 1), numpy.array([0, 0])),
        Example(cs.Wheel([0, 0], 1), numpy.array([0.5, 0.5])),
        Example(cs.Wheel([0, 0], 1), numpy.array([1, 0])),
        Example(cs.Wheel([0, 0], 1), numpy.array([0, 1])),
        Example(cs.Wheel([4, 3], 1), numpy.array([4, 3])),
        Example(cs.Rectangle([0, 0], 2, 4), numpy.array([1, 2])),
        Example(cs.Rectangle([1, 1], 2, 4), numpy.array([2, 3])),
    ],
)
def test_contains(in_data):
    """positive test for the method __contains__"""
    assert in_data.point in in_data.shape


@pytest.mark.parametrize(
    "in_data",
    [
        Example(cs.Wheel([0, 0], 1), numpy.array([1.1, 0])),
        Example(cs.Wheel([0, 0], 1), numpy.array([0, -1.1])),
        Example(cs.Rectangle([0, 0], 2, 4), numpy.array([1.1, 0])),
        Example(cs.Rectangle([0, 0], 2, 4), numpy.array([0, 2.1])),
        Example(cs.Rectangle([1, 1], 2, 4), numpy.array([2, 3.1])),
    ],
)
def test_does_not_contain(in_data):
    """negative test for the method __contains__"""
    assert in_data.point not in in_data.shape
