#!/usr/bin/env python
"""Module containing definition of class ProtocolPpcDistribution."""

from .distribution import Distribution
from .interfaces.IParameter import IParameter
from ..value_formats.value_format import Format
from ..processing_rules.enums.port_pair_class import PPC


class ProtocolPpcDistribution(IParameter):
    """
    Class representing parameter: port pair classes (PPCs) distribution over unique protocols in filter set.
    """

    def __init__(self):
        """
        Constructor only initialize instance variable distribution as new instance of dictionary.
        """
        self.distribution = dict()
        """Instance variable of type dictionary. Elements in dictionary have protocol enum value as key and 
        instance of class Distribution as value."""

    def extract_data(self, filter_rule):
        """
        Function fills dictionary (instance variable distribution) with new elements and data.
        If protocol extracted from filter rule is new key in dictionary, then it adds new element
        with this key to dictionary.
        Value (instance of class Distribution) of element with extracted protocol as key is always updated
        with PPC class of filter rule.

        :param filter_rule: FilterRule instance.
        """
        if filter_rule.protocol not in self.distribution:
            self.distribution[filter_rule.protocol] = Distribution()

        self.distribution.get(filter_rule.protocol).add_value(filter_rule.get_ppc_class())

    def compute_parameter(self):
        """
        Function computes parameter from all elements stored in dictionary (instance variable distribution).

        :return: PPCs distribution over protocols in string format.
        """
        parameter = ""

        # total count of processed protocols in all filter rules
        rules_count = sum([value.total_count for key, value in self.distribution.items()])
        first = True

        for protocol, value in sorted(self.distribution.items()):

            # for first protocol we do not want print new line
            if first:
                first = False
            else:
                parameter += '\n'

            # total count of processed filter rules with specific protocol
            protocol_count = value.total_count
            parameter += str(protocol.value) + '\t' + str(Format.decimal(protocol_count / rules_count))

            i = 0
            while i < 25:
                ppc_distribution = value.distribution[PPC(i)]
                parameter += '\t' + str(Format.decimal(ppc_distribution / protocol_count))
                i += 1

        return parameter

    def print_parameter(self, output):
        """
        Function calls method compute_parameter() to compute parameter and then prints parameter to output in
        ClassBench format.

        :param output: OutputPrint instance.
        """
        output.print('-prots')
        output.print(self.compute_parameter())
        output.print('#')
