#!/usr/bin/env python
"""Module containing definition of class ProcessingFileHelper."""

from ..processing_errors.enums.Error import Error
from ..processing_errors.error_process import ErrorProcess


class ProcessingFileHelper:
    """
    Class contains only static functions to help with processing of files.
    """

    @staticmethod
    def create_lines_generator(file_path):
        """
        Function creates generator of lines from file.

        :param file_path: Path to file.

        :return: Generator of lines in file.
        If function can not open file, it prints error message and exits with error code 20.
        """
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    yield line.strip()
        except EnvironmentError:
            ErrorProcess.process_error(Error.FILE_OPENING_ERROR, file_path)

    @staticmethod
    def get_format(file_path):
        """
        Function processes file with format of rules and returns format from first line of file.

        :param file_path: Path to file with format of rule.

        :return: First line of file.
        If line is empty, it prints error message and exits with error code 30.
        """
        rule_format = ''

        for line in ProcessingFileHelper.create_lines_generator(file_path):
            rule_format = line
            break

        if not rule_format or rule_format.isspace():
            ErrorProcess.process_error(Error.RULE_FORMAT_ERROR, file_path)
        else:
            return rule_format
