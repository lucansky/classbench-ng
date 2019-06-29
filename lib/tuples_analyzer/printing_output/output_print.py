#!/usr/bin/env python
"""Module containing definition of class OutputDirection."""

import os
from .enums.output_direction import OutputDirection
from ..processing_errors.enums.Error import Error
from ..processing_errors.error_process import ErrorProcess


class OutputPrint:
    """
    Class used to print computed parameters in same way to different directions (STDOUT or to file).
    """

    def __init__(self, output_file_path):
        """
        Constructor is calling function decide_direction() to initialize instance variables.

        :param output_file_path: Path to file, where user wants to save computed parameters.
        """
        self.output_direction = None
        """Printing output direction."""
        self.output_file_path = None
        """Path to file, where user wants to save computed parameters."""
        self.decide_direction(output_file_path)

    def decide_direction(self, output_file_path):
        """
        Function decides, where will be printed output.
        If parameter output_file_path is None, output will be printed on STDOUT,
        otherwise output will be printed to file specified by parameter.

        :param output_file_path: Path to file, where user wants to save computed parameters.

        :return: If file where user wants to save computed parameters already exists or is not at least empty,
        then program prints error message and exits with error code 40.
        """
        if output_file_path is None:
            self.output_direction = OutputDirection.STDOUT

        else:
            if not os.path.isfile(output_file_path) or os.stat(output_file_path).st_size == 0:
                try:
                    with open(output_file_path, 'a+'):
                        pass

                except EnvironmentError:
                    ErrorProcess.process_error(Error.CREATING_FILE_ERROR,
                                               f'Wrong path to file where you want to save computed parameters: '
                                               f'\'{output_file_path}\'.')
                self.output_direction = OutputDirection.FILE
                self.output_file_path = output_file_path
            else:
                ErrorProcess.process_error(Error.CREATING_FILE_ERROR,
                                           f'File where you want to save computed parameters: '
                                           f'\'{output_file_path}\' '
                                           f'already exists.')

    def print(self, message):
        """
        Function prints message to output direction specified in instance variable output_direction.

        :param message: String message.
        """
        if self.output_direction == OutputDirection.STDOUT:
            print(message)
        else:
            with open(self.output_file_path, 'a+') as the_file:
                the_file.write(str(message) + '\n')
