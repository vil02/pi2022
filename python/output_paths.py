"""contains the definition of the OutputPats class"""
import project_config as pc


def _tmp_data_dir():

    return pc.get_config_parameter('tmpDataFolder')


def _get_core_name(in_tex_name):
    res = pc.get_config_parameter(in_tex_name)
    assert res.endswith('.tex')
    return res[:-4]


class OutputPaths:
    """
    helper class to manage the paths of the all TeX tmp_data
    """
    def __init__(self, in_config_tex_name):
        self._output_core_name = _get_core_name(in_config_tex_name)
        self._cofig_tex_name = in_config_tex_name

    def _get_output_dir(self):
        res_dir = _tmp_data_dir()/self._output_core_name
        res_dir.mkdir(parents=True, exist_ok=True)
        return res_dir

    def _get_file_name(self, in_file_name_postfix):
        return f'{self._output_core_name}_{in_file_name_postfix}'

    def get_file_name(self, in_num):
        """returns the name of the pdf file of given number"""
        return self._get_file_name(f'{in_num}.pdf')

    def get_short_pdf_path(self, in_num):
        """
        returns the result pdf file path relative to the main output path
        """
        return self.get_pdf_file_path(in_num).relative_to(_tmp_data_dir())

    def get_pdf_file_path(self, in_num):
        """
        returns the path of the ouput file for the given number
        """
        return self._get_output_dir()/self.get_file_name(in_num)

    def get_tex_file_path(self):
        """
        returns the path of the TeX file to be included into the main document
        """
        return \
            _tmp_data_dir()/pc.get_config_parameter(self._cofig_tex_name)

    def get_general_file_path(self, in_file_name_postfix):
        """returns the path of the output file with given postfix"""
        return self._get_output_dir()/self._get_file_name(in_file_name_postfix)
