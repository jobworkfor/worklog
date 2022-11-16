android-ndk-r13b
================

```bash
bob@bob-server:~/bin/android-ndk-r13b$ tree -d -L 4
```

```
.
├── build ------------------------------------------------------+ Makefile编译框架
│   ├── awk                                                     |
│   ├── cmake                                                   |
│   ├── core ---------------------------------------------------+ 对应与源码编译系统，这里是简化版
│   │   └── toolchains                                          |
│   │       ├── aarch64-linux-android-4.9                       |
│   │       ├── aarch64-linux-android-clang                     |
│   │       ├── arm-linux-androideabi-4.9                       |
│   │       ├── arm-linux-androideabi-clang                     |
│   │       ├── mips64el-linux-android-4.9                      |
│   │       ├── mips64el-linux-android-clang                    |
│   │       ├── mipsel-linux-android-4.9                        |
│   │       ├── mipsel-linux-android-clang                      │
│   │       ├── x86-4.9                                         |
│   │       ├── x86_64-4.9                                      |
│   │       ├── x86_64-clang                                    |
│   │       └── x86-clang                                       |
│   ├── gmsl ---------------------------------------------------+ GNU Make Standard Library
│   ├── lib                                                     |
│   └── tools                                                   |
│       ├── toolchain-licenses                                  |
│       └── unwanted-symbols                                    |
│           ├── arm                                             |
│           ├── arm64                                           |
│           ├── mips                                            |
│           ├── mips64                                          |
│           ├── x86                                             |
│           └── x86_64                                          |
```

```
├── platforms --------------------------------------------------+ 在各API下，提供不同架构的头文件和库文件，
│   ├── android-12                                              | 应用通过设置： APP_PLATFORM := android-24
│   │   ├── arch-arm                                            | 选择android api，然后可以直接使用其头文件和库
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           | 编译过程中会添加如下参数
│   │   │   └── usr                                             | -isystem /android-ndk-r13b/platforms/android-??/arch-arm/usr/include
│   │   └── arch-x86                                            |
│   │       └── usr                                             | 可以到如下目录查看当前ndk支持的库
│   ├── android-13                                              | /android-ndk-r13b/platforms/android-??/arch-arm/usr/lib
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   └── arch-x86                                            |
│   │       └── usr                                             |
│   ├── android-14                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   └── arch-x86                                            |
│   │       └── usr                                             |
│   ├── android-15                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   └── arch-x86                                            |
│   │       └── usr                                             |
│   ├── android-16                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   └── arch-x86                                            |
│   │       └── usr                                             |
│   ├── android-17                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   └── arch-x86                                            |
│   │       └── usr                                             |
│   ├── android-18                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   └── arch-x86                                            |
│   │       └── usr                                             |
│   ├── android-19                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   └── arch-x86                                            |
│   │       └── usr                                             |
│   ├── android-21                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-arm64                                          |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   ├── arch-mips64                                         |
│   │   │   └── usr                                             |
│   │   ├── arch-x86                                            |
│   │   │   └── usr                                             |
│   │   └── arch-x86_64                                         |
│   │       └── usr                                             |
│   ├── android-22                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-arm64                                          |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   ├── arch-mips64                                         |
│   │   │   └── usr                                             |
│   │   ├── arch-x86                                            |
│   │   │   └── usr                                             |
│   │   └── arch-x86_64                                         |
│   │       └── usr                                             |
│   ├── android-23                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-arm64                                          |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   ├── arch-mips64                                         |
│   │   │   └── usr                                             |
│   │   ├── arch-x86                                            |
│   │   │   └── usr                                             |
│   │   └── arch-x86_64                                         |
│   │       └── usr                                             |
│   ├── android-24                                              |
│   │   ├── arch-arm                                            |
│   │   │   └── usr                                             |
│   │   ├── arch-arm64                                          |
│   │   │   └── usr                                             |
│   │   ├── arch-mips                                           |
│   │   │   └── usr                                             |
│   │   ├── arch-mips64                                         |
│   │   │   └── usr                                             |
│   │   ├── arch-x86                                            |
│   │   │   └── usr                                             |
│   │   └── arch-x86_64                                         |
│   │       └── usr                                             |
│   └── android-9                                               |
│       ├── arch-arm                                            |
│       │   └── usr                                             |
│       ├── arch-mips                                           |
│       │   └── usr                                             |
│       └── arch-x86                                            |
│           └── usr                                             |
```

