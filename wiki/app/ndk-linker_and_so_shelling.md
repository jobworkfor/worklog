【腾讯Bugly干货分享】Android Linker 与 SO 加壳技术
==============================================

1. 前言

Android 系统安全愈发重要，像传统pc安全的可执行文件加固一样，应用加固是Android系统安全中非常重要的一环。目前Android 应用加固可以分为dex加固和Native加固，Native 加固的保护对象为 Native 层的 SO 文件，使用加壳、反调试、混淆、VM 等手段增加SO文件的反编译难度。目前最主流的 SO 文件保护方案还是加壳技术， 在SO文件加壳和脱壳的攻防技术领域，最重要的基础的便是对于 Linker 即装载链接机制的理解。对于非安全方向开发者，深刻理解系统的装载与链接机制也是进阶的必要条件。

本文详细分析了 Linker 对 SO 文件的装载和链接过程，最后对 SO 加壳的关键技术进行了简要的介绍。

对于 Linker 的学习，还应该包括 Linker 自举、可执行文件的加载等技术，但是限于本人的技术水平，本文的讨论范围限定在 SO 文件的加载，也就是在调用dlopen("libxx.SO")之后，Linker 的处理过程。

本文基于 Android 5.0 AOSP 源码，仅针对 ARM 平台，为了增强可读性，文中列举的源码均经过删减，去除了其他 CPU 架构的相关源码以及错误处理。

P.S. :阅读本文的读者需要对 ELF 文件结构有一定的了解。

2. SO 的装载与链接

2.1 整体流程说明

1. do_dlopen
调用 dl_open 后，中间经过 dlopen_ext, 到达第一个主要函数 do_dlopen:

 soinfo* do_dlopen(const char* name, int flags, const Android_dlextinfo* extinfo) {
   protect_data(PROT_READ | PROT_WRITE);
   soinfo* si = find_library(name, flags, extinfo); // 查找 SO
   if (si != NULL) {
     si->CallConstructors(); // 调用 SO 的 init 函数
   }
   protect_data(PROT_READ);
   return si;
 }
do_dlopen 调用了两个重要的函数，第一个是find_library, 第二个是 soinfo 的成员函数 CallConstructors，find_library 函数是 SO 装载链接的后续函数， 完成 SO 的装载链接后， 通过 CallConstructors 调用 SO 的初始化函数。

2. find_library_internal
find_library 直接调用了 find_library_internal，下面直接看 find_library_internal函数:

 static soinfo* find_library_internal(const char* name, int dlflags, const Android_dlextinfo* extinfo) {
   if (name == NULL) {
     return somain;
   }
   soinfo* si = find_loaded_library_by_name(name);  // 判断 SO 是否已经加载
   if (si == NULL) {
     TRACE("[ '%s' has not been found by name.  Trying harder...]", name);
     si = load_library(name, dlflags, extinfo);     // 继续 SO 的加载流程
   }
   if (si != NULL && (si->flags & FLAG_LINKED) == 0) {
     DL_ERR("recursive link to \"%s\"", si->name);
     return NULL;
   }
   return si;
 }
find_library_internal 首先通过 find_loaded_library_by_name 函数判断目标 SO 是否已经加载，如果已经加载则直接返回对应的soinfo指针，没有加载的话则调用 load_library 继续加载流程，下面看 load_library 函数。

3. load_library

 static soinfo* load_library(const char* name, int dlflags, const Android_dlextinfo* extinfo) {
     int fd = -1;
     ...
     // Open the file.
     fd = open_library(name);                // 打开 SO 文件，获得文件描述符 fd

     ElfReader elf_reader(name, fd);         // 创建 ElfReader 对象
     ...
     // Read the ELF header and load the segments.
     if (!elf_reader.Load(extinfo)) {        // 使用 ElfReader 的 Load 方法，完成 SO 装载
         return NULL;
     }
    
     soinfo* si = soinfo_alloc(SEARCH_NAME(name), &file_stat);  // 为 SO 分配新的 soinfo 结构
     if (si == NULL) {
         return NULL;
     }
     si->base = elf_reader.load_start();  // 根据装载结果，更新 soinfo 的成员变量
     si->size = elf_reader.load_size();
     si->load_bias = elf_reader.load_bias();
     si->phnum = elf_reader.phdr_count();
     si->phdr = elf_reader.loaded_phdr();
     ...
     if (!soinfo_link_image(si, extinfo)) {  // 调用 soinfo_link_image 完成 SO 的链接过程
       soinfo_free(si);
       return NULL;
     }
     return si;
 }
