"""
    Test the list command and subcommand do not introduce regressions
"""

import pytest
from test_show import compare
from test_show import patterns as extra_patterns


def compare_list(*args):
    return compare("list", *args, sort=True)


patterns = ["*NN*", "ct*", "*18", "MS"] + extra_patterns
arguments = ["--installed", "--outdated", "--codes"]


@pytest.mark.parametrize("pattern", patterns)
@pytest.mark.parametrize("argument", arguments)
def test_list(pattern, argument):
    """Test the list command"""
    assert compare_list(pattern, argument)
