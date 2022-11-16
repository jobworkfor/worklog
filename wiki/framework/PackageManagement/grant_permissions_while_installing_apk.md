Grant Signature Permission
==========================

授予权限时的调用栈
----------------------------------------------------------------------------------------------------
* [mSession.commit(statusReceiver, false);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/core/java/android/content/pm/PackageInstaller.java#969)
    * [<b>mHandler.obtainMessage(MSG_COMMIT).sendToTarget();</b>](#MSG_COMMIT)
* [commitLocked();](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageInstallerSession.java#294)    
    * [mPm.installStage(mPackageName, stageDir, localObserver, params,](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageInstallerSession.java#1041)
        * [final Message msg = mHandler.obtainMessage(INIT_COPY);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#13798)
        * [<b>mHandler.sendMessage(msg);</b>](#INIT_COPY)
* [doHandleMessage(msg);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#1448)
    * [if (!connectToService()) {](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#1479)
        * [<b>if (mContext.bindServiceAsUser(service, mDefContainerConn,</b>](#bindServiceAsUser)
* [public void onServiceConnected(ComponentName name, IBinder service) {](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#1347)
    * [<b>mHandler.sendMessage(mHandler.obtainMessage(MCS_BOUND, imcs));</b>](#MCS_BOUND)
* [doHandleMessage(msg);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#1448)
    * [if (params.startCopy()) {](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#1536)
        * [handleReturnCode();](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#15104)
            * [processPendingInstall(mArgs, mRet);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#15645)
                * [<b>mHandler.post(new Runnable() {</b>](#postrunnable)
* [installPackageTracedLI(args, res);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#14928)
    * [installPackageLI(args, res);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#17012)
        * [installNewPackageLIF(pkg, parseFlags, scanFlags | SCAN_DELETE_DATA_ON_FAILURES,](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#17524)
            * [updateSettingsLI(newPackage, installerPackageName, null, res, user, installReason);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#16316)
                * [updateSettingsInternalLI(newPackage, installerPackageName, allUsers, res.origUsers,](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#16905)
                    * [mPermissionManager.updatePermissions(pkg.packageName, pkg, true, mPackages.values(),](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#16928)
                        * [grantPermissions(pkg, replace, changingPkgName, callback);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/permission/PermissionManagerService.java#1744)
                            * [allowedSig = grantSignaturePermission(perm, pkg, bp, origPermissions);](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/permission/PermissionManagerService.java#787)
                                * [<b>boolean allowed =</b>](#grantSignaturePermission)
                            * [grant = GRANT_INSTALL;](http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/permission/PermissionManagerService.java#789)

> refs/tags/android-9.0.0_r18

----------------------------------------------------------------------------------------------------
### <a id=MSG_COMMIT></a>MSG:mHandler.obtainMessage(MSG_COMMIT, adapter.getBinder()).sendToTarget();
```cpp
    "Binder:20317_3@8038" prio=5 tid=0x22 nid=NA runnable
      java.lang.Thread.State: RUNNABLE
          at com.android.server.pm.PackageInstallerSession.commit(PackageInstallerSession.java:542)
          at android.content.pm.PackageInstaller$Session.commit(PackageInstaller.java:815)
          at com.android.server.pm.PackageManagerShellCommand.doCommitSession(PackageManagerShellCommand.java:1267)
          at com.android.server.pm.PackageManagerShellCommand.runInstall(PackageManagerShellCommand.java:180)
          at com.android.server.pm.PackageManagerShellCommand.onCommand(PackageManagerShellCommand.java:99)
          at android.os.ShellCommand.exec(ShellCommand.java:94)
          at com.android.server.pm.PackageManagerService.onShellCommand(PackageManagerService.java:18942)
          at android.os.Binder.shellCommand(Binder.java:468)
          at android.os.Binder.onTransact(Binder.java:367)
          at android.content.pm.IPackageManager$Stub.onTransact(IPackageManager.java:2387)
          at com.android.server.pm.PackageManagerService.onTransact(PackageManagerService.java:3182)
          at android.os.Binder.execTransact(Binder.java:565)
```
> http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageInstallerSession.java#829


### <a id=INIT_COPY></a>MSG:mHandler.sendMessage(INIT_COPY);
```cpp
    "PackageInstaller@8128" prio=5 tid=0x2b nid=NA runnable
      java.lang.Thread.State: RUNNABLE
          at android.os.Handler.sendMessage(Handler.java:519)
          at com.android.server.pm.PackageManagerService.installStage(PackageManagerService.java:12129)
          at com.android.server.pm.PackageInstallerSession.commitLocked(PackageInstallerSession.java:660)
          at com.android.server.pm.PackageInstallerSession.-wrap0(PackageInstallerSession.java:-1)
          at com.android.server.pm.PackageInstallerSession$3.handleMessage(PackageInstallerSession.java:216)
          - locked <0x2060> (a java.lang.Object)
          at android.os.Handler.dispatchMessage(Handler.java:98)
          at android.os.Looper.loop(Looper.java:154)
          at android.os.HandlerThread.run(HandlerThread.java:61)

```
> http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#13813


### <a id=bindServiceAsUser></a>MSG:mContext.bindServiceAsUser(service, mDefContainerConn, Context.BIND_AUTO_CREATE, UserHandle.SYSTEM)
```cpp
    "PackageManager@8067" prio=5 tid=0x22 nid=NA runnable
      java.lang.Thread.State: RUNNABLE
          at com.android.server.pm.PackageManagerService$PackageHandler.connectToService(PackageManagerService.java:1191)
          at com.android.server.pm.PackageManagerService$PackageHandler.doHandleMessage(PackageManagerService.java:1235)
          at com.android.server.pm.PackageManagerService$PackageHandler.handleMessage(PackageManagerService.java:1215)
          at android.os.Handler.dispatchMessage(Handler.java:102)
          at android.os.Looper.loop(Looper.java:154)
          at android.os.HandlerThread.run(HandlerThread.java:61)
          at com.android.server.ServiceThread.run(ServiceThread.java:46)
```
> http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#1424

### <a id=MCS_BOUND></a>MSG:mHandler.sendMessage(mHandler.obtainMessage(MCS_BOUND, imcs));
```cpp
    "main@33635" prio=5 tid=0x1 nid=NA runnable
      java.lang.Thread.State: RUNNABLE
          at android.os.Handler.sendMessage(Handler.java:519)
          at com.android.server.pm.PackageManagerService$DefaultContainerConnection.onServiceConnected(PackageManagerService.java:1118)
          at android.app.LoadedApk$ServiceDispatcher.doConnected(LoadedApk.java:1467)
          at android.app.LoadedApk$ServiceDispatcher$RunConnection.run(LoadedApk.java:1495)
          at android.os.Handler.handleCallback(Handler.java:751)
          at android.os.Handler.dispatchMessage(Handler.java:95)
          at android.os.Looper.loop(Looper.java:154)
          at com.android.server.SystemServer.run(SystemServer.java:376)
          at com.android.server.SystemServer.main(SystemServer.java:242)
          at java.lang.reflect.Method.invoke(Method.java:-1)
          at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:929)
          at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:819)
```
> http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#1351

### <a id=postrunnable></a>MSG:mHandler.post(new Runnable() {...})
```cpp
    "PackageManager@8207" prio=5 tid=0x22 nid=NA runnable
      java.lang.Thread.State: RUNNABLE
          at android.os.Handler.post(Handler.java:338)
          at com.android.server.pm.PackageManagerService.processPendingInstall(PackageManagerService.java:12885)
          at com.android.server.pm.PackageManagerService.-wrap33(PackageManagerService.java:-1)
          at com.android.server.pm.PackageManagerService$InstallParams.handleReturnCode(PackageManagerService.java:13693)
          at com.android.server.pm.PackageManagerService$HandlerParams.startCopy(PackageManagerService.java:13068)
          at com.android.server.pm.PackageManagerService$PackageHandler.doHandleMessage(PackageManagerService.java:1293)
          at com.android.server.pm.PackageManagerService$PackageHandler.handleMessage(PackageManagerService.java:1215)
          at android.os.Handler.dispatchMessage(Handler.java:102)
          at android.os.Looper.loop(Looper.java:154)
          at android.os.HandlerThread.run(HandlerThread.java:61)
          at com.android.server.ServiceThread.run(ServiceThread.java:46)
```
> http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java#14916


### <a id=grantSignaturePermission></a>PackageManagerService.grantSignaturePermission
```cpp
    11-28 14:33:39.175  1685  1883 D bob_log_tag:  	_ [PackageManagerService.grantSignaturePermission:10626] 
    11-28 14:33:39.175  1685  1883 D bob_log_tag:   param: android.permission.MODIFY_PHONE_STATE
    11-28 14:33:39.175  1685  1883 D bob_log_tag:   pkg: Package{5a29170 com.qrd.omadownload}
    11-28 14:33:39.175  1685  1883 D bob_log_tag:   bp: BasePermission{b283ce9 android.permission.MODIFY_PHONE_STATE}
    11-28 14:33:39.175  1685  1883 D bob_log_tag:   origPermissions: com.android.server.pm.PermissionsState@7e71d6e
    11-28 14:33:39.175  1685  1883 D bob_log_tag:   pid1685
    11-28 14:33:39.175  1685  1883 D bob_log_tag:   tName: PackageManager
    11-28 14:33:39.175  1685  1883 D bob_log_tag:   this: 9733c0f
    11-28 14:33:39.175  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.grantSignaturePermission(PackageManagerService.java:10635)
    11-28 14:33:39.175  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.grantPermissionsLPw(PackageManagerService.java:10390)
    11-28 14:33:39.175  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.updatePermissionsLPw(PackageManagerService.java:10259)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.updatePermissionsLPw(PackageManagerService.java:10182)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.updateSettingsInternalLI(PackageManagerService.java:15366)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.updateSettingsLI(PackageManagerService.java:15335)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.installNewPackageLIF(PackageManagerService.java:14710)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.installPackageLI(PackageManagerService.java:15788)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.installPackageTracedLI(PackageManagerService.java:15427)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService.-wrap26(PackageManagerService.java)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.pm.PackageManagerService$10.run(PackageManagerService.java:12897)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- android.os.Handler.handleCallback(Handler.java:751)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- android.os.Handler.dispatchMessage(Handler.java:95)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- android.os.Looper.loop(Looper.java:154)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- android.os.HandlerThread.run(HandlerThread.java:61)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	|-- com.android.server.ServiceThread.run(ServiceThread.java:46)
    11-28 14:33:39.176  1685  1883 D bob_log_tag:  	@
```
> http://127.0.0.1:8080/android-aosp/xref/frameworks/base/services/core/java/com/android/server/pm/permission/PermissionManagerService.java#1096



权限定义相关文件
----------------------------------------------------------------------------------------------------
### /frameworks/base/core/res/AndroidManifest.xml
声明android permission的地方。对于protectionLevel是signature的权限，因此处声明的package是"android"，所以其他应用需要使用该权限时，
需要和"android"应用相同的签名，即系统签名。

官方文档介绍
```
"signature"
A permission that the system grants only if the requesting application is signed with the same certificate as
the application that declared the permission. If the certificates match, the system automatically grants
the permission without notifying the user or asking for the user's explicit approval.
```

eg.
```
1542    <permission android:name="android.permission.NET_ADMIN"
1543        android:protectionLevel="signature" />
```

### /frameworks/base/data/etc/platform.xml
android权限和gid匹配声明的地方，该文件将android权限和linux gid联系起来。

eg.
```
71    <permission name="android.permission.NET_ADMIN" >
72        <group gid="net_admin" />
73    </permission>
```

### /system/core/include/private/android_filesystem_config.h
定义gid的地方，模仿已有的变量名（AID_前缀），系统会自动生成对应的gid。

代码注释
```
188/*
189 * android_ids has moved to pwd/grp functionality.
190 * If you need to add one, the structure is now
191 * auto-generated based on the AID_ constraints
192 * documented at the top of this header file.
193 * Also see build/tools/fs_config for more details.
194 */
```

eg.
```
152#define AID_NET_ADMIN 3005    /* can configure interfaces and routing tables. */
```


签名权限授予
------------
如下patch会绕过授权签名权限检查，只要包名是"com.ezx.probe"的应用，都可以授予平台签名权限
```
frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java

    private boolean grantSignaturePermission(String perm, PackageParser.Package pkg,
            BasePermission bp, PermissionsState origPermissions) {
        allowed = (compareSignatures(
                ...
                || "com.ezx.probe".equals(pkg.packageName);
    }
```

eg.
在"com.ezx.probe"应用的AndroidManifest.xml中添加使用权限：
```
    <uses-permission android:name="android.permission.NET_ADMIN"/>
```
安装后查看`/data/system/packages.list`文件：
```
com.ezx.probe 10104 1 /data/user/0/com.ezx.probe default 3003,3005
```
有`3005`说明来该应用已经具备来本不能有的`android.permission.NET_ADMIN`权限。

