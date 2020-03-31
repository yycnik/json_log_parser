"""
json_log_parser.exceptions.json_schema_error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when JSON document cannot be validated against given schema
"""
from json_log_parser.exceptions.json_error import JSONError


class JSONSchemaError(JSONError):
    pass
