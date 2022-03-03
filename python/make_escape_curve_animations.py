import collections
import scipy.optimize
import numpy
import matplotlib.pyplot as plt

import itertools

import output_paths as op
import escape_curve
import plotable_convex_shapes
import rotations


class Optimizer():
    """generates the optimisition data for given scheme"""

    @classmethod
    def to_curve(cls, in_data):
        return escape_curve.Curve(in_data, cls.max_curve_len/len(in_data))

    @classmethod
    def evaluate_data(cls, in_data):
        return cls.evaluate_curve(cls.to_curve(in_data))

    @classmethod
    def generate_data(cls):
        RowType = collections.namedtuple('RowType', ['data', 'function_value'])
        res_data = []

        def callback_fun(in_data, in_fun_val, context):
            nonlocal res_data
            res_data.append(RowType(in_data, in_fun_val))

        scipy.optimize.dual_annealing(
            lambda x: cls.evaluate_data(x),
            cls.bounds,
            maxiter=cls.maxiter,
            callback=callback_fun)
        return res_data


def _init_figure():
    plt.figure(figsize=(3.5, 3.5))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


class ExampleWithSingleShape(Optimizer):
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
    def plot_state(cls, in_data):
        cur_curve = cls.to_curve(in_data)
        _init_figure()
        cls.shape.plot(facecolor='lightgreen', edgecolor='green')
        plt.plot(cur_curve.x_list, cur_curve.y_list, color='orange')
        cls._set_limits()


class UnitBallExample(ExampleWithSingleShape):
    shape = plotable_convex_shapes.Wheel([0, 0], 1)

    @classmethod
    def _set_limits(_):
        plot_size = 1.2
        plt.gca().set_xlim([-plot_size, plot_size])
        plt.gca().set_ylim([-plot_size, plot_size])


class UnitBallFixedDirectionExample(UnitBallExample):
    @classmethod
    def to_curve(cls, in_data):
        angle_list = numpy.insert(in_data, 0, 0, axis=0)
        return super().to_curve(angle_list)


class RectangleExample(ExampleWithSingleShape):
    shape = plotable_convex_shapes.Rectangle([0, 0], 2, 1.8)

    @classmethod
    def _set_limits(_):
        plot_size = 1.1
        plt.gca().set_xlim([-plot_size, plot_size])
        plt.gca().set_ylim([-plot_size, plot_size])


class ExampleWithMultipleShapes(Optimizer):
    maxiter = 20
    data_size = 50
    max_curve_len = 7
    segment_size = max_curve_len/data_size
    bounds = [
        (numpy.radians(-180), numpy.radians(180)) for _ in range(data_size)]

    @classmethod
    def evaluate_curve(cls, curve):
        return max(curve.get_max_len_inside(_) for _ in cls.shapes)

    @classmethod
    def plot_state(cls, in_data):
        cur_curve = cls.to_curve(in_data)
        _init_figure()
        # for _ in cls.shapes:
        #     _.plot(facecolor='lightgreen')
        for _ in cls.shapes:
            _.plot(edgecolor='green', facecolor='none')
        plt.plot(cur_curve.x_list, cur_curve.y_list, color='orange')
        cls._set_limits()

    @classmethod
    def _set_limits(_):
        plot_size = 3.3
        plt.gca().set_xlim([-plot_size, plot_size])
        plt.gca().set_ylim([-plot_size, plot_size])


class Rectangle:
    def __init__(self, in_xy_data):
        self.xy_data = in_xy_data
        self._patch_data = plt.Polygon(self.xy_data)

    def __contains__(self, in_pos):
        return self._patch_data.contains_point(in_pos, radius=0.001)

    def plot(self, **kwargs):
        plt.gca().add_patch(plt.Polygon(self.xy_data, **kwargs))


def get_all_squares(in_shift_num, in_rotation_num):
    initial_xy_data = numpy.array([[-1, 1], [1, 1], [1, -1], [-1, -1]])
    res_list = []
    for _ in itertools.product(list(numpy.linspace(-0.999, 0.999, in_shift_num)), repeat=2):
        cur_shift = numpy.array(_)
        for cur_rot in numpy.linspace(numpy.radians(0), numpy.radians(360), in_rotation_num, endpoint=False):
            cur_xy = [rotations.rotate_2d(_, cur_rot)+cur_shift for _ in initial_xy_data]
            cur_shape = Rectangle(cur_xy)
            if numpy.array([0, 0]) in cur_shape:
                res_list.append(cur_shape)
    return res_list


class ExampleSquares(ExampleWithMultipleShapes):
    shapes = get_all_squares(3, 5)


def make_plots(optimiser, core_name, tex_propety_name):
    cur_paths = op.OutputPaths(core_name, tex_propety_name)
    optimisation_data = optimiser.generate_data()
    for (frame_number, cur_data) in enumerate(optimisation_data):
        optimiser.plot_state(cur_data.data)
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


make_plots(
    UnitBallExample, 'esape_from_unit_circle_example', 'escapeFromCircleTex')

make_plots(
    UnitBallFixedDirectionExample, 'esape_from_unit_circle_fixed_example', 'escapeFromCircleFixedTex')

make_plots(
    RectangleExample, 'esape_from_rectangle_example', 'escapeFromRectangleTex')

make_plots(
    ExampleSquares, 'esape_from_free_square_example', 'escapeFromFreeSquareTex')
