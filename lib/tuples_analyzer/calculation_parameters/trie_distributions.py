#!/usr/bin/env python
"""Module containing definition of class TrieDistributions."""

from .enums.trie_type import TrieType
from .interfaces.IParameter import IParameter
from .trie_node import TrieNode
from ..value_formats.value_format import Format


class TrieDistributions(IParameter):
    """
    Class representing 3 parameters gained by constructing binary prefix tree (trie).
    These parameters are: distributions over prefix branching probability, skew average and prefix nesting threshold.
    """

    def __init__(self, trie_type):
        """
        Constructor decides from which prefixes (source/destination) will be created trie. Decision is made by enum
        value of trie type given by parameter.

        :param trie_type: Enum value of trie type.
        """
        self.trie_type = trie_type
        """Type of trie is telling from which prefixes is trie constructed (source/destination prefixes)."""
        self.root_node = TrieNode('*')
        """Root node of trie. Trie is constructed by adding new prefixes to root."""

    def extract_data(self, filter_rule):
        """
        Function is filling trie with source or destination prefixes extracted from filter rule.

        :param filter_rule: FilterRule instance.
        """
        if self.trie_type == TrieType.SPT and filter_rule.src_ip_add_bin != '*':
            self.root_node.add_prefix(filter_rule.src_ip_add_bin)

        elif self.trie_type == TrieType.DPT and filter_rule.dst_ip_add_bin != '*':
            self.root_node.add_prefix(filter_rule.dst_ip_add_bin)

    def compute_parameter(self):
        """
        Function computes parameters from constructed trie.

        :return: Computed parameters of trie distributions in string form.
        """
        parameter = ""
        first = True
        i = 0

        # checking if trie is not empty
        if self.root_node.children:
            # current level nodes
            nodes = [self.root_node]

            while self.root_node.max_level > i:

                # for first level we do not want print new line
                if first:
                    first = False
                else:
                    parameter += '\n'

                count_1child = 0
                count_2children = 0
                # skew values on level
                skew_list = []
                # nodes on next level are stored here
                temp_list = []

                for node in nodes:
                    if len(node.children) == 1:
                        count_1child += 1
                        temp_list.extend(node.children)
                    elif len(node.children) == 2:
                        count_2children += 1
                        temp_list.extend(node.children)
                        skew_list.append(node.count_skew())

                nodes = temp_list
                parameter += str(i) + '\t' + TrieDistributions.get_branching_probability(count_1child, count_2children)
                parameter += '\t' + TrieDistributions.get_average_skews(skew_list)
                i += 1

        # for undefined levels of trie, lines have this format:
        while i < 33:
            if first:
                first = False
            else:
                parameter += '\n'
            parameter += str(i) + "\t0.00000000\t0.00000000\t0.00000000"
            i += 1

        return parameter

    def print_parameter(self, output):
        """
        Function calls method compute_parameter() to compute parameter and then prints parameter to output in
        ClassBench format.

        :param output: OutputPrint instance.
        """
        if self.trie_type == TrieType.SPT:
            output.print('-snest')
            output.print(str(self.root_node.threshold))
            output.print('#')
            output.print('-sskew')
            output.print(self.compute_parameter())
            output.print('#')

        elif self.trie_type == TrieType.DPT:
            output.print('-dnest')
            output.print(str(self.root_node.threshold))
            output.print('#')
            output.print('-dskew')
            output.print(self.compute_parameter())
            output.print('#')

    @staticmethod
    def get_branching_probability(count_1child, count_2children):
        """
        Function returns probability of node having 1 child or 2 children on some level of prefix trie.

        :param count_1child: Count of nodes with 1 child on level.

        :param count_2children: Count of nodes with 2 children on level.

        :return: Probability of node having 1 child or 2 children on level.
        """
        sum = count_1child + count_2children
        probability_1child = Format.decimal(count_1child / sum)
        probability_2children = Format.decimal(count_2children / sum)
        probability = str(probability_1child) + '\t' + str(probability_2children)
        return probability

    @staticmethod
    def get_average_skews(skew_list):
        """
        Function returns average of skews in list given by parameter.

        :param skew_list: List with skew values.

        :return: Average of skew values in list.
        """
        # skew list is empty
        if len(skew_list) == 0:
            return '0.00000000'

        count_skews = 0
        sum_skews = 0

        for skew in skew_list:
            sum_skews += skew
            count_skews += 1

        skew_average = str(Format.decimal(sum_skews / count_skews))
        return skew_average
