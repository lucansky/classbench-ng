#!/usr/bin/env python
"""Module containing definition of interface IParameter."""

from abc import ABCMeta, abstractmethod


class IParameter:
    """
    Interface which has to be implemented by all parameter computation classes.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_data(self, filter_rule):
        """
        Function extracts all needed data from FilterRule instance to compute specific parameter.
        Extracted data are stored in instance variables.

        :param filter_rule: FilterRule instance.
        """
        pass

    @abstractmethod
    def compute_parameter(self):
        """
        Function computes parameter from all extracted data.

        :return: Computed parameter.
        """
        pass

    @abstractmethod
    def print_parameter(self, output):
        """
        Function prints parameter to output in ClassBench format.

        :param output: OutputPrint instance.
        """
        pass
