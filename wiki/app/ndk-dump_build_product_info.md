Check build product info
========================

查看`.a`文件的内容
----------------------------------------------------------------------------------------------------
### 查看`Linux`静态库`*.a`中的函数和文件
```bash
bob@bob-server:~/dev/ezx/ezProject.server/android/native$ nm -g -l -o --defined-only obj/local/armeabi-v7a/libpcre_static.a 
obj/local/armeabi-v7a/libpcre_static.a:pcre_chartables.o:00000000 R _pcre_default_tables	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/pcre_chartables.c:29
obj/local/armeabi-v7a/libpcre_static.a:pcre_byte_order.o:00000001 T pcre_pattern_to_host_byte_order	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_byte_order.c:99
obj/local/armeabi-v7a/libpcre_static.a:pcre_compile.o:00000001 T pcre_compile	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_compile.c:4458
obj/local/armeabi-v7a/libpcre_static.a:pcre_compile.o:00000001 T pcre_compile2	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_compile.c:8984
obj/local/armeabi-v7a/libpcre_static.a:pcre_compile.o:00000001 T _pcre_find_bracket	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_compile.c:2080
obj/local/armeabi-v7a/libpcre_static.a:pcre_config.o:00000001 T pcre_config	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_config.c:70
obj/local/armeabi-v7a/libpcre_static.a:pcre_dfa_exec.o:00000001 T pcre_dfa_exec	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_dfa_exec.c:3177
obj/local/armeabi-v7a/libpcre_static.a:pcre_exec.o:00000001 T pcre_exec	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_exec.c:6347
obj/local/armeabi-v7a/libpcre_static.a:pcre_fullinfo.o:00000001 T pcre_fullinfo	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_fullinfo.c:70
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_copy_named_substring	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:161
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_copy_substring
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_free_substring	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:650
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_free_substring_list	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:503
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_get_named_substring	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:607
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_get_stringnumber	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:70
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_get_stringtable_entries	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:150
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_get_substring	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:544
obj/local/armeabi-v7a/libpcre_static.a:pcre_get.o:00000001 T pcre_get_substring_list	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_get.c:441
obj/local/armeabi-v7a/libpcre_static.a:pcre_globals.o:00000000 B pcre_callout
obj/local/armeabi-v7a/libpcre_static.a:pcre_globals.o:00000004 D pcre_free
obj/local/armeabi-v7a/libpcre_static.a:pcre_globals.o:00000000 D pcre_malloc	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_globals.c:78
obj/local/armeabi-v7a/libpcre_static.a:pcre_globals.o:0000000c D pcre_stack_free
obj/local/armeabi-v7a/libpcre_static.a:pcre_globals.o:00000004 B pcre_stack_guard
obj/local/armeabi-v7a/libpcre_static.a:pcre_globals.o:00000008 D pcre_stack_malloc
obj/local/armeabi-v7a/libpcre_static.a:pcre_jit_compile.o:00000001 T pcre_assign_jit_stack	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_jit_compile.c:10685
obj/local/armeabi-v7a/libpcre_static.a:pcre_jit_compile.o:00000001 T pcre_jit_free_unused_memory	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_jit_compile.c:10720
obj/local/armeabi-v7a/libpcre_static.a:pcre_jit_compile.o:00000001 T pcre_jit_stack_alloc	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_jit_compile.c:10674
obj/local/armeabi-v7a/libpcre_static.a:pcre_jit_compile.o:00000001 T pcre_jit_stack_free	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_jit_compile.c:10690
obj/local/armeabi-v7a/libpcre_static.a:pcre_maketables.o:00000001 T pcre_maketables	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_maketables.c:71
obj/local/armeabi-v7a/libpcre_static.a:pcre_newline.o:00000001 T _pcre_is_newline	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_newline.c:76
obj/local/armeabi-v7a/libpcre_static.a:pcre_newline.o:00000001 T _pcre_was_newline	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_newline.c:151
obj/local/armeabi-v7a/libpcre_static.a:pcre_ord2utf8.o:00000001 T _pcre_ord2utf	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_ord2utf8.c:68
obj/local/armeabi-v7a/libpcre_static.a:pcre_refcount.o:00000001 T pcre_refcount	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_refcount.c:73
obj/local/armeabi-v7a/libpcre_static.a:pcre_study.o:00000001 T pcre_free_study	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_study.c:804
obj/local/armeabi-v7a/libpcre_static.a:pcre_study.o:00000001 T pcre_study	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_study.c:1452
obj/local/armeabi-v7a/libpcre_static.a:pcre_tables.o:000000a4 R _pcre_hspace_list
obj/local/armeabi-v7a/libpcre_static.a:pcre_tables.o:00000000 R _pcre_OP_lengths	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_tables.c:59
obj/local/armeabi-v7a/libpcre_static.a:pcre_tables.o:000000f4 R _pcre_vspace_list
obj/local/armeabi-v7a/libpcre_static.a:pcre_ucd.o:0000000c R _pcre_ucd_caseless_sets
obj/local/armeabi-v7a/libpcre_static.a:pcre_ucd.o:00000000 R _pcre_ucd_records	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_ucd.c:35
obj/local/armeabi-v7a/libpcre_static.a:pcre_ucd.o:00000008 R _pcre_ucd_stage1
obj/local/armeabi-v7a/libpcre_static.a:pcre_ucd.o:0000000a R _pcre_ucd_stage2
obj/local/armeabi-v7a/libpcre_static.a:pcre_valid_utf8.o:00000001 T _pcre_valid_utf	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_valid_utf8.c:107
obj/local/armeabi-v7a/libpcre_static.a:pcre_version.o:00000001 T pcre_version	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_version.c:84
obj/local/armeabi-v7a/libpcre_static.a:pcre_xclass.o:00000001 T _pcre_xclass	/home/bob/dev/ezx/ezProject.server/android/native/lib.a.pcre.mk/../lib.a.pcre/dist/pcre_xclass.c:67
...
```
下面说明符号类型：对于每一个符号来说，其类型如果是小写的，则表明该符号是`local`的；大写则表明该符号是`global`(`external`)的
```
A   该符号的值是绝对的，在以后的链接过程中，不允许进行改变。这样的符号值，常常出现在中断向量表中，例如用符号来表示各个中断向量函数在中断向量表中的位置。
B   该符号的值出现在非初始化数据段(bss)中。例如，在一个文件中定义全局static int test。则该符号test的类型为b，位于bss section中。其值表示该符号在bss段中的偏移。一般而言，bss段分配于RAM中
C   该符号为common。common symbol是未初始话数据段。该符号没有包含于一个普通section中。只有在链接过程中才进行分配。符号的值表示该符号需要的字节数。例如在一个c文件中，定义int test，并且该符号在别的地方会被引用，则该符号类型即为C。否则其类型为B。
D   该符号位于初始话数据段中。一般来说，分配到data section中。例如定义全局int baud_table[5] = {9600, 19200, 38400, 57600, 115200}，则会分配于初始化数据段中。
G   该符号也位于初始化数据段中。主要用于small object提高访问small data object的一种方式。
I   该符号是对另一个符号的间接引用。
N   该符号是一个debugging符号。
R   该符号位于只读数据区。例如定义全局const int test[] = {123, 123};则test就是一个只读数据区的符号。注意在cygwin下如果使用gcc直接编译成MZ格式时，源文件中的test对应_test，并且其符号类型为D，即初始化数据段中。但是如果使用m6812-elf-gcc这样的交叉编译工具，源文件中的test对应目标文件的test,即没有添加下划线，并且其符号类型为R。一般而言，位于rodata section。值得注意的是，如果在一个函数中定义const char *test = “abc”, const char test_int = 3。使用nm都不会得到符号信息，但是字符串“abc”分配于只读存储器中，test在rodata section中，大小为4。
S   符号位于非初始化数据区，用于small object。
T   该符号位于代码区text section。
U   该符号在当前文件中是未定义的，即该符号的定义在别的文件中。例如，当前文件调用另一个文件中定义的函数，在这个被调用的函数在当前就是未定义的；但是在定义它的文件中类型是T。但是对于全局变量来说，在定义它的文件中，其符号类型为C，在使用它的文件中，其类型为U。
V   该符号是一个weak object。
W   The symbol is a weak symbol that has not been specifically tagged as a weak object symbol.
-   该符号是a.out格式文件中的stabs symbol。
?   该符号类型没有定义
```

