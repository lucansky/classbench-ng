#!/usr/bin/env python
"""Module containing definition of enum class Protocol."""

from .ordered_enum import OrderedEnum


class Protocol(OrderedEnum):
    """
    Enum for every protocol located in ClassBench example parameter files.
    Enum values are given by protocol number definition by IANA.
    """

    ANY = 0
    """Wildcard protocol."""
    ICMP = 1
    """Internet Control Message."""
    IGMP = 2
    """Internet Group Management."""
    GGP = 3
    """Gateway-to-Gateway."""
    ST = 5
    """Stream."""
    TCP = 6
    """Transmission Control."""
    EGP = 8
    """Exterior Gateway Protocol."""
    UDP = 17
    """User Datagram."""
    GRE = 47
    """Generic Routing Encapsulation."""
    ESP = 50
    """Encap Security Payload."""
    AH = 51
    """Authentication Header."""
    EIGRP = 88
    """EIGRP."""
    OSPFIGP = 89
    """OSPFIGP."""
