#!/usr/bin/env python
"""Main module for launching program."""

from .calculation_parameters.parameter_file import ParameterFile
from .processing_arguments.processed_arguments import ProcessedArguments
from .processing_files.processing_file_helper import ProcessingFileHelper
from .processing_rules.filter_rule_generator import FilterRuleGenerator

if __name__ == "__main__":
    # instance of class ProcessedArguments contains all processed command line arguments
    processed_arguments = ProcessedArguments()

    # generator of lines from filter set file
    lines_generator = ProcessingFileHelper.create_lines_generator(processed_arguments.rules_path)

    # string with format of rules in filter set
    rule_format = ProcessingFileHelper.get_format(processed_arguments.format_path)

    # generator of FilterRule class instances
    rule_generator = FilterRuleGenerator.create_generator(lines_generator, rule_format, processed_arguments.is_stderr_on)

    # instance of class ParameterFile creates and holds all parameters
    parameter_file = ParameterFile(rule_generator, processed_arguments.output_path)

    # printing calculated parameters to output
    parameter_file.print_parameters()
