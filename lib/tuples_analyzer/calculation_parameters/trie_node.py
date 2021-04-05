#!/usr/bin/env python
"""Module containing definition of class TrieNode."""


class TrieNode:
    """
    Class is representing node of trie (binary prefix tree).
    """

    def __init__(self, bit):
        """
        Constructor initialize node instance variable bit with value of parameter bit.
        Other instance variable are initialized as empty list, zero or None.

        :param bit: Bit value.
        """
        self.parent = None
        """Parent of node. Only root node does not have parent."""
        self.bit = bit
        """Last bit of prefix. For trie nodes can be bit value '0' or '1'. Bit of root node is '*'."""
        self.prefix = False
        """Instance variable prefix is boolean type and is telling, if node is prefix or only node on path to prefix."""
        self.level = 0
        """Prefix level of node in trie."""
        self.children = []
        """List holding instances of children nodes. Trie node can have max. 2 children."""
        self.prefixes = [0, 0]
        """List with prefix counts under children nodes."""
        self.threshold = 0
        """Prefix nesting threshold."""
        self.max_level = 0
        """Highest prefix level of node in trie. Only root node uses this variable while printing distributions."""

    def get_prefix(self, prefix):
        """
        Function returns instance of child node in trie represented by prefix string given by parameter.

        :param prefix: String consisting of numbers 0 and 1.

        :return: If node was found return instance of that node, otherwise return None.
        """
        # trying to find node in trie, which is representing wanted string of prefix
        node = self
        for bit in prefix:
            bit_not_found = True

            for child in node.children:
                if child.bit == bit:
                    bit_not_found = False
                    node = child
                    break

            if bit_not_found:
                return None

        # checking if found node is prefix or only path to some different prefix
        if node.prefix:
            return node
        else:
            return None

    def add_prefix(self, prefix):
        """
        Function adds new prefix to trie.
        Process of adding new prefix always starts from root node.

        :param prefix: String consisting of numbers 0 and 1.
        """
        already_in_trie = self.get_prefix(prefix)

        # if prefix is already in trie, function only needs recalculate prefix counts of parent nodes
        if already_in_trie:
            TrieNode.recalculate_prefix_counts(already_in_trie)

        else:
            node = self

            # search for bit in children of present node, or add a new node to trie if not found
            for bit in prefix:
                found_in_child = False

                for child in node.children:
                    if child.bit == bit:
                        node = child
                        found_in_child = True
                        break

                if not found_in_child:
                    new_node = TrieNode(bit)
                    new_node.level = node.level + 1
                    new_node.parent = node
                    node.children.append(new_node)
                    node = new_node

            # mark new node as prefix
            node.prefix = True

            # update max level of root node
            if node.level > self.max_level:
                self.max_level = node.level

            # recalculate prefix counts of parent nodes
            TrieNode.recalculate_prefix_counts(node)

            # recalculate prefix nesting thresholds of current and parent nodes
            TrieNode.recalculate_prefix_thresholds(node)

    def count_skew(self):
        """
        Function computes skew of current node. It is called only on nodes, which have 2 children.

        :return: Computed skew.
        """
        if self.prefixes[0] > self.prefixes[1]:
            bigger = self.prefixes[0]
            smaller = self.prefixes[1]
        else:
            bigger = self.prefixes[1]
            smaller = self.prefixes[0]

        skew = 1 - smaller / bigger
        return skew

    @staticmethod
    def recalculate_prefix_counts(node):
        """
        After adding node to trie, recalculation of prefix counts of parent nodes has to be done.

        :param node: Instance of newly added node to trie.
        """
        child = node
        parent = child.parent

        while parent:
            if child.bit == '0':
                parent.prefixes[0] += 1
            elif child.bit == '1':
                parent.prefixes[1] += 1

            child = parent
            parent = child.parent

    @staticmethod
    def recalculate_prefix_thresholds(node):
        """
        After adding new node to trie, calculation of prefix nesting threshold of current node and recalculation of
        parent thresholds has to be done.

        :param node: Instance of newly added node to trie.
        """
        # finding bigger of children thresholds
        bigger_child_threshold = 0

        for child in node.children:
            child_threshold = 0

            if child.prefix:
                child_threshold += 1

            child_threshold += child.threshold

            if child_threshold > bigger_child_threshold:
                bigger_child_threshold = child_threshold

        # setting threshold of added node
        node.threshold = bigger_child_threshold

        # recalculate prefix nesting thresholds of parent nodes
        child = node
        parent = child.parent
        threshold = bigger_child_threshold + 1

        while parent:
            if threshold > parent.threshold:
                parent.threshold = threshold
            else:
                break

            if parent.prefix:
                threshold += 1

            child = parent
            parent = child.parent
