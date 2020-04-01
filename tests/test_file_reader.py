"""
Unit tests for json_log_parser.file_reader module
"""
from unittest.mock import patch

import pytest

from json_log_parser.exceptions.input_filename_error import InputFilenameError
from json_log_parser.file_reader import FileReader


def test_read_file_read_existing_file():
    """
    Happy Path: read file that has 3 lines, get 3 lines back
    """
    line_generator = FileReader.read_file('tests/data/file_reader_tests/file_reader_test.json')

    assert sum(1 for line in line_generator) == 3


def test_is_input_filename_valid_empty_filename():
    """
    Pass empty filename, expect InputFilenameError
    """
    with pytest.raises(InputFilenameError):
        FileReader.is_input_filename_valid('')


def test_is_input_filename_valid_null_filename():
    """
    Pass None as filename, expect InputFilenameError
    """
    with pytest.raises(InputFilenameError):
        FileReader.is_input_filename_valid(None)


def test_is_input_filename_valid_null_byte_in_filename():
    """
    Filename contains null byte, expect InputFilenameError
    """
    with pytest.raises(InputFilenameError):
        FileReader.is_input_filename_valid('some\x00filename')


@patch('os.path.exists')
def test_is_input_filename_valid_filename_not_exist(mock_file_exists):
    """
    Filename does not exist, expect InputFilenameError
    """
    mock_file_exists.return_value = False
    with pytest.raises(InputFilenameError) as err:
        FileReader.is_input_filename_valid('/path/to/file')

    assert "does not exist" in str(err)


@patch('os.path.isfile')
@patch('os.path.exists')
def test_is_input_filename_valid_filename_not_file(mock_file_exists, mock_isfile):
    """
    Filename exists but is not a file, expect InputFilenameError
    """
    mock_file_exists.return_value = True
    mock_isfile.return_value = False
    with pytest.raises(InputFilenameError) as err:
        FileReader.is_input_filename_valid('/path/to/file')

    assert "is not a file" in str(err)


@patch('os.access')
@patch('os.path.isfile')
@patch('os.path.exists')
def test_is_input_filename_valid_filename_not_readable(
        mock_file_exists, mock_isfile, mock_osaccess):
    """
    Filename is not readable, expect InputFilenameError
    """
    mock_file_exists.return_value = True
    mock_isfile.return_value = True
    mock_osaccess.return_value = False
    with pytest.raises(InputFilenameError) as err:
        FileReader.is_input_filename_valid('/path/to/file')

    assert "is not readable" in str(err)
