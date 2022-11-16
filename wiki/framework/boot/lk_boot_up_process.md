# bootloader（LK）启动过程分析

LK Overview
----------------------------------------------------------------------------------------------------

LK是android的BootLoader程序，负责：
1. 硬件初始化，包括：建立向量表，MMU，cache，初始化外设，存储器，USB，加密等
2. 从存储器中加载boot.img
3. 支持flash和recovery


ENV Setup
----------------------------------------------------------------------------------------------------

### Download Code
```
git clone git://codeaurora.org/kernel/lk.git

# checkout a specific branch
git checkout –b ‘<the branch name we want to give>’ <commit id from caf>
```

### 编译
直接在源码中运行如下命令：
```
make aboot
```

## 启动流程

在`/bootable/bootloader/lk/arch/arm/system-onesegment.ld`连接文件中`ENTRY(_start)`指定`LK`从`_start`函数开始：

```
/bootable/bootloader/lk/arch/arm/system-onesegment.ld

ENTRY(_start)
SECTIONS
{
    ...
}
```

`_start`在`/bootable/bootloader/lk/arch/arm/crt0.S`中。`crt0.S`主要做一些基本的`CPU`的初始化再通过`bl  kmain`跳转到`C`代码中：
```
/bootable/bootloader/lk/arch/arm/crt0.S

.globl _start
_start:
...
	bl		kmain
	b		.
```

```
/bootable/bootloader/lk/app/app.c

/* one time setup */
void apps_init(void)
{
	const struct app_descriptor *app;

	/* call all the init routines */
	for (app = &__apps_start; app != &__apps_end; app++) {
		if (app->init)
			app->init(app);
	}

	/* start any that want to start on boot */
	for (app = &__apps_start; app != &__apps_end; app++) {
		if (app->entry && (app->flags & APP_FLAG_DONT_START_ON_BOOT) == 0) {
			start_app(app);
		}
	}
}
```

1. LK简介
----------------------------------------------------------------------------------------------------
`LK`是`Little Kernel`它是`appsbl`（`Applications ARM Boot Loader`）流程代码，`little kernel`是小内核小操作系统。其代码在`bootable/bootloadler/lk`目录下，结构如下：

```
+app            // 应用相关
+arch           // arm 体系
+dev            // 设备相关
+include        // 头文件
+kernel         // lk系统相关
+platform       // 相关驱动
+projiect       // makefile文件
+scripts        // Jtag 脚本
+target         // 具体板子相关
```

LK 流程分析
          在 bootable/bootloadler/lk/arch/arm/ssystem-onesegment.ld 连接文件中 ENTRY（_start）指定 LK 从_start 函数开始，_start 在 lk/arch/crt0.S中 。crt0.S 主要做一些基本的 CPU 的初始化再通过 bl  kmain ；跳转到 C 代码中。
          kmain 在 lk/kernel/main.c 中

kmain()
            kmain 主要做两件事：1、本身 lk 这个系统模块的初始化；2、boot 的启动初始化动作。
            kmain 源码分析：
             void kmain（）
          {
           1.初始化进程（lk 中的简单进程）相关结构体。
             thread_init_early();
           2.做一些如 关闭 cache，使能 mmu 的 arm 相关工作。
            arch_early_init();
           3.相关平台的早期初始化
            platform_early_init();
           4.现在就一个函数跳转，初始化UART（板子相关）
            target_early_init();
           5.构造函数相关初始化
            call_constructors();
           6.lk系统相关的堆栈初始化
            heap_init();
           7.简短的初始化定时器对象
            thread_init();
           8.lk系统控制器初始化（相关事件初始化）
            dpc_init();
           9.初始化lk中的定时器
            timer_init();
           10.新建线程入口函数 bootstrap2 用于boot 工作（重点）
           thread_resume(thread_create("bootstrap2", &bootstrap2, NULL, DEFAULT_PRIORITY, DEFAULT_STACK_SIZE));
         }
   以上与 boot 启动初始化相关函数是 arch_early_init、  platform_early_init 、bootstrap2，这些是启动的重点，我们下面慢慢来看。

