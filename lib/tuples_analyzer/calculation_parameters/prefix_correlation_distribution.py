#!/usr/bin/env python
"""Module containing definition of class PrefixCorrelationDistribution."""

from .interfaces.IParameter import IParameter
from ..value_formats.value_format import Format


class PrefixCorrelationDistribution(IParameter):
    """
    Class representing parameter: prefix correlation distribution.
    Correlation means source and destination prefixes of one filter rule are continuing to be same,
    in length where are both defined.
    """

    def __init__(self):
        """
        Constructor initialize two instance variable as lists with zero values.
        Both lists are sizes of 32. Indexes of lists are representing prefix levels.
        """
        self.all_on_level = [0] * 32
        """List with counts of rules which have same source and destination prefixes until previous level."""
        self.same_on_level = [0] * 32
        """List with counts of rules which source and destination prefixes are same on level."""

    def extract_data(self, filter_rule):
        """
        Function updates counts of rules on levels (indexes) in list instance variables.

        :param filter_rule: FilterRule instance.
        """
        # do not care about prefixes with wildcards
        if filter_rule.src_ip_add_bin != '*' and filter_rule.dst_ip_add_bin != '*':

            # prefix length where are both prefixes defined
            valid_length = PrefixCorrelationDistribution.get_smaller_prefix(filter_rule)

            i = 0
            # going through bits of prefix
            for b in filter_rule.src_ip_add_bin[:valid_length]:

                self.all_on_level[i] += 1

                # if prefixes do not continue to be same break the cycle
                if b == filter_rule.dst_ip_add_bin[i]:
                    self.same_on_level[i] += 1
                else:
                    break

                i += 1

    def compute_parameter(self):
        """
        Function computes parameter from counts of rules stored in list instance variables.

        :return: Prefix correlation distribution in string format.
        """
        parameter = ""
        i = 1
        first = True

        for rules_count in self.all_on_level:

            # for first correlation we do not want print new line
            if first:
                first = False
            else:
                parameter += '\n'

            parameter += str(i) + '\t'
            if rules_count == 0:
                parameter += '0.00000000'
            else:
                parameter += str(Format.decimal(self.same_on_level[i - 1] / rules_count))
            i += 1

        return parameter

    def print_parameter(self, output):
        """
        Function calls method compute_parameter() to compute parameter and then prints parameter to output in
        ClassBench format.

        :param output: OutputPrint instance.
        """
        output.print('-pcorr')
        output.print(self.compute_parameter())
        output.print('#')

    @staticmethod
    def get_smaller_prefix(filter_rule):
        """
        Function returns smaller one prefix length of source and destination prefixes in filter rule.

        :param filter_rule: FilterRule instance.
        :return: Smaller prefix length of prefixes in filter rule.
        """
        if filter_rule.src_ip_add_prefix_length > filter_rule.dst_ip_add_prefix_length:
            return filter_rule.dst_ip_add_prefix_length
        else:
            return filter_rule.src_ip_add_prefix_length
