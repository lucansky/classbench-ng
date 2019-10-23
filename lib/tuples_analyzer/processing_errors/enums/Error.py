#!/usr/bin/env python
"""Module containing definition of enum class Error."""

from enum import Enum


class Error(Enum):
    """
    Enum for every possible error, which can occur in program.
    """

    ARGUMENTS_ERROR = 10
    """Error which occurred while processing command line arguments."""
    FILE_OPENING_ERROR = 20
    """Error which occurred while opening file."""
    RULE_FORMAT_ERROR = 30
    """Error which occurred while processing file with format of rules."""
    CREATING_FILE_ERROR = 40
    """Error which occurred while creating file for storing output parameters."""
    NO_VALUE_FILTER_SET_ERROR = 50
    """Error telling that file with filter rules has no valuable content in it."""
