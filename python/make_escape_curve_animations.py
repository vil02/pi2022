import collections
import scipy.optimize
import numpy
import matplotlib.pyplot as plt
import time

import output_paths as op
import escape_curve
import plotable_convex_shapes
import project_styles as ps
import rotations
import tex_string_utils as tsu


class PointCurveDataRepresentation:
    def __init__(self, in_data_size, min_val, max_val):
        assert in_data_size % 2 == 0
        self._data_size = in_data_size
        self._bounds = [(min_val, max_val) for _ in range(in_data_size)]

    @property
    def bounds(self):
        return self._bounds

    def to_curve(self, in_data):
        assert len(in_data) == self._data_size
        point_list = [
            numpy.array(in_data[_:_+2]) for _ in range(0, self._data_size, 2)]
        return escape_curve.PointCurve(point_list)


class ShiftCurveDataRepresentation:
    def __init__(self, in_data_size, min_val, max_val):
        assert in_data_size % 2 == 0
        self._data_size = in_data_size
        self._bounds = [(min_val, max_val) for _ in range(in_data_size)]

    @property
    def bounds(self):
        return self._bounds

    def to_curve(self, in_data):
        assert len(in_data) == self._data_size
        shift_list = [
            numpy.array(in_data[_:_+2]) for _ in range(0, self._data_size, 2)]
        return escape_curve.ShiftCurve(shift_list)


def get_angle_curve_data_representation(in_curve_class):
    class AngleCurveDataRepresentation:
        def __init__(self, data_size, max_curve_len):
            self._segment_size = max_curve_len/data_size
            single_bound = (numpy.radians(-180), numpy.radians(180))
            self._bounds = [single_bound for _ in range(data_size)]

        @property
        def bounds(self):
            return self._bounds

        def to_curve(self, in_angle_data):
            return in_curve_class(in_angle_data, self._segment_size)

    return AngleCurveDataRepresentation


def get_angle_curve_fixed_data_representation(in_curve_class):
    class AngleCurveFixedDataRepresentation:
        def __init__(self, data_size, max_curve_len):
            self._segment_size = max_curve_len/(data_size+1)
            single_bound = (numpy.radians(-180), numpy.radians(180))
            self._bounds = [single_bound for _ in range(data_size)]

        @property
        def bounds(self):
            return self._bounds

        def to_curve(self, in_angle_data):
            angle_list = numpy.insert(in_angle_data, 0, 0, axis=0)
            return in_curve_class(angle_list, self._segment_size)

    return AngleCurveFixedDataRepresentation


def find_last_node_num(curve_data, in_len):
    cur_len = 0
    prev_len = -1
    cur_node_num = 0
    assert 0 < in_len
    while cur_len < in_len:
        cur_shift = curve_data[cur_node_num+1]-curve_data[cur_node_num]
        prev_len = cur_len
        last_segment_len = numpy.linalg.norm(cur_shift)
        cur_len += last_segment_len
        cur_node_num += 1
    return cur_node_num-1, prev_len, last_segment_len


def get_optimizer(data_representation):
    """returns an Optimizer class"""
    class Optimizer():
        """generates the optimisition data for given scheme"""

        @classmethod
        def evaluate_data(cls, in_data):
            return cls.evaluate_curve(data_representation.to_curve(in_data))

        @classmethod
        def generate_data(cls, x0):
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
                data_representation.bounds,
                maxiter=cls.maxiter,
                callback=callback_fun,
                x0=x0)
            res_data.append(
                RowType(opt_res.x, opt_res.fun, time.time()-start_time))
            return res_data

        @classmethod
        def plot_curve(cls, curve_data, in_length, in_curve_color):
            last_node_num, lower_len, last_segment_len = \
                find_last_node_num(curve_data, in_length)
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
    return Optimizer


def _init_figure():
    plt.figure(figsize=(3.2, 3.2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def get_example_with_single_shape(data_representation):
    class ExampleWithSingleShape(get_optimizer(data_representation)):
        maxiter = 1000

        @classmethod
        def evaluate_curve(cls, curve_data):
            return curve_data.get_max_len_inside(cls.shape)

        @classmethod
        def plot_state(cls, in_data, curve_color):
            cur_curve = data_representation.to_curve(in_data)
            _init_figure()
            cls.shape.plot(facecolor='lightgreen', edgecolor='green')
            cls.plot_curve(
                cur_curve, cls.evaluate_curve(cur_curve), curve_color)
            cls._set_limits()
    return ExampleWithSingleShape


def get_unit_ball_example(data_representation):
    class UnitBallExample(get_example_with_single_shape(data_representation)):
        shape = plotable_convex_shapes.Wheel([0, 0], 1)

        @classmethod
        def _set_limits(_):
            plot_size = 1.15
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])
    return UnitBallExample


def get_rectangle_example(data_representation):
    class RectangleExample(get_example_with_single_shape(data_representation)):
        shape = plotable_convex_shapes.Rectangle([0, 0], 2, 1.8)

        @classmethod
        def _set_limits(_):
            plot_size = 1.3
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])
    return RectangleExample


