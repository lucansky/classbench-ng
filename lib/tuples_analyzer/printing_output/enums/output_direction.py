#!/usr/bin/env python
"""Module containing definition of enum class OutputDirection."""

from enum import Enum


class OutputDirection(Enum):
    """
    Enum for every possible output direction of program.
    """

    STDOUT = 0
    """Standard output."""
    FILE = 1
    """Output to file."""
