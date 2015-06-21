module Classbench

	# Structure representing trie statistics proposed in the ClassBench tool.
	#
	# Array members store statistics defined separately for each level of the
	# trie. Prefix nesting is defined for the whole trie.
	Struct.new("ClassbenchStats",
					# (float[]) number of prefixes (not prefix nodes) with given length
					:prefix_lengths,
					# (float[]) probability of node with only one child (from all non-leaf nodes),
					:branching_one_child,
					# (float[]) probability of node with two children (from all non-leaf nodes)
					:branching_two_children,
					# (float[]) average relative weight ratio of lighter vs heavier subtree (nodes with two children only)
					:skew,
					# (int) maximum number of prefix nodes on an arbitrary path in the trie
					:prefix_nesting)


	# Structure representing statistics related to trie nodes.
	#
	# All the statistics are stored separately for each level of the trie.
	Struct.new("NodeStats",
				:leaf,          # (int[]) number of leaf nodes
				:one_child,     # (int[]) number of nodes with one child only
				:two_children,  # (int[]) number of nodes with both children
				:prefix,        # (int[]) number of prefix nodes (not prefixes)
				:non_prefix     # (int[]) number of non-prefix nodes
				)

	# Structure representing statistics related to the trie.
	#
	# Statistics are divided into two groups:
	#    1) statistics proposed in ClassBench tool and
	#    2) statistics related to trie nodes.
	#
	Struct.new("TrieStats", :classbench_stats, :node_stats)

	# Class for representation of a n-ary prefix tree - trie.
	class Trie
		attr_accessor :root

		def initialize
		end

		def insert(prefix)
			self.root = TrieNode.new(0) if not root

			# Empty prefix
			if prefix.size == 0
				root.increment_prefixes
				return
			end

			current_node = self.root
			next_node = nil

			# For each char
			prefix.split('').each_with_index do |ch, i|
				next_node = current_node.subtree[ch]

				if next_node.nil?
					next_node = TierNode.new(i+1)
					current_node.subtree[ch] = next_node
				end

				current_node = next_node
			end

			current_node.increment_prefixes
		end

		# Erase not implemented/neccessary

		def get_stats
			return if not root
			root.compute_weights

			level = root.level

			que = [root]
			# BFS, append from right, take from left
			while not que.empty?
				node = que.shift # take one from left

				node.subtree.each do |char, subnode|
					que << subnode
				end
			end
		end
	end
end
