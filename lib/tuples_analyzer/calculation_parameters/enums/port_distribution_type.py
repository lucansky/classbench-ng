#!/usr/bin/env python
"""Module containing definition of enum class PortDistributionType."""

from enum import Enum


class PortDistributionType(Enum):
    """
    Enum for every possible distribution type of port values.
    """

    SPAR = 0
    """Source arbitrary port ranges distribution."""
    SPEM = 1
    """Source exact match ports distribution."""
    DPAR = 2
    """Destination arbitrary port ranges distribution."""
    DPEM = 3
    """Destination exact match ports distribution."""
