"""
json_log_parser.exceptions.input_filename_error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when input filename is not valid or not accessible
Useful to gracefully handle invalid user input
"""


class InputFilenameError(Exception):
    pass
