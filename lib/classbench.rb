require 'classbench/trie'
require 'classbench/trie_node'

require 'pp'

module Classbench
	def self.generate_prefix
		len = rand(33)

		(0...len).map { [0,1][rand(2)]}.join
	end

	def self.hi
		t = Trie.new
		#2.times { t.insert "101" }
		#3.times { t.insert "100" }
		500_000.times { t.insert generate_prefix }
		puts "Stats"
		t.get_stats

		puts "Done"



	end
end
