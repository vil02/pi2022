"""generates pdf and tex file for the curve representation example"""

import math
import matplotlib.pyplot as plt
import matplotlib
import scipy.interpolate
import numpy

import curve
import output_paths as op
import project_styles as ps


def mark_logo_angles(in_curve):
    """
    marks the logo_angles of the given in_curve
    """
    total_angle = 0
    cur_zorder = 30
    cur_ax = plt.gca()
    for (cur_pos, cur_angle) in zip(in_curve.point_list, in_curve.angle_list):
        tmp_angles = [
            numpy.degrees(total_angle), numpy.degrees(total_angle+cur_angle)]
        cur_angle_marker = matplotlib.patches.Wedge(
            cur_pos, 0.5*in_curve.segment_size,
            theta1=min(tmp_angles), theta2=max(tmp_angles),
            alpha=0.4,
            zorder=cur_zorder)
        dir_line_len = 0.6*in_curve.segment_size
        plt.plot(
            [cur_pos[0], cur_pos[0]+dir_line_len*numpy.cos(total_angle)],
            [cur_pos[1], cur_pos[1]+dir_line_len*numpy.sin(total_angle)],
            color=[0.1, 0.1, 0.1],
            linestyle='--',
            zorder=cur_zorder)
        total_angle += cur_angle
        cur_ax.add_patch(cur_angle_marker)


def mark_azimuth_angles(in_curve):
    """
    marks the azimuth_angles of the given in_curve
    """
    cur_zorder = 30
    cur_ax = plt.gca()
    for (cur_pos, cur_angle) in zip(in_curve.point_list, in_curve.angle_list):
        angle_to_mark = numpy.degrees(cur_angle)
        if angle_to_mark > 180:
            angle_to_mark -= 360
        cur_angle_marker = matplotlib.patches.Wedge(
            cur_pos, 0.5*in_curve.segment_size,
            theta1=min([0, angle_to_mark]), theta2=max([0, angle_to_mark]),
            alpha=0.4,
            zorder=cur_zorder)
        dir_line_len = 0.6*in_curve.segment_size
        plt.plot(
            [cur_pos[0], cur_pos[0]+dir_line_len],
            [cur_pos[1], cur_pos[1]],
            color=[0.1, 0.1, 0.1],
            linestyle='--',
            zorder=cur_zorder)
        cur_ax.add_patch(cur_angle_marker)


def _get_output_paths():
    return op.OutputPaths('curveRepresentationExampleTex')


def get_smooth_data(in_curve):
    """
    returns the smooth curve passing though the nodes of a given logo-curve
    """
    raw_data = numpy.array([in_curve.x_list, in_curve.y_list]).T
    interpolator = scipy.interpolate.interp1d(
        numpy.linspace(0, 1, len(in_curve.y_list)),
        raw_data, axis=0, kind='cubic')
    return interpolator(numpy.linspace(0, 1, 100))


def _plot_smooth_data(in_smooth_data):
    plt.plot(
        in_smooth_data[:, 0], in_smooth_data[:, 1],
        linewidth=3, zorder=20, color='m')


def _init_figure():
    plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def _save_plot_to_pdf(in_num):
    plt.savefig(
        _get_output_paths().get_pdf_file_path(in_num),
        bbox_inches='tight', pad_inches=0.01)


def plot_all(in_angle_deg_list, save_to_pdf=False, lim_data=None):
    """
    Creates the plots explaining the idea of representation the curve.
    Returns the limits of the last plot.
    """
    def call_save_fig(in_num):
        if save_to_pdf:
            _save_plot_to_pdf(in_num)
    _init_figure()
    if lim_data is not None:
        assert save_to_pdf
        plt.gca().set_xlim(lim_data[0])
        plt.gca().set_ylim(lim_data[1])
    else:
        assert not save_to_pdf
    example_curve = curve.get_curve_class(curve.angles_to_points_logo)(
        [math.radians(_) for _ in in_angle_deg_list], 1)
    _plot_smooth_data(get_smooth_data(example_curve))
    call_save_fig(0)

    plt.plot(
        example_curve.x_list, example_curve.y_list, linewidth=3, zorder=40,
        color=ps.LOGO_COLOR)
    plt.plot(
        example_curve.x_list, example_curve.y_list,
        linestyle='None', marker='o',
        zorder=50,
        color=ps.LOGO_COLOR)
    call_save_fig(1)
    mark_logo_angles(example_curve)
    call_save_fig(2)
    xlim_data = plt.xlim()
    ylim_data = plt.ylim()
    plt.close()
    return [xlim_data, ylim_data]


def plot_azimuth(in_angle_deg_list, lim_data):
    """
    plots the azimuth-representation of the example curve
    """
    _init_figure()
    plt.gca().set_xlim(lim_data[0])
    plt.gca().set_ylim(lim_data[1])

    example_curve = curve.get_curve_class(curve.angles_to_points_azimuth)(
        [math.radians(_) for _ in in_angle_deg_list], 1)
    _plot_smooth_data(get_smooth_data(example_curve))

    plt.plot(
        example_curve.x_list, example_curve.y_list, linewidth=3, zorder=40,
        color=ps.AZIMUTH_COLOR)
    plt.plot(
        example_curve.x_list, example_curve.y_list,
        linestyle='None', marker='o',
        zorder=50,
        color=ps.AZIMUTH_COLOR)
    mark_azimuth_angles(example_curve)
    _save_plot_to_pdf(3)
    plt.close()


ANGLE_DEG_LIST = [10, -20, 115, 50, -60, -60, -60, 10, 30, -30, 20, -45, -30]
LIM_DATA = plot_all(ANGLE_DEG_LIST, False)
plot_all(ANGLE_DEG_LIST, True, LIM_DATA)

plot_azimuth(curve.logo_agnles_to_azimuth_angles(ANGLE_DEG_LIST), LIM_DATA)


def _to_on_slide_num(in_num, max_num):
    res = str(in_num)
    if in_num == max_num:
        res += '-'
    return res


TEX_STR = \
    '\\begin{frame}\n' \
    '  \\begin{center}\n' \
    '    \\begin{overprint}\n'

MAX_NUM = 4


for _ in range(MAX_NUM):
    cur_str = \
        f'        \\onslide<{_to_on_slide_num(_+1, MAX_NUM)}>' \
        r'\centerline{\includegraphics[width=0.9\textwidth]{' \
        f'{_get_output_paths().get_short_pdf_path(_)}' \
        '}}\n'
    TEX_STR += cur_str
TEX_STR += \
    '    \\end{overprint}\n' \
    '  \\end{center}\n'


def _angle_list_to_tex_str(in_angle_deg_list):
    return '$$\\left(' + \
        ', '.join(str(_)+'^{\\circ}' for _ in in_angle_deg_list) + \
        '\\right)$$'


TEX_STR += '  \\begin{overprint}\n'
TEX_STR += '    \\onslide<3>\n    ' + \
    _angle_list_to_tex_str(ANGLE_DEG_LIST)+'\n'
TEX_STR += '   \\onslide<4>\n    ' + \
    _angle_list_to_tex_str(
        curve.logo_agnles_to_azimuth_angles(ANGLE_DEG_LIST))+'\n'
TEX_STR += '  \\end{overprint}\n'

TEX_STR += '\\end{frame}\n'

TEX_FILE_PATH = _get_output_paths().get_tex_file_path()
with open(
        TEX_FILE_PATH, 'w', encoding='utf-8') as tex_file:
    tex_file.write(TEX_STR)
