# !/usr/bin/env python
"""Module containing definition of class PpcPrefixLenDistribution."""

from .distribution import Distribution
from .interfaces.IParameter import IParameter
from ..value_formats.value_format import Format


class PpcPrefixLenDistribution(IParameter):
    """
    Class representing parameter: prefix lengths distribution from rules with same port pair class (PPC).
    There are total 25 PPCs, so for every group of rules with same PPC program has to create one independent instance of
    class.
    """

    def __init__(self, port_pair_class):
        """
        Constructor decides from which rules will be made prefix lengths distribution. Decision is made by enum value of
        PPC given by parameter of constructor.

        :param port_pair_class: Enum value of PPC.
        """
        self.port_pair_class = port_pair_class
        """PPC of rules from which is made distribution."""
        self.distribution = dict()
        """Instance variable of type dictionary. Elements in dictionary have total prefix length as key and 
        instance of class Distribution as value. In value of dictionary are stored counts of unique source prefix 
        lengths."""

    def extract_data(self, filter_rule):
        """
        Function fills dictionary (instance variable distribution) with new elements and data (counts of unique lengths).
        If total prefix length extracted from filter rule is new key in dictionary, then add new element to dictionary
        with this key.
        Value (instance of class Distribution) of element with extracted total prefix length as key is always updated
        with source prefix length of filter rule.

        :param filter_rule: FilterRule instance.
        """
        if self.port_pair_class == filter_rule.get_ppc_class():
            total_length = filter_rule.src_ip_add_prefix_length + filter_rule.dst_ip_add_prefix_length

            if total_length not in self.distribution:
                self.distribution[total_length] = Distribution()

            self.distribution.get(total_length).add_value(filter_rule.src_ip_add_prefix_length)

    def compute_parameter(self):
        """
        Function computes parameter from all elements stored in dictionary (instance variable distribution).

        :return: Prefix lengths distribution in string format.
        """
        parameter = ""

        # total count of processed rules with same PPC
        rules_count = sum([value.total_count for key, value in self.distribution.items()])

        first = True
        for total_prefix_length, value in sorted(self.distribution.items()):

            # for first total prefix length we do not want print new line
            if first:
                first = False
            else:
                parameter += '\n'

            # total count of rules with same total prefix length
            total_prefix_len_count = value.total_count

            parameter += str(total_prefix_length) + ',' + str(Format.decimal(total_prefix_len_count / rules_count))

            for source_prefix_length in sorted(value.distribution):
                # total count of rules with same source prefix length
                src_prefix_len_count = value.distribution[source_prefix_length]

                parameter += '\t' + str(source_prefix_length) + ','
                parameter += str(Format.decimal(src_prefix_len_count / total_prefix_len_count))

        return parameter

    def print_parameter(self, output):
        """
        Function calls method compute_parameter() to compute parameter and then prints parameter to output in
        ClassBench format.

        :param output: OutputPrint instance.
        """
        output.print('-' + str(self.port_pair_class)[-5:].lower())
        if self.distribution:
            output.print(self.compute_parameter())
        output.print('#')
