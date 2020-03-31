"""
json_log_parser.exceptions.file_path_error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when file path string fails validation
"""
from json_log_parser.exceptions.json_error import JSONError


class FilePathError(JSONError):
    pass
