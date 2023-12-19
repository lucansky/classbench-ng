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
    IPV4_ADDRESS = 2
    """IPv4 address without mask."""
    IPV4_ADDRESS_MASK = 3
    """IPv4 address with mask."""
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
    IPV6_ADDRESS = 9
    """IPv6 address without mask."""
    IPV6_ADDRESS_MASK = 10
    """IPv6 address with mask."""
