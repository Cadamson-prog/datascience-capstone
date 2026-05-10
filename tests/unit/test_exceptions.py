"""Unit tests for src/exceptions.py"""

import pytest

from src.exceptions import (
    DataFileNotFoundError,
    InvalidFileNameError,
    InvalidFileTypeError,
    MultipleDataFilesFoundError,
)


# All custom exception classes share the same shape (file_name + message
# attribute, message passed to Exception.__init__). The structural tests below
# parametrize over them; the per-class tests below pin down the wording each
# class produces.
EXCEPTION_CLASSES = [
    DataFileNotFoundError,
    InvalidFileNameError,
    InvalidFileTypeError,
    MultipleDataFilesFoundError,
]


class TestExceptionStructure:
    """Shared invariants every custom exception must satisfy."""

    @pytest.mark.parametrize("cls", EXCEPTION_CLASSES)
    def test_is_exception_subclass(self, cls):
        assert issubclass(cls, Exception)

    @pytest.mark.parametrize("cls", EXCEPTION_CLASSES)
    def test_can_be_raised_and_caught_as_specific_type(self, cls):
        with pytest.raises(cls):
            raise cls("anyfile.csv")

    @pytest.mark.parametrize("cls", EXCEPTION_CLASSES)
    def test_can_be_caught_as_generic_exception(self, cls):
        with pytest.raises(Exception):
            raise cls("anyfile.csv")

    @pytest.mark.parametrize("cls", EXCEPTION_CLASSES)
    def test_stores_file_name_attribute(self, cls):
        exc = cls("specific_file.parquet")
        assert exc.file_name == "specific_file.parquet"

    @pytest.mark.parametrize("cls", EXCEPTION_CLASSES)
    def test_message_attribute_includes_file_name(self, cls):
        exc = cls("unique_token_xyz.csv")
        assert "unique_token_xyz.csv" in exc.message

    @pytest.mark.parametrize("cls", EXCEPTION_CLASSES)
    def test_str_returns_message(self, cls):
        exc = cls("foo.csv")
        assert str(exc) == exc.message

    @pytest.mark.parametrize("cls", EXCEPTION_CLASSES)
    def test_args_contains_message(self, cls):
        # `super().__init__(self.message)` populates exc.args with one element.
        exc = cls("foo.csv")
        assert exc.args == (exc.message,)


class TestExceptionsAreDistinctTypes:
    """Catching one custom exception must not catch the others - callers in
    fileops.py rely on this to handle each error condition separately."""

    def test_data_file_not_found_does_not_catch_invalid_name(self):
        with pytest.raises(InvalidFileNameError):
            try:
                raise InvalidFileNameError("foo")
            except DataFileNotFoundError:
                pytest.fail("InvalidFileNameError was caught as DataFileNotFoundError")

    def test_invalid_type_does_not_catch_multiple_files(self):
        with pytest.raises(MultipleDataFilesFoundError):
            try:
                raise MultipleDataFilesFoundError("dup.csv")
            except InvalidFileTypeError:
                pytest.fail(
                    "MultipleDataFilesFoundError was caught as InvalidFileTypeError"
                )


class TestDataFileNotFoundError:
    def test_message_format(self):
        exc = DataFileNotFoundError("missing.csv")
        assert exc.message == "Data file 'missing.csv' not found in the data directory."


class TestInvalidFileNameError:
    def test_message_format(self):
        exc = InvalidFileNameError("bare")
        assert (
            exc.message
            == "Filename 'bare' is invalid. Expected format: 'filename.ext'."
        )


class TestInvalidFileTypeError:
    def test_message_format(self):
        exc = InvalidFileTypeError("file.xlsx")
        assert exc.message == (
            "Filename 'file.xlsx' has an unsupported type. "
            "Expected types: '.csv', '.parquet'."
        )


class TestMultipleDataFilesFoundError:
    def test_message_format(self):
        exc = MultipleDataFilesFoundError("dup.csv")
        assert exc.message == (
            "Multiple data files found for 'dup.csv'. Expected only one. "
            "To select a specific file, pass the full path from the data directory "
            "to the desired file."
        )
