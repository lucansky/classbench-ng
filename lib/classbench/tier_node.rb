class TrieNode
	attr_accessor :level           # depth of node
	attr_accessor :prefixes_count  # number of occurences of the prefix

	# 0-subtree-related members
	attr_accessor :zero_subtree    # subtree
	attr_accessor :zero_weight     # number of prefixes in the subtree

	# 1-subtree-related members
	attr_accessor :one_subtree     # subtree
	attr_accessor :one_weight      # number of prefixes in the subtree

	def initialize(level)
		self.prefixes_count = 0
		
		self.zero_weight = 0
		self.one_weight = 0

		self.level = level
	end
end