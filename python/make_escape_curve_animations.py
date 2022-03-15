"""
creates all TeX data for the escape curve optimisation animations
"""

import collections
import matplotlib.pyplot as plt
import numpy

import curve_representations as cr
import optimisation_data_generators as odg
import optimisation_animations_utils as oau
import project_styles as ps
import tex_string_utils as tsu
import evaluators as ev
import output_paths as op
import plotable_convex_shapes as pcs


def _apply_dict(in_tex_name, in_dict):
    res = None
    for (cur_key, cur_val) in in_dict.items():
        if cur_key in in_tex_name:
            for _ in in_dict.keys():
                if cur_key != _:
                    assert _ not in in_tex_name
            res = cur_val
            break
    assert res is not None
    return res


def get_curve_color(in_tex_name):
    """returns the curve color based on in_tex_name"""
    res_dict = {
        'Logo': ps.LOGO_COLOR,
        'Azimuth': ps.AZIMUTH_COLOR,
        'Point': ps.POINT_COLOR,
        'Shift': ps.SHIFT_COLOR}

    return _apply_dict(in_tex_name, res_dict)


def get_curve_name(in_tex_name):
    """returns the curve representation name based on in_tex_name"""
    res_dict = {
        'Logo': 'LOGO',
        'Azimuth': 'azymut',
        'Point': 'naiwny',
        'Shift': 'SHIFT'}

    return _apply_dict(in_tex_name, res_dict)


def _init_figure():
    plt.figure(figsize=(3.2, 3.2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def _call_save_fig(in_output_paths, in_plot_num):
    plt.savefig(
        in_output_paths.get_pdf_file_path(in_plot_num),
        bbox_inches='tight', pad_inches=0.01)


def _create_optimisation_animation(
        in_tex_name, in_opt_data, in_data_representation,
        in_draw_backgroud_fun, in_evaluate_fun,
        **kwargs):
    output_paths = op.OutputPaths(in_tex_name)
    for (cur_frame_num, cur_data_row) in enumerate(in_opt_data):
        _init_figure()
        in_draw_backgroud_fun()
        oau.plot_data(
            in_data_representation,
            cur_data_row.data,
            in_evaluate_fun,
            get_curve_color(in_tex_name))
        if kwargs.get('plot_limits', None) is not None:
            plt.gca().set_xlim(kwargs.get('plot_limits', None).xlim)
            plt.gca().set_ylim(kwargs.get('plot_limits', None).ylim)
        _call_save_fig(output_paths, cur_frame_num)
        plt.close()
    tsu.save_animategraphics_str(
        output_paths, 20, 'autoplay', 0, len(in_opt_data)-1)


def _save_tex_str_conv_plot(in_paths):
    tex_str = tsu.includegraphics_str(in_paths, 0, 1)
    tsu.save_to_tex_file(tex_str, in_paths)


def _create_conv_comparison_plot(
        in_opt_data_dict,
        get_evaluate_data_dict, in_conv_plot_tex_name):
    plt.figure(figsize=(5, 1.8))
    for (cur_tex_name, cur_opt_data) in in_opt_data_dict.items():
        cur_evaluate_fun = get_evaluate_data_dict[cur_tex_name]
        oau.plot_conv_data(
            cur_opt_data, cur_evaluate_fun,
            color=get_curve_color(cur_tex_name),
            label=get_curve_name(cur_tex_name))
    output_paths = op.OutputPaths(in_conv_plot_tex_name)
    plt.legend(loc="upper right")
    plt.xlabel('[s]')
    y_limits = plt.gca().get_ylim()
    plt.gca().set_ylim([y_limits[0], 2*y_limits[0]])
    _call_save_fig(output_paths, 0)
    plt.close()
    _save_tex_str_conv_plot(output_paths)


def make_single_shape_plots(
        in_shape,
        in_data_representation_dict,
        in_conv_plot_tex_name,
        in_plot_limits):
    """
    generates all TeX data for the animations and convergence plot
    for single shape problems
    """

    opt_data_dict = {}
    for (cur_tex_name, cur_representation) in \
            in_data_representation_dict.items():
        opt_data_dict[cur_tex_name] = \
            odg.generate_single_shape_optimisation_data(
                cur_representation, in_shape, 5)

    for (cur_tex_name, cur_opt_res) in opt_data_dict.items():
        cur_data_representation = in_data_representation_dict[cur_tex_name]
        cur_evaluate_fun = ev.get_single_shape_evaluator(
            cur_data_representation, in_shape, 10).evaluate_curve
        _create_optimisation_animation(
            cur_tex_name, cur_opt_res,
            cur_data_representation,
            lambda: in_shape.plot(**ps.CONVEX_COLORS),
            cur_evaluate_fun,
            plot_limits=in_plot_limits)

    evaluate_data_fun_dict = {}
    for (cur_tex_name, cur_representation) in \
            in_data_representation_dict.items():
        evaluate_data_fun_dict[cur_tex_name] = ev.get_single_shape_evaluator(
            cur_representation, in_shape, 10).evaluate_data
    _create_conv_comparison_plot(
        opt_data_dict, evaluate_data_fun_dict, in_conv_plot_tex_name)


PlotLimits = collections.namedtuple('PlotLimits', ['xlim', 'ylim'])


def _get_simple_limits(in_r):
    single_ax_lim = [-in_r, in_r]
    return PlotLimits(single_ax_lim, single_ax_lim)


CURVE_REP_PARAMS = (30, 2,)

make_single_shape_plots(
        pcs.Wheel(numpy.array([0.0, 0.0]), 1.0),
        {
            'escapeFromCircleLogoTex':
                cr.LogoRepresentation(*CURVE_REP_PARAMS),
            'escapeFromCircleAzimuthTex':
                cr.AzimuthRepresentation(*CURVE_REP_PARAMS),
        },
        'escapeFromCircleConvPlotTex',
        _get_simple_limits(1.15))

make_single_shape_plots(
        pcs.Wheel(numpy.array([0.0, 0.0]), 1.0),
        {
            'escapeFromCircleLogoFixedTex':
                cr.LogoRepresentationFix(*CURVE_REP_PARAMS),
            'escapeFromCircleAzimuthFixedTex':
                cr.AzimuthRepresentationFix(*CURVE_REP_PARAMS),
        },
        'escapeFromCircleConvPlotFixedTex',
        _get_simple_limits(1.15))

make_single_shape_plots(
        pcs.Rectangle(numpy.array([0, 0]), 2.0, 1.8),
        {
            'escapeFromRectangleLogoTex':
                cr.LogoRepresentation(*CURVE_REP_PARAMS),
            'escapeFromRectangleAzimuthTex':
                cr.AzimuthRepresentation(*CURVE_REP_PARAMS),
        },
        'escapeFromRectangleConvPlotTex',
        _get_simple_limits(1.3))
