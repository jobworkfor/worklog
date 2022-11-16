目录

* 前言
* 环境搭建
    * [Linux内核0.11完全注释.docx](Linux内核0.11完全注释.docx)
    * [基于QEMU的内核环境搭建](envsetup-qemu_kernel_dev.md)
* 第1章 概述
    * 1.1 Linux的诞生和发展
        * 1.1.1 UNIX、MINIX、GNU和POSIX
        * 1.1.2 Linux操作系统的诞生和版本的变迁
    * 1.2 内容综述
    * 1.3 本章小结
* 第2章 Linux内核体系结构
    * 2.1 Linux内核模式和体系结构
    * 2.2 Linux中断机制
    * 2.3 Linux系统定时
    * 2.4 Linux内核进程控制
        * 2.4.1 任务数据结构
        * 2.4.2 进程运行状态
        * 2.4.3 进程初始化
        * 2.4.4 创建新进程
        * 2.4.5 进程调度
        * 2.4.6 终止进程
    * 2.5 Linux内核对内存的使用方法
    * 2.6 Linux系统中堆栈的使用方法
        * 2.6.1 初始化阶段
        * 2.6.2 任务的堆栈
        * 2.6.3 内核态与用户态堆栈之间的切换
    * 2.7 Linux内核源代码的目录结构
        * 2.7.1 引导启动程序目录 boot
        * 2.7.2 文件系统目录 fs
        * 2.7.3 头文件主目录 include
        * 2.7.4 内核初始化程序目录 init
        * 2.7.5 内核程序主目录 kernel
        * 2.7.6 内核库函数目录 lib
        * 2.7.7 内存管理程序目录mm
        * 2.7.8 编译内核工具程序目录 tools
    * 2.8 内核系统与用户程序的关系
    * 2.9 Linux 内核的编译实验环境
    * 2.10 linux/Makefile 文件
    * 2.11 本章小结
* 第3章 内核引导启动程序
    * 3.1 总体功能描述
    * 3.2 程序分析
        * 3.2.1 bootsect.s 程序
        * 3.2.2 setup.s 程序
        * 3.2.3 head.s 程序
    * 3.3 本章小结
* 第4章 内核初始化过程
    * 4.1 main.c程序分析
    * 4.2 本章小结
* 第5章 进程调度与系统调用
    * 5.1 总体功能描述
        * 5.1.1 中断处理程序
        * 5.1.2 系统调用处理相关程序
    * 5.2 程序分析
        * 5.2.1 asm.s 程序
        * 5.2.2 traps.c 程序
        * 5.2.3 systemcall.s 程序
        * 5.2.4 mktime.c 程序
        * 5.2.5 sched.c 程序
        * 5.2.6 signal.c 程序
        * 5.2.7 exit.c 程序
        * 5.2.8 fork.c 程序
        * 5.2.9 sys.c 程序
        * 5.2.10 vsprintf.c 程序
        * 5.2.11 printk.c 程序
        * 5.2.12 panic.c 程序
    * 5.3 本章小结
* 第6章 输入输出系统——块设备驱动程序
    * 6.1 总体功能描述
        * 6.1.1 块设备请求项和请求队列
        * 6.1.2 块设备操作方式
    * 6.2 程序分析
        * 6.2.1 blk.h 文件
        * 6.2.2 hd.c 程序
        * 6.2.3 llrwblk.c 程序
        * 6.2.4 ramdisk.c 程序
        * 6.2.5 floppy.c 程序
    * 6.3 本章小结
* 第7章 输入输出系统——字符设备驱动程序
    * 7.1 总体功能描述
        * 7.1.1 终端驱动程序基本原理
        * 7.1.2 终端基本数据结构
        * 7.1.3 规范模式和非规范模式
        * 7.1.4 控制台驱动程序
        * 7.1.5 串行终端驱动程序
        * 7.1.6 终端驱动程序接口
    * 7.2 程序分析
        * 7.2.1 keyboard.S 程序
        * 7.2.2 console.c 程序
        * 7.2.3 serial.c 程序
        * 7.2.4 rsio.s 程序
        * 7.2.5 ttyio.c 程序
        * 7.2.6 ttyioctl.c 程序
    * 7.3 本章小结
* 第8章 数学协处理器
    * 8.1 math.emulation.c程序分析
    * 8.2 本章小结
