*   https://elinux.org/Android_Zygote_Startup
*   art虚拟机启动过程分析 https://www.jianshu.com/p/29fbc15589d1
*   Allow debugging only for apps forked from zygote https://gitlab.tubit.tu-berlin.de/justus.beyer/streamagame_platform_frameworks_base/commit/7a09b8322cab26d6e3da1362d3c74964ae66b5d4
*   Android VM 的启动流程以及 JNI 的通信原理 https://juejin.im/post/6844904084814708744
*   http://androidxref.blackshark.com:8088/sm8250/xref/frameworks/base/cmds/app_process/app_main.cpp

````bash
xref: /system/core/rootdir/init.zygote64.rc
1service zygote /system/bin/app_process64 -Xzygote /system/bin --zygote --start-system-server
2    class main
3    priority -20
4    user root
5    group root readproc reserved_disk
6    socket zygote stream 660 root system
7    socket usap_pool_primary stream 660 root system
8    onrestart write /sys/android_power/request_state wake
9    onrestart write /sys/power/state on
10    onrestart restart audioserver
11    onrestart restart cameraserver
12    onrestart restart media
13    onrestart restart netd
14    onrestart restart wificond
15    onrestart restart vendor.servicetracker-1-1
16    writepid /dev/cpuset/foreground/tasks
````



