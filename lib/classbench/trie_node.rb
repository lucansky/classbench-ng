class TrieNode
	attr_accessor :level           # depth of node
	attr_accessor :prefixes_count  # number of occurences of the prefix

	attr_accessor :subtree # Hash mapping character -> TrieNode
	attr_accessor :subtree_weights

	def initialize(level)
		self.prefixes_count = 0

		self.subtree = {}
		self.subtree_weights = {}

		self.level = level
	end

	def compute_weights
		weight = 0

		subtree.each do |char, st|
			self.subtree_weights[char] = st.compute_weights
			weight += self.subtree_weights[char]
		end

		weight += self.prefixes_count
	end

	def increment_prefixes
		self.prefixes_count += 1
	end
end
