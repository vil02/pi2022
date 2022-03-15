"""
generates TeX data for lost in forest explanation
"""
import matplotlib.pyplot as plt
import numpy
import scipy.interpolate
import scipy.spatial

import output_paths as op
import project_styles as ps
import figure_saver as fs
import tex_string_utils as tsu


def _get_start_pos():
    return -1.3, -0.4


def _smooth_data(in_raw_data):
    in_data_size = len(in_raw_data)
    interpolator = scipy.interpolate.interp1d(
        numpy.linspace(0, 1, in_data_size),
        numpy.array(in_raw_data), axis=0, kind='cubic')
    return interpolator(numpy.linspace(0, 1, 9*in_data_size))


def _get_raw_shape():
    raw_data = [
        [-3, 0.1], [-1.7, 1.6], [0.5, 1.1], [1, 0.9],
        [0.14, -0.9], [-1.2, -1.0], [-3, 0.1]]
    smooth_data = _smooth_data(raw_data)
    # pylint: disable-next=no-member
    convex_hull = scipy.spatial.ConvexHull(smooth_data)
    return smooth_data[convex_hull.vertices]


def _get_escape_path():
    raw_data = [
        _get_start_pos(), [-0.5, -0.3], [0, 0.4], [-0.06, 0.6],
        [-0.6, 0.3], [-0.7, 0.6], [0, 1], [1.7, 0.5]]
    return _smooth_data(raw_data)


def _init_figure():
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


_init_figure()
plt.gca().add_patch(plt.Polygon(_get_raw_shape(), **ps.CONVEX_COLORS))

plt.plot(*_get_start_pos(), marker='o', color='black')
plt.plot(
    _get_escape_path()[:, 0], _get_escape_path()[:, 1],
    linestyle='--', color='black')

OUTPUT_PATHS = op.OutputPaths('lostInForestExTex')
FIGURE_SAVER = fs.FigureSaver(OUTPUT_PATHS)
FIGURE_SAVER.save_fig([-3.3, 2], [-1.4, 1.7])
plt.close()
TEX_STR = \
    r'\includegraphics[width=0.7\textwidth]' + \
    f'{{{OUTPUT_PATHS.get_short_pdf_path(0)}}}\n'
tsu.save_to_tex_file(TEX_STR, OUTPUT_PATHS)
