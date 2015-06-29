module Classbench
	DEFAULT_DEPTH = 32

	# Structure representing trie statistics proposed in the ClassBench tool.
	#
	# Array members store statistics defined separately for each level of the
	# trie. Prefix nesting is defined for the whole trie.
	class ClassbenchStats
		# (float[]) number of prefixes (not prefix nodes) with given length
		attr_accessor :prefix_lengths

		# (float[]) probability of node with only one child (from all non-leaf nodes),
		attr_accessor :branching_one_child

		# (float[]) probability of node with two children (from all non-leaf nodes)
		attr_accessor :branching_two_children

		# (float[]) average relative weight ratio of lighter vs heavier subtree (nodes with two children only)
		attr_accessor :skew

		# (int) maximum number of prefix nodes on an arbitrary path in the trie
		attr_accessor :prefix_nesting

		def initialize
			preinitialized_hash = Hash[*(0..DEFAULT_DEPTH).flat_map { |k, v| [k , 0.0] }]

			self.prefix_lengths         = preinitialized_hash.dup
			self.branching_one_child    = preinitialized_hash.dup
			self.branching_two_children = preinitialized_hash.dup
			self.skew                   = preinitialized_hash.dup
			self.prefix_nesting         = 0
		end
	end


	# Structure representing statistics related to trie nodes.
	#
	# All the statistics are stored separately for each level of the trie.
	class NodeStats
		attr_accessor :leaf           # (int[]) number of leaf nodes
		attr_accessor :one_child      # (int[]) number of nodes with one child only
		attr_accessor :two_children   # (int[]) number of nodes with both children
		attr_accessor :prefix         # (int[]) number of prefix nodes (not prefixes)
		attr_accessor :non_prefix     # (int[]) number of non-prefix nodes

		def initialize
			preinitialized_hash = Hash[*(0..DEFAULT_DEPTH).flat_map { |k, v| [k , 0] }]

			self.leaf         = preinitialized_hash.dup;
			self.one_child    = preinitialized_hash.dup;
			self.two_children = preinitialized_hash.dup;
			self.prefix       = preinitialized_hash.dup;
			self.non_prefix   = preinitialized_hash.dup;
		end
	end

	# Class representing statistics related to the trie.
	#
	# Statistics are divided into two groups:
	#    1) statistics proposed in ClassBench tool and
	#    2) statistics related to trie nodes.
	#
	class TrieStats
		attr_accessor :classbench
		attr_accessor :nodes

		def initialize
			self.classbench = ClassbenchStats.new
			self.nodes = NodeStats.new
		end
	end

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
					next_node = TrieNode.new(i+1)
					current_node.subtree[ch] = next_node
				end

				current_node = next_node
			end

			current_node.increment_prefixes
		end

		def self.get_prefix_nesting(node)
			if node # non-empty subtree
			   # get prefix nesting from successor nodes
			   zero_nesting = get_prefix_nesting(node.subtree["0"])
			   one_nesting = get_prefix_nesting(node.subtree["1"])
			   # will this node increase prefix nesting?
			   if node.prefixes_count > 0 # this is a prefix node
				  is_prefix = 1
			   else
				  is_prefix = 0
			   end

			   # return maximum of successors' nesting, possibly incremented
			   if zero_nesting > one_nesting
				  return zero_nesting + is_prefix
			   else
				  return one_nesting + is_prefix
			   end
			else # empty subtree
			   return 0
			end
		end

		# Erase not implemented/neccessary

		def get_stats
			stats = TrieStats.new

			return stats if not root
			root.compute_weights

			level = root.level

			que = [root]
			# BFS, append from right, take from left
			while not que.empty?
				node = que.shift # take one from left

				node.subtree.each do |char, subnode|
					que << subnode
				end

				# level change - finish statistics computation for the previous level
				if node.level != level
					# auxiliary variables
					one_child = stats.nodes.one_child[level];
					two_children = stats.nodes.two_children[level];
					sum = one_child + two_children;
					# branching_one_child and branching_two_children
					if sum != 0
						stats.classbench.branching_one_child[level] =
							one_child.to_f / sum;
						stats.classbench.branching_two_children[level] =
							two_children.to_f / sum;
					end
					# skew
					if two_children != 0
						stats.classbench.skew[level] /= two_children.to_f;
					end
					# increment the level counter
					level += 1;
				end

				# trie node visit - classbench statistics
				stats.classbench.prefix_lengths[level] += node.prefixes_count;
				if node.subtree["0"] and node.subtree["1"] # skew is defined
					if node.zero_weight > node.one_weight # lighter 1-subtree
						skew = 1 - (node.one_weight.to_f / node.zero_weight);
					else # lighter 0-subtree
						skew = 1 - (node.zero_weight.to_f / node.one_weight);
					end
					stats.classbench.skew[level] += skew;
				end

				# trie node visit - nodes statistics
				if node.subtree["0"].nil?
					if node.subtree["1"].nil? # leaf node
						stats.nodes.leaf[level] += 1
					else # one child node
						stats.nodes.one_child[level] += 1
					end
				else # node->zero != NULL
					if node.subtree["1"] # two child node
						stats.nodes.two_children[level] += 1
					else # one child node
						stats.nodes.one_child[level] += 1
					end
				end

				if node.prefixes_count > 0 # prefix node
					stats.nodes.prefix[level] += 1
				else # non-prefix node
					stats.nodes.non_prefix[level] += 1
				end

			end # end of while BFS

			# finish statistics computation for the last level
			# auxiliary variables
			one_child = stats.nodes.one_child[level]
			two_children = stats.nodes.two_children[level]
			sum = one_child + two_children
			# branching_one_child and branching_two_children
			if sum != 0
				stats.classbench.branching_one_child[level] =
					one_child.to_f / sum
				stats.classbench.branching_two_children[level] =
					two_children.to_f / sum
			end
			# skew
			if two_children != 0
				stats.classbench.skew[level] /= two_children.to_f
			end
			# compute prefix nesting
			stats.classbench.prefix_nesting = Trie.get_prefix_nesting(root)

			return stats
		end # end of get_stats
	end
end
