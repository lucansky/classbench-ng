#!/usr/bin/env python
"""Module containing definition of enum class TrieType."""

from enum import Enum


class TrieType(Enum):
    """
    Enum for types of trie (binary prefix tree).
    """

    SPT = 0
    """Trie created from source prefixes of filter rules."""
    DPT = 1
    """Trie created from destination prefixes of filter rules."""
