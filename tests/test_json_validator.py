"""
Unit tests for json_log_parser.json_validator module
"""
import hashlib
import uuid
from datetime import datetime

import pytest

from json_log_parser.exceptions.file_path_error import FilePathError
from json_log_parser.exceptions.filename_error import FilenameError
from json_log_parser.exceptions.json_schema_error import JSONSchemaError
from json_log_parser.exceptions.timestamp_error import TimestampError
from json_log_parser.json_validator import JSONValidator


def get_uuid():
    """
    Generates UUID v4 for test data
    """
    return str(uuid.uuid4())


def get_sha256():
    """
    Generates SHA256 for test data
    """
    return hashlib.sha256(b'We need something to hash').hexdigest()


@pytest.fixture(scope='function')
def validator():
    """
    JSONValidator object to run tests on
    """
    return JSONValidator()


@pytest.fixture(scope='function')
def json_document():
    """
    Valid test document
    """
    return {
            "ts": datetime.utcnow().timestamp(),
            "pt": 12,
            "si": get_uuid(),
            "uu":  get_uuid(),
            "bg":  get_uuid(),
            "sha": get_sha256(),
            "nm": 'verymalicious.virus',
            "ph": 'this/is/my/valid/path/',
            "dp": 1,
        }


def test_validate_document_returns_nothing(validator, json_document):
    """
    Happy path: validate_document, nothing happens
    """
    assert validator.validate_document(json_document) is None


def test_validate_document_missing_element(validator, json_document):
    """
    Document is missing a required key. Raises JSONSchemaError
    """
    del(json_document['si'])
    with pytest.raises(JSONSchemaError) as err:
        validator.validate_document(json_document)

    assert 'is a required property' in str(err)


def test_validate_document_invalid_type(validator, json_document):
    """
    The type of one of the keys does not match the schema
    Raises JSONSchemaError
    """
    json_document['ts'] = 'not a timestamp'
    with pytest.raises(JSONSchemaError) as err:
        validator.validate_document(json_document)

    assert 'is not of type' in str(err)


def test_validate_document_invalid_uuid(validator, json_document):
    """
    A UUID field does not match the regex
    Raises JSONSchemaError
    """
    json_document['bg'] = 'not a uuid'
    with pytest.raises(JSONSchemaError) as err:
        validator.validate_document(json_document)

    assert 'does not match' in str(err)


def test_validate_document_invalid_sha256(validator, json_document):
    """
    SHA256 in the document does not match the regex
    Raises JSONSchemaError
    """
    json_document['sha'] = 'not a sha256'
    with pytest.raises(JSONSchemaError) as err:
        validator.validate_document(json_document)

    assert 'does not match' in str(err)


def test_validate_document_timestamp_in_future(validator, json_document):
    """
    Timestamp values is in the future
    Raises TimestampError
    """
    json_document['ts'] = json_document['ts'] * 2
    with pytest.raises(TimestampError) as err:
        validator.validate_document(json_document)

    assert 'Timestamp is in the future' in str(err)


def test_validate_document_timestamp_overflow(validator, json_document):
    """
    Value of timestamp is too big
    Raises TimestampError
    """
    json_document['ts'] = json_document['ts'] ** 20
    with pytest.raises(TimestampError) as err:
        validator.validate_document(json_document)

    assert 'timestamp out of range' in str(err)


def test_validate_document_null_byte_in_path(validator, json_document):
    """
    File path contains null byte
    Raises FilePathError
    """
    json_document['ph'] = 'find/the\x00/byte'
    with pytest.raises(FilePathError) as err:
        validator.validate_document(json_document)

    assert 'File path contains null bytes' in str(err)


def test_validate_document_path_exceeds_limit(validator, json_document):
    """
    File path contains more than 4096 characters
    Raises FilePathError
    """
    long_list = ['a' for i in range(4097)]
    json_document['ph'] = ''.join(long_list)
    with pytest.raises(FilePathError) as err:
        validator.validate_document(json_document)

    assert 'File path is longer than 4096' in str(err)


def test_validate_document_slash_in_filename(validator, json_document):
    """
    Filename contains '/'
    Raises FilenameError
    """
    json_document['nm'] = 'not/a/filename/byte.pdf'
    with pytest.raises(FilenameError) as err:
        validator.validate_document(json_document)

    assert 'Invalid character' in str(err)


def test_validate_document_null_byte_in_filename(validator, json_document):
    """
    Filename contains null byte
    Raises FilenameError
    """
    json_document['nm'] = 'thereis\x00byte.pdf'
    with pytest.raises(FilenameError) as err:
        validator.validate_document(json_document)

    assert 'Filename contains null bytes' in str(err)