def get_example_with_multiple_shapes(data_representation):
    class ExampleWithMultipleShapes(get_optimizer(data_representation)):
        maxiter = 100#400

        @classmethod
        def evaluate_curve_max(cls, curve, in_iter_limit):
            return max(curve.get_max_len_inside(_, in_iter_limit) for _ in cls.shapes)

        @classmethod
        def evaluate_curve_sum(cls, curve, in_iter_limit):
            return sum(curve.get_max_len_inside(_, in_iter_limit) for _ in cls.shapes)

        @classmethod
        def evaluate_data_max(cls, in_data, in_iter_limit=3):
            return cls.evaluate_curve_max(data_representation.to_curve(in_data), in_iter_limit)

        @classmethod
        def evaluate_data_sum(cls, in_data, in_iter_limit=3):
            return cls.evaluate_curve_sum(data_representation.to_curve(in_data), in_iter_limit)

        @classmethod
        def generate_data(cls, x0):
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
            print('x0=', x0)
            initial_temp = 5230
            if x0 is not None:
                initial_temp = 10
            res_sum = scipy.optimize.dual_annealing(
                lambda x: cls.evaluate_data_sum(x),
                data_representation.bounds,
                maxiter=cls.maxiter,
                callback=callback_fun,
                x0=x0, initial_temp=initial_temp)
            res_data.append(RowType(
                res_sum.x, cls.evaluate_data_max(res_sum.x),
                time.time()-start_time))
            res_max = scipy.optimize.dual_annealing(
                lambda x: cls.evaluate_data_max(x),
                data_representation.bounds,
                maxiter=40,
                callback=callback_fun,
                x0=res_sum.x)
            res_data.append(RowType(
                res_max.x, cls.evaluate_data_max(res_max.x),
                time.time()-start_time))
            return res_data

        @classmethod
        def plot_state(cls, in_data, curve_color):
            cur_curve = data_representation.to_curve(in_data)
            _init_figure()
            # for _ in cls.shapes:
            #     _.plot(facecolor='none', edgecolor='green')
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
        for cur_rot in numpy.linspace(numpy.radians(0), numpy.radians(180), in_rotation_num, endpoint=False):
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


def get_strip_example(data_representation):
    class StripExample(
            get_example_with_multiple_shapes(data_representation)):
        shapes = _get_data_for_strip(60, 25)

        @classmethod
        def _set_limits(_):
            plot_size = 1.7
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])
    return StripExample


def get_halfplane_example(data_representation):
    class HalfplaneExample(
            get_example_with_multiple_shapes(data_representation)):
        shapes = _get_data_for_halfplane(30)#70

        @classmethod
        def _set_limits(_):
            plot_size = 3.1
            plt.gca().set_xlim([-plot_size, plot_size])
            plt.gca().set_ylim([-plot_size, plot_size])

    return HalfplaneExample


def generate_animation_data(
        optimiser, tex_propety_name, curve_color, anim_params, x0=None):
    cur_paths = op.OutputPaths(tex_propety_name)
    optimisation_data = optimiser.generate_data(x0)
    for (frame_number, cur_data) in enumerate(optimisation_data):
        optimiser.plot_state(cur_data.data, curve_color)
        plt.savefig(
            cur_paths.get_pdf_file_path(frame_number),
            bbox_inches='tight', pad_inches=0.01)
        plt.close()

    if anim_params is None:
        anim_params = '[autoplay]'
    assert anim_params[0] == '[' and anim_params[-1] == ']'
    tsu.save_animategraphics_str(
        cur_paths, 20, anim_params[1:-1], 0, len(optimisation_data)-1)

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


def create_comparison_conv_plot(in_data_dict, in_paths):
    _init_conv_plot()
    for (cur_name, cur_data) in in_data_dict.items():
        _plot_conv_data(
            cur_data, get_curve_color(cur_name),
            get_curve_name(cur_name))
    plt.legend(loc="upper right")
    plt.xlabel('[s]')
    y_limits = plt.gca().get_ylim()
    plt.gca().set_ylim([y_limits[0], 2])
    plt.savefig(
        in_paths.get_pdf_file_path(0),
        bbox_inches='tight', pad_inches=0.01)
    plt.close()
    _save_tex_str_conv_plot(in_paths)


def apply_dict(in_tex_name, in_dict):
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
    res_dict = {
        'Logo': ps.LOGO_COLOR,
        'Azimuth': ps.AZIMUTH_COLOR,
        'Point': ps.POINT_COLOR,
        'Shift': ps.SHIFT_COLOR}

    return apply_dict(in_tex_name, res_dict)


def get_curve_name(in_tex_name):
    res_dict = {
        'Logo': 'LOGO',
        'Azimuth': 'azymut',
        'Point': 'naiwny',
        'Shift': 'SHIFT'}

    return apply_dict(in_tex_name, res_dict)


