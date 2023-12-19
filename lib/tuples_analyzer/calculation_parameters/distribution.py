#!/usr/bin/env python
"""Module containing definition of class Distribution."""

from collections import Counter


class Distribution:
    """
    Class representing distribution over different type of values.
    """

    def __init__(self):
        """
        Constructor initialize instance variable total_counts with zero.
        Variable distribution is initialized as new instance of class Counter.
        Counter is collection for counting objects.
        """
        self.total_count = 0
        """Total count of values in distribution."""
        self.distribution = Counter()
        """Variable holding count of every unique value in distribution."""

    def add_value(self, value):
        """
        When adding new value to distribution, total counts of values has to be incremented by one and
        instance variable distribution has to be updated with new value (updating counts of unique values in collection
        Counter).

        :param value: Distribution value.
        """
        self.total_count += 1
        self.distribution.update({value: 1})
