# Shell Commands


```cpp
PID
Process Id
进程id
       The task's unique process ID, which periodically wraps, though never  restarting at zero.


PPID
Parent Process Pid
父进程id
       The process ID of a task's parent.


RUSER
 Real User Name
Real user name
       The real user name of the task's owner.


UID
User Id
进程所有者的用户id
       The effective user ID of the task's owner.


USER
User Name
进程所有者的用户名
       The effective user name of the task's owner.


GROUP
Group Name
进程所有者的组名
       The effective group name of the task's owner.


TTY
Controlling Tty
启动进程的终端名。不是从终端启动的进程则显示为 ?
       The  name of the controlling terminal.  This is usually the device (serial port, pty, etc.) from which the process was started, and which it uses  for  input  oroutput.   However,  a task need not be associated with a terminal, in which case you'll see '?' displayed.


PR
Priority
优先级
       The priority of the task.


NI
Nice value
nice值。负值表示高优先级，正值表示低优先级
       The nice value of the task.   A  negative  nice  value  means  higher  priority, whereas  a  positive nice value means lower priority.  Zero in this field simply means priority will not be adjusted in determining a task's dispatchability.


P
Last used CPU (SMP)
最后使用的CPU，仅在多CPU环境下有意义
       A number representing the last used processor.  In a true SMP  environment  this will likely change frequently since the kernel intentionally uses weak affinity. Also, the very act of running top may break this weak affinity  and  cause  more processes  to change CPUs more often (because of the extra demand for cpu time).


%CPU
CPU usage
上次更新到现在的CPU时间占用百分比
       The task's share of the elapsed CPU time since the last screen update, expressed as a percentage of total CPU time.  In a true SMP environment, if 'Irix mode' is Off, top will operate in 'Solaris mode' where a task's cpu usage will be divided by  the  total  number  of  CPUs.   You toggle 'Irix/Solaris' modes with the 'I' interactive command.


TIME
CPU Time
进程使用的CPU时间总计，单位秒
       Total CPU time the task has used since it started.  When  'Cumulative  mode'  is On,  each  process is listed with the cpu time that it and its dead children has used.  You toggle 'Cumulative mode' with 'S', which is a command-line option and an interactive command.  See the 'S' interactive command for additional information regarding this mode.


TIME+
CPU Time, hundredths
进程使用的CPU时间总计，单位1/100秒
       The same as 'TIME', but reflecting more granularity through hundredths of a sec          ond.


%MEM
Memory usage (RES)
进程使用的物理内存百分比
       A task's currently used share of available physical memory.


VIRT
Virtual Image (kb)
进程使用的虚拟内存总量，单位kb。VIRT=SWAP+RES
       The total amount of virtual memory used by the task.  It includes all code, data and shared libraries plus pages that have  been  swapped  out.  (Note:  you  can define  the STATSIZE=1 environment variable and the VIRT will be calculated from the /proc/#/state VmSize field.)
       VIRT = SWAP + RES.



SWAP
Swapped size (kb)
进程使用的虚拟内存中，被换出的大小，单位kb。
       The swapped out portion of a task's total virtual memory image.


RES
Resident size (kb)
进程使用的、未被换出的物理内存大小，单位kb。RES=CODE+DATA
       The non-swapped physical memory a task has used.
       RES = CODE + DATA.


CODE
 Code size (kb)
可执行代码占用的物理内存大小，单位kb
       The amount of physical memory devoted to executable  code,  also  known  as  the'text resident set' size or TRS.


DATA
Data+Stack size (kb)
可执行代码以外的部分(数据段+栈)占用的物理内存大小，单位kb
       The  amount of physical memory devoted to other than executable code, also known the 'data resident set' size or DRS.


SHR
Shared Mem size (kb)
共享内存大小，单位kb
       The amount of shared memory used by a task.   It  simply  reflects  memory  that could be potentially shared with other processes.


nFLT
Page Fault count
页面错误次数
       The  number  of  major  page faults that have occurred for a task.  A page fault occurs when a process attempts to read from or write to a virtual page  that  is not  currently  present  in  its address space.  A major page fault is when disk access is involved in making that page available.


nDRT
Dirty Pages count
最后一次写入到现在，被修改过的页面数。
       The number of pages that have been modified since  they  were  last  written  to disk.   Dirty  pages  must  be written to disk before the corresponding physical memory location can be used for some other virtual page.


S
Process Status
进程状态。
            D=不可中断的睡眠状态
            R=运行
            S=睡眠
            T=跟踪/停止
            Z=僵尸进程
       Tasks shown as running should be more properly thought of as 'ready to run'  --their  task_struct is simply represented on the Linux run-queue.  Even without a true SMP machine, you may see numerous tasks in this state  depending  on  top's delay interval and nice value.


COMMAND
 Command line or Program name
命令名/命令行
Display the command line used to start a task or the name of the associated program.  You toggle between command line and name with 'c', which is both  a  command-line option and an interactive command. When  you've  chosen  to display command lines, processes without a command line (like kernel threads) will be shown with only the program name  in  parentheses, as in this example:                ( mdrecoveryd ) Either  form  of  display is subject to potential truncation if it's too long to fit in this field's  current  width.   That  width  depends  upon  other  fields  selected, their order and the current screen width.
       Note: The 'Command' field/column is unique, in that it is not fixed-width.  When displayed, this column will be allocated all remaining screen width (up  to  the maximum  512  characters)  to  provide for the potential growth of program names into command lines.

WCHAN
Sleeping in Function
若该进程在睡眠，则显示睡眠中的系统函数名
       Depending on the availability of the kernel link map ('System.map'), this  field will  show  the  name or the address of the kernel function in which the task is currently sleeping.  Running tasks will display a dash ('-') in this column.
       Note: By displaying this field, top's own working set will be increased by  over 700Kb.   Your  only  means of reducing that overhead will be to stop and restart          top.
       
Flags
Task Flags
任务标志，参考 sched.h
       This column represents the task's current scheduling flags which  are  expressed in  hexadecimal  notation and with zeros suppressed.  These flags are officially documented in <linux/sched.h>.  Less formal documentation can also be  found  on the 'Fields select' and 'Order fields' screens.

```

```cpp
RSS
RSS（ Resident Set Size ）常驻内存集合大小，表示相应进程在RAM中占用了多少内存，并不包含在SWAP中占用的虚拟内存。
即使是在内存中的使用了共享库的内存大小也一并计算在内，包含了完整的在stack和heap中的内存。

VSZ
VSZ （Virtual Memory Size)，表明是虚拟内存大小，表明了该进程可以访问的所有内存，包括被交换的内存和共享库内存。

如果进程A的二进制文件大小为500KB，并且链接到了2500KB的共享库，有200KB的stack/heap大小，这200KB中又有100KB位于内存中，
100KB位于SWAP空间中，并且加载了1000KB的共享库和400KB的自身二进制文件。则

RSS:
400K + 1000K + 100K = 1500K

VSZ
500K + 2500K + 200K = 3200K
```
