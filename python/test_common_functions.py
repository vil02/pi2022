"""
tests of project_config module
"""
import pathlib
import project_config as pc


def test_project_root_dir_exists():
    """checks result of pc.get_project_root_dir() exists"""
    assert pc.get_project_root_dir().exists()


def test_project_root_dir_is_dir():
    """checks result of pc.get_project_root_dir() is a directory"""
    assert pc.get_project_root_dir().is_dir()


def test_result_of_read_paths_and_names_is_a_dict():
    """checks if result of pc.read_paths_and_names() is a dictionary"""
    assert isinstance(pc.read_paths_and_names(), dict)


def test_result_of_read_paths_and_names_is_not_empty():
    """checks if result of pc.read_paths_and_names() is not empty"""
    assert pc.read_paths_and_names()


def test_get_config_parameter():
    """
    checks if pc.get_config_parameter() uses the result of
    pc.read_paths_and_names()
    """
    for (key, value) in pc.read_paths_and_names().items():
        assert value == pc.get_config_parameter(key)


def test_get_config_parameter_tmp_data_folder():
    """
    checks if pc.get_config_parameter('tmpDataFolder')
    returns a pathlib.Path object
    """
    assert isinstance(pc.get_config_parameter('tmpDataFolder'), pathlib.Path)