load_library 函数呈现了 SO 装载链接的整个流程，主要有3步:

装载:创建ElfReader对象，通过 ElfReader 对象的 Load 方法将 SO 文件装载到内存
分配soinfo:调用 soinfo_alloc 函数为 SO 分配新的 soinfo 结构，并按照装载结果更新相应的成员变量
链接: 调用 soinfo_link_image 完成 SO 的链接
通过前面的分析，可以看到， load_library 函数中包含了 SO 装载链接的主要过程, 后文主要通过分析 ElfReader 类和 soinfo_link_image 函数, 来分别介绍 SO 的装载和链接过程。

2.2 装载

在 load_library 中， 首先初始化 elf_reader 对象, 第一个参数为 SO 的名字， 第二个参数为文件描述符 fd:
ElfReader elf_reader(name, fd)
之后调用 ElfReader 的 load 方法装载 SO。

     ...
     // Read the ELF header and load the segments.
     if (!elf_reader.Load(extinfo)) {
         return NULL;
     }
     ...
ElfReader::Load 方法如下:

 bool ElfReader::Load(const Android_dlextinfo* extinfo) {
   return ReadElfHeader() &&             // 读取 elf header
          VerifyElfHeader() &&           // 验证 elf header
          ReadProgramHeader() &&         // 读取 program header
          ReserveAddressSpace(extinfo) &&// 分配空间
          LoadSegments() &&              // 按照 program header 指示装载 segments
          FindPhdr();                    // 找到装载后的 phdr 地址
 }
ElfReader::Load 方法首先读取 SO 的elf header，再对elf header进行验证，之后读取program header，根据program header 计算 SO 需要的内存大小并分配相应的空间，紧接着将 SO 按照以 segment 为单位装载到内存，最后在装载到内存的 SO 中找到program header，方便之后的链接过程使用。
下面深入 ElfReader 的这几个成员函数进行详细介绍。

2.2.1 read&verify elfheader

 bool ElfReader::ReadElfHeader() {
   ssize_t rc = read(fd_, &header_, sizeof(header_));

   if (rc != sizeof(header_)) {
     return false;
   }
   return true;
 }
ReadElfHeader 使用 read 直接从 SO 文件中将 elfheader 读取 header 中，header_ 为 ElfReader 的成员变量，类型为 Elf32_Ehdr，通过 header 可以方便的访问 elf header中各个字段，elf header中包含有 program header table、section header table等重要信息。
对 elf header 的验证包括:

magic字节
32/64 bit 与当前平台是否一致
大小端
类型:可执行文件、SO …
版本:一般为 1，表示当前版本
平台:ARM、x86、amd64 …
有任何错误都会导致加载失败。

2.2.2 Read ProgramHeader

 bool ElfReader::ReadProgramHeader() {
   phdr_num_ = header_.e_phnum;      // program header 数量

   // mmap 要求页对齐
   ElfW(Addr) page_min = PAGE_START(header_.e_phoff);
   ElfW(Addr) page_max = PAGE_END(header_.e_phoff + (phdr_num_ * sizeof(ElfW(Phdr))));
   ElfW(Addr) page_offset = PAGE_OFFSET(header_.e_phoff);

   phdr_size_ = page_max - page_min;
   // 使用 mmap 将 program header 映射到内存
   void* mmap_result = mmap(NULL, phdr_size_, PROT_READ, MAP_PRIVATE, fd_, page_min);

   phdr_mmap_ = mmap_result;
   // ElfReader 的成员变量 phdr_table_ 指向program header table
   phdr_table_ = reinterpret_cast<ElfW(Phdr)*>(reinterpret_cast<char*>(mmap_result) + page_offset);
   return true;
 }
将 program header 在内存中单独映射一份，用于解析program header 时临时使用，在 SO 装载到内存后，便会释放这块内存，转而使用装载后的 SO 中的program header。

2.2.3 reserve space & 计算 load size

 bool ElfReader::ReserveAddressSpace(const Android_dlextinfo* extinfo) {
   ElfW(Addr) min_vaddr;
   // 计算 加载SO 需要的空间大小
   load_size_ = phdr_table_get_load_size(phdr_table_, phdr_num_, &min_vaddr);
   // min_vaddr 一般情况为零，如果不是则表明 SO 指定了加载基址
   uint8_t* addr = reinterpret_cast<uint8_t*>(min_vaddr);
   void* start;

   int mmap_flags = MAP_PRIVATE | MAP_ANONYMOUS;
   start = mmap(addr, load_size_, PROT_NONE, mmap_flags, -1, 0);

   load_start_ = start;
   load_bias_ = reinterpret_cast<uint8_t*>(start) - addr;
   return true;
 }
