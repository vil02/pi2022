"""prepares all TeX data for the examples of convex and non-convex sets"""

import matplotlib.patches
import matplotlib.pyplot as plt
import numpy
import scipy.interpolate

import output_paths as op
import project_styles as ps
import tex_string_utils as tsu


def _get_raw_convex_shape_a():
    res_list = []
    res_list.append([-1, 1])
    for _ in numpy.linspace(numpy.radians(90), numpy.radians(-90), 50):
        res_list.append([numpy.cos(_), numpy.sin(_)])
    res_list.append([-1, -1])
    return numpy.array(res_list)+numpy.array([2, -1.5])


def _get_raw_convex_shape_b():
    return numpy.array(
        [[-2.1, 0], [0, 1], [2.1, 0], [0, -1]])+numpy.array([-2, 2])


def _get_raw_nonconvex_shape_a():
    raw_data = [
        [-2, 0], [-1.5, 1], [0, 1.3], [1, 0.7],
        [-0.6, 0.3], [0.3, -0.2], [1, -1], [0.14, -1.6], [-1.2, -1.7], [-2, 0]]
    interpolator = scipy.interpolate.interp1d(
        numpy.linspace(0, 1, len(raw_data)),
        numpy.array(raw_data), axis=0, kind='cubic')
    return interpolator(numpy.linspace(0, 1, 75))+numpy.array([-2, -1.2])


def _get_raw_nonconvex_shape_b():
    return numpy.array(
        [[-1.5, 0], [0, 1.5], [0, 0], [1.5, 0], [0, -1.5]])+numpy.array([2, 2])


def plot_shape(xy_data, **kwargs):
    """plots given polygon"""
    plt.gca().add_patch(matplotlib.patches.Polygon(xy_data, **kwargs))


def _init_figure():
    plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def _set_limits():
    plt.gca().set_xlim([-4.5, 3.5])
    plt.gca().set_ylim([-4, 4])


def _get_output_paths():
    return op.OutputPaths('convexExamplesTex')


def _call_save_fig(in_num):
    plt.savefig(
        _get_output_paths().get_pdf_file_path(in_num),
        bbox_inches='tight', pad_inches=0.01)


def _mark_segment(in_beg, in_end):
    plt.plot(
        [in_beg[0], in_end[0]], [in_beg[1], in_end[1]],
        linestyle='-',
        marker='o',
        color='black',
        linewidth=2)


CONVEX_SHAPES = [_get_raw_convex_shape_a(), _get_raw_convex_shape_b()]
NONCONVEX_SHAPES = [_get_raw_nonconvex_shape_a(), _get_raw_nonconvex_shape_b()]

_init_figure()
for _ in CONVEX_SHAPES+NONCONVEX_SHAPES:
    plot_shape(_, edgecolor='black', facecolor=[0.5, 0.5, 0.5])
_set_limits()
_call_save_fig(0)
plt.close()

_init_figure()
for _ in CONVEX_SHAPES:
    plot_shape(_, **ps.CONVEX_COLORS)


for _ in NONCONVEX_SHAPES:
    plot_shape(_, facecolor='salmon', edgecolor='red')

_mark_segment([1.65, 2.7], [3, 1.8])
_mark_segment([-1.58, -0.36], [-2.30, -1.75])

_set_limits()
_call_save_fig(1)
plt.close()


tsu.save_simple_overprint_frame(_get_output_paths(), 2, 0.5)
