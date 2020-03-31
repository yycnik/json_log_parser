"""
json_log_parser.exceptions.json_format_error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when JSON string is malformed.
"""
from json_log_parser.exceptions.json_error import JSONError


class JSONFormatError(JSONError):
    pass
