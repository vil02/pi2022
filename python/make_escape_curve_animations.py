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
import rotations


def get_optimizer(in_angles_to_points_fun):
    """returns an Optimizer class"""
    class Optimizer():
        """generates the optimisition data for given scheme"""
        @classmethod
        def _check_data(cls):
            print(cls.max_curve_len, cls.data_size, cls.segment_size)
            assert cls.max_curve_len/cls.data_size == cls.segment_size
            assert len(cls.bounds) == cls.data_size

        @classmethod
        def to_curve(cls, in_data):
            curve_type = escape_curve.get_curve_class(in_angles_to_points_fun)
            return curve_type(in_data, cls.max_curve_len/len(in_data))

        @classmethod
        def evaluate_data(cls, in_data):
            return cls.evaluate_curve(cls.to_curve(in_data))

        @classmethod
        def generate_data(cls):
            cls._check_data()
            RowType = collections.namedtuple(
                'RowType', ['data', 'function_value', 'time'])
            res_data = []
            start_time = time.time()

            def callback_fun(in_data, in_fun_val, context):
                nonlocal res_data
                res_data.append(
                    RowType(in_data, in_fun_val, time.time()-start_time))

            opt_res = scipy.optimize.dual_annealing(
                lambda x: cls.evaluate_data(x),
                cls.bounds,
                maxiter=cls.maxiter,
                callback=callback_fun)
            res_data.append(
                RowType(opt_res.x, opt_res.fun, time.time()-start_time))
            return res_data

        @classmethod
        def plot_curve(cls, curve_data, in_length, in_curve_color):
            last_segment_num = int(in_length/curve_data.segment_size)
            rem_len = in_length-last_segment_num*curve_data.segment_size
            assert 0 <= rem_len < curve_data.segment_size
            if len(curve_data.point_list) > last_segment_num:
                plt.plot(
                    curve_data.x_list[last_segment_num:],
                    curve_data.y_list[last_segment_num:],
                    color='lightgray')
            pos_a = numpy.array(curve_data.point_list[last_segment_num])
            pos_b = numpy.array(curve_data.point_list[last_segment_num+1])
            pos_c = pos_a+(rem_len/curve_data.segment_size)*(pos_b-pos_a)
            used_x_list = list(curve_data.x_list[0:last_segment_num+1]) + \
                [pos_a[0], pos_c[0]]
            used_y_list = list(curve_data.y_list[0:last_segment_num+1]) + \
                [pos_a[1], pos_c[1]]
            plt.plot(used_x_list, used_y_list, color=in_curve_color)
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
            cls.plot_curve(
                cur_curve, cls.evaluate_curve(cur_curve), curve_color)
            cls._set_limits()
    return ExampleWithSingleShape


def get_unit_ball_example(in_angles_to_points_fun):
    class UnitBallExample(get_example_with_single_shape(
            in_angles_to_points_fun)):
        shape = plotable_convex_shapes.Wheel([0, 0], 1)

        @classmethod
        def _set_limits(_):
            plot_size = 1.15
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


def get_example_with_multiple_shapes(in_angles_to_points_fun):
    class ExampleWithMultipleShapes(get_optimizer(in_angles_to_points_fun)):
        maxiter = 40
        data_size = 50
        max_curve_len = 3
        segment_size = max_curve_len/data_size
        bounds = [
            (numpy.radians(-180), numpy.radians(180)) for _ in range(data_size)]

        @classmethod
        def evaluate_curve_max(cls, curve, in_iter_limit):
            return max(curve.get_max_len_inside(_, in_iter_limit) for _ in cls.shapes)

        @classmethod
        def evaluate_curve_sum(cls, curve, in_iter_limit):
            return sum(curve.get_max_len_inside(_, in_iter_limit) for _ in cls.shapes)

        @classmethod
        def evaluate_data_max(cls, in_data, in_iter_limit=3):
            return cls.evaluate_curve_max(cls.to_curve(in_data), in_iter_limit)

        @classmethod
        def evaluate_data_sum(cls, in_data, in_iter_limit=3):
            return cls.evaluate_curve_sum(cls.to_curve(in_data), in_iter_limit)

        @classmethod
        def generate_data(cls):
            cls._check_data()
            RowType = collections.namedtuple(
                'RowType', ['data', 'function_value', 'time'])
            res_data = []
            start_time = time.time()

            def callback_fun(in_data, in_fun_val, context):
                nonlocal res_data
                y_val = cls.evaluate_data_max(in_data)
                print(y_val, cls.evaluate_data_max(in_data, 5), cls.evaluate_data_max(in_data, 10))
                res_data.append(RowType(
                    in_data,
                    y_val,
                    time.time()-start_time))

            res_sum = scipy.optimize.dual_annealing(
                lambda x: cls.evaluate_data_sum(x),
                cls.bounds,
                maxiter=cls.maxiter,
                callback=callback_fun)
            res_data.append(RowType(
                res_sum.x, cls.evaluate_data_max(res_sum.x),
                time.time()-start_time))
            res_max = scipy.optimize.dual_annealing(
                lambda x: cls.evaluate_data_max(x),
                cls.bounds,
                maxiter=40,
                callback=callback_fun,
                x0=res_sum.x)
            res_data.append(RowType(
                res_max.x, cls.evaluate_data_max(res_max.x),
                time.time()-start_time))
            return res_data

        @classmethod
        def plot_state(cls, in_data, curve_color):
            cur_curve = cls.to_curve(in_data)
            _init_figure()
            #cls.shape.plot(facecolor='lightgreen', edgecolor='green')
            cls.plot_curve(
                cur_curve, cls.evaluate_curve_max(cur_curve, 10), curve_color)
            cls._set_limits()
    return ExampleWithMultipleShapes


