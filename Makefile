
# Recurse into vendor and run Makefile
# (downloads, patches and compiles ClassBench)
all:
	make -C vendor all

clean:
	$(MAKE) -C vendor $@
