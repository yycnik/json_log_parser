"""
json_log_parser.exceptions.timestamp_error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised if timestamp in a JSON document is invalid
"""
from json_log_parser.exceptions.json_error import JSONError


class TimestampError(JSONError):
    pass
