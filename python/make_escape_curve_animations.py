import collections
import scipy.optimize
import numpy
import matplotlib.pyplot as plt
import time

import output_paths as op
import curve
import escape_curve
import plotable_convex_shapes
import project_styles as ps


def get_optimizer(in_angles_to_points_fun):
    """returns an Optimizer class"""
    class Optimizer():
        """generates the optimisition data for given scheme"""

        @classmethod
        def to_curve(cls, in_data):
            curve_type = escape_curve.get_curve_class(in_angles_to_points_fun)
            return curve_type(in_data, cls.max_curve_len/len(in_data))

        @classmethod
        def evaluate_data(cls, in_data):
            return cls.evaluate_curve(cls.to_curve(in_data))

        @classmethod
        def generate_data(cls):
            RowType = collections.namedtuple(
                'RowType', ['data', 'function_value', 'time'])
            res_data = []
            start_time = time.time()

            def callback_fun(in_data, in_fun_val, context):
                nonlocal res_data
                res_data.append(
                    RowType(in_data, in_fun_val, time.time()-start_time))

            scipy.optimize.dual_annealing(
                lambda x: cls.evaluate_data(x),
                cls.bounds,
                maxiter=cls.maxiter,
                callback=callback_fun)
            return res_data
    return Optimizer


def _init_figure():
    plt.figure(figsize=(3.2, 3.2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def get_example_with_single_shape(in_angles_to_points_fun):
    class ExampleWithSingleShape(get_optimizer(in_angles_to_points_fun)):
        maxiter = 1000
        data_size = 30
        max_curve_len = 2
        segment_size = max_curve_len/data_size
        bounds = [
            (numpy.radians(-180), numpy.radians(180)) for _ in range(data_size)]

        @classmethod
        def evaluate_curve(cls, curve):
            return curve.get_max_len_inside(cls.shape)

        @classmethod
        def plot_state(cls, in_data, curve_color):
            cur_curve = cls.to_curve(in_data)
            _init_figure()
            cls.shape.plot(facecolor='lightgreen', edgecolor='green')
            plt.plot(cur_curve.x_list, cur_curve.y_list, color=curve_color)
            cls._set_limits()
    return ExampleWithSingleShape


def get_unit_ball_example(in_angles_to_points_fun):
    class UnitBallExample(get_example_with_single_shape(
            in_angles_to_points_fun)):
        shape = plotable_convex_shapes.Wheel([0, 0], 1)

        @classmethod
        def _set_limits(_):
            plot_size = 1.05
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])
    return UnitBallExample


def get_unit_ball_fixed_direction_example(in_angles_to_points_fun):
    class UnitBallFixedDirectionExample(
            get_unit_ball_example(in_angles_to_points_fun)):
        @classmethod
        def to_curve(cls, in_data):
            angle_list = numpy.insert(in_data, 0, 0, axis=0)
            return super().to_curve(angle_list)
    return UnitBallFixedDirectionExample


def get_rectangle_example(in_angles_to_points_fun):
    class RectangleExample(
            get_example_with_single_shape(in_angles_to_points_fun)):
        shape = plotable_convex_shapes.Rectangle([0, 0], 2, 1.8)

        @classmethod
        def _set_limits(_):
            plot_size = 1.3
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])
    return RectangleExample


def generate_animation_data(
        optimiser, core_name, tex_propety_name, curve_color):
    cur_paths = op.OutputPaths(core_name, tex_propety_name)
    optimisation_data = optimiser.generate_data()
    for (frame_number, cur_data) in enumerate(optimisation_data):
        optimiser.plot_state(cur_data.data, curve_color)
        plt.savefig(
            cur_paths.get_pdf_file_path(frame_number),
            bbox_inches='tight', pad_inches=0.01)
        plt.close()
    short_path = str(cur_paths.get_short_pdf_path(-1))
    assert short_path.endswith('_-1.pdf')
    short_path = short_path[0:-6]
    tex_str = '\\animategraphics[autoplay]{20}{' + \
              short_path+'}' + \
              '{0}'+f'{{{len(optimisation_data)-1}}}'
    with open(
            cur_paths.get_tex_file_path(), 'w', encoding='utf-8') as tex_file:
        tex_file.write(tex_str)
    return optimisation_data


def create_comparison_conv_plot(in_logo_data, in_azimuth_data, in_paths):
    def plot_data(in_data, in_color, in_label):
        plt.plot(
            [_.time for _ in in_data],
            [_.function_value for _ in in_data],
            color=in_color, label=in_label)
    plt.figure(figsize=(5, 2.0))
    plot_data(in_logo_data, ps.LOGO_COLOR, 'LOGO')
    plot_data(in_azimuth_data, ps.AZIMUTH_COLOR, 'azymut')
    plt.legend(loc="upper right")
    plt.xlabel('[s]')
    plt.savefig(
        in_paths.get_pdf_file_path(0),
        bbox_inches='tight', pad_inches=0.01)
    plt.close()
    tex_str = \
        f'\\includegraphics[width=\\textwidth]{{{in_paths.get_short_pdf_path(0)}}}\n'
    with open(
            in_paths.get_tex_file_path(), 'w', encoding='utf-8') as tex_file:
        tex_file.write(tex_str)


def make_single_shape_plots(
        in_example_fun,
        logo_core_name, logo_tex_name,
        azimuth_core_name, azimuth_tex_name,
        conv_plot_core_name, conv_plot_tex_name):
    logo_data = generate_animation_data(
        in_example_fun(curve.angles_to_points_logo),
        logo_core_name, logo_tex_name,
        ps.LOGO_COLOR)

    azimuth_data = generate_animation_data(
        in_example_fun(curve.angles_to_points_azimuth),
        azimuth_core_name, azimuth_tex_name,
        ps.AZIMUTH_COLOR)

    create_comparison_conv_plot(
        logo_data, azimuth_data,
        op.OutputPaths(conv_plot_core_name, conv_plot_tex_name))


make_single_shape_plots(
    get_unit_ball_example,
    'esape_from_unit_circle_logo_example', 'escapeFromCircleLogoTex',
    'esape_from_unit_circle_azimuth_example', 'escapeFromCircleAzimuthTex',
    'escape_from_unit_circle_conv_plot', 'escapeFromCircleConvPlotTex')

make_single_shape_plots(
    get_unit_ball_fixed_direction_example,
    'esape_from_unit_circle_logo_fixed_example',
    'escapeFromCircleLogoFixedTex',
    'esape_from_unit_circle_azimuth_fixed_example',
    'escapeFromCircleAzimuthFixedTex',
    'escape_from_unit_circle_conv_fixed_plot',
    'escapeFromCircleConvPlotFixedTex')

make_single_shape_plots(
    get_rectangle_example,
    'esape_from_rectangle_logo_example', 'escapeFromRectangleLogoTex',
    'esape_from_rectangle_azimuth_example', 'escapeFromRectangleAzimuthTex',
    'escape_from_rectangle_conv_plot', 'escapeFromRectangleConvPlotTex')
