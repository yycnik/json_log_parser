"""
json_log_parser.json_schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains json schema elements needed to validate a log line entry
"""


class JsonSchema:
    @staticmethod
    def get_json_schema():
        """
        This method returns the schema for a valid log line entry
        :return: Dictionary object
        """
        uuid_schema = JsonSchema.get_uuid_schema()
        sha256_schema = JsonSchema.get_sha256_schema()
        return {
            "type": "object",
            "properties": {
                "ts": {"type": "number"},
                "pt": {"type": "integer",
                       "minimum": 0},
                "si": uuid_schema,
                "uu": uuid_schema,
                "bg": uuid_schema,
                "sha": sha256_schema,
                "nm": {"type": "string"},
                "ph": {"type": "string"},
                "dp": {"type": "integer",
                       "minimum": 1,
                       "maximum": 3
                       },
            },
            "required": ["ts", "pt", "si", "uu", "bg", "sha", "nm"]
        }

    @staticmethod
    def get_uuid_schema():
        """
        This method returns the json schema for valid UUID entry
        :return: Dictionary object
        """
        return JsonSchema.get_regex_schema(
            JsonSchema.get_uuid_regex())

    @staticmethod
    def get_uuid_regex():
        """
        This method returns a regex expression that matches a valid UUID string.

        The regex validates against version 4 UUID format. Other formats will not be matched.

        The regex allows both lowercase and uppercase as per online documentation.
        :return: string
        """
        return "^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-" \
               "[89aAbB][a-fA-F0-9]{3}-[a-fA-F0-9]{12})$"

    @staticmethod
    def get_sha256_schema():
        """
        This method returns the schema for valid sha256 entry
        :return: Dictionary object
        """
        return JsonSchema.get_regex_schema(
            JsonSchema.get_sha256_regex())

    @staticmethod
    def get_sha256_regex():
        """
        This method returns a regex pattern that matches a valid SHA256 string
        :return: str
        """
        return "(?i)^(0x)?([a-f0-9]{64})$"

    @staticmethod
    def get_regex_schema(pattern):
        """
        This method returns generic json schema used to validate a string value
        using a regex pattern
        :param pattern: regex expression
        :return: Dictionary object
        """
        return {"type": "string",
                "format": "regex",
                "pattern": pattern
                }
