require 'ipaddress'

module Classbench
	class Rule
		CLASSBENCH_FORMAT = /^@(?<src_ip>.*)\/(?<src_ip_prefix>\d+)\t(?<dst_ip>.*)\/(?<dst_ip_prefix>\d+)\t(?<src_port_from>\d+) : (?<src_port_to>\d+)\t(?<dst_port_from>\d+) : (?<dst_port_to>\d+)\t(?<proto>0x[0-9a-f]+?)\/(.*)\t?$/

		attr_accessor :attributes

		def initialize(attrs)
			self.attributes = attrs
			convert_ports

			#p port_class_name
		end

		def self.from_classbench_format(line)
			match = line.match(CLASSBENCH_FORMAT)
			src_ip = match[:src_ip]+"/"+match[:src_ip_prefix]
			dst_ip = match[:dst_ip]+"/"+match[:dst_ip_prefix]
			src_port_range = (match[:src_port_from].to_i..match[:src_port_to].to_i)
			dst_port_range = (match[:dst_port_from].to_i..match[:dst_port_to].to_i)
			protocol = match[:proto].to_i(16)

			#p [src_ip, dst_ip, protocol, src_port_range, dst_port_range]
			r = Rule.new({"nw_proto" => protocol,
							"nw_src" => src_ip,
							"nw_dst" => dst_ip})
			r.attributes["tp_src"] = src_port_range
			r.attributes["tp_dst"] = dst_port_range

			return r
		end

		def src_length
			IPAddress.parse(attributes["nw_src"] || '0.0.0.0').prefix.to_i
		end

		def dst_length
			IPAddress.parse(attributes["nw_dst"] || '0.0.0.0').prefix.to_i
		end

		def remove_missing_attributes(attrs)
			attributes.keep_if {|a| attrs.include?(a)}
		end

		def convert_ports
			# TODO: Accepting only exact match
			if attributes["tp_src"]
				attributes["tp_src"] = attributes["tp_src"].to_i(attributes["tp_src"] =~ /^0x/ ? 16 : 10)
				# Convert to range
				attributes["tp_src"] = (attributes["tp_src"]..attributes["tp_src"])
			end

			if attributes["tp_dst"]
				attributes["tp_dst"] = attributes["tp_dst"].to_i(attributes["tp_dst"] =~ /^0x/ ? 16 : 10)
				# Convert to range
				attributes["tp_dst"] = (attributes["tp_dst"]..attributes["tp_dst"])
			end
		end

		def protocol
			if attributes["nw_proto"]
				attributes["nw_proto"].to_i
			else
				0
			end
		end

		def fields
			attributes.keys
		end

		# Returns string representation of port class
		def port_class_name
			"#{src_port_range_group.upcase}/#{dst_port_range_group.upcase}"
		end

		def port_class
			PortClass.name_to_index(port_class_name)
		end

		def src_port_range_group
			PortClass.port_range_group(attributes["tp_src"] || (0..65535))
		end

		def dst_port_range_group
			PortClass.port_range_group(attributes["tp_dst"] || (0..65535))
		end

		def of_format

		end

		def l2_vendor(type)
			begin
				attributes["dl_#{type}"][0,8]
			rescue NoMethodError
				nil
			end
		end

		def to_vswitch_format
			attributes.to_a.map { |k,v| "#{k}=#{v}" }.join(", ")
		end

	end
end
