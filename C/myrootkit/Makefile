KERN_DIR := /lib/modules/$(shell uname -r)/build
obj-m    := lkm.o 

all:
	make -C $(KERN_DIR) M=$(shell pwd) modules
clean:
	make -C $(KERN_DIR) M=$(shell pwd) modules clean
	rm -rf modules.order
	rm -f *.symvers

