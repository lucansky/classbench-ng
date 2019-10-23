#!/usr/bin/env python
"""Module containing definition of enum class PPC."""

from enum import Enum


class PPC(Enum):
    """
    Enum for every possible port pair class (PPC).
    PPC is pair consisting of source and destination port classes.
    There are 25 total PPC for every combination of source and destination port classes.
    """

    WC_WC = 0
    """Source port class is WC and destination port class is WC."""
    WC_HI = 1
    """Source port class is WC and destination port class is HI."""
    HI_WC = 2
    """Source port class is HI and destination port class is WC."""
    HI_HI = 3
    """Source port class is HI and destination port class is HI."""
    WC_LO = 4
    """Source port class is WC and destination port class is LO."""
    LO_WC = 5
    """Source port class is LO and destination port class is WC."""
    HI_LO = 6
    """Source port class is HI and destination port class is LO."""
    LO_HI = 7
    """Source port class is LO and destination port class is HI."""
    LO_LO = 8
    """Source port class is LO and destination port class is LO."""
    WC_AR = 9
    """Source port class is WC and destination port class is AR."""
    AR_WC = 10
    """Source port class is AR and destination port class is WC."""
    HI_AR = 11
    """Source port class is HI and destination port class is AR."""
    AR_HI = 12
    """Source port class is AR and destination port class is HI."""
    WC_EM = 13
    """Source port class is WC and destination port class is EM."""
    EM_WC = 14
    """Source port class is EM and destination port class is WC."""
    HI_EM = 15
    """Source port class is HI and destination port class is EM."""
    EM_HI = 16
    """Source port class is EM and destination port class is HI."""
    LO_AR = 17
    """Source port class is LO and destination port class is AR."""
    AR_LO = 18
    """Source port class is AR and destination port class is LO."""
    LO_EM = 19
    """Source port class is LO and destination port class is EM."""
    EM_LO = 20
    """Source port class is EM and destination port class is LO."""
    AR_AR = 21
    """Source port class is AR and destination port class is AR."""
    AR_EM = 22
    """Source port class is AR and destination port class is EM."""
    EM_AR = 23
    """Source port class is EM and destination port class is AR."""
    EM_EM = 24
    """Source port class is EM and destination port class is EM."""
