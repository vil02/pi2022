"""
generates the TeX data for the illustrating the differences
between LOGO and azimuth curve
"""
import copy
import math
import itertools
import numpy
import matplotlib.pyplot as plt

import curve
import output_paths as op
import project_styles as ps

_PERTURBED_IND = 3


def _to_curve(in_curve_class, in_angle_list):
    return in_curve_class(in_angle_list, 1)


def _plot_angle_list(in_curve_class, angle_list):
    color_dict = {
        curve.LogoCurve: ps.LOGO_COLOR,
        curve.AzimuthCurve: ps.AZIMUTH_COLOR}
    cur_curve = _to_curve(in_curve_class, angle_list)
    plt.plot(
        cur_curve.x_list, cur_curve.y_list,
        color=color_dict[in_curve_class], linewidth=4)
    plt.plot(
        cur_curve.x_list[_PERTURBED_IND], cur_curve.y_list[_PERTURBED_IND],
        marker='o', color='red', markersize=10)


def _perturbe_angle_list(in_angle_list, in_perturbation):
    res = copy.deepcopy(in_angle_list)
    res[_PERTURBED_IND] += in_perturbation
    return res


def _find_limits(in_curve_class_list, angle_list, perturbation_list):
    def update_limits(cur_limits, val_list):
        cur_limits[0] = min(cur_limits[0], min(val_list))
        cur_limits[1] = max(cur_limits[1], max(val_list))

    def add_margin(cur_limits):
        margin_size = 0.3
        cur_limits[0] -= margin_size
        cur_limits[1] += margin_size
    x_limits = [math.inf, -math.inf]
    y_limits = [math.inf, -math.inf]
    for (cur_curve_class, cur_perturbation) in itertools.product(
            in_curve_class_list, perturbation_list):
        cur_curve = _to_curve(
            cur_curve_class,
            _perturbe_angle_list(
                _transform_angles(cur_curve_class, angle_list),
                cur_perturbation))
        update_limits(x_limits, cur_curve.x_list)
        update_limits(y_limits, cur_curve.y_list)
    add_margin(x_limits)
    add_margin(y_limits)
    return x_limits, y_limits


def _transform_angles(in_curve_class, in_angle_list):
    proc_angles_dict = {
        curve.LogoCurve: lambda x: x,
        curve.AzimuthCurve: curve.logo_agnles_to_azimuth_angles}
    return proc_angles_dict[in_curve_class](in_angle_list)


def _make_animation_data(
        in_curve_class, angle_list, perturbation_list, limits, in_tex_name):

    def init_figure():
        plt.figure()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')

    def save_plot_to_pdf(in_num, in_output_paths):
        plt.savefig(
            in_output_paths.get_pdf_file_path(in_num),
            bbox_inches='tight', pad_inches=0.01)
    output_paths = op.OutputPaths(in_tex_name)
    true_angle_list = _transform_angles(in_curve_class, angle_list)
    frame_params = list(perturbation_list)
    frame_params = frame_params+(frame_params[1:-1])[::-1]
    for (frame_num, cur_perturbation) in enumerate(frame_params):
        init_figure()
        _plot_angle_list(
            in_curve_class,
            _perturbe_angle_list(true_angle_list, cur_perturbation))
        plt.gca().set_xlim(limits[0])
        plt.gca().set_ylim(limits[1])
        save_plot_to_pdf(frame_num, output_paths)
        plt.close()
    short_path = str(output_paths.get_short_pdf_path(-1))
    assert short_path.endswith('_-1.pdf')
    short_path = short_path[0:-6]

    tex_str = '\\animategraphics[autoplay,loop,width=\\textwidth]{15}{' + \
              short_path+'}' + \
              '{0}'+f'{{{len(frame_params)-1}}}'
    with open(
            output_paths.get_tex_file_path(), 'w', encoding='utf-8') as t_file:
        t_file.write(tex_str)


LOGO_ANGLE_LIST = [numpy.radians(_) for _ in [15, 20, -30, 40, 50, 40, -60]]
PERTURBATION_LIST = numpy.linspace(-1, 1, 30)

CURVE_CLASS_DICT = {
    'curveComparisonLogoTex': curve.LogoCurve,
    'curveComparisonAzimuthTex': curve.AzimuthCurve}
LIMITS = _find_limits(
    CURVE_CLASS_DICT.values(), LOGO_ANGLE_LIST, PERTURBATION_LIST)

for (tex_name, curve_class) in CURVE_CLASS_DICT.items():
    _make_animation_data(
        curve_class, LOGO_ANGLE_LIST, PERTURBATION_LIST, LIMITS, tex_name)