#### nm --help
```bash
bob@bob-server:~/dev/ezx/ezProject.server/android/native$ nm --help
Usage: nm [option(s)] [file(s)]
 List symbols in [file(s)] (a.out by default).
 The options are:
  -a, --debug-syms       Display debugger-only symbols
  -A, --print-file-name  Print name of the input file before every symbol
  -B                     Same as --format=bsd
  -C, --demangle[=STYLE] Decode low-level symbol names into user-level names
                          The STYLE, if specified, can be `auto' (the default),
                          `gnu', `lucid', `arm', `hp', `edg', `gnu-v3', `java'
                          or `gnat'
      --no-demangle      Do not demangle low-level symbol names
  -D, --dynamic          Display dynamic symbols instead of normal symbols
      --defined-only     Display only defined symbols
  -e                     (ignored)
  -f, --format=FORMAT    Use the output format FORMAT.  FORMAT can be `bsd',
                           `sysv' or `posix'.  The default is `bsd'
  -g, --extern-only      Display only external symbols
  -l, --line-numbers     Use debugging information to find a filename and
                           line number for each symbol
  -n, --numeric-sort     Sort symbols numerically by address
  -o                     Same as -A
  -p, --no-sort          Do not sort the symbols
  -P, --portability      Same as --format=posix
  -r, --reverse-sort     Reverse the sense of the sort
      --plugin NAME      Load the specified plugin
  -S, --print-size       Print size of defined symbols
  -s, --print-armap      Include index for symbols from archive members
      --size-sort        Sort symbols by size
      --special-syms     Include special symbols in the output
      --synthetic        Display synthetic symbols as well
  -t, --radix=RADIX      Use RADIX for printing symbol values
      --target=BFDNAME   Specify the target object format as BFDNAME
  -u, --undefined-only   Display only undefined symbols
  -X 32_64               (ignored)
  @FILE                  Read options from FILE
  -h, --help             Display this information
  -V, --version          Display this program's version number
```

### 查看`*.a`中的文件

```bash
bob@bob-server:~/dev/ezx/ezProject.server/android/native$ ar -t obj/local/armeabi-v7a/libpcre_static.a 
pcre_chartables.o
pcre_byte_order.o
pcre_compile.o
pcre_config.o
pcre_dfa_exec.o
pcre_exec.o
pcre_fullinfo.o
pcre_get.o
pcre_globals.o
pcre_jit_compile.o
pcre_maketables.o
pcre_newline.o
pcre_ord2utf8.o
pcre_refcount.o
pcre_string_utils.o
pcre_study.o
pcre_tables.o
pcre_ucd.o
pcre_valid_utf8.o
pcre_version.o
pcre_xclass.o
```




















