"""
    Test the update command and compare with LHAPDF
"""
from filecmp import dircmp
import os
from pathlib import Path
import subprocess as sp
from tempfile import mkdtemp

import pytest
from test_show import patterns as pdfsets

ENV_VAR = "LHAPDF_DATA_PATH"
BASE_ENV = dict(os.environ)


def install_and_check(pdfset, reference_path, new_path, *args):
    """Install a pdfset with both lhapdf and lhapdf-management
    in reference_path and new_path and check that it is inside
    Using --upgrade so we can utilize the same set and then test different arguments
    """
    print(f"\nTesting {pdfset}")

    if all(i is None for i in args):
        args = []

    # It is necessary to use upgrade also because lhapdf is still looking at the global path
    # and LHAPATH despite LHAPDF_DATA_PATH for the installation of pdfs
    sp.run(
        ["lhapdf", "install", pdfset, "--upgrade"] + list(args),
        env={ENV_VAR: reference_path.as_posix(), "LHAPATH": reference_path.as_posix(), **BASE_ENV},
    )
    sp.run(
        ["lhapdf-management", "install", pdfset, "--upgrade"] + list(args),
        env={ENV_VAR: new_path.as_posix(), **BASE_ENV},
    )

    comparison = dircmp(reference_path, new_path)

    failure = False
    if comparison.diff_files:
        failure = True
        print(f"> Different files inside: {comparison.diff_files}")
    if comparison.right_only:
        failure = True
        print(f" > Files only in lhapdf-management: {comparison.right_only}")
    if comparison.left_only:
        failure = True
        print(f" > Files only in lhapdf: {comparison.left_only}")

    if failure:
        raise ValueError(f"lhapdf path: {new_path}, lhapdf-management: {reference_path}")
    print("Ok!")
    return True


@pytest.mark.parametrize("arg", ["--dryrun", None, "--keep"])
def test_install(arg):
    """Test the install command"""
    # Use LHAPDF_DATA_PATH to download the pdfs to different locations for both scripts
    legacy_path = Path(mkdtemp(prefix="lhapdf_test"))
    new_path = Path(mkdtemp(prefix="lhapdf_test"))

    # Update the index file
    sp.run(["lhapdf", "update"], env={ENV_VAR: legacy_path.as_posix(), **BASE_ENV})
    sp.run(["lhapdf-management", "update"], env={ENV_VAR: new_path.as_posix(), **BASE_ENV})

    for pdf in pdfsets:
        assert install_and_check(pdf, legacy_path, new_path, arg)