arch_early_init()
         体系架构相关的初始化我们一般用的 ARM 体系
         1.关闭cache
         arch_disable_cache(UCACHE);
         2.设置向量基地址（中断相关）
         set_vector_base(MEMBASE);
         3.初始化MMU
         arm_mmu_init();
         4.初始化MMU映射__平台相关
         platform_init_mmu_mappings();
         5.开启cache         
         arch_enable_cache(UCACHE)
         6.使能 cp10 和 cp11
         __asm__ volatile("mrc    p15, 0, %0, c1, c0, 2" : "=r" (val));
         val |= (3<<22)|(3<<20);
         __asm__ volatile("mcr    p15, 0, %0, c1, c0, 2" :: "r" (val));

        7.设置使能 fpexc 位 （中断相关）
        __asm__ volatile("mrc  p10, 7, %0, c8, c0, 0" : "=r" (val));
        val |= (1<<30);
        __asm__ volatile("mcr  p10, 7, %0, c8, c0, 0" :: "r" (val));
        8.使能循环计数寄存器
        __asm__ volatile("mrc    p15, 0, %0, c9, c12, 0" : "=r" (en));
        en &= ~(1<<3); /*循环计算每个周期*/
        en |= 1; 
        __asm__ volatile("mcr    p15, 0, %0, c9, c12, 0" :: "r" (en));
       9.使能循环计数器
       en = (1<<31);
       __asm__ volatile("mcr    p15, 0, %0, c9, c12, 1" :: "r" (en));

platform_early_init()
       平台相关初始化不同平台不同的初始化下面是msm7x30
        1.初始化中断
        platform_init_interrupts();
        2.初始化定时器
        platform_init_timer();

bootstrap2 
         bootstrap2 在kmain的末尾以线程方式开启。主要分三步：platform_init、target_init、apps_init。
        1.platform_init
               platform_init 中主要是函数 acpu_clock_init。
               在 acpu_clock_init 对 arm11 进行系统时钟设置，超频 
        2.target_init
              针对硬件平台进行设置。主要对 arm9 和 arm11 的分区表进行整合，初始化flash和读取FLASH信息
        3.apps_init  
             apps_init 是关键，对 LK 中所谓 app 初始化并运行起来，而 aboot_init 就将在这里开始被运行，Android Linux 内核的加载工作就在 aboot_init 中完成的 。

aboot_init
        1.设置NAND/ EMMC读取信息页面大小
        if (target_is_emmc_boot())
        {
                  page_size = 2048;
                  page_mask = page_size - 1;
        }
       else
       {
                 page_size = flash_page_size();
                 page_mask = page_size - 1;
        }
      2.读取按键信息，判断是正常开机，还是进入 fastboot ,还是进入recovery 模式
       。。。。。。。。。
      通过一系列的 if (keys_get_state() == XXX) 判断
       。。。。。。。。。
      3.从 nand 中加载 内核

    boot_linux_from_flash();
    partition_dump();
    sz = target_get_max_flash_size();
    fastboot_init(target_get_scratch_address(), sz);
    udc_start(); // 开始 USB 协议

boot_linux_from_flash
             主要是内核的加载过程，我们的 boot.img 包含：kernel 头、kernel、ramdisk、second stage（可以没有）。
           1.读取boot 头部
           flash_read(p, offset, raw_header, 2048) 
           offset += 2048;
           2.读取 内核    
           memcmp(hdr->magic, BOOT_MAGIC, BOOT_MAGIC_SIZE)
           n = (hdr->kernel_size + (FLASH_PAGE_SIZE - 1)) & (~(FLASH_PAGE_SIZE - 1));
           flash_read(p, offset, (void*) hdr->kernel_addr, n)
           offset += n;
           3.读取 ramdisk
           n = (hdr->ramdisk_size + (FLASH_PAGE_SIZE - 1)) & (~(FLASH_PAGE_SIZE - 1));
           flash_read(p, offset, (void*) hdr->ramdisk_addr, n)
           offset += n;
            4.启动内核，
                boot_linux()；//在boot_linux 中entry(0,machtype,tags);从kernel加载在内核中的地址开始运行了。
    

到这里LK的启动过程就结束了。  

Reference
----------------------------------------------------------------------------------------------------
* http://blog.csdn.net/jmq_0000/article/details/7378348
* http://www.cnblogs.com/xiaolei-kaiyuan/p/5458145.html