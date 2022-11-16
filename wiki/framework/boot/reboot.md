Android Reboot
================

reboot的类型：
1. 手动长按power键选择reboot；
2. adb reboot；
3. 手动长按power键11s触发reboot；
4. BUG_ON(1)，触发kernel panic流程reboot;

上面1、2、4的本质上代码跑的是一样的，3 是直接触发hardware实现，下面主要分析第1类正常的关键源码流程。


重启流程(reboot.c)
----------------------------------------------------------------------------------------------------
* == shell ==
* [`int main(int argc, char* argv[]) {`](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/reboot/reboot.c#24)
    * [prop_len = snprintf(property_val, sizeof(property_val), "%s,%s", cmd, optarg);](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/reboot/reboot.c#67)
    * [ret = property_set(ANDROID_RB_PROPERTY="sys.powerctl", property_val);](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/reboot/reboot.c#67)
* == init ==
* [`static uint32_t PropertySet(const std::string& name, const std::string& value, std::string* error) {`](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/property_service.cpp#130)
    * [property_changed(name, value);](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/property_service.cpp#170)
    * [`void property_changed(const std::string& name, const std::string& value) {`](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/init.cpp#165)
        * [shutdown_command = value;](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/init.cpp#181)
        * [do_shutdown = true;](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/init.cpp#182)
        * [if (property_triggers_enabled) ActionManager::GetInstance().QueuePropertyChange(name, value);](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/init.cpp#185)
* [<b>if (HandlePowerctlMessage(shutdown_command)) {</b>](#3)
    * [bool HandlePowerctlMessage(const std::string& command) {](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/reboot.cpp#480)
        * [<b>DoReboot(cmd, command, reboot_target, run_fsck);</b>](#4)
            * [RebootSystem(cmd, rebootTarget);](http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/reboot.cpp#476)
                * [<b>syscall(__NR_reboot, LINUX_REBOOT_MAGIC1, LINUX_REBOOT_MAGIC2,</b>](#5)
* -- kernel --
* [`SYSCALL_DEFINE4(reboot, int, magic1, int, magic2, unsigned int, cmd,`](http://androidxref.blackshark.com:8088/sm8150/xref/kernel/msm-4.14/kernel/reboot.c#280)
    * [<b>kernel_restart(buffer);</b>](#6)

----------------------------------------------------------------------------------------------------

### <a id=3></a>HandlePowerctlMessage(shutdown_command)
init进程一直监听着`property`变更事件，当发生变化时，走如下代码。

```cpp
808    while (true) {
809        // By default, sleep until something happens.
810        int epoll_timeout_ms = -1;
811
812        if (do_shutdown && !shutting_down) {
813            do_shutdown = false;
814            if (HandlePowerctlMessage(shutdown_command)) {
815                shutting_down = true;
816            }
817        }
...
846    }
```
> http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/init.cpp#814

### <a id=4></a>HandlePowerctlMessage(const std::string& command)
```cpp
480bool HandlePowerctlMessage(const std::string& command) {
481    unsigned int cmd = 0;
482    std::vector<std::string> cmd_params = Split(command, ",");
...
489    } else if (cmd_params[0] == "shutdown") {
...
492            if (cmd_params[1] == "userrequested") {
...
496            } else if (cmd_params[1] == "thermal") {
...
503    } else if (cmd_params[0] == "reboot") {
504        cmd = ANDROID_RB_RESTART2;
...
507            // When rebooting to the bootloader notify the bootloader writing
508            // also the BCB.
509            if (reboot_target == "bootloader") {
...
524    }
...
535    auto shutdown_handler = [cmd, command, reboot_target, run_fsck](const BuiltinArguments&) {
536        DoReboot(cmd, command, reboot_target, run_fsck);
537        return Success();
538    };
539->  ActionManager::GetInstance().QueueBuiltinAction(shutdown_handler, "shutdown_done");
...
550}
```
此处`cmd = ANDROID_RB_RESTART2;`，接着调用DoReboot()->RebootSystem()函数

> http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/reboot.cpp#536

### <a id=5></a>RebootSystem(unsigned int cmd, const std::string& rebootTarget)
```cpp
184void __attribute__((noreturn)) RebootSystem(unsigned int cmd, const std::string& rebootTarget) {
185    LOG(INFO) << "Reboot ending, jumping to kernel";
186
187    if (!IsRebootCapable()) {
188        // On systems where init does not have the capability of rebooting the
189        // device, just exit cleanly.
190        exit(0);
191    }
192
193    switch (cmd) {
194        case ANDROID_RB_POWEROFF:
195            reboot(RB_POWER_OFF);
196            break;
197
198        case ANDROID_RB_RESTART2:
199->          syscall(__NR_reboot, LINUX_REBOOT_MAGIC1, LINUX_REBOOT_MAGIC2,
200                    LINUX_REBOOT_CMD_RESTART2, rebootTarget.c_str());
201            break;
202
203        case ANDROID_RB_THERMOFF:
204            reboot(RB_POWER_OFF);
205            break;
206    }
207    // In normal case, reboot should not return.
208    PLOG(ERROR) << "reboot call returned";
209    abort();
210}
```
> http://androidxref.blackshark.com:8088/sm8150/xref/system/core/init/reboot.cpp#199


### <a id=6></a>SYSCALL_DEFINE4(reboot, int, magic1, int, magic2, unsigned int, cmd,

```cpp
280SYSCALL_DEFINE4(reboot, int, magic1, int, magic2, unsigned int, cmd,
281		void __user *, arg)
282{
...
333	case LINUX_REBOOT_CMD_POWER_OFF:
334		kernel_power_off();
335		do_exit(0);
336		break;
337
338	case LINUX_REBOOT_CMD_RESTART2:
339		ret = strncpy_from_user(&buffer[0], arg, sizeof(buffer) - 1);
340		if (ret < 0) {
341			ret = -EFAULT;
342			break;
343		}
344		buffer[sizeof(buffer) - 1] = '\0';
345
346->   kernel_restart(buffer);
347		break;
348
...
366	return ret;
367}
```
> http://androidxref.blackshark.com:8088/sm8150/xref/kernel/msm-4.14/kernel/reboot.c#346


FWK重启流程(PowerManager.java)
----------------------------------------------------------------------------------------------------
* == system_server ==
* [<b>`public void reboot(String reason) {`</b>](#main)
    * [mService.reboot(false, reason, true);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/core/java/android/os/PowerManager.java#1099)
    * [`public void reboot(boolean confirm, String reason, boolean wait) {`](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/PowerManagerService.java#4420)
        * [shutdownOrRebootInternal(HALT_MODE_REBOOT, confirm, reason, wait);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/PowerManagerService.java#4429)
            * [<b>ShutdownThread.reboot(getUiContext(), reason, confirm);</b>](#1)
                * [shutdownInner(context, confirm);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#242)
                    * [Log.d(TAG, "Notifying thread to start shutdown longPressBehavior=" + longPressBehavior);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#178)
                    * [beginShutdownSequence(context);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#192)
                        * [sInstance.start();](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#408)
* -- shutdown thread --
* [public void run() {](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#422)
    * [Log.i(TAG, "Shutting down package manager...");](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#506)
    * [shutdownTimingLog.traceBegin("ShutdownRadios");](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#522)
    * [rebootOrShutdown(mContext, mReboot, mReason);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#543)
        * [Log.i(TAG, "Rebooting, reason: " + reason);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#718)
        * [PowerManagerService.lowLevelReboot(reason);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/ShutdownThread.java#719)
            * [SystemProperties.set("sys.powerctl", "reboot," + reason);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/PowerManagerService.java#3202)

----------------------------------------------------------------------------------------------------

### <a id=main></a>PowerManager.main()
1. 在PowerManager的API文档中，给出了一个关机/重启接口：
```cpp
    public void reboot (String reason)
```
> http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/core/java/android/os/PowerManager.java#1097
2. 对于这个接口的描述很简单，就是几句话。
    * 接口的作用就是重启设备，而且，就算重启成功了也没有返回值。
    * 需要包含REBOOT权限，也就是android.permission.REBOOT
    * 唯一参数reason代表需要的特定重启模式，比如recovery，当然也可以为null。


### <a id=1></a>ShutdownThread.reboot()
```cpp
2723    private void shutdownOrRebootInternal(final @HaltMode int haltMode, final boolean confirm,
2724            final String reason, boolean wait) {
...
2736        Runnable runnable = new Runnable() {
2737            @Override
2738            public void run() {
2739                synchronized (this) {
2740                    if (haltMode == HALT_MODE_REBOOT_SAFE_MODE) {
2741                        ShutdownThread.rebootSafeMode(getUiContext(), confirm);
2742                    } else if (haltMode == HALT_MODE_REBOOT) {
2743->                      ShutdownThread.reboot(getUiContext(), reason, confirm);
2744                    } else {
2745                        ShutdownThread.shutdown(getUiContext(), reason, confirm);
2746                    }
2747                }
2748            }
2749        };
```
> http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/power/PowerManagerService.java#2743
