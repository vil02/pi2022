import curve
import math
import matplotlib.pyplot as plt
import matplotlib
import scipy.interpolate
import numpy


def mark_angles(in_curve):
    total_angle = 0
    cur_ax = plt.gca()
    for (cur_pos, cur_angle) in zip(in_curve.point_list, in_curve.angle_list):
        tmp_angles = [
            numpy.degrees(total_angle), numpy.degrees(total_angle+cur_angle)]
        cur_angle_marker = matplotlib.patches.Wedge(
            cur_pos, 0.5*in_curve.segment_size,
            theta1=min(tmp_angles), theta2=max(tmp_angles),
            alpha=0.3)
        dir_line_len = 0.6*in_curve.segment_size
        plt.plot(
            [cur_pos[0], cur_pos[0]+dir_line_len*numpy.cos(total_angle)],
            [cur_pos[1], cur_pos[1]+dir_line_len*numpy.sin(total_angle)],
            color=[0.1, 0.1, 0.1],
            linestyle='--')
        total_angle += cur_angle
        cur_ax.add_patch(cur_angle_marker)


ANGLE_DEG_LIST = [15, 50, -60, -60, -60, 5, 30]

EXAMPLE_CURVE = curve.Curve([math.radians(_) for _ in ANGLE_DEG_LIST], 1)

RAW_DATA = numpy.array([EXAMPLE_CURVE.x_list, EXAMPLE_CURVE.y_list]).T
interpolator = scipy.interpolate.interp1d(
    numpy.linspace(0, 1, len(EXAMPLE_CURVE.y_list)),
    RAW_DATA, axis=0, kind='cubic')
SMOOTH_DATA = interpolator(numpy.linspace(0, 1, 100))

mark_angles(EXAMPLE_CURVE)
plt.plot(SMOOTH_DATA[:, 0], SMOOTH_DATA[:, 1], linewidth=3)
plt.plot(EXAMPLE_CURVE.x_list, EXAMPLE_CURVE.y_list, linewidth=3)
plt.plot(EXAMPLE_CURVE.x_list, EXAMPLE_CURVE.y_list, linestyle='None', marker='o')


plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')
plt.show()
