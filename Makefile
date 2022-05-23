obj-m += winesync.o
ccflags-y := -std=gnu99 -Wno-declaration-after-statement
KERNEL_SOURCE_DIR := /lib/modules/$(shell uname -r)/build

all:
	make -C "$(KERNEL_SOURCE_DIR)" M="$(PWD)" modules

clean:
	make -C "$(KERNEL_SOURCE_DIR)" M="$(PWD)" clean
