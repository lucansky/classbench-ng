require_relative 'classbench/trie'
require_relative 'classbench/trie_node'
require_relative 'classbench/analyser'
require_relative 'classbench/rule'
require 'ip' # ruby-ip gem
require 'pp'

module Classbench
	def self.generate_prefix
		len = rand(33)

		(0...len).map { [0,1][rand(2)]}.join
	end

	def self.ip_to_binary_string(ip)
		ip = IP.new(ip)
		ip.to_b.to_s[0,ip.pfxlen]
	end

	def self.load_prefixes_from_file(filename)
		t = Trie.new

		prefixes = File.readlines(filename).map(&:chomp)
		prefixes.each do |pfx|
			t.insert ip_to_binary_string(pfx)
		end
		t
	end

	def self.analyse(filename)
		analyser = Analyser.new
		analyser.parse_openflow(File.read(filename))
		100.times { p analyser.generate }
	end

	def self.hi
		t = Trie.new
		#2.times { t.insert "101" }
		#3.times { t.insert "100" }
		100_000.times { t.insert generate_prefix }
		puts "Stats"
		pp t.get_stats

		puts "Done"
	end
end
