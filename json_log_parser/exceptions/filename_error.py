"""
json_log_parser.exceptions.filename_error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when filename string fails validation
"""
from json_log_parser.exceptions.json_error import JSONError


class FilenameError(JSONError):
    pass
