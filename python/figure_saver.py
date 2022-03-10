"""contains the definition of the class FigureSaver"""

import matplotlib.pyplot as plt


class FigureSaver:
    """utility class to hande saving figure in sequences"""
    _cur_fig_num = 0

    def __init__(self, output_paths):
        self._output_paths = output_paths

    def save_fig(self, in_xlim, in_ylim):
        """saves the current figre and increases the counter"""
        def _set_limits():
            plt.gca().set_xlim(in_xlim)
            plt.gca().set_ylim(in_ylim)
        _set_limits()
        plt.savefig(
            self._output_paths.get_pdf_file_path(self.fig_num),
            bbox_inches='tight', pad_inches=0.01)
        self._cur_fig_num += 1

    @property
    def fig_num(self):
        """returns the current figure number"""
        return self._cur_fig_num