class Rectangle:
    def __init__(self, in_xy_data):
        self._xy_data = in_xy_data
        self._patch_data = plt.Polygon(self._xy_data)

    def __contains__(self, in_pos):
        return self._patch_data.contains_point(in_pos)

    def plot(self, **kwargs):
        plt.gca().add_patch(plt.Polygon(self._xy_data, **kwargs))


def _get_data_for_strip(in_shift_num, in_rotation_num):
    x_rad = 4
    initial_xy_data = numpy.array(
        [[-x_rad, 0.5], [x_rad, 0.5], [x_rad, -0.5], [-x_rad, -0.5]])
    res_list = []
    for y_shift in numpy.linspace(-0.4995, 0.4995, in_shift_num):
        cur_shift = numpy.array([0, y_shift])
        for cur_rot in numpy.linspace(numpy.radians(0), numpy.radians(360), in_rotation_num, endpoint=False):
            cur_xy = [rotations.rotate_2d(_, cur_rot)+cur_shift for _ in initial_xy_data]
            cur_shape = Rectangle(cur_xy)
            assert numpy.array([0, 0]) in cur_shape
            res_list.append(cur_shape)
    print(len(res_list))
    return res_list


def _get_data_for_halfplane(in_rotation_num):
    margin_size = 20
    x_shift = -0.9
    initial_xy_data = numpy.array(
        [[-margin_size, margin_size], [margin_size, margin_size],
         [margin_size, x_shift], [-margin_size, x_shift]])
    res_list = []
    for cur_rot in numpy.linspace(numpy.radians(0), numpy.radians(360), in_rotation_num, endpoint=False):
        cur_xy = [rotations.rotate_2d(_, cur_rot) for _ in initial_xy_data]
        cur_shape = Rectangle(cur_xy)
        assert numpy.array([0, 0]) in cur_shape
        res_list.append(cur_shape)
    print(len(res_list))
    return res_list


def get_strip_example(in_angles_to_points_fun):
    class StripExample(
            get_example_with_multiple_shapes(in_angles_to_points_fun)):
        shapes = _get_data_for_strip(60, 50)

        @classmethod
        def _set_limits(_):
            plot_size = 1.7
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])
    return StripExample


def get_halfplane_example(in_angles_to_points_fun):
    class HalfplaneExample(
            get_example_with_multiple_shapes(in_angles_to_points_fun)):
        shapes = _get_data_for_halfplane(70)
        maxiter = 250
        data_size = 80
        max_curve_len = 9
        segment_size = max_curve_len/data_size
        bounds = [
            (numpy.radians(-180), numpy.radians(180)) for _ in range(data_size)]

        @classmethod
        def _set_limits(_):
            plot_size = 3.1
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])

    return HalfplaneExample


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

    with open(
            cur_paths.get_general_file_path('_raw_res.txt'),
            'w', encoding='utf-8') as res_file:
        res_file.write(f'{optimisation_data}')
    return optimisation_data


def _init_conv_plot():
    plt.figure(figsize=(5, 1.8))


def _plot_conv_data(in_data, in_color, in_label):
    plt.plot(
        [_.time for _ in in_data],
        [_.function_value for _ in in_data],
        color=in_color, label=in_label)


def _save_tex_str_conv_plot(in_paths):
    tex_str = \
        f'\\includegraphics[width=\\textwidth]{{{in_paths.get_short_pdf_path(0)}}}\n'
    with open(
            in_paths.get_tex_file_path(), 'w', encoding='utf-8') as tex_file:
        tex_file.write(tex_str)


def create_comparison_conv_plot(in_logo_data, in_azimuth_data, in_paths):
    _init_conv_plot()
    _plot_conv_data(in_logo_data, ps.LOGO_COLOR, 'LOGO')
    _plot_conv_data(in_azimuth_data, ps.AZIMUTH_COLOR, 'azymut')
    plt.legend(loc="upper right")
    plt.xlabel('[s]')
    plt.savefig(
        in_paths.get_pdf_file_path(0),
        bbox_inches='tight', pad_inches=0.01)
    plt.close()
    _save_tex_str_conv_plot(in_paths)


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


def make_multiple_shapes_plots(
        in_example_class, core_name, tex_name,
        conv_plot_name, conv_plot_tex_name):
    opt_data = generate_animation_data(
            in_example_class,
            core_name, tex_name, ps.AZIMUTH_COLOR)

    conv_paths = op.OutputPaths(conv_plot_name, conv_plot_tex_name)
    _init_conv_plot()
    _plot_conv_data(opt_data, ps.AZIMUTH_COLOR, 'azumut')
    plt.xlabel('[s]')
    y_limits = plt.gca().get_ylim()
    plt.gca().set_ylim([y_limits[0], 8])
    plt.savefig(
        conv_paths.get_pdf_file_path(0),
        bbox_inches='tight', pad_inches=0.01)
    plt.close()
    _save_tex_str_conv_plot(conv_paths)


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

generate_animation_data(
        get_strip_example(curve.angles_to_points_azimuth),
        'escape_from_strip', 'escapeFromStripTex', ps.AZIMUTH_COLOR)

make_multiple_shapes_plots(
        get_strip_example(curve.angles_to_points_azimuth),
        'escape_from_strip', 'escapeFromStripTex',
        'escape_from_strip_conv_plot', 'escapeFromStripConvPlotTex')

make_multiple_shapes_plots(
        get_halfplane_example(curve.angles_to_points_azimuth),
        'escape_from_halfplane', 'escapeFromHalfplaneTex',
        'escape_from_halfplane_conv_plot', 'escapeFromHalfplaneConvPlotTex')
