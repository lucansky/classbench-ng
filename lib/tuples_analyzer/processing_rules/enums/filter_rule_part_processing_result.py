#!/usr/bin/env python
"""Module containing definition of enum class FilterRulePartProcessingResult."""

from enum import Enum


class FilterRulePartProcessingResult(Enum):
    """
    Enum for every possible result scenario while processing filter rule part into FilterRule instance.
    """

    MANDATORY_PART_PROCESSED = 0
    """Mandatory part of filter rule was processed."""
    OPTIONAL_PART_PROCESSED = 1
    """Optional part of filter rule was processed."""
    MANDATORY_PART_MISSING = 2
    """Mandatory part of filter rule is missing."""
    OPTIONAL_PART_MISSING = 3
    """Optional part of filter rule is missing."""
