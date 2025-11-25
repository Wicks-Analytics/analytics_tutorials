"""Basic tests to verify project setup and dependencies."""

import sys
from pathlib import Path

import pytest


def test_python_version():
    """Test that Python version is 3.8 or higher."""
    assert sys.version_info >= (3, 8), "Python 3.8 or higher is required"


def test_imports():
    """Test that all required packages can be imported."""
    try:
        import dotenv
        import faker
        import matplotlib
        import numpy
        import polars
        import scipy
        import seaborn
        import sklearn
        import sqlalchemy
    except ImportError as e:
        pytest.fail(f"Failed to import required package: {e}")


def test_project_structure():
    """Test that required directories and files exist."""
    project_root = Path(__file__).parent.parent

    required_dirs = [
        "tutorials",
        "utils",
        "notebooks",
    ]

    required_files = [
        "README.md",
        "QUICKSTART.md",
        "TUTORIAL_INDEX.md",
        "requirements.txt",
        "pyproject.toml",
        "setup_database.py",
        "convert_to_notebooks.py",
    ]

    for dir_name in required_dirs:
        assert (project_root / dir_name).exists(), f"Directory {dir_name} not found"

    for file_name in required_files:
        assert (project_root / file_name).exists(), f"File {file_name} not found"


def test_utils_module():
    """Test that utils module can be imported."""
    try:
        from utils import data_generators, database_helpers
    except ImportError as e:
        pytest.fail(f"Failed to import utils module: {e}")


def test_polars_version():
    """Test that Polars version is 0.20.0 or higher."""
    import polars as pl

    version_parts = pl.__version__.split(".")
    major = int(version_parts[0])
    minor = int(version_parts[1])

    assert (major > 0) or (
        major == 0 and minor >= 20
    ), f"Polars version {pl.__version__} is too old, need 0.20.0 or higher"


def test_numpy_basic_operations():
    """Test basic NumPy operations."""
    import numpy as np

    arr = np.array([1, 2, 3, 4, 5])
    assert arr.mean() == 3.0
    assert arr.sum() == 15


def test_polars_basic_operations():
    """Test basic Polars operations."""
    import polars as pl

    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    assert df.shape == (3, 2)
    assert df["a"].sum() == 6
    assert df["b"].mean() == 5.0