* 第9章 文件系统
    * [自制简单文件系统](自制简单文件系统.md)
    * 9.1 总体功能描述
        * 9.1.1 MINIX文件系统
        * 9.1.2 高速缓冲区
        * 9.1.3 文件系统底层函数
        * 9.1.4 文件中数据的访问操作
    * 9.2 程序分析
        * 9.2.1 buffer.c程序
        * 9.2.2 bitmap.c程序
        * 9.2.3 inode.c程序
        * 9.2.4 super.c程序
        * 9.2.5 namei.c程序
        * 9.2.6 filetable.c程序
        * 9.2.7 blockdev.c程序
        * 9.2.8 filedev.c程序
        * 9.2.9 pipe.c程序
        * 9.2.10 chardev.c程序
        * 9.2.11 readwrite.c程序
        * 9.2.12 truncate.c程序
        * 9.2.13 open.c程序
        * 9.2.14 exec.c程序
        * 9.2.15 stat.c程序
        * 9.2.16 fcntl.c程序
        * 9.2.17 ioctl.c程序
    * 9.3 本章小结
* 第10章 内存管理
    * 10.1 总体功能描述
        * 10.1.1 内存分页管理机制
            * [四级页表](memory-four_level_page_tables.md)
        * 10.1.2 Linux中内存的管理和分配
        * 10.1.3 写时复制机制
    * 10.2 程序分析
        * 10.2.1 memory.c程序
        * 10.2.2 page.s程序
    * 10.3 本章小结
* 电源管理
    * [Linux(android) Suspend流程](电源管理.Linux(android) Suspend流程.md)
    * TODO：[Intelligent Power Allocation (IPA) ](https://developer.arm.com/tools-and-software/open-source-software/linux-kernel/intelligent-power-allocation)
* 时间管理
    * [alarmtimer介绍](time-alarmtimer.md)
* 第11章 包含文件
    * 11.1 程序分析
        * 11.1.1 include/目录下的文件
        * 11.1.2 a.out.h文件
        * 11.1.3 const.h文件
        * 11.1.4 ctype.h文件
        * 11.1.5 errno.h文件
        * 11.1.6 fcntl.h文件
        * 11.1.7 signal.h文件
        * 11.1.8 stdarg.h文件
        * 11.1.9 stddef.h文件
        * 11.1.10 string.h文件
        * 11.1.11 termios.h文件
        * 11.1.12 time.h文件
        * 11.1.13 unistd.h文件
        * 11.1.14 utime.h文件
        * 11.1.15 include/asm/目录下的文件
        * 11.1.16 io.h文件
        * 11.1.17 memory.h文件
        * 11.1.18 segment.h文件
        * 11.1.19 system.h文件
        * 11.1.20 include/linux/目录下的文件
        * 11.1.21 config.h文件
        * 11.1.22 fdreg.h头文件
        * 11.1.23 fs.h文件
        * 11.1.24 hdreg.h文件
        * 11.2.25 head.h文件
        * 11.1.26 kernel.h文件
        * 11.1.27 mm.h文件
        * 11.1.28 sched.h文件
        * 11.1.29 sys.h文件
        * 11.1.30 tty.h文件
        * 11.1.31 include/sys/目录中的文件
        * 11.1.32 stat.h文件
        * 11.1.33 times.h文件
        * 11.1.34 types.h文件
        * 11.1.35 utsname.h文件
        * 11.1.36 wait.h文件
    * 11.2 本章小结
* 第12章 内核库文件
    * 12.1程序分析
        * 12.1.1 exit.c程序
        * 12.1.2 close.c程序
        * 12.1.3 ctype.c程序
        * 12.1.4 dup.c程序
        * 12.1.5 errno.c程序
        * 12.1.6 execve.c程序
        * 12.1.7 malloc.c程序
        * 12.1.8 open.c程序
        * 12.1.9 setsid.c程序
        * 12.1.10 string.c程序
        * 12.1.11 wait.c程序
        * 12.1.12 write.c程序
    * 12.2 本章小结
* 第13章 内核组建工具
    * 13.1 build.c程序分析
    * 13.2 本章小结
* 内核调试
    * [Trace/Log打印](debug-log_trace_print.md)
    * [Pixel3XL串口线制作](debug-hw_Pixel3xl_UART_cable.md)
* 附录
    * [系统调用](appendix-system_call_function.md)
    * [全局符号说明](appendix-macro_and_gVariables.md)
    * [系统文件节点汇总](appendix-fs_node_path.md)
    * [Shell命令](appendix-shell_command.md)



[back to content](../index.md)