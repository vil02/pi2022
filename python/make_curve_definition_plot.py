"""generates pdf and tex file for the curve representation example"""

import math
import matplotlib.pyplot as plt
import matplotlib
import scipy.interpolate
import numpy

import curve
import project_config as pc


def mark_angles(in_curve):
    """
    marks the angles of the given in_curve
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


def get_pdf_file_path(in_num):
    """
    returns the path of the ouput file for the given number
    """
    pdf_dir = pc.get_config_parameter(
        'tmpDataFolder')/'curve_representation_example'
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return pdf_dir/f'curve_representation_example_{in_num}.pdf'


def get_smooth_data(in_curve):
    """
    returns the smooth curve passing though the nodes of a given logo-curve
    """
    raw_data = numpy.array([in_curve.x_list, in_curve.y_list]).T
    interpolator = scipy.interpolate.interp1d(
        numpy.linspace(0, 1, len(in_curve.y_list)),
        raw_data, axis=0, kind='cubic')
    return interpolator(numpy.linspace(0, 1, 100))


def plot_all(in_angle_deg_list, save_to_pdf=False, lim_data=None):
    """
    Creates the plots explaining the idea of representation the curve.
    Returns the limits of the last plot.
    """
    def call_save_fig(in_num):
        if save_to_pdf:
            plt.savefig(
                get_pdf_file_path(in_num),
                bbox_inches='tight', pad_inches=0.01)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    if lim_data is not None:
        assert save_to_pdf
        plt.gca().set_xlim(lim_data[0])
        plt.gca().set_ylim(lim_data[1])
    else:
        assert not save_to_pdf
    example_curve = curve.Curve(
        [math.radians(_) for _ in in_angle_deg_list], 1)
    smooth_data = get_smooth_data(example_curve)
    plt.plot(smooth_data[:, 0], smooth_data[:, 1], linewidth=3, zorder=20)
    call_save_fig(0)

    plt.plot(
        example_curve.x_list, example_curve.y_list, linewidth=3, zorder=40)
    plt.plot(
        example_curve.x_list, example_curve.y_list,
        linestyle='None', marker='o',
        zorder=50)
    call_save_fig(1)
    mark_angles(example_curve)
    call_save_fig(2)
    xlim_data = plt.xlim()
    ylim_data = plt.ylim()
    plt.close()
    return [xlim_data, ylim_data]


ANGLE_DEG_LIST = [15, 50, -60, -60, -60, 10, 30]
LIM_DATA = plot_all(ANGLE_DEG_LIST, False)
plot_all(ANGLE_DEG_LIST, True, LIM_DATA)
