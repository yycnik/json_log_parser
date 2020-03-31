"""

"""
import os.path
from os import access, R_OK

from json_log_parser.exceptions.input_filename_error import InputFilenameError
from json_log_parser.json_validator import JsonValidator


class FileReader:
    @staticmethod
    def read_file(filename):
        """
        Lazy function (generator) to read a file line by line

        Note that this function will not throw exception even
        if the filename is invalid. The appropriate exception will be
        thrown when the first item in the generator is accessed
        :param filename:
        :return: generator
        """
        FileReader.is_input_filename_valid(filename)

        with open(filename, 'r') as r:
            for line in r:
                yield line

    @staticmethod
    def is_input_filename_valid(filename):
        """
        This function validates if the provided filename is valid
        and can be accessed
        :param filename:
        :return:
        """
        if not filename:
            raise InputFilenameError("Filename not provided")

        # As we learned when validating the JSON objects filenames cannot
        # have null bytes. Why not check it here too
        if JsonValidator.string_has_null_byte(filename):
            raise InputFilenameError("Filename '{0}' contains null bytes".format(filename))

        # Check if the file exists
        if not os.path.exists(filename):
            raise InputFilenameError("Filename '{0}' does not exist".format(filename))

        # Great! The path exists but is it a file or directory
        if not os.path.isfile(filename):
            raise InputFilenameError("Filename '{0}' is not a file".format(filename))

        # We have a file that exists but is it also readable
        # Granted, it might be readable now but before we read it the permissions may
        # change and we will still crash. We will check anyway
        if not access(filename, R_OK):
            raise InputFilenameError("Filename '{0}' is not readable".format(filename))
