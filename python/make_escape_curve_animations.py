"""
creates all TeX data for the escape curve optimisation animations
"""

import collections
import itertools
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
import rotations


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
    if len(in_opt_data_dict) > 0:
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


def make_multiple_shape_plots(
        in_shape_list,
        in_data_representation_dict,
        in_conv_plot_tex_name,
        in_plot_limits):
    """
    generates all TeX data for the animations and convergence plot
    for multiple shape problems
    """

    opt_data_dict = {}
    for (cur_tex_name, cur_representation) in \
            in_data_representation_dict.items():
        opt_data_dict[cur_tex_name] = \
            odg.generate_multiple_shape_optimisation_data(
                cur_representation, in_shape_list, 3,
                {'maxiter': 100},
                {'maxiter': 40})

    for (cur_tex_name, cur_opt_res) in opt_data_dict.items():
        cur_data_representation = in_data_representation_dict[cur_tex_name]
        cur_evaluate_fun = ev.get_multiple_shape_evaluator(
            cur_data_representation, in_shape_list, 10).evaluate_curve_max
        _create_optimisation_animation(
            cur_tex_name, cur_opt_res,
            cur_data_representation,
            lambda: None,
            cur_evaluate_fun,
            plot_limits=in_plot_limits)

    evaluate_data_fun_dict = {}
    for (cur_tex_name, cur_representation) in \
            in_data_representation_dict.items():
        evaluate_data_fun_dict[cur_tex_name] = ev.get_multiple_shape_evaluator(
            cur_representation, in_shape_list, 10).evaluate_data_max
    _create_conv_comparison_plot(
        opt_data_dict, evaluate_data_fun_dict, in_conv_plot_tex_name)


def _get_initial_data_for_second_step(
        in_first_step_representation, in_first_step_res):
    first_step_sol = in_first_step_representation.to_curve(
        in_first_step_res[-1].data)
    raw_first_step_opt = list(itertools.chain(*first_step_sol.point_list[1:]))
    pos_limit_min = 1.05*min(_ for _ in raw_first_step_opt)
    pos_limit_max = 1.05*max(_ for _ in raw_first_step_opt)

    second_step_representation = cr.PointCurveRepresentation(
        len(raw_first_step_opt), pos_limit_min, pos_limit_max)
    return raw_first_step_opt, second_step_representation


def two_step_scheme(
        in_shape_list,
        in_first_step_representation,
        in_first_step_tex_name, in_second_step_tex_name,
        in_conv_plot_tex_name, **kwargs):
    """runs the two-step-scheme"""

    def shift_second_step_time(in_first_step_res, in_second_step_res):
        res = []
        first_step_end_time = in_first_step_res[-1].time
        for _ in in_second_step_res:
            res.append(odg.RowType(
                _.data, _.time+first_step_end_time))
        return res

    opt_res_dict = {}
    opt_res_dict[in_first_step_tex_name] = \
        odg.generate_multiple_shape_optimisation_data(
            in_first_step_representation, in_shape_list, 3,
            {'maxiter': 230},
            {'maxiter': 40})

    raw_first_step_opt, second_step_representation = \
        _get_initial_data_for_second_step(
            in_first_step_representation, opt_res_dict[in_first_step_tex_name])

    opt_res_dict[in_second_step_tex_name] = \
        odg.generate_multiple_shape_optimisation_data(
            second_step_representation, in_shape_list, 3,
            {'maxiter': 60, 'x0': raw_first_step_opt, 'initial_temp': 10},
            {'maxiter': 20, 'initial_temp': 10})
    opt_res_dict[in_second_step_tex_name] = shift_second_step_time(
        opt_res_dict[in_first_step_tex_name],
        opt_res_dict[in_second_step_tex_name])

    curve_eval_fun_dict = {
        in_first_step_tex_name:
            ev.get_multiple_shape_evaluator(
                in_first_step_representation, in_shape_list,
                10).evaluate_curve_max,
        in_second_step_tex_name:
            ev.get_multiple_shape_evaluator(
                second_step_representation, in_shape_list,
                10).evaluate_curve_max}

    data_rep_dict = {
        in_first_step_tex_name: in_first_step_representation,
        in_second_step_tex_name: second_step_representation}

    for (cur_tex_name, cur_opt_res) in opt_res_dict.items():
        _create_optimisation_animation(
            cur_tex_name, cur_opt_res,
            data_rep_dict[cur_tex_name],
            lambda: None,
            curve_eval_fun_dict[cur_tex_name],
            **kwargs)

    _create_conv_comparison_plot(
        opt_res_dict,
        {
            in_first_step_tex_name:
                ev.get_multiple_shape_evaluator(
                    in_first_step_representation, in_shape_list,
                    10).evaluate_data_max,
            in_second_step_tex_name:
                ev.get_multiple_shape_evaluator(
                    second_step_representation, in_shape_list,
                    10).evaluate_data_max,
        },
        in_conv_plot_tex_name)


class _Rectangle:
    def __init__(self, in_xy_data):
        self._xy_data = in_xy_data
        self._patch_data = plt.Polygon(self._xy_data)

    def __contains__(self, in_pos):
        return self._patch_data.contains_point(in_pos)

    def plot(self, **kwargs):
        """plots the represented rectangle"""
        plt.gca().add_patch(plt.Polygon(self._xy_data, **kwargs))


def _get_data_for_strip(in_shift_num, in_rotation_num):
    x_rad = 4
    initial_xy_data = numpy.array(
        [[-x_rad, 0.5], [x_rad, 0.5], [x_rad, -0.5], [-x_rad, -0.5]])
    res_list = []
    all_angles = numpy.linspace(
        0, numpy.radians(180), in_rotation_num, endpoint=False)
    for y_shift in numpy.linspace(-0.4995, 0.4995, in_shift_num):
        cur_shift = numpy.array([0, y_shift])
        for cur_rot in all_angles:
            cur_xy = [
                rotations.rotate_2d(_, cur_rot)+cur_shift
                for _ in initial_xy_data]
            cur_shape = _Rectangle(cur_xy)
            assert numpy.array([0, 0]) in cur_shape
            res_list.append(cur_shape)
    return res_list


def _get_data_for_halfplane(in_rotation_num):
    margin_size = 20
    x_shift = -0.995
    initial_xy_data = numpy.array(
        [[-margin_size, margin_size], [margin_size, margin_size],
         [margin_size, x_shift], [-margin_size, x_shift]])
    res_list = []
    for cur_rot in numpy.linspace(
            0, 2*numpy.pi, in_rotation_num, endpoint=False):
        cur_xy = [rotations.rotate_2d(_, cur_rot) for _ in initial_xy_data]
        cur_shape = _Rectangle(cur_xy)
        assert numpy.array([0, 0]) in cur_shape
        res_list.append(cur_shape)
    return res_list


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

make_multiple_shape_plots(
    _get_data_for_strip(30, 15),
    {'escapeFromStripAzimuthTex': cr.AzimuthRepresentation(20, 2.5)},
    'escapeFromStripConvPlotTex',
    _get_simple_limits(1.7))

two_step_scheme(
    _get_data_for_halfplane(30),
    cr.AzimuthRepresentation(20, 7),
    'escapeFromHalfplaneAzimuthTex',
    'escapeFromHalfplanePointTex',
    'escapeFromHalfplaneConvPlotTex',
    plot_limits=_get_simple_limits(2.25))
