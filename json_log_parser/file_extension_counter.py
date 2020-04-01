"""
json_log_parser.file_extension_counter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains functionality to count number of unique file extensions
that were found during log paring
"""

from collections import defaultdict


class FileExtensionCounter:
    def __init__(self):
        """
        Constructor
        Defaultdict sets the value to 0 for all new keys. This eliminates the need
        to check if the key exists before incrementing the count
        """
        self.file_extension_count = defaultdict(int)

    @staticmethod
    def get_no_extension():
        """
        Returns a string that will be used to group all files that do not have extension
        :return: str
        """
        return 'no_extension'

    def add_extension_from_filename(self, filename):
        """
        Extracts the extension from the filename and increments the count in the dictionary
        :param filename:
        """
        if not filename:
            return

        extension = self.parse_extension(filename)
        self.file_extension_count[extension] += 1

    def parse_extension(self, filename):
        """
        Split the filename using '.' character and take the last element of the array.
        If the split yields a single element the filename will be counted under the
        'no_extension' category
        :param filename:
        """
        split_filename = filename.split('.')
        if len(split_filename) > 1:
            return split_filename[-1]
        else:
            return self.get_no_extension()

    def get_extension_counts(self):
        return self.file_extension_count