首先调用 phdr_table_get_load_size 函数获取 SO 在内存中需要的空间load_size，然后使用 mmap 匿名映射，预留出相应的空间。

关于loadbias: SO 可以指定加载基址，但是 SO 指定的加载基址可能不是页对齐的，这种情况会导致实际映射地址和指定的加载地址有一个偏差，这个偏差便是 load_bias_，之后在针对虚拟地址进行计算时需要使用 load_bias_ 修正。普通的 SO 都不会指定加载基址，这时min_vaddr = 0，则 load_bias_ = load_start_，即load_bias_ 等于加载基址，下文会将 load_bias_ 直接称为基址。

下面深入phdr_table_get_load_size分析一下 load_size 的计算:使用成员变量 phdr_table 遍历所有的program header， 找到所有类型为 PT_LOAD 的 segment 的 p_vaddr 的最小值，p_vaddr + p_memsz 的最大值，分别作为 min_vaddr 和 max_vaddr，在将两个值分别对齐到页首和页尾，最终使用对齐后的 max_vaddr - min_vaddr 得到 load_size。

 size_t phdr_table_get_load_size(const ElfW(Phdr)* phdr_table, size_t phdr_count,
                                 ElfW(Addr)* out_min_vaddr,
                                 ElfW(Addr)* out_max_vaddr) {
   ElfW(Addr) min_vaddr = UINTPTR_MAX;
   ElfW(Addr) max_vaddr = 0;
   bool found_pt_load = false;
   for (size_t i = 0; i < phdr_count; ++i) {  // 遍历 program header
     const ElfW(Phdr)* phdr = &phdr_table[i];
     if (phdr->p_type != PT_LOAD) {
       continue;
     }
     found_pt_load = true;
     if (phdr->p_vaddr < min_vaddr) {
       min_vaddr = phdr->p_vaddr;         // 记录最小的虚拟地址
     }
     if (phdr->p_vaddr + phdr->p_memsz > max_vaddr) {
       max_vaddr = phdr->p_vaddr + phdr->p_memsz;  // 记录最大的虚拟地址
     }
   }
   if (!found_pt_load) {
     min_vaddr = 0;
   }
   min_vaddr = PAGE_START(min_vaddr);      // 页对齐
   max_vaddr = PAGE_END(max_vaddr);      // 页对齐
   if (out_min_vaddr != NULL) {
     *out_min_vaddr = min_vaddr;
   }
   if (out_max_vaddr != NULL) {
     *out_max_vaddr = max_vaddr;
   }
   return max_vaddr - min_vaddr;         // load_size = max_vaddr - min_vaddr
 }
2.2.4 Load Segments

遍历 program header table，找到类型为 PT_LOAD 的 segment:

计算 segment 在内存空间中的起始地址 segstart 和结束地址 seg_end，seg_start 等于虚拟偏移加上基址load_bias，同时由于 mmap 的要求，都要对齐到页边界得到 seg_page_start 和 seg_page_end。
计算 segment 在文件中的页对齐后的起始地址 file_page_start 和长度 file_length。
使用 mmap 将 segment 映射到内存，指定映射地址为 seg_page_start，长度为 file_length，文件偏移为 file_page_start。
 bool ElfReader::LoadSegments() {
   for (size_t i = 0; i < phdr_num_; ++i) {
     const ElfW(Phdr)* phdr = &phdr_table_[i];

     if (phdr->p_type != PT_LOAD) {
       continue;
     }
     // Segment 在内存中的地址.
     ElfW(Addr) seg_start = phdr->p_vaddr + load_bias_;
     ElfW(Addr) seg_end   = seg_start + phdr->p_memsz;
    
     ElfW(Addr) seg_page_start = PAGE_START(seg_start);
     ElfW(Addr) seg_page_end   = PAGE_END(seg_end);
    
     ElfW(Addr) seg_file_end   = seg_start + phdr->p_filesz;
    
     // 文件偏移
     ElfW(Addr) file_start = phdr->p_offset;
     ElfW(Addr) file_end   = file_start + phdr->p_filesz;
    
     ElfW(Addr) file_page_start = PAGE_START(file_start);
     ElfW(Addr) file_length = file_end - file_page_start;
    
     if (file_length != 0) {
       // 将文件中的 segment 映射到内存
       void* seg_addr = mmap(reinterpret_cast<void*>(seg_page_start),
                             file_length,
                             PFLAGS_TO_PROT(phdr->p_flags),
                             MAP_FIXED|MAP_PRIVATE,
                             fd_,
                             file_page_start);
     }
     // 如果 segment 可写, 并且没有在页边界结束，那么就将 segemnt end 到页边界的内存清零。
     if ((phdr->p_flags & PF_W) != 0 && PAGE_OFFSET(seg_file_end) > 0) {
       memset(reinterpret_cast<void*>(seg_file_end), 0, PAGE_SIZE - PAGE_OFFSET(seg_file_end));
     }
    
     seg_file_end = PAGE_END(seg_file_end);
     // 将 (内存长度 - 文件长度) 对应的内存进行匿名映射
     if (seg_page_end > seg_file_end) {
       void* zeromap = mmap(reinterpret_cast<void*>(seg_file_end),
                            seg_page_end - seg_file_end,
                            PFLAGS_TO_PROT(phdr->p_flags),
                            MAP_FIXED|MAP_ANONYMOUS|MAP_PRIVATE,
                            -1,
                            0);
     }
   }
   return true;
 }
