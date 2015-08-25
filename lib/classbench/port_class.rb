class PortClass
	# Incorrect
	# CLASS_NAMES = [	"WC/WC", "WC/LO", "WC/HI", "WC/AR", "WC/EM",
	# 				"LO/WC", "LO/LO", "LO/HI", "LO/AR", "LO/EM",
	# 				"HI/WC", "HI/LO", "HI/HI", "HI/AR", "HI/EM",
	# 				"AR/WC", "AR/LO", "AR/HI", "AR/AR", "AR/EM",
	# 				"EM/WC", "EM/LO", "EM/HI", "EM/AR", "EM/EM"]

	CLASS_NAMES = [ "WC/WC", "WC/HI", "HI/WC", "HI/HI", "WC/LO",
					"LO/WC", "HI/LO", "LO/HI", "LO/LO", "WC/AR",
					"AR/WC", "HI/AR", "AR/HI", "WC/EM", "EM/WC",
					"HI/EM", "EM/HI", "LO/AR", "AR/LO", "LO/EM",
					"EM/LO", "AR/AR", "AR/EM", "EM/AR", "EM/EM"]

	def self.name_to_index(name)
		CLASS_NAMES.find_index(name)
	end

	def self.port_range_group(range)
		return :wc if not range

		if range.first == range.last
			return :em
		elsif range == (0..1023)
			return :lo
		elsif range == (1024..65535)
			return :hi
		elsif range == (0..65535)
			return :wc
		end

		return :ar
	end
end
