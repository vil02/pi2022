"""
generates TeX data for escape from rectangle explanation
"""
import matplotlib.pyplot as plt

import output_paths as op
import project_styles as ps
import tex_string_utils as tsu


def _init_figure():
    plt.figure(figsize=(3.2, 3.2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


OUTPUT_PATHS = op.OutputPaths('escapeFromRectangleExTex')

_init_figure()
D_X = 1
D_Y = 0.9
plt.gca().add_patch(plt.Rectangle(
    (-D_X, -D_Y), 2*D_X, 2*D_Y, **ps.CONVEX_COLORS))
plt.plot(0, 0, color='black', marker='o', markersize=5)
PLOT_R = 1.2
plt.gca().set_xlim([-PLOT_R, PLOT_R])
plt.gca().set_ylim([-PLOT_R, PLOT_R])
plt.savefig(
    OUTPUT_PATHS.get_pdf_file_path(0),
    bbox_inches='tight', pad_inches=0.01)
plt.close()

TEX_STR = \
    f'\\includegraphics{{{OUTPUT_PATHS.get_short_pdf_path(0)}}}\n'
tsu.save_to_tex_file(TEX_STR, OUTPUT_PATHS)
