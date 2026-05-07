"""
Author: Brendan OConnell
Year:   2026

Purpose:
    Custom exceptions for the project.
"""


# Data file exceptions
class DataFileNotFoundError(Exception):
    """Exception raised when a required data file is not found."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.message = f"Data file '{file_name}' not found in the data directory."
        super().__init__(self.message)


class InvalidFileNameError(Exception):
    """Exception raised when a filename does not follow the expected format."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.message = (
            f"Filename '{file_name}' is invalid. Expected format: 'filename.ext'."
        )
        super().__init__(self.message)


class InvalidFileTypeError(Exception):
    """Exception raised when a file type is not supported."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.message = f"Filename '{file_name}' has an unsupported type. Expected types: '.csv', '.parquet'."
        super().__init__(self.message)


class MultipleDataFilesFoundError(Exception):
    """Exception raised when multiple data files are found when only one was expected."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.message = f"Multiple data files found for '{file_name}'. Expected only one. To select a specific file, pass the full path from the data directory to the desired file."
        super().__init__(self.message)
