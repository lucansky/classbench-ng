# Compilation of classbench

all: compile

download:
	# Make backup of db_generator if exists
	-[ -d db_generator ] && mv db_generator db_generator-$(shell date --rfc-3339=seconds | tr ' ' '_')

	# Download and unpack ClassBench
	wget -O- -q http://www.arl.wustl.edu/classbench/db_generator.tar.gz | tar -xvz

patch: download
	# Apply patches from ../patches
	git apply --directory=vendor/db_generator ../patches/ipv6.patch

	# Patching PortList (extension of preallocated array is necessary)
	# Raise limit of L5 rules from 200 to 20000.
	sed -i 's/200/20000/' db_generator/PortList.h

compile: patch

	# Recurse to ClassBench compilation
	make -C db_generator -B db_generator
