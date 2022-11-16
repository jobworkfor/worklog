# 系统文件节点说明

## /proc/

### kenel符号表

````bash
# 全局符号表 /proc/kallsyms
130|kaiser:/ # cat /proc/kallsyms |more
0000000000000000 t _head
0000000000000000 T _text
0000000000000000 t pe_header
0000000000000000 t coff_header
0000000000000000 t optional_header

# 权限等级，为0时全局符号表中显示入口地址 /proc/sys/kernel/kptr_restrict
kaiser:/ # echo 0 > /proc/sys/kernel/kptr_restrict
kaiser:/ # cat /proc/sys/kernel/kptr_restrict
0

kaiser:/ # cat /proc/kallsyms |more
ffffffef03a80000 t _head
ffffffef03a80000 T _text
ffffffef03a80040 t pe_header
ffffffef03a80044 t coff_header
````



