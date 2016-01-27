require "base64"
require "yaml"

module Classbench
	class Analyser
		INTERESTING_ATTRIBUTES = %w(dl_dst dl_src dl_type dl_vlan dl_vlan_pcp eth_type in_port nw_dst nw_proto nw_src nw_tos tp_dst tp_src)

		attr_accessor :rules
		attr_accessor :protocol_port_class_stats

		def initialize
			self.rules ||= []
		end

		def parse_openflow(lines)
			lines.split("\n").each do |line|
				# Array of arrays ... [["dl_dst", "fa:16:3e:91:c3:01", ","], ["nw_src", "255.255.255.255", ","],
				attributes = line.scan(/([a-z_\-]+)=([A-Za-z0-9\-_:\.\/]+)(,|\w)?/).
									keep_if {|a| INTERESTING_ATTRIBUTES.include?(a.first) }

				next if attributes.empty?

				rule = {}
				attributes.each do |attr|
					if INTERESTING_ATTRIBUTES.include? attr.first
						rule[attr.first] = attr[1]
					end
				end
				self.rules << Rule.new(rule)
			end
		end

		def generate_seed
			calculate_stats

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

			# FIXME
			seed += "-wc_wc\n0,0.02702703\t0,1.00000000\n13,0.01351351\t13,1.00000000\n14,0.00450450\t14,1.00000000\n15,0.00450450\t15,1.00000000\n16,0.00450450\t16,1.00000000\n17,0.00450450\t17,1.00000000\n20,0.00450450\t0,1.00000000\n24,0.07207207\t0,0.93750000\t24,0.06250000\n28,0.00450450\t0,1.00000000\n32,0.13063063\t0,0.89655173\t32,0.10344828\n45,0.13513513\t13,1.00000000\n46,0.04504504\t14,1.00000000\n47,0.04954955\t15,0.90909094\t23,0.09090909\n48,0.09009009\t16,1.00000000\n51,0.04504504\t19,1.00000000\n56,0.17567568\t24,1.00000000\n58,0.01351351\t27,1.00000000\n59,0.13513513\t27,1.00000000\n62,0.03153153\t30,1.00000000\n64,0.00900901\t32,1.00000000\n#\n-wc_hi\n0,0.00300300\t0,1.00000000\n24,0.01801802\t0,0.83333331\t24,0.16666667\n26,0.00300300\t0,1.00000000\n27,0.01801802\t0,0.33333334\t27,0.66666669\n31,0.00300300\t0,1.00000000\n32,0.14714715\t0,0.93877554\t32,0.06122449\n48,0.01201201\t16,1.00000000\n49,0.00600601\t17,1.00000000\n51,0.00600601\t19,1.00000000\n52,0.00600601\t20,1.00000000\n54,0.00600601\t22,1.00000000\n55,0.04504504\t23,1.00000000\n56,0.16816817\t24,0.91071427\t25,0.03571429\t32,0.05357143\n57,0.04204204\t25,0.71428573\t26,0.28571430\n58,0.06306306\t26,0.71428573\t27,0.28571430\n59,0.06906907\t27,0.95652175\t32,0.04347826\n62,0.01501502\t30,0.80000001\t31,0.20000000\n63,0.00900901\t32,1.00000000\n64,0.36036035\t32,1.00000000\n#\n-hi_wc\n#\n-hi_hi\n#\n-wc_lo\n#\n-lo_wc\n#\n-hi_lo\n#\n-lo_hi\n#\n-lo_lo\n#\n-wc_ar\n0,0.00377358\t0,1.00000000\n8,0.00377358\t8,1.00000000\n12,0.00754717\t12,1.00000000\n16,0.01886792\t16,1.00000000\n19,0.00377358\t19,1.00000000\n21,0.04150943\t21,1.00000000\n23,0.04528302\t23,1.00000000\n24,0.10943396\t24,1.00000000\n27,0.00377358\t27,1.00000000\n31,0.00377358\t0,1.00000000\n32,0.03396226\t0,1.00000000\n45,0.01132075\t13,1.00000000\n46,0.00377358\t14,1.00000000\n47,0.00377358\t15,1.00000000\n48,0.02264151\t16,1.00000000\n49,0.00754717\t17,1.00000000\n51,0.00754717\t19,1.00000000\n52,0.00377358\t20,1.00000000\n53,0.01886792\t21,0.20000000\t26,0.20000000\t27,0.60000002\n54,0.06037736\t22,0.06250000\t27,0.93750000\n55,0.04150943\t23,1.00000000\n56,0.10943396\t24,0.96551722\t25,0.03448276\n57,0.03396226\t25,0.66666669\t26,0.33333334\n58,0.05660377\t26,0.80000001\t27,0.20000000\n59,0.03018868\t27,0.87500000\t32,0.12500000\n60,0.00377358\t29,1.00000000\n61,0.01132075\t29,0.66666669\t30,0.33333334\n62,0.01886792\t30,0.20000000\t31,0.80000001\n63,0.03018868\t31,0.37500000\t32,0.62500000\n64,0.24905661\t32,1.00000000\n#\n-ar_wc\n#\n-hi_ar\n#\n-ar_hi\n#\n-wc_em\n0,0.00253485\t0,1.00000000\n21,0.01140684\t21,1.00000000\n23,0.01267427\t23,1.00000000\n24,0.03105197\t24,1.00000000\n26,0.00063371\t26,1.00000000\n27,0.00316857\t0,0.80000001\t27,0.20000000\n29,0.00063371\t0,1.00000000\n32,0.06147021\t0,0.87628865\t16,0.10309278\t32,0.02061856\n39,0.00126743\t12,1.00000000\n40,0.00887199\t13,1.00000000\n41,0.00570342\t13,0.55555558\t14,0.44444445\n42,0.00506971\t12,0.25000000\t14,0.12500000\t15,0.62500000\n43,0.00760456\t15,0.16666667\t16,0.83333331\n44,0.01077313\t12,0.94117647\t16,0.05882353\n46,0.00253485\t16,0.50000000\t19,0.50000000\n47,0.00190114\t20,1.00000000\n48,0.05513308\t16,0.98850572\t20,0.01149425\n49,0.00697085\t17,0.18181819\t22,0.27272728\t27,0.54545456\n50,0.01013942\t22,0.06250000\t23,0.93750000\n51,0.04816223\t19,0.35526314\t23,0.06578948\t24,0.42105263\t27,0.15789473\n52,0.00950570\t20,0.13333334\t24,0.73333335\t26,0.13333334\n53,0.03231939\t21,0.49019608\t26,0.09803922\t27,0.41176471\n54,0.05703422\t22,0.05555556\t23,0.01111111\t27,0.93333334\n55,0.03358682\t23,0.92452830\t24,0.07547170\n56,0.10709759\t24,0.97633135\t25,0.02366864\n57,0.01837769\t25,0.68965518\t26,0.27586207\t27,0.03448276\n58,0.06147021\t26,0.85567009\t27,0.10309278\t29,0.04123711\n59,0.04879595\t27,0.79220778\t29,0.02597403\t32,0.18181819\n60,0.03231939\t28,0.68627453\t29,0.19607843\t31,0.03921569\t32,0.07843138\n61,0.02471483\t29,0.89743590\t31,0.10256410\n62,0.00253485\t30,0.75000000\t32,0.25000000\n63,0.01837769\t31,0.89655173\t32,0.10344828\n64,0.26615968\t32,1.00000000\n#\n-em_wc\n#\n-hi_em\n#\n-em_hi\n0,0.50000000\t0,1.00000000\n64,0.50000000\t32,1.00000000\n#\n-lo_ar\n#\n-ar_lo\n#\n-lo_em\n#\n-em_lo\n#\n-ar_ar\n#\n-ar_em\n#\n-em_ar\n#\n-em_em\n#\n"

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
				if r.src_port_range_group == port_class.to_sym
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
			self.protocol_port_class_stats = {}
			rules.each do |r|
				protocol_port_class_stats[ r.protocol ] ||= {}
				protocol_port_class_stats[ r.protocol ][r.port_class_name] ||= 0
				protocol_port_class_stats[ r.protocol ][r.port_class_name] += 1
			end
		end

		# TODO: MAC
		def openflow_stats
			{"in_port" => in_ports,
			 "eth_type" => eth_types,
				"dl_src" => vendors("src"),
				"dl_dst" => vendors("dst"),
				"rule_counts" => occurences_of_rule_types}
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
