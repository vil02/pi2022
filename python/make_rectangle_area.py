"""
makes the plot for the rectangle area example
"""
import matplotlib.pyplot as plt
import numpy

import output_paths as op
import figure_saver as fs
import tex_string_utils as tsu


def _init_figure():
    plt.gca().set_aspect('equal', adjustable='box')


_init_figure()
X_DATA = numpy.linspace(0, 1, 40)
Y_DATA = [_*(1-_) for _ in X_DATA]

plt.plot(X_DATA, Y_DATA, color='blue')

OUTPUT_PATHS = op.OutputPaths('rectangleAreaPlotTex')
FIGURE_SAVER = fs.FigureSaver(OUTPUT_PATHS)
FIGURE_SAVER.save_fig()
plt.close()
TEX_STR = \
    r'\includegraphics[width=0.85\textwidth]' + \
    f'{{{OUTPUT_PATHS.get_short_pdf_path(0)}}}\n'
tsu.save_to_tex_file(TEX_STR, OUTPUT_PATHS)
