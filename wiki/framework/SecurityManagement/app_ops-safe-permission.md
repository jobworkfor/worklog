Android 4.3 隐藏功能 App Ops 分析
===============================
http://blog.mssun.me/security/android-4-3-app-ops-analysis/

一、背景知识
----------------------------------------------------------------------------------------------------
这一部分介绍了权限管理的相关知识，如果了解的可以跳过。我将简单介绍几个概念，提供一个方向，想深入了解的可以自己搜索相关资料。

1. 什么叫权限管理？

Android 的安全保护源于权限，每个 App 需要申请权限才能使用特定的功能，用户在安装的时候可以浏览 App 已申请的权限再决定是否安装。但是随着权限不断增多和残酷的现实证明了这一功能基本属于鸡肋。所以就出现了权限管理这一安全防护，所谓权限管理，就是能够手动配置某个 App 的权限，进而阻止恶意软件以及防止隐私泄漏。当然，更进一步的权限管理，是能够在 App 动态使用某个权限的时候，弹窗提示用户允许和拒绝。这样的权限管理就更加类似于 Windows 中的主动防御。

实现权限管理主要有三种方法：

重打包 (Repackage) ：app权限修改器：App Shield
Patch System ：PDroid
注入钩子 (Injection, Hook)：LBE安全大师，腾讯手机管家，360手机卫士……
当然，Android 4.3 出现 App Ops 以后，随着新版本的不断完善，这些方法可能就没有存在的意义了。

2. 什么是 Binder 通信？

TBA

3. 什么是权限中的保护级别 (Protection Level) 以及系统权限 (System Permission)？

Android 文档介绍的很清楚，protectionLevel 是 signatureOrSystem 的权限是系统 App 和相同签名的 App 才可以申请的。

4. 系统服务(System_Server)？

Android 启动后有很多服务进程提供比本功能，一些系统级的服务由 system_server 这个进程进行处理，其中包括电源管理，电话管理，包管理，蓝牙管理等等，详见Android的系统服务一览。还有一类我们常用的服务是不包括在系统服务当中的，比如说发短信，GPS等等，是由各自的服务进程处理的。

5. 如何开启 App Ops？

App Ops 其实就是 Settings 里面的一个 Activity,所以找个方法直接把它打开即可。
有两种简单方法:

在 Google Play 中直接安装 Permission Mangager。
下载一个 launcher，在桌面上建立快捷方式，选择 settings 里面的 App Ops。
二、系统架构
----------------------------------------------------------------------------------------------------

1. 架构

App Ops 的基本架构如图所示：
2013-07-31 18.58.51
其中包含两个重要部分，一个叫做AppOpsService，另外一个叫AppOpsManager。

AppOpsService 是一个系统服务，注册的名字叫做 “appops”，是最终检查权限的服务，其中权限管理存储在 appops.xml 文件里面。

AppOpsManager 是一个访问 AppOps 服务的类，同时有 Java 和 C 的实现，为了应对某些 native code 的服务，比如说 Camera。

Settings 可以使用 AppOpsManger 来读取和修改权限管理信息。当其他 App 使用某个权限的时候，会通过 Binder 访问服务端的某项服务。在服务端的各个服务中都插入了检查权限的代码，同样通过使用 AppOpsManger 来检查权限。

2. 代码分析

2.1 AppOpsService 代码在：/frameworks/base/services/java/com/android/server/AppOpsService.java

检查用户设定权限的函数是：checkOperation() 和 noteOperation()，区别是 checkOperation() 只是检查 Operation 的情况，noteOperation() 还会记录访问时间等信息，代码如下：

@Override
public int checkOperation(int code, int uid, String packageName) {
    verifyIncomingUid(uid);
    verifyIncomingOp(code);
    synchronized (this) {
        Op op = getOpLocked(AppOpsManager.opToSwitch(code), uid, packageName, false);
        if (op == null) {
            return AppOpsManager.MODE_ALLOWED;
        }
        return op.mode;
    }
}
 
