# LOG、Trace 打印汇总

## LOG打印

printk

````cpp
printk(fmt, ##__VA_ARGS__);
````

pr_xxx 宏

````cpp
#define pr_emerg(fmt, ...) 	printk(KERN_EMERG pr_fmt(fmt), ##__VA_ARGS__)
#define pr_alert(fmt, ...) 	printk(KERN_ALERT pr_fmt(fmt), ##__VA_ARGS__)
#define pr_crit(fmt, ...) 	printk(KERN_CRIT pr_fmt(fmt), ##__VA_ARGS__)
#define pr_err(fmt, ...) 	printk(KERN_ERR pr_fmt(fmt), ##__VA_ARGS__)
#define pr_warning(fmt, ...) 	printk(KERN_WARNING pr_fmt(fmt), ##__VA_ARGS__)
#define pr_warn pr_warning
#define pr_notice(fmt, ...)	printk(KERN_NOTICE pr_fmt(fmt), ##__VA_ARGS__)
#define pr_info(fmt, ...) 	printk(KERN_INFO pr_fmt(fmt), ##__VA_ARGS__)
````

内核使用printk打印出这句log： [ 1463.495062] [5:11331:Binder:1385_1A] [log]

前面的时间戳1463.495062表示1463s+495062us

````cpp
static size_t print_time(u64 ts, char *buf)
{
	unsigned long rem_nsec = do_div(ts, 1000000000);
	return sprintf(buf, "[%5lu.%06lu]",
		       (unsigned long)ts, rem_nsec / 1000);
}
````



## Linux打印内核函数调用栈（dump_stack）

打开debug选项：

````bash
make menuconfig -> kernel hacking--> kernel debug
````

添加调用：

```cpp
#include <asm/ptrace.h>

void foo(){
    ...
    dump_stack();
    ...
}
```

eg.

test.c

````cpp
#include <linux/module.h>   
#include <linux/kernel.h>
#include <linux/init.h>
#include <asm/ptrace.h>
 
void aaa(int a);
void bbb(int b);
void ccc(int c);
 
void aaa(int a)
{
	int b = a + 10;
	bbb(b);
}
 
void bbb(int b)
{
	int c = b + 10;
	ccc(c);
}
 
void ccc(int c)
{
	dump_stack();
	printk("c is %d\n",c);
}
 
static int __init my_init( void )
{
	int a = 10;
	aaa(a);
	printk("my_init \n");  
}
 
static void __exit my_exit(void )
{
    	printk("my_exit \n");	
}
 
module_init(my_init);
module_exit(my_exit);
MODULE_LICENSE("GPL");
````

Makefile

```makefile
ifneq   ($(KERNELRELEASE),)
obj-m   := test.o
 
else
KDIR    := /lib/modules/$(shell uname -r)/build
PWD     := $(shell pwd)
default:        
	$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules 
	rm -r -f .tmp_versions *.mod.c .*.cmd *.o *.symvers 
 
endif
```

dmesg

````bash
[ 1311.888605] Call Trace:
[ 1311.888612]  [<ffffffffa001a000>] ? 0xffffffffa0019fff
[ 1311.888616]  [<ffffffff816cd58e>] dump_stack+0x19/0x1b
[ 1311.888619]  [<ffffffffa038c015>] ccc+0x15/0x30 [test]
[ 1311.888621]  [<ffffffffa038c041>] bbb+0x11/0x20 [test]
[ 1311.888623]  [<ffffffffa038c061>] aaa+0x11/0x14 [test]
[ 1311.888625]  [<ffffffffa001a00e>] my_init+0xe/0x1000 [test]
[ 1311.888628]  [<ffffffff81002122>] do_one_initcall+0xf2/0x1a0
[ 1311.888632]  [<ffffffff810c3ef3>] load_module+0x1403/0x1c00
[ 1311.888637]  [<ffffffff8134fab0>] ? ddebug_add_module+0xf0/0xf0
[ 1311.888639]  [<ffffffff810c47d1>] SyS_init_module+0xe1/0x130
[ 1311.888643]  [<ffffffff816dc86f>] tracesys+0xe1/0xe6
[ 1311.888645] c is 30
[ 1311.888645] my_init 
````















>   [back to content](index.md)