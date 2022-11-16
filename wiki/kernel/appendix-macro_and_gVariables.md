# 全局宏和全局变量

## 全局宏

### EXPORT_SYMBOL_GPL

When a loadable module is inserted, any references it makes to kernel functions and data structures must be linked to the current running kernel. The module loader does not provide access to all kernel symbols, however; only those which have been explicitly exported are available. The export requirement narrows the API seen by modules, though not by all that much: there are over 6,000 symbols exported in the 2.6.13 kernel.
Exports come in two flavors: vanilla (EXPORT_SYMBOL) and GPL-only (EXPORT_SYMBOL_GPL). The former are available to any kernel module, while the latter cannot be used by any modules which do not carry a GPL-compatible license. The module loader will enforce this distinction by denying access to GPL-only symbols if the module's declared license does not pass muster. Currently, less that 10% of the kernel's symbols are GPL-only, but the number of GPL-only symbols is growing. There is a certain amount of pressure to make new exports GPL-only in many cases.

It has often been argued that there is no practical difference between the two types of exports. Those who believe that all kernel modules are required by the kernel license to be GPL-licensed see all symbols as being implicitly GPL-only in any case. Another camp, which sees the module interface as a boundary which the GPL cannot cross, does not believe that GPL-only restrictions can be made to stick. In any case, GPL-only symbols can be easily circumvented by patching the kernel, falsely declaring a GPL-compatible license, or by inserting a shim module which provides wider access to the symbols of interest.

Linus, however, believes that GPL-only exports are significant.
* I've talked to a lawyer or two, and (a) there's an absolutely _huge_ difference and (b) they liked it.
* The fact is, the law isn't a blind and mindless computer that takes what you say literally. Intent matters a LOT. And using the xxx_GPL() version to show that it's an internal interface is very meaningful indeed.
* One of the lawyers said that it was a much better approach than trying to make the license explain all the details - codifying the intention in the code itself is not only more flexible, but a lot less likely to be misunderstood.

He also points out that circumventing a GPL-only export requires an explicit action, making it clear that the resulting copyright infringement was a deliberate act.

Regardless of any legal significance they may have, the GPL-only exports do succeed in communicating the will of the large subset of the kernel development community which wants to restrict the use of non-free kernel modules. The outright banning of such modules may not be on the agenda anytime soon, but the functionality available to them is not likely to grow much.

https://lwn.net/Articles/154602/



### container_of

Your usage example `container_of(dev, struct wifi_device, dev);` might be a bit misleading as you are mixing two namespaces there.

While the first `dev` in your example refers to the name of pointer the second `dev` refers to the name of a structure member.

Most probably this mix up is provoking all that headache. In fact the `member` parameter in your quote refers to the name given to that member in the container structure.

Taking this container for example:

```c
struct container {
  int some_other_data;
  int this_data;
}
```

And a pointer `int *my_ptr` to the `this_data` member you'd use the macro to get a pointer to `struct container *my_container` by using:

```c
struct container *my_container;
my_container = container_of(my_ptr, struct container, this_data);
```

Taking the offset of `this_data` to the beginning of the struct into account is essential to getting the correct pointer location.

Effectively you just have to subtract the offset of the member `this_data` from your pointer `my_ptr` to get the correct location.

That's exactly what the last line of the macro does.

https://stackoverflow.com/questions/15832301/understanding-container-of-macro-in-the-linux-kernel





## 全局变量

### current 

```c
// xref: /kernel/msm-5.4/arch/arm64/include/asm/current.h

/* SPDX-License-Identifier: GPL-2.0 */
#ifndef __ASM_CURRENT_H
#define __ASM_CURRENT_H
#include <linux/compiler.h>
#ifndef __ASSEMBLY__
struct task_struct;

/*
 * We don't use read_sysreg() as we want the compiler to cache the value where
 * possible.
 */
static __always_inline struct task_struct *get_current(void)
{
	unsigned long sp_el0;
	asm ("mrs %0, sp_el0" : "=r" (sp_el0));
	return (struct task_struct *)sp_el0;
}

#define current get_current()
#endif /* __ASSEMBLY__ */
#endif /* __ASM_CURRENT_H */
```

````cpp
// xref: /kernel/msm-5.4/include/linux/sched.h

struct task_struct {
...
};
````

More information in [Linux Device Drivers](http://www.xml.com/ldd/chapter/book/ch02.html) chapter 2:

>   The current pointer refers to the user process currently executing. During the execution of a system call, such as open or read, the current process is the one that invoked the call. Kernel code can use process-specific information by using current, if it needs to do so. [...]

https://stackoverflow.com/questions/12434651/what-is-the-current-in-linux-kernel-source

