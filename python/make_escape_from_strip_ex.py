"""
generates TeX data for escape from strip explanation
"""
import itertools
import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy


import output_paths as op
import project_styles as ps
import figure_saver as fs
import tex_string_utils as tsu


OUTPUT_PATHS = op.OutputPaths('escapeFromStripExTex')
FIGURE_SAVER = fs.FigureSaver(OUTPUT_PATHS)


def _init_figure():
    plt.close()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def _draw_strip():
    plt.gca().add_patch(plt.Rectangle((-50, -0.5), 100, 1, **ps.CONVEX_COLORS))


def _get_rectangle(**kwargs):
    return plt.Rectangle((-2, -0.5), 4, 1, **kwargs)


def _draw_rectangle():
    plt.gca().add_patch(_get_rectangle(**ps.CONVEX_COLORS))


def _mark_pos(in_y_pos):
    assert -1 <= in_y_pos < 1
    plt.plot(0, in_y_pos, marker='o', color='black', markersize=8)


def _mark_all_start_positions(in_y_pos_list, in_angle_list):
    for (pos_y, rot_angle) in itertools.product(in_y_pos_list, in_angle_list):
        arrow_len = 0.2
        _mark_pos(pos_y)
        cur_x = arrow_len*numpy.cos(rot_angle)
        cur_y = arrow_len*numpy.sin(rot_angle)
        plt.arrow(
            0, pos_y, cur_x, cur_y,
            overhang=0.3, head_width=0.1, color='black')


X_LIM = [-2.5, 2.5]
Y_LIM = [-1, 1]

_init_figure()
_draw_strip()
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

_init_figure()
_draw_rectangle()
plt.plot([0, 0], [-0.5, 0.5], color='black', linestyle='--')
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

POS_LIST = list(numpy.linspace(-0.55, 0.55, 4, endpoint=False))[1:]
_init_figure()
_draw_rectangle()
for _ in POS_LIST:
    _mark_pos(_)
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

_mark_all_start_positions(POS_LIST, numpy.linspace(0, 2*numpy.pi, 6, False))
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

ANGLE_LIST = numpy.linspace(0, numpy.pi, 3, False)
_init_figure()
_draw_rectangle()
_mark_all_start_positions(POS_LIST, ANGLE_LIST)
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

_init_figure()
TOTAL_SIZE = len(POS_LIST)*len(ANGLE_LIST)
# pylint: disable-next=no-member
COLOR_LIST = [plt.cm.get_cmap('hsv', TOTAL_SIZE)(_) for _ in range(TOTAL_SIZE)]
for (_, cur_color) in zip(itertools.product(POS_LIST, ANGLE_LIST), COLOR_LIST):
    cur_y_pos, cur_angle = _
    cur_patch = _get_rectangle(color=cur_color, alpha=0.3)
    cur_transform = \
        matplotlib.transforms.Affine2D().rotate(cur_angle) + \
        matplotlib.transforms.Affine2D().translate(0, cur_y_pos) + \
        plt.gca().transData
    cur_patch.set_transform(cur_transform)

    plt.gca().add_patch(cur_patch)
_mark_pos(0)
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)
plt.close()

tsu.save_simple_overprint_frame(OUTPUT_PATHS, FIGURE_SAVER.fig_num, 0.9)
