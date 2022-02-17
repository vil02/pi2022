"""
common functions for pi2022
"""


def to_core_name(in_str):
    """
    returns the core name of given tex-file
    """
    assert in_str.endswith('.tex')
    return in_str[0:-4]
