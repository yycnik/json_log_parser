"""
Unit tests to validate regex expressions used to enforce JSON schema
"""

import hashlib
import pytest
import re
import uuid


from json_log_parser.json_schema import JsonSchema


@pytest.fixture(scope='module')
def uuid_regex():
    return re.compile(JsonSchema.get_uuid_regex())


@pytest.fixture(scope='module')
def sha_regex():
    return re.compile(JsonSchema.get_sha256_regex())


def test_uuid_v4_should_match(uuid_regex):
    uuid_to_test = uuid.uuid4()
    assert uuid_regex.search(str(uuid_to_test)) is not None


def test_uuid_v3_should_not_match(uuid_regex):
    uuid_to_test = uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
    assert uuid_regex.search(str(uuid_to_test)) is None


def test_uuid_v1_should_not_match(uuid_regex):
    uuid_to_test = uuid.uuid1()
    assert uuid_regex.search(str(uuid_to_test)) is None


def test_sha256_should_match(sha_regex):
    sha = hashlib.sha256(b'We need something to hash').hexdigest()
    assert sha_regex.search(sha) is not None


def test_sha256_upper_should_match(sha_regex):
    sha = hashlib.sha256(b'We need something to hash').hexdigest()
    assert sha_regex.search(sha.upper()) is not None


def test_sha256_with_0x_should_match(sha_regex):
    sha = hashlib.sha256(b'We need something to hash').hexdigest()
    assert sha_regex.search('0x' + sha) is not None


def test_sha256_with_md5_should_not_match(sha_regex):
    sha = hashlib.md5(b'We need something to hash').hexdigest()
    assert sha_regex.search('0x' + sha) is None


def test_sha256_with_sha384_should_not_match(sha_regex):
    sha = hashlib.sha384(b'We need something to hash').hexdigest()
    assert sha_regex.search('0x' + sha) is None


def test_sha256_with_sha512_should_not_match(sha_regex):
    sha = hashlib.sha512(b'We need something to hash').hexdigest()
    assert sha_regex.search('0x' + sha) is None

