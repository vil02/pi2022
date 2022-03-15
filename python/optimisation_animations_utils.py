"""
utilities related to creation of animations illustrating
the optimisation process
"""
import numpy

import matplotlib.pyplot as plt


def _find_last_node_num(curve_data, in_len):
    cur_len = 0
    prev_len = -1
    cur_node_num = 0
    assert in_len > 0
    while cur_len < in_len:
        cur_shift = curve_data[cur_node_num+1]-curve_data[cur_node_num]
        prev_len = cur_len
        last_segment_len = numpy.linalg.norm(cur_shift)
        cur_len += last_segment_len
        cur_node_num += 1
    return cur_node_num-1, prev_len, last_segment_len


def _plot_curve(curve_data, in_length, in_curve_color):
    last_node_num, lower_len, last_segment_len = \
        _find_last_node_num(curve_data, in_length)
    rem_len = in_length-lower_len
    assert 0 <= rem_len < last_segment_len
    if len(curve_data.point_list) > last_node_num:
        plt.plot(
            curve_data.x_list[last_node_num:],
            curve_data.y_list[last_node_num:],
            color='lightgray')
    pos_a = numpy.array(curve_data.point_list[last_node_num])
    pos_b = numpy.array(curve_data.point_list[last_node_num+1])
    pos_c = pos_a+(rem_len/last_segment_len)*(pos_b-pos_a)
    used_x_list = list(curve_data.x_list[0:last_node_num+1]) + \
        [pos_a[0], pos_c[0]]
    used_y_list = list(curve_data.y_list[0:last_node_num+1]) + \
        [pos_a[1], pos_c[1]]
    plt.plot(used_x_list, used_y_list, color=in_curve_color)


def plot_data(
        in_data_representation, in_data, in_evaluate_function, in_curve_color):
    """plots the curve represented by in_data"""
    cur_curve = in_data_representation.to_curve(in_data)
    used_curve_length = in_evaluate_function(cur_curve)
    _plot_curve(cur_curve, used_curve_length, in_curve_color)


def plot_conv_data(in_data, in_evaluate_function, **kwargs):
    """plots the convergence data into current figure"""
    x_data = [_.time for _ in in_data]
    y_data = [in_evaluate_function(_.data) for _ in in_data]
    plt.plot(x_data, y_data, **kwargs)
