#!/usr/bin/env python
"""Module containing definition of enum class FilterRulePartLocation."""

from enum import Enum


class FilterRulePartLocation(Enum):
    """
    Enum for every possible 'location' of these filter rule parameters: port and ip address.
    """

    SOURCE = 0
    """Source location of filter rule parameter."""
    DESTINATION = 1
    """Destination location of filter rule parameter."""
