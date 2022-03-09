"""
generates TeX data for escape from circle explanation
"""
import matplotlib.pyplot as plt

import output_paths as op
import plotable_convex_shapes as pcs
import project_styles as ps


def _init_figure():
    plt.figure(figsize=(3.2, 3.2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


OUTPUT_PATHS = op.OutputPaths('escapeFromCircleExTex')

_init_figure()
WHEEL = pcs.Wheel((0, 0), 1)
WHEEL.plot(**ps.CONVEX_COLORS)
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
with open(
        OUTPUT_PATHS.get_tex_file_path(), 'w', encoding='utf-8') as tex_file:
    tex_file.write(TEX_STR)
