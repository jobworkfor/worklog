> TelecomService运行在system进程中，其对应的binder引用被保存到ServiceManager的service引用中。TelecomService是在TelecomLoaderService中通过bind方式启动的，TelecomLoaderService是由SystemServer在开机启动过程中创建的。

TelecomService
==============

启动过程
------------------------------------------------------------------------------------------------------------------------
最初的启动过程
```
02-16 22:34:12.257  1305  1305 D bob_log_tag:  	_ [com.android.server.SystemServer.startOtherServices]   this: ec8650b
02-16 22:34:12.259  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServer.startOtherServices(SystemServer.java:572) <-
02-16 22:34:12.260  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServer.run(SystemServer.java:335)
02-16 22:34:12.260  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServer.main(SystemServer.java:220)
02-16 22:34:12.260  1305  1305 D bob_log_tag:  	|-- java.lang.reflect.Method.invoke(Native Method)
02-16 22:34:12.260  1305  1305 D bob_log_tag:  	|-- com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:886)
02-16 22:34:12.260  1305  1305 D bob_log_tag:  	|-- com.android.internal.os.ZygoteInit.main(ZygoteInit.java:776)
02-16 22:34:12.260  1305  1305 D bob_log_tag:  	@
```

```
com.android.server.SystemServer.startOtherServices(){
    mSystemServiceManager.startService(TelecomLoaderService.class);
}
```
startService()会new出TelecomLoaderService对象，接着会调用PMS来设置一些telecom相关默认应用的信息。


接着在startOtherServices()方法中继续调用onBootPhase()方法，调用栈如下：
```
02-16 22:34:13.038  1305  1305 D bob_log_tag:  	_ [onBootPhase]   this: 29f104
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.server.telecom.TelecomLoaderService.onBootPhase(TelecomLoaderService.java:173)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServiceManager.startBootPhase(SystemServiceManager.java:142)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServer$2.run(SystemServer.java:1320)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.server.am.ActivityManagerService.systemReady(ActivityManagerService.java:13313)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServer.startOtherServices(SystemServer.java:1316) <-
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServer.run(SystemServer.java:335)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.server.SystemServer.main(SystemServer.java:220)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- java.lang.reflect.Method.invoke(Native Method)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:886)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	|-- com.android.internal.os.ZygoteInit.main(ZygoteInit.java:776)
02-16 22:34:13.039  1305  1305 D bob_log_tag:  	@
```

```
com.android.server.telecom.TelecomLoaderService.onBootPhase(){
    connectToTelecom();
}
```

### 启动过程中bind到TelecomService
```
com.android.server.telecom.TelecomLoaderService.connectToTelecom(){
    // SERVICE_ACTION = "com.android.ITelecomService"
    Intent intent = new Intent(SERVICE_ACTION);

    // SERVICE_COMPONENT = new ComponentName(
    //         "com.android.server.telecom",
    //         "com.android.server.telecom.components.TelecomService");
    intent.setComponent(SERVICE_COMPONENT);

    // Bind to Telecom and register the service
    if (mContext.bindServiceAsUser(intent, serviceConnection, flags, UserHandle.SYSTEM)) {
        ...
    }
}
```

### 将"telecom"添加到系统服务
```
com.android.server.telecom.TelecomLoaderService.TelecomServiceConnection.onServiceConnected(){
    // Normally, we would listen for death here, but since telecom runs in the same process
    // as this loader (process="system") thats redundant here.

    // TELECOM_SERVICE = "telecom";
    ServiceManager.addService(Context.TELECOM_SERVICE, service);
}
```



