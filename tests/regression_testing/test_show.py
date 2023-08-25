"""
    Test the show command
"""
import subprocess as sp

import pytest

patterns = [
    "CT18ZNNLO",
    "MSTW2008lo68cl_nf3",
    "PDF4LHC15_nnlo_100",
    "NNPDF40_nlo_as_01180",
    "MSHT20nnlo_nf*",
]


def run_command(program, command, *args):
    """ "Run a given command with given arguments and return standard output as text"""
    ret = sp.run([program, command] + list(args), capture_output=True)
    ret_text = ret.stdout.decode()
    return ret_text


def compare(command, *args, verbose=False, sort=False):
    """Compare the old and new python script"""
    old_raw = run_command("lhapdf", command, *args)
    new_raw = run_command("lhapdf-management", command, *args)

    old = old_raw.split()
    new = old_raw.split()

    if sort:
        old = sorted(old)
        new = sorted(new)

    print(f"\nFor {args}: ")
    if verbose:
        print(">>>>>>>>>>>")
        print(old_raw)
        print("<<<<<<<<<<")
        print(new_raw)
    if len(old) != len(new):
        print(f"Lists of different lengths: {len(old)} vs {len(new)}")
        return False
    for i, j in zip(old, new):
        if i != j:
            print(f"> Difference found: {i} vs {j}")
            break
    else:
        print("No difference found!")
        return True
    return False


@pytest.mark.parametrize("pattern", patterns)
def test_show(pattern):
    """Test the show command for different sets and patterns"""
    assert compare("show", pattern)


def test_show_all():
    assert compare("show", *patterns)
