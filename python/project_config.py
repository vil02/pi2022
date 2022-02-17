"""config data for pi2022"""

import pathlib
import re


def _proj_core_name():
    return 'pi2022'


def get_project_root_dir():
    """
    returns the path of the root directory of the project
    """
    this_file_path = pathlib.Path(__file__)
    assert _proj_core_name() in str(this_file_path)
    return next(
        _ for _ in this_file_path.parents if _.name == _proj_core_name())


def read_paths_and_names():
    """
    reads the pi2022/latex/paths_and_names.tex file into a dict
    """
    latex_folder = get_project_root_dir()/'latex'
    assert latex_folder.is_dir()
    assert latex_folder.exists()
    config_file_path = latex_folder/'paths_and_names.tex'
    assert config_file_path.is_file()
    assert config_file_path.exists()

    res = {}

    def proc_single_line(in_line):
        tmp_line = re.sub(r'\s*%.*', '', in_line).strip()
        if re.fullmatch(r'\\newcommand{\\[^{^}]*}{[^{^}]*}', tmp_line):
            raw_str_list = re.findall(r'{[^{^}]*}', tmp_line)
            assert len(raw_str_list) == 2
            assert re.fullmatch(r'\{[^{^}]*}', raw_str_list[0])
            key_str = raw_str_list[0][2:-1].strip()
            assert re.fullmatch(r'{[^{^}]*}', raw_str_list[1])
            value_str = raw_str_list[1][1:-1].strip()
            assert key_str not in res
            assert value_str not in res.values()
            res[key_str] = value_str
    with open(config_file_path, encoding='utf-8') as config_file:
        for _ in config_file.readlines():
            proc_single_line(_)
    for _ in res:
        if _.endswith('Folder'):
            res[_] = latex_folder/pathlib.Path(res[_])

    return res


def get_config_parameter(in_parameter_name):
    """
    returns the value of given parameter from paths_and_names_file
    """
    return _CONFIG_DATA[in_parameter_name]


_CONFIG_DATA = read_paths_and_names()
