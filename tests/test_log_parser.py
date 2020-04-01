"""
Unit tests for json_log_parser.log_parser module
"""
import sys
from contextlib import contextmanager
from io import StringIO
from unittest.mock import patch

import pytest

from json_log_parser.exceptions.json_format_error import JSONFormatError
from json_log_parser.exceptions.json_schema_error import JSONSchemaError
from json_log_parser.file_reader import FileReader
from json_log_parser.log_parser import LogParser


@pytest.fixture(scope='function')
def parser():
    """
    Object to perform the tests on
    """
    return LogParser()


def test_get_unique_file_set(parser):
    """
    Happy path: read sample test file and count the number of unique files
    """
    line_generator = FileReader.read_file('tests/data/log_parser_tests/log_parser.json')
    unique_files = parser.get_unique_file_set(line_generator)

    assert len(unique_files) == 3
    assert 'file1.ext' in unique_files
    assert 'file2.pdf' in unique_files
    assert 'file3.txt' in unique_files


def test_get_json_document_loads_document(parser):
    """
    Happy path: load a well formed JSON string
    Returns dict
    """
    json_string = '{"ts":1551140352,' \
                  '"pt":55,' \
                  '"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074",' \
                  '"uu":"0dd24034-36d6-4b1e-a6c1-a52cc984f105",' \
                  '"bg":"77e28e28-745a-474b-a496-3c0e086eaec0",' \
                  '"sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52",' \
                  '"nm":"phkkrw.ext",' \
                  '"ph":"/efvrfutgp/expgh/phkkrw",' \
                  '"dp":2}'
    document = parser.get_json_document(json_string)

    assert type(document) is dict


def test_get_json_document_malformed_string_raises_exception(parser):
    """
    Load malformed JSON string
    Raises JSONFormatError
    """
    json_string = 'a52cc984f105",' \
                  '"bg":"77e28e28-745a-474b-a496-3c0e086eaec0",' \
                  '"sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52",' \
                  '"nm":"phkkrw.ext",' \
                  '"ph":"/efvrfutgp/expgh/phkkrw",' \
                  '"dp":2}'

    with pytest.raises(JSONFormatError):
        parser.get_json_document(json_string)


def test_get_json_document_missing_key_raises_exception(parser):
    """
    Load JSON document with a required key missing
    Raises JSONSchemaError
    """
    json_string = '{"ts":1551140352,' \
                  '"pt":55,' \
                  '"si":"3380fb19-0bdb-46ab-8781-e4c5cd448074",' \
                  '"bg":"77e28e28-745a-474b-a496-3c0e086eaec0",' \
                  '"sha":"abb3ec1b8174043d5cd21d21fbe3c3fb3e9a11c7ceff3314a3222404feedda52",' \
                  '"nm":"phkkrw.ext",' \
                  '"ph":"/efvrfutgp/expgh/phkkrw",' \
                  '"dp":2}'

    with pytest.raises(JSONSchemaError) as err:
        parser.get_json_document(json_string)
    assert 'is a required property' in str(err)


def test_count_file_extensions(parser):
    """
    Happy path: given a set of filenames, count the unique extensions
    """
    unique_files = {'file1.txt', 'file2.txt', 'file3.txt', 'file4.pdf', 'file5'}
    extensions = parser.count_file_extensions(unique_files)

    assert extensions['txt'] == 3
    assert extensions['pdf'] == 1
    assert extensions['no_extension'] == 1


def test_count_file_extensions_null_set_expects_empty_dict(parser):
    """
    Pass None to count_file_extensions
    Expect empty dict
    """
    extensions = parser.count_file_extensions(None)

    assert len(extensions.keys()) == 0


@contextmanager
def captured_output():
    """
    Arguable approach (aka hack) to validate output in unit tests
    Source: https://bit.ly/39reBMI

    This provides some value because we can capture changes if output format changes
    Moreover, this gives us the ultimate prize of achieving 100% code coverage
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def test_process_log_validate_output(parser):
    """
    Happy path: load data from test file and print the results
    """
    with captured_output() as (out, err):
        parser.process_log('tests/data/log_parser_tests/log_parser.json')

    output = out.getvalue().strip()
    assert 'ext: 1\npdf: 1\ntxt: 1' == output


@patch('logging.basicConfig')
def test_process_log_cannot_create_logger_produce_valid_output(mock_logging):
    """
    We still should be able to do the job even if we cannot properly setup logging
    """
    mock_logging.side_effect = PermissionError('Permission denied')
    log_parser = LogParser()
    with captured_output() as (out, err):
        log_parser.process_log('tests/data/log_parser_tests/log_parser.json')

    output = out.getvalue().strip()
    assert 'ext: 1\npdf: 1\ntxt: 1' == output


@patch('json_log_parser.log_parser.FileReader')
def test_process_log_runtime_error_validate_output(mock_file_reader, parser):
    """
    In the event of an error that we did not expect we should still exit gracefully
    """
    mock_file_reader.read_file.side_effect = RuntimeError('Crash')
    with captured_output() as (out, err):
        parser.process_log('something')

    output = out.getvalue().strip()
    assert 'LogParser encountered unexpected error' in output


def test_process_log_file_does_not_exist(parser):
    """
    The given input file does not exist
    Print an error and exit
    """
    with captured_output() as (out, err):
        parser.process_log('file/does/not/exist')

    output = out.getvalue().strip()
    assert 'does not exist' in output
