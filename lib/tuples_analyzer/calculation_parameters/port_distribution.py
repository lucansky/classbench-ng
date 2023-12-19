#!/usr/bin/env python
"""Module containing definition of class PortDistribution."""

from .distribution import Distribution
from .enums.port_distribution_type import PortDistributionType
from .interfaces.IParameter import IParameter
from ..value_formats.value_format import Format
from ..processing_rules.enums.port_class import PC


class PortDistribution(IParameter):
    """
    Class representing parameter: port values distribution.
    There are 4 types of port values distributions (SPAR, SPEM, DPAR, DPEM).
    Type of distribution tells from which port values of filter rules will be created distribution.
    Types are more described in enum class PortDistributionClass.
    """

    def __init__(self, port_distribution_type):
        """
        Parameter of constructor decides which type of port values distribution will be represented by created instance
        of that class.

        :param port_distribution_type: Enum value of type of port values distribution.
        """
        self.distribution_type = port_distribution_type
        """Type of port values distribution."""
        self.distribution = Distribution()
        """Distribution of unique port values."""

    def extract_data(self, filter_rule):
        """
        Function updates instance variable distribution with new counts of unique port values extracted from filter rules.

        :param filter_rule: FilterRule instance.
        """
        if self.distribution_type == PortDistributionType.SPAR and filter_rule.src_port_class == PC.AR:
            self.distribution.add_value(filter_rule.src_port)

        elif self.distribution_type == PortDistributionType.SPEM and filter_rule.src_port_class == PC.EM:
            self.distribution.add_value(filter_rule.src_port)

        elif self.distribution_type == PortDistributionType.DPAR and filter_rule.dst_port_class == PC.AR:
            self.distribution.add_value(filter_rule.dst_port)

        elif self.distribution_type == PortDistributionType.DPEM and filter_rule.dst_port_class == PC.EM:
            self.distribution.add_value(filter_rule.dst_port)

    def compute_parameter(self):
        """
        Function computes parameter from all counts of unique port values stored in instance variable distribution.

        :return: Port values distribution in string format.
        """
        parameter = ""

        first = True
        for port_range in self.distribution.distribution.most_common():

            # for first port range we do not want print new line
            if first:
                first = False
            else:
                parameter += '\n'

            parameter += str(Format.decimal(port_range[1] / self.distribution.total_count)) + '\t' + str(port_range[0])
        return parameter

    def print_parameter(self, output):
        """
        Function calls method compute_parameter() to compute parameter and then prints parameter to output in
        ClassBench format.

        :param output: OutputPrint instance.
        """
        output.print('-' + str(self.distribution_type)[-4:].lower())
        if self.distribution.total_count != 0:
            output.print(self.compute_parameter())
        output.print('#')
