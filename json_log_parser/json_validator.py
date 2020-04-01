"""
json_log_parser.json_validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module ensures that a given JSON document conforms with the provided schema
"""

from datetime import datetime

import jsonschema
from jsonschema.exceptions import ValidationError

from .exceptions.file_path_error import FilePathError
from .exceptions.filename_error import FilenameError
from .exceptions.json_schema_error import JSONSchemaError
from .exceptions.timestamp_error import TimestampError
from .json_schema import JSONSchema


class JSONValidator:
    def __init__(self):
        """
        Constructor
        Loads the schema that will be used to validate documents
        """
        self.schema = JSONSchema.get_json_schema()

    def validate_document(self, document):
        """
        Validate the provided document
        Validation is done two steps:
        1) Use jsonschema module to ensure that the document has all the required
            keys and the values are the expected type.
            Also, UUIDs and SHA256 are validated using regex
        2) Manually validate additional fields such as timestamp, path and filename
        :param document:
        Raises exception if validation fails. All exceptions raised in this module
        inherit from JSONError to allow for single catch in the calling function
        """
        self.has_valid_json_schema(document)
        JSONValidator.has_valid_data(document)

    def has_valid_json_schema(self, document):
        """
        This function validates the input document against the provided schema
        :param document:
        Raises InvalidJSONSchemaException if validation fails
        """
        try:
            jsonschema.validate(document, self.schema)
        except ValidationError as v:
            raise JSONSchemaError(v)

    @staticmethod
    def has_valid_data(document):
        """
        This function validates fields in the JSON document that could not be
        validated using the jsonschema module
        :param document:
        """
        JSONValidator.is_valid_timestamp(document['ts'])
        JSONValidator.is_valid_path(document['ph'])
        JSONValidator.is_valid_filename(document['nm'])

    @staticmethod
    def is_valid_timestamp(timestamp):
        """
        This function checks if the input timestamp is valid
        Timestamp is valid if
            - Can be parsed using datetime module
            - It does not have a value in the future
        :param timestamp:
        Raises InvalidTimestampException
        """
        try:
            d = datetime.fromtimestamp(timestamp)

            now = datetime.utcnow()
            if d > now:
                raise TimestampError('Timestamp is in the future'.format(d))
        except OverflowError as err:
            raise TimestampError(err)

    @staticmethod
    def is_valid_path(path_string):
        """
        This function attempts to validate the file path in the JSON document
        First, I want to acknowledge that a cross-platform solution to check if the path
        is valid is not straightforward. I am not sure if this is important for our use case
        because we don't do anything with the path.

        There is a fairly comprehensive posting on Stackoverflow here
        https://bit.ly/2JnPe3F
        I first thought of copying that code as I could not do much better but I ultimately
        decided that this will be an overkill for our purpose

        As a result, we will perform the following simple validation for the sake of having
        some minimal sanity check
        1) No null byte in path
        2) Path size cannot exceed 4096 characters
        :param path_string:
        Raises exception if path_string is longer than 4096 characters or
        path_string contains null bytes
        """

        if len(path_string) > 4096:
            raise FilePathError("File path is longer than 4096 characters")

        if JSONValidator.string_has_null_byte(path_string):
            raise FilePathError("File path contains null bytes")

    @staticmethod
    def is_valid_filename(filename):
        """
        This function checks if filename is valid

        Similar to the file path problem above this is platform dependent.

        We will keep it simple by checking for null byte and '/'
        :param filename:
        Raises exception if filename contains null byte or '/'
        """
        if '/' in filename:
            raise FilenameError("Invalid character '/' in filename")

        if JSONValidator.string_has_null_byte(filename):
            raise FilenameError("Filename contains null bytes")

    @staticmethod
    def string_has_null_byte(string_to_check):
        """
        This function checks if the given string contains null byte
        :param string_to_check:
        :return: True if null byte is found False otherwise
        """
        if b'\x00' in string_to_check.encode('utf-8'):
            return True

        return False
