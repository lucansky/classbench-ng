# Compilation of classbench

all: compile

download:
	wget -O- -q http://www.arl.wustl.edu/classbench/db_generator.tar.gz | tar -xvz

compile: download
	make -C db_generator -B db_generator
