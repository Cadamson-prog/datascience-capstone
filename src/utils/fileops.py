"""
Author: Brendan OConnell
Year:   2026

Purpose:
    File operation helpers for locating and loading project data files.
"""

from pathlib import Path
import pandas as pd
from .. import exceptions as exc


def load_data_file(file_name: str) -> pd.DataFrame:
    """
    Load a file from the data directory.

    Args:
        file_name (str):
            The name of the file to load in the form `filename.ext`.
            The file must be located in the `data` directory for this project.
            If more than one file matches the provided name,
            pass the full path from the data directory to the desired file
            (e.g. `data/processed/filename.parquet`).

    Returns:
        DataFrame: The loaded data as a pandas DataFrame.

    Raises:
        InvalidFileNameError: If `file_name` does not have an extension.
        DataFileNotFoundError: If no file matching `file_name` is found in the data directory.
        MultipleDataFilesFoundError: If more than one file matching `file_name` is found in the data directory.
        InvalidFileTypeError: If the file extension of `file_name` is not supported for loading.
    """

    p = Path(file_name)
    # fileops.py lives at <project-root>/src/utils/fileops.py - climb three
    # parents to reach the project root, then descend into `data`.
    data_dir = Path(__file__).resolve().parent.parent.parent / "data"

    # `file_name` must have an extension
    if not p.suffix:
        raise exc.InvalidFileNameError(file_name)

    # `file_name` is a path + filename
    if p.parent != Path("."):
        # handle path names that include the `data` parent dir
        if p.parts[0] == data_dir.name:
            data_path = data_dir.parent / p
        # handle path names that are missing the `data` parent dir
        else:
            data_path = data_dir / p

        if not data_path.exists():
            raise exc.DataFileNotFoundError(file_name)

    # `file_name` is a filename (no path)
    else:
        # Search data dir recursively for the file
        matches = list(data_dir.rglob(p.name))

        # catch file not found
        if not matches:
            raise exc.DataFileNotFoundError(file_name)

        # catch multiple files with the same name
        if len(matches) > 1:
            raise exc.MultipleDataFilesFoundError(file_name)

        data_path = matches[0]

    # load the file based on its extension
    suffix = data_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(data_path)
    elif suffix == ".parquet":
        return pd.read_parquet(data_path)
    # NOTE: If we want to support other file types, add `elif` blocks here to handle them.
    else:
        raise exc.InvalidFileTypeError(file_name)
