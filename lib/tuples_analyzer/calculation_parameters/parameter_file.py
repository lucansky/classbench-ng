#!/usr/bin/env python
"""Module containing definition of class ParameterFile."""

from .enums.port_distribution_type import PortDistributionType
from .enums.trie_type import TrieType
from .port_distribution import PortDistribution
from .ppc_prefixlen_distribution import PpcPrefixLenDistribution
from .prefix_correlation_distribution import PrefixCorrelationDistribution
from .protocol_ppc_distribution import ProtocolPpcDistribution
from .trie_distributions import TrieDistributions
from ..printing_output.output_print import OutputPrint
from ..processing_rules.enums.port_pair_class import PPC


class ParameterFile:
    """
    Class representing parameter file.
    Every parameter located in ClassBench parameter file has its own class.
    This class holds all instances of parameter classes required to create desired parameter file.
    """
    loaded_rules = 0
    """Count of processed rules in process of extraction data."""

    def __init__(self, rule_generator, output_path):
        """
        Constructor initialize instance variables as new instances of parameter classes, rule generator class
        and output class.
        It also calls function load_rules() to load parameter instances with extracted data from filter rules.

        :param rule_generator: Generator of FilterRule instances.

        :param output_path: Path to file, where user wants to save computed parameters.
        """
        self.rule_generator = rule_generator
        """Generator of FilterRule instances."""
        self.output = OutputPrint(output_path)
        """Instance of class used to print computed parameters to output."""
        self.protocol_ppc_distribution = ProtocolPpcDistribution()
        """Instance of class ProtocolPpcDistribution."""
        self.port_distributions = []
        """List of instances of class PortDistribution."""
        i = 0
        while i < 4:
            self.port_distributions.insert(i, PortDistribution(PortDistributionType(i)))
            i += 1

        self.ppc_prefix_length_distributions = []
        """List of instances of class PpcPrefixLenDistribution."""
        i = 0
        while i < 25:
            self.ppc_prefix_length_distributions.insert(i, PpcPrefixLenDistribution(PPC(i)))
            i += 1

        self.trie_distributions = []
        """List of instances of class TrieDistributions."""
        i = 0
        while i < 2:
            self.trie_distributions.insert(i, TrieDistributions(TrieType(i)))
            i += 1

        self.prefix_correlation_distribution = PrefixCorrelationDistribution()
        """Instance of class PrefixCorrelationDistribution."""

        self.load_parameters()

    def load_parameters(self):
        """
        Function fills structures of all parameter instances with data needed to calculate parameters.
        Data are extracted from generator of FilterRule instances.
        """
        for rule in self.rule_generator:
            self.protocol_ppc_distribution.extract_data(rule)

            for port_distribution in self.port_distributions:
                port_distribution.extract_data(rule)

            for ppc_prefix_length_distribution in self.ppc_prefix_length_distributions:
                ppc_prefix_length_distribution.extract_data(rule)

            for trie_distributions in self.trie_distributions:
                trie_distributions.extract_data(rule)

            self.prefix_correlation_distribution.extract_data(rule)
            ParameterFile.loaded_rules += 1

    def print_parameters(self):
        """
        Function calls print functions of all parameter instances to print calculated parameters in ClassBench format.
        """
        self.output.print('-scale')
        self.output.print(str(ParameterFile.loaded_rules))
        self.output.print('#')

        self.protocol_ppc_distribution.print_parameter(self.output)

        self.output.print('-flags')
        self.output.print('#')

        self.output.print('-extra')
        self.output.print('0')
        self.output.print('#')

        for port_distribution in self.port_distributions:
            port_distribution.print_parameter(self.output)

        for ppc_prefix_length_distribution in self.ppc_prefix_length_distributions:
            ppc_prefix_length_distribution.print_parameter(self.output)

        for trie_distributions in self.trie_distributions:
            trie_distributions.print_parameter(self.output)

        self.prefix_correlation_distribution.print_parameter(self.output)
