"""
Unit tests for json_log_parser.file_extension_counter module
"""
import pytest

from json_log_parser.file_extension_counter import FileExtensionCounter


@pytest.fixture(scope="function")
def extension_counter():
    return FileExtensionCounter()


def test_add_extension_from_filename_single_extension(extension_counter):
    extension_counter.add_extension_from_filename('textfile.txt')

    assert extension_counter.file_extension_count['txt'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_multiple_files(extension_counter):
    extension_counter.add_extension_from_filename('textfile.txt')
    extension_counter.add_extension_from_filename('anothertext.txt')

    assert extension_counter.file_extension_count['txt'] == 2
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_multi_extension(extension_counter):
    extension_counter.add_extension_from_filename('multi.ext1.ext2.ext3')

    assert extension_counter.file_extension_count['ext3'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_multi_extension_no_extension(extension_counter):
    extension_counter.add_extension_from_filename('noextensionfile')

    assert extension_counter.file_extension_count['no_extension'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1


def test_add_extension_from_filename_non_ascii_filename(extension_counter):
    extension_counter.add_extension_from_filename('тест.ткт')

    assert extension_counter.file_extension_count['ткт'] == 1
    assert len(extension_counter.file_extension_count.keys()) == 1
