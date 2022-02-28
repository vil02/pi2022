import project_config as pc


def _tmp_data_dir():
    return pc.get_config_parameter('tmpDataFolder')


class OutputPaths:
    def __init__(self, in_output_core_name, in_config_tex_name):
        self._output_core_name = in_output_core_name
        self._cofig_tex_name = in_config_tex_name

    def get_file_name(self, in_num):
        """returns the name of the pdf file of given number"""
        return f'{self._output_core_name}_{in_num}.pdf'

    def get_short_pdf_path(self, in_num):
        """
        returns the result pdf file path relative to the main output path
        """
        return self.get_pdf_file_path(in_num).relative_to(_tmp_data_dir())

    def get_pdf_file_path(self, in_num):
        """
        returns the path of the ouput file for the given number
        """
        pdf_dir = _tmp_data_dir()/self._output_core_name
        pdf_dir.mkdir(parents=True, exist_ok=True)
        return pdf_dir/self.get_file_name(in_num)

    def get_tex_file_path(self):
        return \
            _tmp_data_dir()/pc.get_config_parameter(self._cofig_tex_name)
