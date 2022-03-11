"""
contains utilities to cast list of numbers into a curve
"""
import numpy
import escape_curve


class PointCurveRepresentation:
    """allows to cast list of numbers into PointCurve"""
    def __init__(self, in_data_size, min_val, max_val):
        assert in_data_size % 2 == 0
        self._data_size = in_data_size
        self._bounds = [(min_val, max_val) for _ in range(in_data_size)]

    @property
    def bounds(self):
        """returns the bounds"""
        return self._bounds

    def to_curve(self, in_data):
        """returns a PointCurve object for given data"""
        assert len(in_data) == self._data_size
        point_list = [
            numpy.array(in_data[_:_+2]) for _ in range(0, self._data_size, 2)]
        return escape_curve.PointCurve(point_list)


class ShiftCurveRepresentation:
    """allows to cast list of numbers into ShiftCurve"""
    def __init__(self, in_data_size, min_val, max_val):
        assert in_data_size % 2 == 0
        self._data_size = in_data_size
        self._bounds = [(min_val, max_val) for _ in range(in_data_size)]

    @property
    def bounds(self):
        """returns the bounds"""
        return self._bounds

    def to_curve(self, in_data):
        """returns a ShiftCurve object for given data"""
        assert len(in_data) == self._data_size
        shift_list = [
            numpy.array(in_data[_:_+2]) for _ in range(0, self._data_size, 2)]
        return escape_curve.ShiftCurve(shift_list)


def get_angle_curve_data_representation(in_curve_class):
    """returns a class allowing to cast a list of points into an AngleCurve"""
    class AngleCurveRepresentation:
        """allows to cast list of numbers into an AngleCurve"""
        def __init__(self, data_size, max_curve_len):
            self._data_size = data_size
            self._segment_size = max_curve_len/data_size
            single_bound = (numpy.radians(-180), numpy.radians(180))
            self._bounds = [single_bound for _ in range(data_size)]

        @property
        def bounds(self):
            """returns the bounds"""
            return self._bounds

        def to_curve(self, in_angle_data):
            """returns an AngleCurve object for given data"""
            assert len(in_angle_data) == self._data_size
            return in_curve_class(in_angle_data, self._segment_size)

    return AngleCurveRepresentation


def get_angle_curve_fixed_data_representation(in_curve_class):
    """
    returns a class allowing to cast a list of points into an AngleCurve
    with first angle set to 0
    """
    class AngleCurveFixedRepresentation:
        """
        allows to cast list of numbers into an AngleCurve
        with first angle set to 0
        """
        def __init__(self, data_size, max_curve_len):
            self._data_size = data_size
            self._segment_size = max_curve_len/(data_size+1)
            single_bound = (numpy.radians(-180), numpy.radians(180))
            self._bounds = [single_bound for _ in range(data_size)]

        @property
        def bounds(self):
            """returns the bounds"""
            return self._bounds

        def to_curve(self, in_angle_data):
            """returns an AngleCurve object for given data"""
            assert len(in_angle_data) == self._data_size
            angle_list = numpy.insert(in_angle_data, 0, 0, axis=0)
            return in_curve_class(angle_list, self._segment_size)

    return AngleCurveFixedRepresentation


LogoRepresentation = \
    get_angle_curve_data_representation(escape_curve.LogoCurve)
AzimuthRepresentation = \
    get_angle_curve_data_representation(escape_curve.AzimuthCurve)

LogoRepresentationFix = \
    get_angle_curve_fixed_data_representation(escape_curve.LogoCurve)
AzimuthRepresentationFix = \
    get_angle_curve_fixed_data_representation(escape_curve.AzimuthCurve)
