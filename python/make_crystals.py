"""
generates data for the crystals example/annealing explanation
"""
import itertools
import copy
import random
import matplotlib.pyplot as plt

import output_paths as op
import tex_string_utils as tsu


class _Crystal:
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.shifts = {}
        self.node_styles = {}

    def _check_node(self, in_node):
        assert in_node in self.nodes

    def add_edge(self, node_a, node_b):
        """adds an edge"""
        self._check_node(node_a)
        self._check_node(node_b)
        if node_a < node_b:
            self.edges.add(tuple([node_a, node_b]))
        else:
            self.edges.add(tuple([node_b, node_a]))

    def remove_edge(self, node_a, node_b):
        """removes  an edge"""
        self._check_node(node_a)
        self._check_node(node_b)
        if node_a < node_b:
            self.edges.remove(tuple([node_a, node_b]))
        else:
            self.edges.remove(tuple([node_b, node_a]))

    def add_node(self, in_node):
        """adds a node"""
        self.nodes.add(in_node)

    def add_shift(self, in_node, in_shift):
        """
        adds a shift (visible on plot) to a node
        """
        self._check_node(in_node)
        cur_shift = self.shifts.get(in_node, (0, 0))
        cur_shift = tuple(sum(_) for _ in zip(cur_shift, in_shift))
        self.shifts[in_node] = cur_shift

    def set_node_style(self, in_node, **kwargs):
        """sets plotting style for given node"""
        self.node_styles[in_node] = kwargs

    def try_add_shift(self, in_node, in_shift):
        """tries to add a shift of a node"""
        if in_node in self.nodes:
            self.add_shift(in_node, in_shift)

    def _get_node_pos(self, in_node):
        cur_shift = self.shifts.get(in_node, (0, 0))
        return in_node[0]+cur_shift[0], in_node[1]+cur_shift[1]

    def plot(self):
        """plots crystal net"""
        for cur_nodes in self.edges:
            plt.plot(
                [self._get_node_pos(_)[0] for _ in cur_nodes],
                [self._get_node_pos(_)[1] for _ in cur_nodes],
                linestyle='-', color='gray', marker='')
        for _ in self.nodes:
            plt.plot(
                *self._get_node_pos(_),
                **self.node_styles.get(
                    _, {'color': 'black', 'marker': 'o', 'markersize': 4}))


def _get_all_neighbours(in_pos_x, in_pos_y, in_size_x, in_size_y):
    def check_pos(in_x, in_y):
        return 0 <= in_x < in_size_x and 0 <= in_y < in_size_y
    all_pos_list = [
        (in_pos_x-1, in_pos_y), (in_pos_x+1, in_pos_y),
        (in_pos_x, in_pos_y-1), (in_pos_x, in_pos_y+1)]
    return [_ for _ in all_pos_list if check_pos(*_)]


def _init_figure():
    plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')


def _get_example_crystal_size():
    return (23, 12)


def _get_regular_crystal():
    all_raw_nodes = list(itertools.product(
        range(_get_example_crystal_size()[0]),
        range(_get_example_crystal_size()[1])))
    res = _Crystal()
    for _ in all_raw_nodes:
        res.add_node(_)
    for cur_node in all_raw_nodes:
        for _ in _get_all_neighbours(*cur_node, *_get_example_crystal_size()):
            res.add_edge(_, cur_node)
    return res


def _add_shift_for_four(crystal, min_x, min_y, s_size):
    crystal.try_add_shift((min_x, min_y), (-s_size, -s_size))
    crystal.try_add_shift((min_x+1, min_y), (s_size, -s_size))
    crystal.try_add_shift((min_x, min_y+1), (-s_size, s_size))
    crystal.try_add_shift((min_x+1, min_y+1), (s_size, s_size))

    crystal.try_add_shift((min_x-1, min_y+1), (-s_size/2, 0))
    crystal.try_add_shift((min_x-1, min_y), (-s_size/2, 0))

    crystal.try_add_shift((min_x+2, min_y+1), (s_size/2, 0))
    crystal.try_add_shift((min_x+2, min_y), (s_size/2, 0))

    crystal.try_add_shift((min_x, min_y+2), (0, s_size/2))
    crystal.try_add_shift((min_x+1, min_y+2), (0, s_size/2))

    crystal.try_add_shift((min_x, min_y-1), (0, -s_size/2))
    crystal.try_add_shift((min_x+1, min_y-1), (0, -s_size/2))


def _add_horizontal_shift(crystal, center_x, center_y, s_size):
    crystal.try_add_shift((center_x-1, center_y), (s_size, 0))
    crystal.try_add_shift((center_x-2, center_y), (s_size/2, 0))
    crystal.try_add_shift((center_x+1, center_y), (-s_size, 0))
    crystal.try_add_shift((center_x+2, center_y), (-s_size/2, 0))