@Override
public int noteOperation(int code, int uid, String packageName) {
    verifyIncomingUid(uid);
    verifyIncomingOp(code);
    synchronized (this) {
        Ops ops = getOpsLocked(uid, packageName, true);
        if (ops == null) {
            if (DEBUG) Log.d(TAG, "noteOperation: no op for code " + code + " uid " + uid
                    + " package " + packageName);
            return AppOpsManager.MODE_IGNORED;
        }
        Op op = getOpLocked(ops, code, true);
        if (op.duration == -1) {
            Slog.w(TAG, "Noting op not finished: uid " + uid + " pkg " + packageName
                    + " code " + code + " time=" + op.time + " duration=" + op.duration);
        }
        op.duration = 0;
        final int switchCode = AppOpsManager.opToSwitch(code);
        final Op switchOp = switchCode != code ? getOpLocked(ops, switchCode, true) : op;
        if (switchOp.mode != AppOpsManager.MODE_ALLOWED) {
            if (DEBUG) Log.d(TAG, "noteOperation: reject #" + op.mode + " for code "
                    + switchCode + " (" + code + ") uid " + uid + " package " + packageName);
            op.rejectTime = System.currentTimeMillis();
            return switchOp.mode;
        }
        if (DEBUG) Log.d(TAG, "noteOperation: allowing code " + code + " uid " + uid
                + " package " + packageName);
        op.time = System.currentTimeMillis();
        op.rejectTime = 0;
        return AppOpsManager.MODE_ALLOWED;
    }
}
修改某个 App 的某项权限的函数是 setMode()，其中就是修改成员变量 mUidOps。mUidOps 是一个List 保存了某个package对应的所有权限的mode (允许，忽略)，具体代码如下：


@Override
public void setMode(int code, int uid, String packageName, int mode) {
    verifyIncomingUid(uid);
    verifyIncomingOp(code);
    ArrayList<Callback> repCbs = null;
    code = AppOpsManager.opToSwitch(code);
    synchronized (this) {
        Op op = getOpLocked(code, uid, packageName, true);
        if (op != null) {
            if (op.mode != mode) {
                op.mode = mode;
                ArrayList<Callback> cbs = mOpModeWatchers.get(code);
                if (cbs != null) {
                    if (repCbs == null) {
                        repCbs = new ArrayList<Callback>();
                    }
                    repCbs.addAll(cbs);
                }
                cbs = mPackageModeWatchers.get(packageName);
                if (cbs != null) {
                    if (repCbs == null) {
                        repCbs = new ArrayList<Callback>();
                    }
                    repCbs.addAll(cbs);
                }
                if (mode == AppOpsManager.MODE_ALLOWED) {
                    // If going into the default mode, prune this op
                    // if there is nothing else interesting in it.
                    if (op.time == 0 && op.rejectTime == 0) {
                        Ops ops = getOpsLocked(uid, packageName, false);
                        if (ops != null) {
                            ops.remove(op.op);
                            if (ops.size() <= 0) {
                                HashMap<String, Ops> pkgOps = mUidOps.get(uid);
                                if (pkgOps != null) {
                                    pkgOps.remove(ops.packageName);
                                    if (pkgOps.size() <= 0) {
                                        mUidOps.remove(uid);
                                    }
                                }
                            }
                        }
                    }
                }
                scheduleWriteNowLocked();
            }
        }
    }
    if (repCbs != null) {
        for (int i=0; i<repCbs.size(); i++) {
            try {
                repCbs.get(i).mCallback.opChanged(code, packageName);
            } catch (RemoteException e) {
            }
        }
    }
}
修改 mode 之后会通过 writeState（） 的函数，最终写入文件当中，他用 appops.xml 来存储 App Ops 信息，如果想了解 xml 中的各个 tag 的语义，可以查看 writeState() 函数的实现。 简单来说他会记录 uid, 包名，mode,访问时间，拒绝时间。

