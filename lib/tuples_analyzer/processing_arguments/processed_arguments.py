#!/usr/bin/env python
"""Module containing definition of class ProcessedArguments."""

import sys
import getopt
from ..processing_errors.enums.Error import Error
from ..processing_errors.error_process import ErrorProcess


class ProcessedArguments:
    """
    Class for processing and storing command line arguments from user.
    """

    def __init__(self):
        """
        Constructor is calling function process_arguments() to process arguments and
        to initialize instance variables with argument values.
        """
        self.rules_path = None
        """Path to file with filter rules."""
        self.format_path = None
        """Path to file with format of filter rules."""
        self.output_path = None
        """Path to file, where user wants to save computed parameters."""
        self.is_stderr_on = False
        """Variable telling, if printing error logs while parsing filter rules is enabled."""
        self.process_arguments()

    def process_arguments(self):
        """
        Function processing command line arguments of program.

        :return: If it processed wrong or no arguments, it prints error message and exits with error code 10.

        If it processed argument -h, it calls function usage() and exit.

        If it processed both mandatory arguments: -r and -f with specified path to file with rules and
        path to file with format of rules, then it initializes instance variables.
        """
        argv = sys.argv[1:]

        rules_path = None
        format_path = None
        output_path = None
        is_stderr_on = False

        try:
            opts, args = getopt.getopt(argv, "r:f:o:lh", ["rules=", "format=", "output=", "logs", "help"])
        except getopt.GetoptError as err:
            ErrorProcess.process_error(Error.ARGUMENTS_ERROR, f'{err}')

        if len(opts) < 1 or len(opts) > 4 or len(args) > 0:
            ErrorProcess.process_error(Error.ARGUMENTS_ERROR, f'Wrong or no arguments selected.')

        for o, a in opts:
            if o in ("-h", "--help"):
                ProcessedArguments.print_manual()
                sys.exit()
            elif o in ("-r", "--rules"):
                rules_path = a
            elif o in ("-f", "--format"):
                format_path = a
            elif o in ("-o", "--output"):
                output_path = a
            elif o in ("-l", "--logs"):
                is_stderr_on = True

        if rules_path is None or format_path is None:
            ErrorProcess.process_error(Error.ARGUMENTS_ERROR, f'Missing argument -r or -f.')
        else:
            self.rules_path = rules_path
            self.format_path = format_path
            self.output_path = output_path
            self.is_stderr_on = is_stderr_on

    @staticmethod
    def print_manual():
        """
        Function prints manual of program.
        """
        print('1.PROGRAM:\n\ttuples_analyzer\n\n'
              '2.FUNCTION:\n\tProgram creates parameter file from statistics and distributions of real filter set.\n\t'
              'File with format of rules is needed for processing filter rules.\n\t'
              'Computed parameters are then used to generate synthetic filter set by tools ClassBench and '
              'ClassBench-ng. \n\tFormat of rules and examples usages of program are described in README file.\n\n'
              '3.USAGE:\n\tpython3 -m tuples_analyzer -r <rules_file> -f <format_file>  [-o <output_file>  -l -h]'
              '\n\n'
              '4.MANDATORY ARGUMENTS:\n'
              '\t-r rules_file  | --rules=rules_file\t\tspecify path to file with filter rules\n'
              '\t-f format_file | --format=format_file\t\tspecify path to file with format of rules\n\n'
              '5.OPTIONAL ARGUMENTS:\n'
              '\t-o output_file | --output=output_file\t\tspecify path to file, which will be created\n'
              '\t\t\t\t\t\t\tto store computed parameters\n\n'
              '\t-l | --logs\t\t\t\t\tprinting error logs during computation is enabled\n'
              '\t-h | --help\t\t\t\t\tdisplay this manual\n'
              '\n6.AUTHOR:\n\tJozef Sabo')