2.3 分配 soinfo

load_library 在调用 load_segments 完成装载后，接着调用 soinfo_alloc 函数为目标SO分配soinfo，soinfo_alloc 函数实现如下:

 static soinfo* soinfo_alloc(const char* name, struct stat* file_stat) {

   soinfo* si = g_soinfo_allocator.alloc();  //分配空间，可以简单理解为 malloc
   // Initialize the new element.
   memset(si, 0, sizeof(soinfo));
   strlcpy(si->name, name, sizeof(si->name));
   si->flags = FLAG_NEW_SOINFO;

   sonext->next = si;    // 加入到存有所有 soinfo 的链表中
   sonext = si;
   return si;
 }
Linker 为 每个 SO 维护了一个soinfo结构，调用 dlopen时，返回的句柄其实就是一个指向该 SO 的 soinfo 指针。soinfo 保存了 SO 加载链接以及运行期间所需的各类信息，简单列举一下:

装载链接期间主要使用的成员:

装载信息
const ElfW(Phdr)* phdr;
size_t phnum;
ElfW(Addr) base;
size_t size;

符号信息
const char* strtab;
ElfW(Sym)* symtab;

重定位信息
ElfW(Rel)* plt_rel;
size_t plt_rel_count;
ElfW(Rel)* rel;
size_t rel_count;

init 函数和 finit 函数
Linker_function_t* init_array;
size_t init_array_count;
Linker_function_t* fini_array;
size_t fini_array_count;
Linker_function_t init_func;
Linker_function_t fini_func;
运行期间主要使用的成员:

导出符号查找（dlsym）:
const char* strtab;
ElfW(Sym)* symtab;
size_t nbucket;
size_t nchain;
unsigned* bucket;
unsigned* chain;
ElfW(Addr) load_bias;

异常处理:
unsigned* ARM_exidx;
size_t ARM_exidx_count;
load_library 在为 SO 分配 soinfo 后，会将装载结果更新到 soinfo 中，后面的链接过程就可以直接使用soinfo的相关字段去访问 SO 中的信息。

     ...
     si->base = elf_reader.load_start();
     si->size = elf_reader.load_size();
     si->load_bias = elf_reader.load_bias();
     si->phnum = elf_reader.phdr_count();
     si->phdr = elf_reader.loaded_phdr();
     ...
2.4 链接

链接过程由 soinfo_link_image 函数完成，主要可以分为四个主要步骤:

1. 定位 dynamic section，
由函数 phdr_table_get_dynamic_section 完成，该函数会遍历 program header，找到为类型为 PT_DYNAMIC 的 header, 从中获取的是 dynamic section 的信息，主要就是虚拟地址和项数。

2. 解析 dynamic section
dynamic section本质上是类型为Elf32_Dyn的数组，Elf32_Dyn 结构如下

 typedef struct {
     Elf32_Sword d_tag;      /* 类型(e.g. DT_SYMTAB)，决定 d_un 表示的意义*/
     union {
         Elf32_Word  d_val;  /* 根据 d_tag的不同，有不同的意义*/
         Elf32_Addr  d_ptr;  /* 虚拟地址 */
     } d_un;
 } Elf32_Dyn;