def _add_vertical_shift(crystal, center_x, center_y, s_size):
    crystal.try_add_shift((center_x, center_y-1), (0, s_size))
    crystal.try_add_shift((center_x, center_y-2), (0, s_size/2))
    crystal.try_add_shift((center_x, center_y+1), (0, -s_size))
    crystal.try_add_shift((center_x, center_y+2), (0, -s_size/2))


def _add_shift_for_central(crystal, center_x, center_y, s_size):
    _add_horizontal_shift(crystal, center_x, center_y, s_size)
    _add_vertical_shift(crystal, center_x, center_y, s_size)
    crystal.try_add_shift((center_x-1, center_y-1), (s_size/3, s_size/3))
    crystal.try_add_shift((center_x-1, center_y+1), (s_size/3, -s_size/3))
    crystal.try_add_shift((center_x+1, center_y+1), (-s_size/3, -s_size/3))
    crystal.try_add_shift((center_x+1, center_y-1), (-s_size/3, s_size/3))


def _get_defected_crystal():
    all_raw_nodes = set(itertools.product(
        range(_get_example_crystal_size()[0]),
        range(_get_example_crystal_size()[1])))
    all_raw_nodes.remove((5, 6))
    res = _Crystal()
    for _ in all_raw_nodes:
        res.add_node(_)
    for cur_node in all_raw_nodes:
        for _ in _get_all_neighbours(*cur_node, *_get_example_crystal_size()):
            if _ in all_raw_nodes:
                res.add_edge(_, cur_node)

    other_node_style = {'color': 'red', 'marker': 'o', 'markersize': 6}
    _add_shift_for_four(res, 1, 1, 0.1)
    res.add_node((1.5, 1.5))
    res.set_node_style((1.5, 1.5), **other_node_style)

    _add_shift_for_four(res, 10, 6, 0.2)
    res.add_node((10.5, 6.5))
    _add_shift_for_central(res, 5, 6, 0.3)

    insertion_shift = 0.3
    insertion_range = list(range(14, 19))
    for cur_x in insertion_range:
        res.add_node((cur_x, 2.5))
        res.remove_edge((cur_x, 2), (cur_x, 3))
        res.add_edge((cur_x, 2), (cur_x, 2.5))
        res.add_edge((cur_x, 3), (cur_x, 2.5))
        res.try_add_shift((cur_x, 2), (0, -insertion_shift))
        res.try_add_shift((cur_x, 1), (0, -insertion_shift/2))
        res.try_add_shift((cur_x, 3), (0, insertion_shift))
        res.try_add_shift((cur_x, 4), (0, insertion_shift/2))
    for cur_x in insertion_range[:-1]:
        res.add_edge((cur_x, 2.5), (cur_x+1, 2.5))

    x_insertion_range = list(range(17, 20))
    y_insertion_min = 7
    y_insertion_max = 8
    for _ in itertools.product(
            x_insertion_range, [y_insertion_min, y_insertion_max]):
        res.set_node_style(_, **other_node_style)
        _add_shift_for_central(res, *_, -0.09)

    res.add_shift((17, 7), (0.2, 0.2))
    res.add_shift((17, 8), (0.2, -0.2))

    res.add_shift((18, 7), (0, 0.2))
    res.add_shift((18, 8), (0, -0.2))

    res.add_shift((19, 7), (-0.2, 0.2))
    res.add_shift((19, 8), (-0.2, -0.2))

    return res


def _get_output_paths():
    return op.OutputPaths('crystalsExamplesTex')


def _call_save_fig(in_num):
    plt.savefig(
        _get_output_paths().get_pdf_file_path(in_num),
        bbox_inches='tight', pad_inches=0.01)


_init_figure()
_get_regular_crystal().plot()
_call_save_fig(0)
plt.close()

DEFECTED_CRYSTAL = _get_defected_crystal()
_init_figure()
DEFECTED_CRYSTAL.plot()
_call_save_fig(1)
plt.close()

FRAME_LIMIT = 15
for frame_num in range(2, FRAME_LIMIT):
    _init_figure()
    tmp_crystal = copy.deepcopy(DEFECTED_CRYSTAL)
    for _ in tmp_crystal.nodes:
        tmp_crystal.add_shift(
            _, tuple(random.normalvariate(0, 0.025) for _ in range(2)))
    tmp_crystal.plot()
    _call_save_fig(frame_num)
    plt.close()

TEX_STR = ''
for _ in range(2):
    cur_file = _get_output_paths().get_short_pdf_path(_)
    TEX_STR += \
        '\\begin{frame}\n' + \
        '  \\begin{center}\n' + \
        f'    \\includegraphics{{{cur_file}}}\n' \
        '  \\end{center}\n' \
        '\\end{frame}\n'


ANIM_STR = tsu.animategraphics_str(
    _get_output_paths(), 15, 'autoplay,loop', 2, FRAME_LIMIT-1)

TEX_STR += \
    '\\begin{frame}\n' + \
    '  \\begin{center}\n' + \
    '    ' + ANIM_STR + '\n' + \
    '  \\end{center}\n' \
    '\\end{frame}\n'

tsu.save_to_tex_file(TEX_STR, _get_output_paths())
