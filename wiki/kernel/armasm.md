# ARMv8 架构与指令集.学习笔记

## 目 录

第1章 ARMv8简介. 3

*   1.1基础认识. 3
*   1.2 相关专业名词解释. 3

第2章 Execution State 4

*   2.1 提供两种Execution State 4
*   2.2 决定Execution State的条件. 4

第3章 Exception Level 5

*   3.1 Exception Level 与Security 5
    *   3.1.1 EL3使用AArch64、AArch32的对比. 5

*   3.2 ELx 和 Execution State 组合. 6

*   3.3路由控制. 7
    *   3.3.1 路由规则. 7
    *   3.3.2 IRQ/FIQ/SError路由流程图. 8

第4章 ARMv8寄存器. 9

-   4.1 AArch32重要寄存器. 9
    -   4.1.1 A32状态下寄存器组织. 10
    -   4.1.1 T32状态下寄存器组织. 10

-   4.2 AArch64重要寄存器. 11

-   4.3 64、32位寄存器的映射关系. 11

第5章 异常模型. 12

-   5.1 异常类型描述. 12
    -   5.1.1 AArch32异常类型. 12
    -   5.1.2 AArch64异常类型. 12

-   5.2异常处理逻辑. 13
    -   5.2.1 寄存器操作. 13
    -   5.2.2 路由控制. 14

-   5.3流程图对比. 14
    -   5.3.1 IRQ 流程图. 15
    -   5.3.2 Data Abort 流程图. 18

-   5.4  源代码异常入口. 20
    -   5.4.1 C函数入口. 20
    -   5.4.2 上报流程图. 20
    -   5.4.3 异常进入压栈准备. 21
    -   5.4.4 栈布局. 21

第6章 ARMv8指令集. 22

-   6.1 概况. 22
    -   6.1.1 指令基本格式. 22
    -   6.1.2 指令分类. 22

-   6.2 A64指令集. 22
    -   6.2.1 指令助记符. 23
    -   6.2.2 指令条件码. 23
    -   6.2.3 跳转指令. 24
    -   6.2.4 异常产生和返回指令. 24
    -   6.2.5 系统寄存器指令. 24
    -   6.2.6 数据处理指令. 25
    -   6.2.7 Load/Store指令. 27
    -   6.2.8 屏障指令. 31

-   6.3 A32 & T32指令集. 31
    -   6.3.1 跳转指令. 31
    -   6.3.2 异常产生、返回指令. 32
    -   6.3.3 系统寄存器指令. 32
    -   6.3.4 系统寄存器指令. 32
    -   6.3.5 数据处理指令. 32
    -   6.3.6 Load/Store指令. 32
    -   6.3.7 IT(if then)指令. 34
    -   6.3.8 协处理器指令. 34

-   6.4 指令编码. 34
    -   6.4.1 A32编码. 34
    -   6.4.2 T32-16bit编码. 35
    -   6.4.3 T32-32bit编码. 35
    -   6.4.4 A64编码. 35

-   6.4 汇编代码分析. 35

第7章 流水线. 36

-   7.1 简介. 36
    -   7.1.1 简单三级流水线. 36
    -   7.1.2 经典五级流水线. 36
-   7.2 流水线冲突. 37

-   7.3 指令并行. 37




## 第1章 ARMv8简介

### 1.1 基础认识

ARMv8的架构继承以往ARMv7与之前处理器技术的基础，除了现有的16/32bit的Thumb2指令支持外，也向前兼容现有的A32(ARM 32bit)指令集，基于64bit的AArch64架构，除了新增A64(ARM 64bit)指令集外，也扩充了现有的A32(ARM 32bit)和T32(Thumb2 32bit）指令集，另外还新增加了CRYPTO(加密)模块支持。

### 1.2 相关专业名词解释

| 名词            | 解释                                               |
| --------------- | -------------------------------------------------- |
| AArch32         | 描述32bit Execution State                          |
| AArch64         | 描述64bit Execution State                          |
| A32、T32        | AArch32 ISA （Instruction Architecture）           |
| A64             | AArch64 ISA （Instruction Architecture）           |
| Interprocessing | 描述AArch32和AArch64两种执行状态之间的切换         |
| SIMD            | Single-Instruction, Multiple-Data （单指令多数据） |

(参考文档：ARMv8-A Architecture reference manual-DDI0487A_g_armv8_arm.pdf)






Reference
----------------------------------------------------------------------------------------------------

* [ARM Compiler armasm Reference Guide](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0802a/a64_general_instructions.html)
* [ARMv8 架构与指令集.学习笔记](http://blog.csdn.net/forever_2015/article/details/50285865)

