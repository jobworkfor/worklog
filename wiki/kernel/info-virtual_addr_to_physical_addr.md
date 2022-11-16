首先摘录如下URL对pagemap的描述。

https://www.kernel.org/doc/Documentation/vm/pagemap.txt

```cpp
 * /proc/pid/pagemap.  This file lets a userspace process find out which
   physical frame each virtual page is mapped to.  It contains one 64-bit
   value for each virtual page, containing the following data (from
   fs/proc/task_mmu.c, above pagemap_read):


    * Bits 0-54  page frame number (PFN) if present
    * Bits 0-4   swap type if swapped
    * Bits 5-54  swap offset if swapped
    * Bit  55    pte is soft-dirty (see Documentation/vm/soft-dirty.txt)
    * Bits 56-60 zero
    * Bit  61    page is file-page or shared-anon
    * Bit  62    page swapped
    * Bit  63    page present


   If the page is not present but in swap, then the PFN contains an
   encoding of the swap file number and the page's offset into the
   swap. Unmapped pages return a null PFN. This allows determining
   precisely which pages are mapped (or in swap) and comparing mapped
   pages between processes.
```

接下来，我们根据上述描述，给出获取虚拟地址对应的物理地址的代码

```cpp
#include <stdio.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#define    page_map_file     "/proc/self/pagemap"
#define    PFN_MASK          ((((uint64_t)1)<<55)-1)
#define    PFN_PRESENT_FLAG  (((uint64_t)1)<<63)


int mem_addr_vir2phy(unsigned long vir, unsigned long *phy)
{
    int fd;
    int page_size=getpagesize();
    unsigned long vir_page_idx = vir/page_size;
    unsigned long pfn_item_offset = vir_page_idx*sizeof(uint64_t);
    uint64_t pfn_item;
    
    fd = open(page_map_file, O_RDONLY);
    if (fd<0)
    {
        printf("open %s failed", page_map_file);
        return -1;
    }


    if ((off_t)-1 == lseek(fd, pfn_item_offset, SEEK_SET))
    {
        printf("lseek %s failed", page_map_file);
        return -1;
    }


    if (sizeof(uint64_t) != read(fd, &pfn_item, sizeof(uint64_t)))
    {
        printf("read %s failed", page_map_file);
        return -1;
    }


    if (0==(pfn_item & PFN_PRESENT_FLAG))
    {
        printf("page is not present");
        return -1;
    }


    *phy = (pfn_item & PFN_MASK)*page_size + vir % page_size;
    return 0;


}
```

如果担心vir地址对应的页面不在内存中，可以在调用mem_addr_vir2phy之前，先访问一下此地址。

例如， `int  a=*(int *)(void *)vir;`

如果担心Linux的swap功能将进程的页面交换到硬盘上从而导致页面的物理地址变化，可以关闭swap功能。

下面两个C库函数可以阻止Linux将当前进程的部分或全部页面交换到硬盘上。
```cpp
int mlock(const void *addr, size_t len);
int mlockall(int flags);
```
