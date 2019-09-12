require "base64"
require "yaml"

module Classbench
	class Analyser
		INTERESTING_ATTRIBUTES = %w(dl_dst dl_src dl_type dl_vlan dl_pcp eth_type in_port nw_dst nw_proto nw_src nw_tos tp_dst tp_src)

		attr_accessor :rules
		attr_accessor :protocol_port_class_stats
		attr_accessor :port_class_prefix_lengths
		attr_accessor :omitted_rules_count

		def initialize
			self.rules ||= []
			self.omitted_rules_count = 0
		end

		def parse_openflow(lines)
			lines.split("\n").each do |line|
				# Array of arrays ... [["dl_dst", "fa:16:3e:91:c3:01", ","], ["nw_src", "255.255.255.255", ","],
				attributes = line.scan(/([a-z_\-]+)=([A-Za-z0-9\-_:\.\/]+)(,|\w)?/).
									keep_if {|a| INTERESTING_ATTRIBUTES.include?(a.first) }

				if attributes.empty?
					self.omitted_rules_count += 1
					next
				end

				rule = {}
				attributes.each do |attr|
					if INTERESTING_ATTRIBUTES.include? attr.first
						rule[attr.first] = attr[1]
					end
				end
				self.rules << Rule.new(rule)
			end

			calculate_stats
		end

		def rules_per_port_class(class_name)
			self.port_class_prefix_lengths[class_name].values.map(&:values).flatten.inject(&:+)
		end

		def generate_seed
			seed = ""
			seed += "-scale\n#{rules.size}\n#\n"

			seed += "-prots\n"

			#puts rules.count
			protocol_port_class_stats.each do |protocol_number, port_classes|
				protocol_probability = port_classes.values.inject(&:+) / rules.count.to_f
				#p port_classes
				seed += "#{protocol_number}\t#{protocol_probability}"

				protocol_rule_count = port_classes.values.inject(&:+)

				0.upto(24).each do |i|
					class_name = PortClass::CLASS_NAMES[i]
					probability_of_port_class = (port_classes[class_name]||0)/protocol_rule_count.to_f
					seed += "\t#{probability_of_port_class}"
				end
				seed += "\n"
			end
			seed += "#\n"

			seed += "-flags\n"
			protocol_port_class_stats.each do |protocol_number, port_classes|
				seed += "#{protocol_number}\t0x0000/0x0000,1.00000000\t\n"
			end
			seed += "#\n"

			seed += "-extra\n0\n#\n"

			seed += generate_range_probability("src","ar")
			seed += generate_range_probability("src","em")
			seed += generate_range_probability("dst","ar")
			seed += generate_range_probability("dst","em")

			PortClass::CLASS_NAMES.each do |class_name|
				seed += "-#{class_name.downcase.gsub('/', '_')}"

				rules_of_port_class = rules_per_port_class(class_name)

				# Foreach distinct total length
				self.port_class_prefix_lengths[class_name].each do |total_length, partial_lengths|
					count_of_rules_in_total_length = partial_lengths.values.inject(&:+)
					seed += "\n#{total_length},#{count_of_rules_in_total_length/rules_of_port_class.to_f}\t"

					# Foreach source length
					partial_lengths.each do |length, count|
						seed += "\t#{length},#{count/count_of_rules_in_total_length.to_f}"
					end
				end
				seed += "\n#\n"
			end

			nw_src_trie = Trie.new
			rules.map {|r| r.attributes["nw_src"]}.compact.each do |ip|
				nw_src_trie.insert Classbench::ip_to_binary_string(ip)
			end

			nw_src_stats = nw_src_trie.get_stats

			seed += "-snest\n#{nw_src_stats.classbench.prefix_nesting}\n#\n"

			seed += "-sskew\n"
			seed += nw_src_trie.get_stats.classbench_stats
			seed += "#\n"

			nw_dst_trie = Trie.new
			rules.map {|r| r.attributes["nw_dst"]}.compact.each do |ip|
				nw_dst_trie.insert Classbench::ip_to_binary_string(ip)
			end

			nw_dst_stats = nw_dst_trie.get_stats

			seed += "-dnest\n#{nw_dst_stats.classbench.prefix_nesting}\n#\n"

			seed += "-dskew\n"
			seed += nw_dst_trie.get_stats.classbench_stats
			seed += "#\n"

			#pp nw_dst_trie.get_stats
			seed += "-pcorr\n"
			1.upto(32).each do |i|
				seed += "#{i}\t0.0\n"
			end

			seed += "#\n"

			# Openflow
			seed += "-openflow\n"

			seed += YAML.dump(openflow_stats)
			seed += "#\n"

			seed
		end

		# Direction: "src" or "dst"
		# port_class: "em" or "ar"
		def generate_range_probability(direction, port_class)
			seed = ""
			if direction == "src"
				seed += "-sp#{port_class}\n"
			else
				seed += "-dp#{port_class}\n"
			end

			accumulator = {}
			rules.each do |r|
				rule_port_class = (direction == "src") ? r.src_port_range_group : r.dst_port_range_group

				if rule_port_class == port_class.to_sym
					range = r.attributes["tp_#{direction}"]
					accumulator[range] ||= 0
					accumulator[range] += 1
				end
			end

			total = accumulator.values.inject(&:+)
			accumulator.each do |range, count|
				seed += "#{count/total.to_f}\t#{range.first}:#{range.last}\n"
				#p [count, range]
			end
			seed += "#\n"
		end

		def calculate_stats

			# Port class statistics
			self.protocol_port_class_stats = {}
			rules.each do |r|
				protocol_port_class_stats[ r.protocol ] ||= {}
				protocol_port_class_stats[ r.protocol ][r.port_class_name] ||= 0
				protocol_port_class_stats[ r.protocol ][r.port_class_name] += 1
			end

			# Prefix lengths of dst/src address based on port class
			self.port_class_prefix_lengths = {}

			# Prefill port_class_prefix_lengths with empty hashes
			PortClass::CLASS_NAMES.each {|cn| self.port_class_prefix_lengths[cn] = {}}

			rules.each do |r|
				lengths_of_class = port_class_prefix_lengths[r.port_class_name]

				specific_length = lengths_of_class[r.src_length + r.dst_length] ||= {}
				specific_length[r.src_length] = (specific_length[r.src_length] || 0) + 1
			end
		end

		def openflow_stats
			{"in_port" => in_ports,
			 "eth_type" => eth_types,
			 "dl_src" => vendors("src"),
			 "dl_dst" => vendors("dst"),
			 "unique_vlan_ids_count" => unique_vlans_count,
			 "empty_rules_count" => omitted_rules_count,
			 "rule_distribution" => occurences_of_rule_types}
		end

		# Returns hash with keys MAC address (only vendor part) and values as count
		def vendors(type)
			l2_vendors = rules.map {|r| r.l2_vendor(type)}.compact

			l2_vendors.each_with_object(Hash.new(0)) { |v,counts| counts[v] += 1 }
		end

		def in_ports
			ports = rules.map {|r| r.attributes["in_port"]}.compact
			ports.each_with_object(Hash.new(0)) { |port,counts| counts[port] += 1 }
		end

		def eth_types
			eth_types = rules.map {|r| r.attributes["eth_type"]}.compact
			eth_types.each_with_object(Hash.new(0)) { |eth_type,counts| counts[eth_type] += 1 }
		end

		def unique_vlans_count
			rules.map {|r| r.attributes["dl_vlan"]}.compact.uniq.count
		end

		def occurences_of_rule_types
			rules.each_with_object(Hash.new(0)) { |rule,counts| counts[rule.fields.sort] += 1 }.to_a.map {|a| {"attributes" => a[0], "count" => a[1]}}
		end

		def generate_rule
			random_rule = rules[rand(rules.size)]
			random_rule.fields

			#1. determine its OF type
			#2. remove 5-tuple header fields that ARE NOT defined by the OF type
			#3. add OF-specific header fields that ARE defined by the OF type
			#  1. if the field is ingress port, Ethernet type or IP protocol,
			#  use specified dependencies (see shared Google document) to constrain a set
			#  of possible values for this field
			#  2. generate value for the OF-specific header field in a
			#  specified way (see shared Google document)
			#4. Label all the header fields by the corresponding OF name
		end
	end
end
