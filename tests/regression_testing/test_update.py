"""
    Test the update command and compare with LHAPDF
"""
import os
from pathlib import Path
import subprocess as sp
from tempfile import mkdtemp


def test_update():
    """Test the update command by downloading the index with both programs"""
    base_env = dict(os.environ)

    # Use LHAPDF_DATA_PATH to download the set index to a different place for both scripts
    env_var = "LHAPDF_DATA_PATH"
    index_file = "pdfsets.index"
    legacy_path = Path(mkdtemp())
    new_path = Path(mkdtemp())

    sp.run(["lhapdf", "update"], env={env_var: legacy_path.as_posix(), **base_env})
    sp.run(["lhapdf-management", "update"], env={env_var: new_path.as_posix(), **base_env})

    legacy_file = legacy_path / index_file
    new_file = new_path / index_file

    assert legacy_file.read_bytes() == new_file.read_bytes()
