module Classbench

	# Class for representation of a n-ary prefix tree - trie.
	class Tier
		attr_accessor :root

		def insert(prefix)
			self.root = TierNode.new(0) if not root

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
		end
	end
end
