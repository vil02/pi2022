"""contains definitions of the cost functions"""


def get_single_shape_cost(in_data_representation, in_shape, in_iter_limit):
    """returns the function evaluating given data agains single shape"""
    def evaluate_data(in_data):
        cur_curve = in_data_representation.to_curve(in_data)
        return cur_curve.get_max_len_inside(in_shape, in_iter_limit)
    return evaluate_data


def get_cost_max(in_data_representation, in_shape_list, in_iter_limit):
    """returns the function max-evaluating given data agains list of shapes"""
    def evaluate_data(in_data):
        cur_curve = in_data_representation.to_curve(in_data)
        return max(
            cur_curve.get_max_len_inside(_, in_iter_limit)
            for _ in in_shape_list)
    return evaluate_data


def get_cost_sum(in_data_representation, in_shape_list, in_iter_limit):
    """returns the function sum-evaluating given data agains list of shapes"""
    def evaluate_data(in_data):
        cur_curve = in_data_representation.to_curve(in_data)
        return sum(
            cur_curve.get_max_len_inside(_, in_iter_limit)
            for _ in in_shape_list)
    return evaluate_data
