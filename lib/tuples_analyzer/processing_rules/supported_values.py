#!/usr/bin/env python
"""Module containing global lists of supported protocols, wildcard representations and valuable format parameters."""
from .enums.protocol_numbers import Protocol

supported_protocols = [str(e.name).lower() for e in Protocol]
format_parameters = ["PROTOCOL", "SRC_IP", "SRC_PORT", "DST_IP", "DST_PORT"]
supported_wildcard_list = ["any", "all", "*", "ip", "0"]

