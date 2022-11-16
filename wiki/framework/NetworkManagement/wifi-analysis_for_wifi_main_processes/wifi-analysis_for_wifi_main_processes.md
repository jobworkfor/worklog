# WiFi 模块常用流程分析


调试WiFi Calling时总是需要和WiFi打交道，时常出现当WiFi打开时，当前网络连接却是Cell数据的情况，本文介绍Android系统管理WiFi网络的流程分析。

# 相关代码

如果要分析模块功能，首先需要知道分析的对象有哪些。查阅资料，并结合Android 6.0的源码，WiFi功能涉及的的代码大致在如下几个地方。
* APP部分
 * WIFI Settings应用程序位于
   * packages/apps/Settings/src/com/Android/settings/wifi/
 * Framework Java部分：
   * frameworks/base/services/java/com/android/server/
   * frameworks/base/wifi/java/android/net/wifi/
   * frameworks/opt/net/wifi/service/java/com/android/server/wifi

* JNI部分
 * frameworks/opt/net/wifi/service/jni/com_android_server_wifi_WifiNative.cpp

* 库文件
 * wifi管理库
   * hardware/libhardware_legary/wifi/
 * wifi用户空间的程序(wpa_supplicant)和库(libwpaclient.so):
   * external/wpa_supplicant_8/wpa_supplicant

上面列出的代码只是主要流程代码所在，现在对该模块认识还较为肤浅，本文仅涉及上述列出代码，以此作为WiFi模块入门的基石。

# 启动流程