def make_single_shape_plots(
        in_example_dict,
        conv_plot_tex_name, anim_params=None):
    data_dict = {}
    for (cur_tex_name, cur_example) in in_example_dict.items():
        data_dict[cur_tex_name] = generate_animation_data(
            cur_example,
            cur_tex_name,
            get_curve_color(cur_tex_name),
            anim_params)

    create_comparison_conv_plot(data_dict, op.OutputPaths(conv_plot_tex_name))


def make_multiple_shapes_plots(
        in_example_class, tex_name, conv_plot_tex_name, x0=None):
    opt_data = generate_animation_data(
            in_example_class,
            tex_name, get_curve_color(tex_name), None, x0)

    conv_paths = op.OutputPaths(conv_plot_tex_name)
    _init_conv_plot()
    _plot_conv_data(
        opt_data, get_curve_color(tex_name), get_curve_name(tex_name))
    plt.xlabel('[s]')
    y_limits = plt.gca().get_ylim()
    plt.gca().set_ylim([y_limits[0], 8])
    plt.savefig(
        conv_paths.get_pdf_file_path(0),
        bbox_inches='tight', pad_inches=0.01)
    plt.close()
    _save_tex_str_conv_plot(conv_paths)
    return opt_data


LogoRepresentation = \
    get_angle_curve_data_representation(escape_curve.LogoCurve)
AzimuthRepresentation = \
    get_angle_curve_data_representation(escape_curve.AzimuthCurve)

CIRCLE_EXAMPLES = {
    'escapeFromCircleLogoTex':
        get_unit_ball_example(LogoRepresentation(30, 2)),
    'escapeFromCircleAzimuthTex':
        get_unit_ball_example(AzimuthRepresentation(30, 2))}

make_single_shape_plots(CIRCLE_EXAMPLES, 'escapeFromCircleConvPlotTex')

LogoRepresentationFix = \
    get_angle_curve_fixed_data_representation(escape_curve.LogoCurve)
AzimuthRepresentationFix = \
    get_angle_curve_fixed_data_representation(escape_curve.AzimuthCurve)

CIRCLE_EXAMPLES_FIXED = {
    'escapeFromCircleLogoFixedTex':
        get_unit_ball_example(LogoRepresentationFix(30, 2)),
    'escapeFromCircleAzimuthFixedTex':
        get_unit_ball_example(AzimuthRepresentationFix(30, 2))}

make_single_shape_plots(
    CIRCLE_EXAMPLES_FIXED, 'escapeFromCircleConvPlotFixedTex')


RECTANGLE_EXAMPLES = {
    'escapeFromRectangleLogoTex':
        get_rectangle_example(LogoRepresentation(30, 2)),
    'escapeFromRectangleAzimuthTex':
        get_rectangle_example(AzimuthRepresentation(30, 2))}

make_single_shape_plots(RECTANGLE_EXAMPLES, 'escapeFromRectangleConvPlotTex')

HALFPLANE_AZIMUTH_REP = AzimuthRepresentation(20, 7)

AZIMUTH_HALFPLANE_RES = make_multiple_shapes_plots(
        get_halfplane_example(HALFPLANE_AZIMUTH_REP),
        'escapeFromHalfplaneAzimuthTex',
        'escapeFromHalfplaneConvPlotTex')


AZIMUTH_RES_CURVE = HALFPLANE_AZIMUTH_REP.to_curve(AZIMUTH_HALFPLANE_RES[-1].data)

def to_raw_list(in_point_list):
    res_list = []
    for _ in in_point_list:
        res_list.append(_[0])
        res_list.append(_[1])
    print(in_point_list)
    print(res_list)
    return numpy.array(res_list)
RAW_RES = to_raw_list(AZIMUTH_RES_CURVE.point_list[1:])

LIMIT = 1.2*max(abs(_) for _ in RAW_RES)

HALFPLANE_POINT_RES = PointCurveDataRepresentation(len(RAW_RES), -LIMIT, LIMIT)
make_multiple_shapes_plots(
        get_halfplane_example(HALFPLANE_POINT_RES),
        'escapeFromHalfplanePointTex',
        'escapeFromHalfplaneConvPlotTex',
        RAW_RES)
# make_multiple_shapes_plots(
#         get_strip_example(curve.angles_to_points_azimuth),
#         'escapeFromStripTex',
#         'escapeFromStripConvPlotTex')



# AZIMUTH_DATA_REPRESENTATION = get_angle_curve_data_representation(escape_curve.AzimuthCurve)
#
# make_multiple_shapes_plots(
#         get_halfplane_example(AZIMUTH_DATA_REPRESENTATION(9, 5)),
#         'escapeFromHalfplaneTex',
#         'escapeFromHalfplaneConvPlotTex')


# make_multiple_shapes_plots(
#         get_halfplane_example(ShiftCurveDataRepresentation(70, -0.1, 0.1)),
#         'escapeFromHalfplaneShiftTex',
#         'escapeFromHalfplaneConvPlotTex')
