README
======

sensorservice的启动
----------------------------------------------------------------------------------------------------

```cpp
direction: topdown

// android/frameworks/base/services/core/jni/com_android_server_SystemServer.cpp
36static void android_server_SystemServer_startSensorService(JNIEnv* /* env */, jobject /* clazz */) {
37    char propBuf[PROPERTY_VALUE_MAX];
38    property_get("system_init.startsensorservice", propBuf, "1");
39    if (strcmp(propBuf, "1") == 0) {
40        SensorService::publish(false /* allowIsolated */,
41                               IServiceManager::DUMP_FLAG_PRIORITY_CRITICAL);
42    }
43
44}
    
// /frameworks/native/libs/binder/include/binder/BinderService.h
33template<typename SERVICE>
34class BinderService
35{
36public:
37    static status_t publish(bool allowIsolated = false,
38                            int dumpFlags = IServiceManager::DUMP_FLAG_PRIORITY_DEFAULT) {
39        sp<IServiceManager> sm(defaultServiceManager());
40        return sm->addService(String16(SERVICE::getServiceName()), new SERVICE(), allowIsolated,
41                              dumpFlags);
42    }

// xref: /frameworks/native/services/sensorservice/SensorService.h
66class SensorService :
67        public BinderService<SensorService>,
68        public BnSensorServer,
69        protected Thread
70{
...
212    static char const* getServiceName() ANDROID_API { return "sensorservice"; }

```









reference
----------------------------------------------------------------------------------------------------
* https://blog.csdn.net/tamell5555/article/details/52470742
* https://blog.csdn.net/zhangyawen1i/article/details/78536630
* https://blog.csdn.net/LoongEmbedded/article/details/51442241
* https://blog.csdn.net/qq_15807167/article/details/51989374
* http://www.zhimengzhe.com/Androidkaifa/34634.html
* http://www.it610.com/article/5087964.htm
* https://blog.csdn.net/daniel80110_1020/article/details/56854187

























