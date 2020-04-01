import hashlib
import json
import string
import uuid
from datetime import datetime
import random


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


base_filename_len = range(1,20)
extension_len = range(1, 5)
string.ascii_letters


def get_rand_str(max_length):
    length = random.randint(1, max_length)
    rand_str = ''
    for i in range(length):
        rand_str += random.choice(string.ascii_letters)
    return rand_str


def get_extension_list():
    extension_list = []
    for i in range(1000):
        extension_list.append(get_rand_str(5))
    return extension_list


def get_filename(extension_list):
    return '{0}.{1}'.format(get_rand_str(20), random.choice(extension_list))


def json_document(extension_list):
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
            "nm": get_filename(extension_list),
            "ph": 'this/is/my/valid/path/',
            "dp": 1,
        }


def generate_log_file(filename, line_count):
    files = set()
    extension_list = get_extension_list()
    with open(filename, 'w') as w:
        for i in range(line_count):
            doc = json_document(extension_list )
            files.add(doc['nm'])
            w.write(json.dumps(doc))
            w.write('\n')


generate_log_file('log2.log', 3500000)
