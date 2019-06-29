#!/usr/bin/env python
"""Module containing definition of enum class FilterRulePartType."""

from enum import Enum


class FilterRulePartType(Enum):
    """
    Enum for every possible type of filter rule part. One word of filter rule is considered as filter part.
    """

    ANY = 0
    """Representation of wildcard value."""
    PROTOCOL = 1
    """Network protocol abbreviation."""
    IP_ADDRESS = 2
    """IP address without mask."""
    IP_ADDRESS_MASK = 3
    """IP address with mask."""
    PORT = 4
    """Port value."""
    PORT_RANGE = 5
    """Port range value."""
    NUMBER = 6
    """Number bigger than 65535 (not used for computation parameters e.g. precedence number)."""
    KEYWORD = 7
    """Word which is part of rule format definition e.g. from, to."""
    WORD = 8
    """Every other value."""

