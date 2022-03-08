"""contains a definition of the function get_curve_class"""
import curve


def get_curve_class(in_curve_class):
    """returns a Curve class"""
    class Curve(in_curve_class):  # pylint: disable=too-few-public-methods
        """
        represent a curve which can be extended
        in the direction of the last segment
        """
        def __getitem__(self, in_ind):
            while in_ind >= len(self.point_list):
                self._add_single_point()
            return self.point_list[in_ind]

        def _add_single_point(self):
            last_diff = self.point_list[-1]-self.point_list[-2]
            self._point_list.append(self.point_list[-1]+last_diff)
    return Curve


LogoCurve = get_curve_class(curve.LogoCurve)
AzimuthCurve = get_curve_class(curve.AzimuthCurve)
PointCurve = get_curve_class(curve.PointCurve)
