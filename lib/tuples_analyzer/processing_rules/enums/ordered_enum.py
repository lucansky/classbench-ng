#!/usr/bin/env python
"""Module containing definition of enum class OrderedEnum."""

from enum import Enum


class OrderedEnum(Enum):
    """
    Class inheriting from base enum class and making enum values comparable.
    """

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
