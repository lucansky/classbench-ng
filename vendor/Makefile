# Compilation of classbench

# Potential backup time
BACKUP_TIME=$(shell date --rfc-3339=seconds | tr ' ' '_')

all: compile

download:
	# Make backup of db_generator, if exists
	-[ -d db_generator ] && mv db_generator db_generator-$(BACKUP_TIME)

	# Download and unpack ClassBench
	wget -O- -q http://www.arl.wustl.edu/classbench/db_generator.tar.gz | tar -xvz

	# Make backup of parameter_files, if exists
	-[ -d parameter_files ] && mv parameter_files parameter_files-$(BACKUP_TIME)

	# Download and unpack ClassBench parameter files
	wget -O- -q http://www.arl.wustl.edu/classbench/parameter_files.tar.gz | tar -xvz

patch: download
	# Apply patches from ../patches
	git apply --directory=vendor/db_generator ../patches/improvements_ipv6.patch
	#git apply --directory=vendor/db_generator ../patches/ipv6.patch
	#git apply --directory=vendor/db_generator ../patches/improvements.patch

	# Patching PortList (extension of preallocated array is necessary)
	# Raise limit of L5 rules from 200 to 20000.
	sed -i 's/200/20000/' db_generator/PortList.h

compile: patch
	# Recurse to ClassBench compilation
	make -C db_generator -B db_generator

clean:
	rm -rf db_generator* parameter_files*
