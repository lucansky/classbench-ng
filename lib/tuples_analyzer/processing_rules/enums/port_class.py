#!/usr/bin/env python
"""Module containing definition of enum class PC."""

from enum import Enum


class PC(Enum):
    """
    Enum for every possible port class (PC).
    """

    WC = 0
    """Wildcard."""
    LO = 1
    """Port range 0:1023."""
    HI = 2
    """Port range 1024:65535."""
    EM = 3
    """Exact match e.g port 80."""
    AR = 4
    """Arbitrary range e.g. port range 50000:51000."""
