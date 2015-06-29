module Classbench
	class Rule
		attr_accessor :attributes

		def initialize(attrs)
			self.attributes = attrs
		end

		def fields
			attributes.keys
		end
	end
end
