"""Unit tests for src/utils/fileops.py"""

import pytest
import pandas as pd
from unittest.mock import patch
from pathlib import Path

import src.utils.fileops as fileops
from src.exceptions import (
    DataFileNotFoundError,
    InvalidFileNameError,
    InvalidFileTypeError,
    MultipleDataFilesFoundError,
)


DUMMY_DF = pd.DataFrame({"col": [1, 2, 3]})


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    """
    Create a temporary data/ directory and redirect load_data_file to use it.

    fileops.py computes data_dir as:
        Path(__file__).resolve().parent.parent.parent / "data"
    Patching the module's __file__ to tmp_path/src/utils/fileops.py makes
    data_dir resolve to tmp_path/data.
    """

    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setattr(
        fileops, "__file__", str(tmp_path / "src" / "utils" / "fileops.py")
    )
    return d


class TestInvalidFilename:
    """file_name must include a file extension."""

    def test_bare_name_raises(self, data_dir):
        with pytest.raises(InvalidFileNameError):
            fileops.load_data_file("myfile")

    def test_path_without_extension_raises(self, data_dir):
        with pytest.raises(InvalidFileNameError):
            fileops.load_data_file("subdir/myfile")


class TestFilenameOnly:
    """file_name is just a filename (data dir is searched recursively)."""

    def test_csv_loads_successfully(self, data_dir):
        (data_dir / "sample.csv").write_text("a,b\n1,2\n")
        with patch("pandas.read_csv", return_value=DUMMY_DF) as mock_read:
            result = fileops.load_data_file("sample.csv")
        assert result is DUMMY_DF
        mock_read.assert_called_once()

    def test_parquet_loads_successfully(self, data_dir):
        (data_dir / "sample.parquet").touch()
        with patch("pandas.read_parquet", return_value=DUMMY_DF) as mock_read:
            result = fileops.load_data_file("sample.parquet")
        assert result is DUMMY_DF
        mock_read.assert_called_once()

    def test_not_found_raises(self, data_dir):
        with pytest.raises(DataFileNotFoundError):
            fileops.load_data_file("missing.csv")

    def test_multiple_matches_raises(self, data_dir):
        sub = data_dir / "sub"
        sub.mkdir()
        (data_dir / "dup.csv").touch()
        (sub / "dup.csv").touch()
        with pytest.raises(MultipleDataFilesFoundError):
            fileops.load_data_file("dup.csv")

    def test_unsupported_extension_raises(self, data_dir):
        (data_dir / "sample.xlsx").touch()
        with pytest.raises(InvalidFileTypeError):
            fileops.load_data_file("sample.xlsx")


class TestPathWithoutDataPrefix:
    """file_name includes subdirectory path but NOT a leading `data/` segment."""

    def test_csv_loads_successfully(self, data_dir):
        sub = data_dir / "processed"
        sub.mkdir()
        (sub / "labels.csv").write_text("a,b\n1,2\n")
        with patch("pandas.read_csv", return_value=DUMMY_DF) as mock_read:
            result = fileops.load_data_file("processed/labels.csv")
        assert result is DUMMY_DF
        mock_read.assert_called_once()

    def test_parquet_loads_successfully(self, data_dir):
        sub = data_dir / "processed"
        sub.mkdir()
        (sub / "labels.parquet").touch()
        with patch("pandas.read_parquet", return_value=DUMMY_DF) as mock_read:
            result = fileops.load_data_file("processed/labels.parquet")
        assert result is DUMMY_DF
        mock_read.assert_called_once()

    def test_not_found_raises(self, data_dir):
        with pytest.raises(DataFileNotFoundError):
            fileops.load_data_file("processed/missing.csv")


class TestPathWithDataPrefix:
    """file_name starts with `data/` (the data dir is part of the path)."""

    def test_csv_loads_successfully(self, data_dir):
        sub = data_dir / "processed"
        sub.mkdir()
        (sub / "labels.csv").write_text("a,b\n1,2\n")
        with patch("pandas.read_csv", return_value=DUMMY_DF) as mock_read:
            result = fileops.load_data_file("data/processed/labels.csv")
        assert result is DUMMY_DF
        mock_read.assert_called_once()

    def test_parquet_loads_successfully(self, data_dir):
        sub = data_dir / "processed"
        sub.mkdir()
        (sub / "labels.parquet").touch()
        with patch("pandas.read_parquet", return_value=DUMMY_DF) as mock_read:
            result = fileops.load_data_file("data/processed/labels.parquet")
        assert result is DUMMY_DF
        mock_read.assert_called_once()

    def test_not_found_raises(self, data_dir):
        with pytest.raises(DataFileNotFoundError):
            fileops.load_data_file("data/processed/missing.csv")