```
├── prebuilt ---------------------------------------------------+ gdbserver，用于调试
│   ├── android-arm                                             |
│   │   └── gdbserver                                           |
│   ├── android-arm64                                           |
│   │   └── gdbserver                                           |
│   ├── android-mips                                            |
│   │   └── gdbserver                                           |
│   ├── android-mips64                                          |
│   │   └── gdbserver                                           |
│   ├── android-x86                                             |
│   │   └── gdbserver                                           |
│   ├── android-x86_64                                          |
│   │   └── gdbserver                                           |
│   └── linux-x86_64                                            |
│       ├── bin                                                 |
│       ├── include                                             |
│       │   └── python2.7                                       |
│       ├── lib                                                 |
│       │   ├── pkgconfig                                       |
│       │   └── python2.7                                       |
│       └── share                                               |
│           ├── gdb                                             |
│           ├── man                                             |
│           └── pretty-printers                                 |
```

```
├── python-packages --------------------------------------------+ python工具集：
│   ├── adb ----------------------------------------------------+ * A Python interface to the Android Debug Bridge.
│   └── gdbrunner ----------------------------------------------+ * Helpers used by both gdbclient.py and ndk-gdb.py.
```

```
├── shader-tools -----------------------------------------------+ (^1)Tools for SPIR (Standard Portable Intermediate Representation)
│   └── linux-x86_64                                            |
```

```
├── simpleperf -------------------------------------------------+ "perf.data"文件分析工具，具体见其中的README.md
│   └── android                                                 |
│       ├── arm                                                 |
│       ├── arm64                                               |
│       ├── x86                                                 |
│       └── x86_64                                              |
```

```
├── sources ----------------------------------------------------+ 源码工具包
│   ├── android                                                 |
│   │   ├── cpufeatures                                         |
│   │   ├── native_app_glue                                     |
│   │   ├── ndk_helper                                          |
│   │   └── support                                             |
│   │       ├── include                                         |
│   │       ├── src                                             |
│   │       └── tests                                           |
│   ├── cxx-stl ------------------------------------------------+ CPP STL
│   │   ├── gabi++                                              |
│   │   │   ├── include                                         |
│   │   │   ├── src                                             |
│   │   │   └── tests                                           |
│   │   ├── gnu-libstdc++                                       |
│   │   │   └── 4.9                                             |
│   │   ├── llvm-libc++                                         |
│   │   │   ├── buildcmds                                       |
│   │   │   ├── cmake                                           |
│   │   │   ├── docs                                            |
│   │   │   ├── include                                         |
│   │   │   ├── lib                                             |
│   │   │   ├── libs                                            |
│   │   │   ├── src                                             |
│   │   │   ├── test                                            |
│   │   │   ├── utils                                           |
│   │   │   └── www                                             |
│   │   ├── llvm-libc++abi                                      |
│   │   │   ├── cmake                                           |
│   │   │   ├── include                                         |
│   │   │   ├── lib                                             |
│   │   │   ├── src                                             |
│   │   │   ├── test                                            |
│   │   │   └── www                                             |
│   │   ├── stlport                                             |
│   │   │   ├── libs                                            |
│   │   │   ├── src                                             |
│   │   │   ├── stlport                                         |
│   │   │   └── test                                            |
│   │   └── system                                              |
│   │       └── include                                         |
│   └── third_party                                             |
│       ├── googletest                                          |
│       │   ├── googletest                                      |
│       │   └── patches.ndk                                     |
│       ├── shaderc                                             |
│       │   ├── libshaderc                                      |
│       │   ├── libshaderc_util                                 |
│       │   ├── third_party                                     |
│       │   └── utils                                           |
│       └── vulkan                                              |
│           └── src                                             |
```

```
└── toolchains -------------------------------------------------+ 交叉编译工具链
    ├── aarch64-linux-android-4.9                               |
    │   └── prebuilt                                            |
    │       └── linux-x86_64                                    |
    ├── arm-linux-androideabi-4.9                               |
    │   └── prebuilt                                            |
    │       └── linux-x86_64                                    |
    ├── llvm                                                    |
    │   └── prebuilt                                            |
    │       └── linux-x86_64                                    |
    ├── mips64el-linux-android-4.9                              |
    │   └── prebuilt                                            |
    │       └── linux-x86_64                                    |
    ├── mipsel-linux-android-4.9                                |
    │   └── prebuilt                                            |
    │       └── linux-x86_64                                    |
    ├── x86-4.9                                                 |
    │   └── prebuilt                                            |
    │       └── linux-x86_64                                    |
    └── x86_64-4.9                                              |
        └── prebuilt                                            |
            └── linux-x86_64                                    |
                                                                *
```

Comments
----------------------------------------------------------------------------------------------------

### (^1): Standard Portable Intermediate Representation
SPIR (Standard Portable Intermediate Representation) was initially developed for use by OpenCL and SPIR versions 1.2 and 2.0 were based on LLVM. SPIR has now evolved into a true cross-API standard that is fully defined by Khronos with native support for shader and kernel features – called SPIR-V.

> [The first open standard intermediate language for parallel compute and graphics](https://www.khronos.org/spir)