````bash
09-14 07:15:28.051 29532 29532 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
09-14 07:15:28.055 29532 29532 I AndroidRuntime: Using default boot image
09-14 07:15:28.055 29532 29532 I AndroidRuntime: Leaving lock profiling enabled
09-14 07:15:28.057 29532 29532 I vm-printf: Unknown argument: --nice-name=com.ezx.probe
09-14 07:15:28.057 29532 29532 I vm-printf: dalvikvm: [options] class [argument ...]
09-14 07:15:28.057 29532 29532 I vm-printf:
09-14 07:15:28.057 29532 29532 I vm-printf: The following standard options are supported:
09-14 07:15:28.057 29532 29532 I vm-printf:   -classpath classpath (-cp classpath)
09-14 07:15:28.057 29532 29532 I vm-printf:   -Dproperty=value
09-14 07:15:28.057 29532 29532 I vm-printf:   -verbose:tag ('gc', 'jit', 'jni', or 'class')
09-14 07:15:28.057 29532 29532 I vm-printf:   -showversion
09-14 07:15:28.057 29532 29532 I vm-printf:   -help
09-14 07:15:28.057 29532 29532 I vm-printf:   -agentlib:jdwp=options
09-14 07:15:28.057 29532 29532 I vm-printf:   -agentpath:library_path=options (Experimental feature, requires -Xexperimental:agent, some features might not be supported)
09-14 07:15:28.057 29532 29532 I vm-printf:
09-14 07:15:28.057 29532 29532 I vm-printf: The following extended options are supported:
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xrunjdwp:<options>
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xbootclasspath:bootclasspath
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xcheck:tag  (e.g. 'jni')
09-14 07:15:28.057 29532 29532 I vm-printf:   -XmsN (min heap, must be multiple of 1K, >= 1MB)
09-14 07:15:28.057 29532 29532 I vm-printf:   -XmxN (max heap, must be multiple of 1K, >= 2MB)
09-14 07:15:28.057 29532 29532 I vm-printf:   -XssN (stack size)
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xint
09-14 07:15:28.057 29532 29532 I vm-printf:
09-14 07:15:28.057 29532 29532 I vm-printf: The following Dalvik options are supported:
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xzygote
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xjnitrace:substring (eg NativeClass or nativeMethod)
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xgc:[no]preverify
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xgc:[no]postverify
09-14 07:15:28.057 29532 29532 I vm-printf:   -XX:HeapGrowthLimit=N
09-14 07:15:28.057 29532 29532 I vm-printf:   -XX:HeapMinFree=N
09-14 07:15:28.057 29532 29532 I vm-printf:   -XX:HeapMaxFree=N
09-14 07:15:28.057 29532 29532 I vm-printf:   -XX:NonMovingSpaceCapacity=N
09-14 07:15:28.057 29532 29532 I vm-printf:   -XX:HeapTargetUtilization=doublevalue
09-14 07:15:28.057 29532 29532 I vm-printf:   -XX:ForegroundHeapGrowthMultiplier=doublevalue
09-14 07:15:28.057 29532 29532 I vm-printf:   -XX:LowMemoryMode
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xprofile:{threadcpuclock,wallclock,dualclock}
09-14 07:15:28.057 29532 29532 I vm-printf:   -Xjitthreshold:integervalue
09-14 07:15:28.057 29532 29532 I vm-printf:
09-14 07:15:28.057 29532 29532 I vm-printf: The following unique to ART options are supported:
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xgc:[no]preverify_rosalloc
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xgc:[no]postsweepingverify_rosalloc
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xgc:[no]postverify_rosalloc
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xgc:[no]presweepingverify
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xgc:[no]generational_cc
09-14 07:15:28.058 29532 29532 I vm-printf:   -Ximage:filename
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xbootclasspath-locations:bootclasspath
09-14 07:15:28.058 29532 29532 I vm-printf:      (override the dex locations of the -Xbootclasspath files)
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:+DisableExplicitGC
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:ParallelGCThreads=integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:ConcGCThreads=integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:FinalizerTimeoutMs=integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:MaxSpinsBeforeThinLockInflation=integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:LongPauseLogThreshold=integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:LongGCLogThreshold=integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:ThreadSuspendTimeout=integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:DumpGCPerformanceOnShutdown
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:DumpJITInfoOnShutdown
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:IgnoreMaxFootprint
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:UseTLAB
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:BackgroundGC=none
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:LargeObjectSpace={disabled,map,freelist}
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:LargeObjectThreshold=N
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:DumpNativeStackOnSigQuit=booleanvalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:MadviseRandomAccess:booleanvalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -XX:SlowDebug={false,true}
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xmethod-trace
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xmethod-trace-file:filename
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xmethod-trace-file-size:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-min-save-period-ms:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-save-resolved-classes-delay-ms:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-hot-startup-method-samples:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-min-methods-to-save:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-min-classes-to-save:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-min-notification-before-wake:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-max-notification-before-wake:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xps-profile-path:file-path
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xcompiler:filename
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xcompiler-option dex2oat-option
09-14 07:15:28.058 29532 29532 I vm-printf:   -Ximage-compiler-option dex2oat-option
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xusejit:booleanvalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitinitialsize:N
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitmaxsize:N
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitwarmupthreshold:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitosrthreshold:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitprithreadweight:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -X[no]relocate
09-14 07:15:28.058 29532 29532 I vm-printf:   -X[no]dex2oat (Whether to invoke dex2oat on the application)
09-14 07:15:28.058 29532 29532 I vm-printf:   -X[no]image-dex2oat (Whether to create and use a boot image)
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xno-dex-file-fallback (Don't fall back to dex files without oat files)
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xplugin:<library.so> (Load a runtime plugin, requires -Xexperimental:runtime-plugins)
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xexperimental:runtime-plugins(Enable new and experimental agent support)
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xexperimental:agents(Enable new and experimental agent support)
09-14 07:15:28.058 29532 29532 I vm-printf:
09-14 07:15:28.058 29532 29532 I vm-printf: The following previously supported Dalvik options are ignored:
09-14 07:15:28.058 29532 29532 I vm-printf:   -ea[:<package name>... |:<class name>]
09-14 07:15:28.058 29532 29532 I vm-printf:   -da[:<package name>... |:<class name>]
09-14 07:15:28.058 29532 29532 I vm-printf:    (-enableassertions, -disableassertions)
09-14 07:15:28.058 29532 29532 I vm-printf:   -esa
09-14 07:15:28.058 29532 29532 I vm-printf:   -dsa
09-14 07:15:28.058 29532 29532 I vm-printf:    (-enablesystemassertions, -disablesystemassertions)
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xverify:{none,remote,all,softfail}
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xrs
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xint:portable, -Xint:fast, -Xint:jit
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xdexopt:{none,verified,all,full}
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xnoquithandler
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjniopts:{warnonly,forcecopy}
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjnigreflimit:integervalue
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xgc:[no]precise
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xgc:[no]verifycardtable
09-14 07:15:28.058 29532 29532 I vm-printf:   -X[no]genregmap
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xverifyopt:[no]checkmon
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xcheckdexsum
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xincludeselectedop
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitop:hexopvalue[-endvalue][,hexopvalue[-endvalue]]*
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xincludeselectedmethod
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitblocking
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitmethod:signature[,signature]* (eg Ljava/lang/String\;replace)
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitclass:classname[,classname]*
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitcodecachesize:N
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitoffset:offset[,offset]
09-14 07:15:28.058 29532 29532 I vm-printf:   -Xjitconfig:filename
09-14 07:15:28.059 29532 29532 I vm-printf:   -Xjitcheckcg
09-14 07:15:28.059 29532 29532 I vm-printf:   -Xjitverbose
09-14 07:15:28.059 29532 29532 I vm-printf:   -Xjitprofile
09-14 07:15:28.059 29532 29532 I vm-printf:   -Xjitdisableopt
09-14 07:15:28.059 29532 29532 I vm-printf:   -Xjitsuspendpoll
09-14 07:15:28.059 29532 29532 I vm-printf:   -XX:mainThreadStackSize=N
09-14 07:15:28.059 29532 29532 I vm-printf:
09-14 07:15:28.059 29532 29532 I AndroidRuntime: VM exiting with result code 1.
````

