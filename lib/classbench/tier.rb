class Trie
	attr_accessor :root

	def insert(prefix)
		if not root
			root = TrieNode.new(0)
		end
	end
end