"""generates TeX data for functions with local optimums"""
import matplotlib.pyplot as plt
import matplotlib.cm
import mpl_toolkits.mplot3d
import numpy


import output_paths as op
import figure_saver as fs
import tex_string_utils as tsu


OUTPUT_PATHS = op.OutputPaths('localOptimumsTex')
FIGURE_SAVER = fs.FigureSaver(OUTPUT_PATHS)


def _init_figure():
    plt.close()
    plt.axis('off')


X_DATA = numpy.linspace(0, 3, 700)
GRAPH_COLOR = 'blue'

_init_figure()
plt.plot(
    X_DATA,
    [0.9*(numpy.cos(3*_)+numpy.sin(6*_)+_**0.7+0.1*_) for _ in X_DATA],
    color=GRAPH_COLOR)
FIGURE_SAVER.save_fig()


def _second_fun(in_x):
    y_val = 0.8*numpy.cos(60*in_x+5) + \
        numpy.cos(15*in_x)+numpy.sin(17*in_x)+in_x**0.7+0.1*in_x
    return 0.9*y_val


_init_figure()
plt.plot(X_DATA, [_second_fun(_) for _ in X_DATA], color=GRAPH_COLOR)
FIGURE_SAVER.save_fig()
plt.close()

X_DATA = numpy.linspace(0, 3, 70)
Y_DATA = numpy.linspace(0, 3, 70)
X_MESH, Y_MESH = numpy.meshgrid(X_DATA, Y_DATA)
Z_VALS = numpy.cos(2*X_MESH)*numpy.sin(3*Y_MESH)*numpy.cos(Y_MESH*X_MESH)

plt.figure()
CUR_AX = mpl_toolkits.mplot3d.Axes3D(plt.gcf())
plt.axis('off')
CUR_AX.plot_surface(
    X_MESH, Y_MESH, Z_VALS,
    # pylint: disable-next=no-member
    cmap=matplotlib.cm.coolwarm,
    antialiased=True, linewidth=0,
    rcount=100,
    ccount=100)

plt.gca().set_ylim3d(0, 3)
plt.gca().set_xlim3d(0, 3)
plt.gca().set_zlim3d(numpy.min(Z_VALS), numpy.max(Z_VALS))

FIGURE_SAVER.save_fig()
plt.close()

tsu.save_simple_overprint_frame(OUTPUT_PATHS, FIGURE_SAVER.fig_num, 0.5)
