

(17:01:42,31.2110449507,121.5228004422)

```
android.app.SystemServiceRegistry.SYSTEM_SERVICE_FETCHERS
    private static final HashMap<String, ServiceFetcher<?>> SYSTEM_SERVICE_FETCHERS =
            new HashMap<String, ServiceFetcher<?>>();
```
`android.app.SystemServiceRegistry.registerService()`和`android.app.ContextImpl.getSystemService()`都将
到`SYSTEM_SERVICE_FETCHERS`中存取对应service的Manager。

获取到的Manager是对应service的句柄，封装了IPC到system_server进程的API调用，比如`TelephonyManager`包装了`ITelephony.aidl`的接口。




