"""creates data for the measuring the length of a curve inside convex set"""

import copy
import matplotlib.patches
import matplotlib.pyplot as plt
import numpy
import scipy.interpolate

import output_paths as op
import curve


def _get_output_paths_convex():
    return op.OutputPaths(
        'length_inside_examples', 'lengthInsideExampleTex')


def _get_output_paths_nonconvex():
    return op.OutputPaths(
        'length_inside_nonconvex_example', 'lengthInsideExampleNonconvexTex')


def _get_raw_shape():
    raw_data = [
        [-2, 0], [-1.5, 1], [0, 1.3], [1, 0.7],
        [-0.6, 0.3], [0.3, -0.2], [1, -0.6],
        [0.14, -0.9], [-1.2, -1.0], [-2, 0]]
    interpolator = scipy.interpolate.interp1d(
        numpy.linspace(0, 1, len(raw_data)),
        numpy.array(raw_data), axis=0, kind='cubic')
    return 2*(interpolator(numpy.linspace(0, 1, 75))+numpy.array([1.5, 0]))


def _get_raw_convex_shape():
    points = _get_raw_shape()
    convex_hull = scipy.spatial.ConvexHull(points)
    return points[convex_hull.vertices]


def plot_shape(xy_data, **kwargs):
    """plots given polygon"""
    plt.gca().add_patch(matplotlib.patches.Polygon(xy_data, **kwargs))


def _init_figure():
    plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def _set_limits():
    plt.gca().set_xlim([-1.1, 5.1])
    plt.gca().set_ylim([-2.2, 3.95])


def find_last_inside(in_set, in_curve):
    res = None
    for (cur_num, cur_pos) in enumerate(in_curve.point_list):
        if in_set.contains_point(cur_pos):
            res = cur_num
        else:
            break
    return res


def _call_save_fig(in_num, output_path_obj):
    plt.savefig(
        output_path_obj.get_pdf_file_path(in_num),
        bbox_inches='tight', pad_inches=0.01)


def _get_example_curve():
    return curve.Curve(
        [numpy.radians(_) for _ in [-60, 70, 30, 40, -10, 5, -5, 10]], 1)


def _get_example_curve_plot_params():
    return {'marker': 'o', 'color': [0.3, 0.3, 0.3], 'linestyle': ':'}


def _draw_frame(in_frame_num):
    example_curve = _get_example_curve()
    example_patch = matplotlib.patches.Polygon(_get_raw_convex_shape())
    assert example_patch.contains_point(example_curve.point_list[0])
    assert not example_patch.contains_point(example_curve.point_list[-1])

    _init_figure()
    plot_shape(
        _get_raw_convex_shape(), facecolor='lightgreen', edgecolor='green')
    plt.plot(
        example_curve.x_list,
        example_curve.y_list,
        **_get_example_curve_plot_params())
    last_inside = find_last_inside(example_patch, example_curve)

    logo_curve_inside_style = {
        'marker': 'o', 'color': 'orange', 'linestyle': '-', 'linewidth': 1.5}

    def plot_curve_inside(in_limit):
        plt.plot(
            example_curve.x_list[0:in_limit],
            example_curve.y_list[0:in_limit],
            **logo_curve_inside_style)

    def plot_bisection(in_pos_inside, in_pos_outside, in_step_limit):
        pos_inside = copy.deepcopy(in_pos_inside)
        pos_outside = copy.deepcopy(in_pos_outside)
        for _ in range(in_step_limit):
            mid_pos = (pos_inside+pos_outside)/2
            if example_patch.contains_point(mid_pos):
                pos_inside = mid_pos
            else:
                pos_outside = mid_pos
        plt.plot(
            [in_pos_inside[0], pos_inside[0]],
            [in_pos_inside[1], pos_inside[1]],
            **logo_curve_inside_style)
        plt.plot(
            [pos_outside[0], pos_inside[0]],
            [pos_outside[1], pos_inside[1]],
            marker='.', color='red', markersize=8, linestyle='none')

    if 0 < in_frame_num <= last_inside+1:
        plot_curve_inside(in_frame_num)
    elif in_frame_num > last_inside+1:
        plot_curve_inside(last_inside+1)
        plot_bisection(
            example_curve.point_list[last_inside],
            example_curve.point_list[last_inside+1],
            in_frame_num-last_inside-2)

    _set_limits()
    _call_save_fig(in_frame_num, _get_output_paths_convex())
    plt.close()


NUMBER_OF_FRAMES = 15
for _ in range(NUMBER_OF_FRAMES):
    _draw_frame(_)

TEX_STR_CONVEX = \
    '\\begin{frame}\n' \
    '  \\begin{center}\n' \
    '    \\begin{overprint}\n'
for _ in range(NUMBER_OF_FRAMES):
    cur_str = \
        f'        \\onslide<{_+1}>' \
        r'\centerline{\includegraphics[width=0.5\textwidth]{' \
        f'{_get_output_paths_convex().get_short_pdf_path(_)}' \
        '}}\n'
    TEX_STR_CONVEX += cur_str
TEX_STR_CONVEX += \
    '    \\end{overprint}\n' \
    '  \\end{center}\n'

TEX_STR_CONVEX += '\\end{frame}\n'

with open(
        _get_output_paths_convex().get_tex_file_path(),
        'w', encoding='utf-8') as tex_file:
    tex_file.write(TEX_STR_CONVEX)

_init_figure()
plot_shape(
    _get_raw_shape(), facecolor='salmon', edgecolor='red')
plt.plot(
    _get_example_curve().x_list,
    _get_example_curve().y_list,
    **_get_example_curve_plot_params())

_set_limits()
_call_save_fig(0, _get_output_paths_nonconvex())

TEX_STR_NONCONVEX = \
    '\\begin{frame}\n' \
    '  \\begin{center}\n' \
    r'    \includegraphics[width=0.5\textwidth]{' \
    f'{_get_output_paths_nonconvex().get_short_pdf_path(0)}' \
    '}\n' \
    '  \\end{center}\n' \
    '\\end{frame}\n'

with open(
        _get_output_paths_nonconvex().get_tex_file_path(),
        'w', encoding='utf-8') as tex_file:
    tex_file.write(TEX_STR_NONCONVEX)
