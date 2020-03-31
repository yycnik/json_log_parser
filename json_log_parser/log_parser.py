"""
json_log_parser.log_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module process a given log file and counts unique extensions and
the number of unique filenames for that extension
"""
import time
from collections import defaultdict
import json
from json.decoder import JSONDecodeError

from json_log_parser.exceptions.input_filename_error import InputFilenameError
from json_log_parser.exceptions.json_error import JSONError
from json_log_parser.exceptions.json_format_error import JSONFormatError
from json_log_parser.file_extension_counter import FileExtensionCounter
from json_log_parser.json_validator import JsonValidator
from json_log_parser.file_reader import FileReader


class LogParser:
    def __init__(self):
        """
        Constructor
        Initialize a JsonValidator class used to validate each log line
        """
        self.json_validator = JsonValidator()

    def process_log(self, input_filename):
        """
        Process a log file containing one JSON document per line
            - Read the input file
            - Validate each line
            - Build a set of unique filenames
            - Build a dictionary of unique extensions and
            the number of unique filenames for that extension
        :param input_filename:
        """
        try:
            line_generator = FileReader.read_file(input_filename)
            unique_files = self.get_unique_file_set(line_generator)
            extension_counter = self.count_file_extensions(unique_files)
            self.print_file_extensions(extension_counter)
        # Handle gracefully problems with the input filename
        except InputFilenameError as error:
            print(str(error))

    def get_unique_file_set(self, line_generator):
        """
        This function builds a set of unique filenames found in the log file

        The built-in collection set() ensures that all entries are unique. This
        eliminates the need for explicit checks

        The function will also keep track of number of valid and invalid log lines.
        The stats will be printed in the log file.
        :param line_generator:
        :return:
        """
        unique_files = set()
        processing_stats = defaultdict(int)
        exception_stats = defaultdict(int)

        for line in line_generator:
            processing_stats['total'] += 1
            try:
                document = self.get_json_document(line)
                unique_files.add(document['nm'])
                processing_stats['success'] += 1
            except JSONError as invalid_json:
                processing_stats['fail'] += 1
                exception_key = '{0}-{1}'.format(type(invalid_json).__name__, str(invalid_json))
                exception_stats[exception_key] += 1

        self.log_processing_stats(exception_stats, processing_stats)
        return unique_files

    def log_processing_stats(self, processing_stats, exception_stats):
        """
        This function logs the stats from processing the input file
        Processing stats show total, valid and invalid number of lines,
        Exception stats provide a breakdown of all invalid log lines
        :param processing_stats:
        :param exception_stats:
        :return:
        """
        for k, v in processing_stats.items():
            print(k, v)
        for k, v in exception_stats.items():
            print(k, v)

    def get_json_document(self, json_string):
        """
        This function takes a JSON string, loads it as JSON object,
        and validates it against the schema
        """
        document = self.load_json_from_string(json_string)
        self.json_validator.validate_document(document)
        return document

    def load_json_from_string(self, json_string):
        """
        This function tries to a load the input json_string into a JSON object

        :param json_string:
        Raises InvalidJSONFormatException if sting is malformed JSON
        """
        try:
            return json.loads(json_string)
        except JSONDecodeError as json_error:
            raise JSONFormatError(json_error)

    def count_file_extensions(self, unique_files):
        extension_counter = FileExtensionCounter()
        if not unique_files:
            return defaultdict()

        for file in unique_files:
            extension_counter.add_extension_from_filename(file)

        return extension_counter.get_extension_counts()

    def print_file_extensions(self, extension_counter):
        for key, value in extension_counter.items():
            print("{0}: {1}".format(key, value))


l = LogParser()
l.process_log('../tests/data/data2.json')
# l.process_log('')
# l.process_log('tests/data/')
# l.process_log('tests/data/nothingthere')
# print(time.time)
