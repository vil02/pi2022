"""contains a definition of the class Curve"""

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


class Curve(extendable_curve.Curve):
    """
    represents a curve used for the "escape problems"
    """
    def get_max_len_inside(self, in_convex_set, inter_limit=10):
        """
        returns the length of the curve inside in_convex_set
        """
        assert self.point_list[0] in in_convex_set
        cur_ind = 0
        while self[cur_ind] in in_convex_set:
            cur_ind += 1
        return self.segment_size*(cur_ind-1) + \
            find_distance_to_boundary(
                self[cur_ind-1], self[cur_ind], in_convex_set, inter_limit)
