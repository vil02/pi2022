"""contains a definition of the function get_curve_class"""
import curve


def get_curve_class(in_to_point_list_fun):
    """returns a Curve class"""
    class Curve(curve.get_curve_class(in_to_point_list_fun)):
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