Elf32_Dyn结构的d_tag属性表示该项的类型，类型决定了dun中信息的意义，e.g.:当d_tag = DT_SYMTAB表示该项存储的是符号表的信息，d_un.d_ptr 表示符号表的虚拟地址的偏移，当d_tag = DT_RELSZ时，d_un.d_val 表示重定位表rel的项数。
解析的过程就是遍历数组中的每一项，根据d_tag的不同，获取到不同的信息。
dynamic section 中包含的信息主要包括以下 3 类:

 - 符号信息
 - 重定位信息
 - init&finit funcs
3. 加载 needed SO
调用 find_library 获取所有依赖的 SO 的 soinfo 指针，如果 SO 还没有加载，则会将 SO 加载到内存，分配一个soinfo*[]指针数组，用于存放 soinfo 指针。

4. 重定位
重定位SO 链接中最复杂同时也是最关键的一步。重定位做的工作主要是修复导入符号的引用，下面一节将对重定位过程进行详细分析。

soinfo_link_image 的示意代码:

 static bool soinfo_link_image(soinfo* si, const Android_dlextinfo* extinfo) {
 ...
     // 1. 获取 dynamic section 的信息，si->dynamic 指向 dynamic section
     phdr_table_get_dynamic_section(phdr, phnum, base, &si->dynamic,
                                    &dynamic_count, &dynamic_flags);
 ...
     // 2. 解析dynamic section
     uint32_t needed_count = 0;
     for (ElfW(Dyn)* d = si->dynamic; d->d_tag != DT_NULL; ++d) {
         switch (d->d_tag) {
          // 以下为符号信息
          case DT_HASH:
             si->nbucket = reinterpret_cast<uint32_t*>(base + d->d_un.d_ptr)[0];
             si->nchain = reinterpret_cast<uint32_t*>(base + d->d_un.d_ptr)[1];
             si->bucket = reinterpret_cast<uint32_t*>(base + d->d_un.d_ptr + 8);
             si->chain = reinterpret_cast<uint32_t*>(base + d->d_un.d_ptr + 8 + si->nbucket * 4);
             break;
          case DT_SYMTAB:
             si->symtab = reinterpret_cast<ElfW(Sym)*>(base + d->d_un.d_ptr);
             break;
          case DT_STRTAB:
             si->strtab = reinterpret_cast<const char*>(base + d->d_un.d_ptr);
             break;
          // 以下为重定位信息
          case DT_JMPREL:
             si->plt_rel = reinterpret_cast<ElfW(Rel)*>(base + d->d_un.d_ptr);
             break;
          case DT_PLTRELSZ:
             si->plt_rel_count = d->d_un.d_val / sizeof(ElfW(Rel));
             break;
          case DT_REL:
             si->rel = reinterpret_cast<ElfW(Rel)*>(base + d->d_un.d_ptr);
             break;
          case DT_RELSZ:
             si->rel_count = d->d_un.d_val / sizeof(ElfW(Rel));
             break;
          // 以下为 init&finit funcs
          case DT_INIT:
             si->init_func = reinterpret_cast<Linker_function_t>(base + d->d_un.d_ptr);
             break;
          case DT_FINI:
             ...
          case DT_INIT_ARRAY:
             si->init_array = reinterpret_cast<Linker_function_t*>(base + d->d_un.d_ptr);
             break;
          case DT_INIT_ARRAYSZ:
             ...
          case DT_FINI_ARRAY:
             ...
          case DT_FINI_ARRAYSZ:
             ...
          // SO 依赖
          case DT_NEEDED:
             ...
         ...
         }
 ...
     // 3. 加载依赖的SO
     for (ElfW(Dyn)* d = si->dynamic; d->d_tag != DT_NULL; ++d) {
         if (d->d_tag == DT_NEEDED) {
             soinfo* lsi = find_library(library_name, 0, NULL);
             si->add_child(lsi);
             *pneeded++ = lsi;
         }
     }
     *pneeded = NULL;
 ...
     // 4. 重定位
     soinfo_relocate(si, si->plt_rel, si->plt_rel_count, needed);
     soinfo_relocate(si, si->rel, si->rel_count, needed);
 ...
     // 设置已链接标志
     si->flags |= FLAG_LINKED;
     DEBUG("[ finished linking %s ]", si->name);
 ｝
2.4.1 重定位 relocate

Android ARM 下需要处理两个重定位表，plt_rel 和 rel，plt 指的是延迟绑定，但是 Android 目前并不对延迟绑定做特殊处理，直接与普通的重定位同时处理。两个重定位的表都由 soinfo_relocate 函数处理。
soinfo_relocate 函数需要遍历重定位表，处理每个重定位项，每个重定位项的处理过程可以分为 3 步:
1. 解析重定位项和导入符号的信息

重定位项的结构如下

 typedef struct {
      Elf32_Addr  r_offset;   /* 需要重定位的位置的偏移 */
      Elf32_Word  r_info;     /* 高24位为符号在符号表中的index，低8位为重定位类型 */
 } Elf32_Rel;
首先从重定位项获取的信息如下:

重定位的类型 type
符号在符号表中的索引号 sym，sym 为0表示为本SO内部的重定位，如果不为0，意味着该符号为导入符号
重定位的目标地址 reloc，使用r_offset + si_load_bias，相当于 偏移地址+基地址

符号表表项的结构为elf32_sym:

typedef struct elf32_sym {
  Elf32_Word  st_name;    /* 名称 - index into string table */
  Elf32_Addr  st_value;   /* 偏移地址 */
  Elf32_Word  st_size;    /* 符号长度（ e.g. 函数的长度） */
  unsigned char   st_info;    /* 类型和绑定类型 */
  unsigned char   st_other;   /* 未定义 */
  Elf32_Half  st_shndx;   /* section header的索引号，表示位于哪个 section 中 */
} Elf32_Sym;
2. 如果 sym 不为0，则查找导入符号的信息
如果 sym 不为0，则继续使用 sym 在符号表中获取符号信息，从符号信息中进一步获取符号的名称。随后调用 soinfo_do_lookup 函数在所有依赖的 SO 中根据符号名称查找符号信息，返回值类型为 elf32_sym，同时还会返回含有该符号的 SO 的 soinfo( lsi )，如果查找成功则该导入符号的地址为:
sym_addr = s->st_value + lsi->load_bias;

3. 修正需要重定位的地址
根据重定位类型的不同，修正重定位地址，具体的重定位类型定义和计算方法可以参考 aaelf 文档的 4.6.1.2 节。
对于导入符号，则使用根据第二步得到 sym_addr 去修正，对于 SO 内部的相对偏移修正，则直接将reloc的地址加上 SO 的基址。

static int soinfo_relocate(soinfo* si, ElfW(Rel)* rel, unsigned count, soinfo* needed[]) {
  ElfW(Sym)* s;
  soinfo* lsi;

  // 遍历重定位表
  for (size_t idx = 0; idx < count; ++idx, ++rel) {
      //
      // 1. 解析重定位项和导入符号的信息
      //
      // 重定位类型
      unsigned type = ELFW(R_TYPE)(rel->r_info);
      // 导入符号在符号表中的 index，可以为0,(修正 SO 内部的相对偏移)
      unsigned sym = ELFW(R_SYM)(rel->r_info);
      // 需要重定位的地址
      ElfW(Addr) reloc = static_cast<ElfW(Addr)>(rel->r_offset + si->load_bias);
      ElfW(Addr) sym_addr = 0;
      const char* sym_name = NULL;

      if (type == 0) { // R_*_NONE
          continue;
      }
      if (sym != 0) {
          //
          // 2. 如果 sym 有效，则查找导入符号
          //
          // 从符号表中获得符号信息，在根据符号信息从字符串表中获取字符串名
          sym_name = reinterpret_cast<const char*>(si->strtab + si->symtab[sym].st_name);
          // 在依赖的 SO 中查找符号，返回值为 Elf32_Sym 类型
          s = soinfo_do_lookup(si, sym_name, &lsi, needed);
          if (s == NULL) {}
              // 查找失败，不关心
          } else {
              // 查找成功，最终的符号地址 = s->st_value + lsi->load_bias
              // s->st_value 是符号在依赖 SO 中的偏移，lsi->load_bias 为依赖 SO 的基址
              sym_addr = static_cast<ElfW(Addr)>(s->st_value + lsi->load_bias);
          }
      } else {
          s = NULL;
      }
      //
      // 3. 根据重定位类型，修正需要重定位的地址
      //
      switch (type) {
      // 判断重定位类型，将需要重定位的地址 reloc 修正为目标符号地址
      // 修正导入符号
      case R_ARM_JUMP_SLOT:
          *reinterpret_cast<ElfW(Addr)*>(reloc) = sym_addr;
          break;
      case R_ARM_GLOB_DAT:
          *reinterpret_cast<ElfW(Addr)*>(reloc) = sym_addr;
          break;
      case R_ARM_ABS32:
          *reinterpret_cast<ElfW(Addr)*>(reloc) += sym_addr;
          break;
      case R_ARM_REL32:
          *reinterpret_cast<ElfW(Addr)*>(reloc) += sym_addr - rel->r_offset;
          break;
      // 不支持
      case R_ARM_COPY:
          /*
           * ET_EXEC is not supported SO this should not happen.
           */
          DL_ERR("%s R_ARM_COPY relocations are not supported", si->name);
          return -1;
      // SO 内部的偏移修正
      case R_ARM_RELATIVE:
          if (sym) {
              DL_ERR("odd RELATIVE form...");
              return -1;
          }
          *reinterpret_cast<ElfW(Addr)*>(reloc) += si->base;
          break;
    
      default:
          DL_ERR("unknown reloc type %d @ %p (%zu)", type, rel, idx);
          return -1;
      }
  }
  return 0;
}
2.5 CallConstructors

在编译 SO 时，可以通过链接选项-init或是给函数添加属性__attribute__((constructor))来指定 SO 的初始化函数，这些初始化函数在 SO 装载链接后便会被调用，再之后才会将 SO 的 soinfo 指针返回给 dl_open 的调用者。SO 层面的保护手段，有两个介入点, 一个是 jni_onload, 另一个就是初始化函数，比如反调试、脱壳等，逆向分析时经常需要动态调试分析这些初始化函数。

完成 SO 的装载链接后，返回到 do_dlopen 函数, do_open 获得 find_library 返回的刚刚加载的 SO 的 soinfo，在将 soinfo 返回给其他模块使用之前，最后还需要调用 soinfo 的成员函数 CallConstructors。

 soinfo* do_dlopen(const char* name, int flags, const Android_dlextinfo* extinfo) {
 ...
   soinfo* si = find_library(name, flags, extinfo);
   if (si != NULL) {
     si->CallConstructors();
   }
   return si;
 ...
 }
CallConstructors 函数会调用 SO 的首先调用所有依赖的 SO 的 soinfo 的 CallConstructors 函数，接着调用自己的 soinfo 成员变量 init 和 看 init_array 指定的函数，这两个变量在在解析 dynamic section 时赋值。

 void soinfo::CallConstructors() {
   //如果已经调用过，则直接返回
   if (constructors_called) {
     return;
   }
   // 调用依赖 SO 的 Constructors 函数
   get_children().for_each([] (soinfo* si) {
     si->CallConstructors();
   });
   // 调用 init_func
   CallFunction("DT_INIT", init_func);
   // 调用 init_array 中的函数
   CallArray("DT_INIT_ARRAY", init_array, init_array_count, false);
 }
有了以上分析基础后，在需要动态跟踪初始化函数时，我们就知道可以将断点设在 do_dlopen 或是 CallConstructors。

3. 加壳技术

在病毒和版权保护领域，“壳”一直扮演着极为重要的角色。通过加壳可以对代码进行压缩和加密，同时再辅以虚拟化、代码混淆和反调试等手段，达到防止静态和动态分析。

在 Android 环境中，Native 层的加壳主要是针对动态链接库 SO，SO 加壳的示意图如下:

<pre>
<img src="data:image/png;base64,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" />
</pre>

加壳工具、loader、被保护SO。

SO: 即被保护的目标 SO。
loader: 自身也是一个 SO，系统加载时首先加载 loader，loader 首先还原出经过加密、压缩、变换的 SO，再将 SO 加载到内存，并完成链接过程，使 SO 可以正常被其他模块使用。
加壳工具: 将被保护的 SO 加密、压缩、变换，并将结果作为数据与 loader 整合为 packed SO。
下面对 SO 加壳的关键技术进行简单介绍。

3.1 loader 执行时机

Linker 加载完 loader 后，loader 需要将被保护的 SO 加载起来，这就要求 loader 的代码需要被执行，而且要在 被保护 SO 被使用之前，前文介绍了 SO 的初始化函数便可以满足这个要求，同时在 Android 系统下还可以使用 JNI_ONLOAD 函数，因此 loader 的执行时机有两个选择:

SO 的 init 或 initarray
jni_onload
3.2 loader 完成 SO 的加载链接

loader 开始执行后，首先需要在内存中还原出 SO，SO 可以是经过加密、压缩、变换等手段，也可已单纯的以完全明文的数据存储，这与 SO 加壳的技术没有必要的关系，在此不进行讨论。
在内存中还原出 SO 后，loader 还需要执行装载和链接，这两个过程可以完全模仿 Linker 来实现，下面主要介绍一下相对 Linker，loader 执行这两个过程有哪些变化。

3.2.1 装载

还原后的 SO 在内存中，所以装载时的主要变化就是从文件装载到从内存装载。
Linker 在装载 PT_LAOD segment时，使用 SO 文件的描述符 fd：

       void* seg_addr = mmap(reinterpret_cast<void*>(seg_page_start),
                             file_length,
                             PFLAGS_TO_PROT(phdr->p_flags),
                             MAP_FIXED|MAP_PRIVATE,
                             fd_,
                             file_page_start);
按照 Linker 装载，PT_LAOD segment时，需要分为两步：

       // 1、改用匿名映射
       void* seg_addr = mmap(reinterpret_cast<void*>(seg_page_start),
                             file_length,
                             PFLAGS_TO_PROT(phdr->p_flags),
                             MAP_FIXED|MAP_PRIVATE,
                             -1,
                             0);
      // 2、将内存中的 segment 复制到映射的内存中
      memcpy(seg_addr+seg_page_offset, elf_data_buf + phdr->p_offset, phdr->p_filesz);
注意第2步复制 segment 时，目标地址需要加上 seg_page_offset，seg_page_offset 是 segment 相对与页面起始地址的偏移。
其他的步骤基本按照 Linker 的实现即可，只需要将一些从文件读取修改为从内存读取，比如读 elfheader和program header时。

3.2.2 分配 soinfo

soinfo 保存了 SO 装载链接和运行时需要的所有信息，为了维护相关的信息，loader 可以照搬 Linker 的 soinfo 结构，用于存储中间信息，装载链接结束后，还需要将 soinfo 的信息修复到 Linker 维护的soinfo，3.3节进行详细说明。

3.2.3 链接

链接过程完全是操作内存，不论是从文件装载还是内存装载，链接过程都是一样，完全模仿 Linker 即可。
另外链接后记得顺便调用 SO 初始化函数( init 和 init_array )。

3.3 soinfo 修复

SO 加壳的最关键技术点在于 soinfo 的修复，由于 Linker 加载的是 loader，而实际对外使用的是被保护的 SO，所以 Linker 维护的 soinfo 可以说是错误，loader 需要将自己维护的 soinfo 中的部分信息导出给 Linker 的soinfo。

修复过程如下：

获取 Linker 维护的 soinfo，可以通过 dlopen 打开自己来获得：self_soinfo = dlopen(self)。
将 loader soinfo 中的信息导出到 self_soinfo，最简单粗暴的方式就是直接赋值，比如：self_soinfo.base = soinfo.base。需要导出的主要有以下几项：
SO地址范围：base、size、load_bias
符号信息:sym_tab、str_tab、
符号查找信息：nbucket、nchain、bucket、chain
异常处理：ARM_exidx、ARM_exidx_count
参考

<<Linkers and loaders>>
<<ELF for the ARM Architecture>>
更多精彩内容欢迎关注bugly的微信公众账号：


腾讯 Bugly是一款专为移动开发者打造的质量监控工具，帮助开发者快速，便捷的定位线上应用崩溃的情况以及解决方案。智能合并功能帮助开发同学把每天上报的数千条 Crash 根据根因合并分类，每日日报会列出影响用户数最多的崩溃，精准定位功能帮助开发同学定位到出问题的代码行，实时上报可以在发布后快速的了解应用的质量情况，适配最新的 iOS, Android 官方操作系统，鹅厂的工程师都在使用，快来加入我们吧！


Reference
----------------------------------------------------------------------------------------------------
* [【腾讯Bugly干货分享】Android Linker 与 SO 加壳技术](https://zhuanlan.zhihu.com/p/22652847)
* [常见app加固厂商脱壳方法研究](http://www.tuicool.com/articles/fUFJbaB)
* [[原创] 梆梆加固方案分析和破解--论梆梆安全加固的不可靠](http://bbs.hiapk.com/thread-25621953-1-1.html)​
* [ 梆梆加固方案分析和破解---论梆梆安全加固的不可靠 ...](http://bbs.51cto.com/thread-1172473-1.html)​
* [梆梆脱壳方法](http://www.2cto.com/article/201606/521380.html)​
* [Android DEX加壳](http://www.2cto.com/article/201303/196420.html)​
* [Android中的Apk的加固(加壳)原理解析和实现（转）](http://blog.csdn.net/lostinai/article/details/50899093)​
* [APK加壳详解和demo](http://blog.csdn.net/pvlking/article/details/42168233)​
