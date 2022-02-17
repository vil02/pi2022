"""tests of common_functions module"""
import common_functions as cf


def test_to_core_name():
    """basic check for the function to_core_name()"""
    assert cf.to_core_name('dummy_name.tex') == 'dummy_name'
