"""
tests of common_functions module
"""
import pathlib
import common_functions as cf


def test_project_root_dir_exists():
    """checks result of cf.get_project_root_dir() exists"""
    assert cf.get_project_root_dir().exists()


def test_project_root_dir_is_dir():
    """checks result of cf.get_project_root_dir() is a directory"""
    assert cf.get_project_root_dir().is_dir()


def test_result_of_read_paths_and_names_is_a_dict():
    """checks if result of cf.read_paths_and_names() is a dictionary"""
    assert isinstance(cf.read_paths_and_names(), dict)


def test_result_of_read_paths_and_names_is_not_empty():
    """checks if result of cf.read_paths_and_names() is not empty"""
    assert cf.read_paths_and_names()


def test_get_config_parameter():
    """
    checks if cf.get_config_parameter() uses the result of
    cf.read_paths_and_names()
    """
    for (key, value) in cf.read_paths_and_names().items():
        assert value == cf.get_config_parameter(key)


def test_get_config_parameter_tmp_data_folder():
    assert isinstance(cf.get_config_parameter('tmpDataFolder'), pathlib.Path)
