"""
generates TeX data for escape from halfplane explanation
"""
import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy

import output_paths as op
import project_styles as ps
import figure_saver as fs
import tex_string_utils as tsu


OUTPUT_PATHS = op.OutputPaths('escapeFromHalfplaneExTex')
FIGURE_SAVER = fs.FigureSaver(OUTPUT_PATHS)


def _init_figure():
    plt.close()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def _draw_halfplane():
    plt.gca().add_patch(plt.Rectangle((-50, -1), 100, 101, **ps.CONVEX_COLORS))


def _get_rectangle(**kwargs):
    return plt.Rectangle((-5.5, -1), 11, 6.5, **kwargs)


def _draw_rectangle():
    plt.gca().add_patch(_get_rectangle(**ps.CONVEX_COLORS))


def _mark_pos():
    plt.plot(0, 0, marker='o', color='black', markersize=8)


X_LIM = [-13, 13]
Y_LIM = [-8, 7]

_init_figure()
_draw_halfplane()
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)
plt.plot([-50, 50], [0, 0], color='black', linestyle='--')
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

_init_figure()
_draw_rectangle()
_mark_pos()
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

ANGLE_LIST = numpy.linspace(0, 2*numpy.pi, 5, False)

for _ in ANGLE_LIST:
    _arrow_len = 1.7
    cur_x = _arrow_len*numpy.cos(_)
    cur_y = _arrow_len*numpy.sin(_)
    plt.arrow(0, 0, cur_x, cur_y, overhang=0.3, head_width=0.5, color='black')
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)

_init_figure()
COLOR_LIST = ['teal', 'maroon', 'blue', 'magenta', 'crimson']
for (cur_angle, cur_color) in zip(ANGLE_LIST, COLOR_LIST):
    cur_patch = _get_rectangle(color=cur_color, alpha=0.3)
    cur_rot = \
        matplotlib.transforms.Affine2D().rotate(cur_angle)+plt.gca().transData
    cur_patch.set_transform(cur_rot)

    plt.gca().add_patch(cur_patch)
_mark_pos()
FIGURE_SAVER.save_fig(X_LIM, Y_LIM)
plt.close()

tsu.save_simple_overprint_frame(OUTPUT_PATHS, FIGURE_SAVER.fig_num, 0.9)
