#!/usr/bin/env python
"""Module containing definition of class ErrorProcess."""

import sys
from .enums.Error import Error


class ErrorProcess:
    """
    Class used for correctly ending program while different type of error occurred.
    Class also used for printing error logs to stderr.
    """

    @staticmethod
    def print_warning(message):
        """
        Function prints warning log message to stderr.

        :param message: Message which will be printed to stderr.
        """
        sys.stderr.write(f'{sys.argv[0]}:\nWARNING: {message}\n\n')

    @staticmethod
    def process_error(error, message=''):
        """
        Function prints error message and exits program with value of parameter error.

        :param error: Enum value representing error which occurred.

        :param message: Message which will be printed to stderr.
        """
        if error == Error.ARGUMENTS_ERROR:
            sys.stderr.write(f'{sys.argv[0]}:\nERROR: {message}\nTry \'python3 -m filter_rule_analyzer --help\'.\n')

        elif error == Error.FILE_OPENING_ERROR:
            sys.stderr.write(f'{sys.argv[0]}:\nERROR: Error while opening file with path: \'{message}\'.\n')

        elif error == Error.RULE_FORMAT_ERROR:
            sys.stderr.write(f'{sys.argv[0]}:\nERROR: Error while processing file with format: \'{message}\'.\n')

        elif error == Error.CREATING_FILE_ERROR:
            sys.stderr.write(f'{sys.argv[0]}:\nERROR: {message}\n')

        elif error == Error.NO_VALUE_FILTER_SET_ERROR:
            sys.stderr.write(f'{sys.argv[0]}:\nERROR: File with filter rules is empty or has not valuable content.\n')

        exit(error.value)
