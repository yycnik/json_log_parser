"""
Unit tests for json_log_parser.file_extension_counter module
"""
import pytest

from json_log_parser.file_extension_counter import FileExtensionCounter


@pytest.fixture(scope="function")
def extension_counter():
    return FileExtensionCounter()


def test_add_extension_from_filename_single_extension(extension_counter):
    """
    Count single filename
    """
    extension_counter.add_extension_from_filename('textfile.txt')

    assert extension_counter.file_extension_count['txt'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_multiple_files(extension_counter):
    """
    Two filenames with same extension. Expect counter to be 2
    """
    extension_counter.add_extension_from_filename('textfile.txt')
    extension_counter.add_extension_from_filename('anothertext.txt')

    assert extension_counter.file_extension_count['txt'] == 2
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_multi_extension(extension_counter):
    """
    Filename has multiple extensions. Only the last one should be counted
    """
    extension_counter.add_extension_from_filename('multi.ext1.ext2.ext3')

    assert extension_counter.file_extension_count['ext3'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_no_extension(extension_counter):
    """
    Filename with no extension. It should be grouped under
    'no_extension' category
    """
    extension_counter.add_extension_from_filename('noextensionfile')

    assert extension_counter.file_extension_count['no_extension'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_non_ascii_filename(extension_counter):
    """
    Test with filename that has non-ascii characters.
    Python handles that well internally
    """
    extension_counter.add_extension_from_filename('тест.ткт')

    assert extension_counter.file_extension_count['ткт'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_null_value(extension_counter):
    """
    Pass None as filename. Dictionary should not be updated
    """
    extension_counter.add_extension_from_filename(None)
    assert len(extension_counter.file_extension_count.keys()) == 0


def test_add_extension_from_filename_empty_string(extension_counter):
    """
    Pass empty string as filename. Dictionary should not be updated
    """
    extension_counter.add_extension_from_filename('')
    assert len(extension_counter.file_extension_count.keys()) == 0
