"""contains a definition of the function get_curve_class"""

import copy
import numpy.linalg

import extendable_curve


def find_distance_to_boundary(pos_in, pos_out, convex_set, inter_limit):
    """
    returns the distance between the pos_in and the boundary of the cinvex_set
    in direction of pos_out
    """
    assert pos_in in convex_set
    assert pos_out not in convex_set

    def get_mid_point(pos_a, pos_b):
        return (pos_a+pos_b)/2

    def single_iteration(pos_a, pos_b):
        assert pos_a in convex_set
        assert pos_b not in convex_set
        pos_c = get_mid_point(pos_a, pos_b)
        return (pos_a, pos_c) if pos_c not in convex_set else (pos_c, pos_b)
    tmp_a = copy.deepcopy(pos_in)
    tmp_b = copy.deepcopy(pos_out)
    for _ in range(inter_limit):
        tmp_a, tmp_b = single_iteration(tmp_a, tmp_b)
    res_pos = get_mid_point(tmp_a, tmp_b)
    return numpy.linalg.norm(res_pos-pos_in)


def _add_single_segment(dist_list, in_segment_len):
    dist_list.append(dist_list[-1]+in_segment_len)


def calculate_dist_list(in_point_list):
    """
    returns the dist_list for given in_to_point_list
    res[k] is the length of the zig-zag curve from
    in_point_list[0] to in_point_list[k]
    """
    res = [0.0]
    for (cur_num, cur_pos) in enumerate(in_point_list[1:], 1):
        prev_pos = in_point_list[cur_num-1]
        _add_single_segment(res, numpy.linalg.norm(cur_pos-prev_pos))
    return res


def get_curve_class(in_curve_class):
    """returns a Curve class"""
    class Curve(in_curve_class):  # pylint: disable=too-few-public-methods
        """
        represents a curve used for the "escape problems"
        """
        def __init__(self, *args):
            super().__init__(*args)
            self._dist_list = calculate_dist_list(self.point_list)

        def _add_single_point(self):
            super()._add_single_point()
            _add_single_segment(
                self._dist_list,
                numpy.linalg.norm(self.point_list[-1]-self.point_list[-2]))
            assert len(self._dist_list) == len(self._point_list)

        def get_max_len_inside(self, in_convex_set, inter_limit=10):
            """
            returns the length of the curve inside in_convex_set
            """
            assert self.point_list[0] in in_convex_set
            cur_ind = 0
            while self[cur_ind] in in_convex_set:
                cur_ind += 1
            return self._dist_list[cur_ind-1] + \
                find_distance_to_boundary(
                    self[cur_ind-1], self[cur_ind], in_convex_set, inter_limit)
    return Curve


LogoCurve = get_curve_class(extendable_curve.LogoCurve)
AzimuthCurve = get_curve_class(extendable_curve.AzimuthCurve)
PointCurve = get_curve_class(extendable_curve.PointCurve)
ShiftCurve = get_curve_class(extendable_curve.ShiftCurve)