2.2 AppOpsManager 是一个管理类来和 AppOpsService 通信，他的函数实现比较简单，重点是把控制转移到 AppOpsService 就可以了。例如 noteOperation() 和 setMode() 在 AppOpsManager 里面调用他们的函数是 noteOp() 和 setMode()，代码如下：

public int noteOp(int op, int uid, String packageName) {
    try {
        int mode = mService.noteOperation(op, uid, packageName);
        if (mode == MODE_ERRORED) {
            throw new SecurityException("Operation not allowed");
        }
        return mode;
    } catch (RemoteException e) {
    }
    return MODE_IGNORED;
}
 
public void setMode(int code, int uid, String packageName, int mode) {
    try {
        mService.setMode(code, uid, packageName, mode);
    } catch (RemoteException e) {
    }
}
2.3 拦截代码
有了 noteOp() 函数，但是要完成权限的动态检查，还要在执行某项权限的时候执行 noteOp()。经过分析，大概有十多个服务被插入了权限检查函数。其中包括：ClipboardService, VibratorService, LocationManagerService, NotificationManagerService, GeofenceManager, GpsLocationProvider, IccSmsInterfaceManager, PhoneInterfaceManager, OutgoingCallBroadcaster, WifiService, ContentProvider, WindowManagerService 等等。更多详细情况，可以查看 AndroidXRef 中的源码。

三、实例分析
----------------------------------------------------------------------------------------------------

我们选取短信相关权限进行分析，看看 App Ops 究竟是如何进行权限控制的。首先我们了解一下发短信的流程，发短信的代码很简单，主要分两个步骤：


SmsManager smsManager=SmsManager.getDefault();
smsManager.sendTextMessage("dest", "src", "content", null, null);
第一步是通过 Binder 获取 Server 段的发送短信服务 isms service。第二部是调用远端的sendTextMessage() 函数。通过 Proxy Pattern，最后到达实现的方法，位于IccSmsInterfaceManager 中的 sendText()方法，我们先看一下代码：

@Override
public void sendText(String callingPackage, String destAddr, String scAddr,
        String text, PendingIntent sentIntent, PendingIntent deliveryIntent) {
    mPhone.getContext().enforceCallingPermission(
            Manifest.permission.SEND_SMS,
            "Sending SMS message");
    if (Rlog.isLoggable("SMS", Log.VERBOSE)) {
        log("sendText: destAddr=" + destAddr + " scAddr=" + scAddr +
            " text='"+ text + "' sentIntent=" +
            sentIntent + " deliveryIntent=" + deliveryIntent);
    }
    if (mAppOps.noteOp(AppOpsManager.OP_SEND_SMS, Binder.getCallingUid(),
            callingPackage) != AppOpsManager.MODE_ALLOWED) {
        return;
    }
    mDispatcher.sendText(destAddr, scAddr, text, sentIntent, deliveryIntent);
}
远端 sendText() 函数首先通过 enforceCallingPermission() 函数来检查 App 是否在 AndroidManifest.xml 中申请了 android.permission.SEND_SMS 的权限。然后在通过调用 mAppOps (AppOpsService 的服务端实例 AppOpsManager) 调用 noteOp（） 函数检查是否通过了用户的权限设置。很有意思的是，如果没有通过检查，就直接 return。所以程序有时候会有提示，有时候假死然后退出。应该说这是 Android 4.3 中 Google 还未完成的代码，只是暂时完成基本功能而已。

四、结语
----------------------------------------------------------------------------------------------------

此次 Google 在 Android 4.3 中加入了权限管理的功能，虽然代码还未完善，但是思路和框架设计的比较好，可能不会引出什么新的漏洞。Google 在迎合大众的需要的同时，故意放出了一个半成品，来测试一下大家的反映。估计照这个效果下去，Android 5 很有可能就能完善这项特性。到那时候我们就真的该考虑，我们还需要 root 么？或许混乱的国内定制机还有他的广阔市场吧。


reference
----------------------------------------------------------------------------------------------------
* [Android 5.1 AppOps总结](http://blog.csdn.net/lewif/article/details/49124757)