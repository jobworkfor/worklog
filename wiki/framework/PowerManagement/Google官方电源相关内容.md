>   官方网址：https://source.android.com/devices/tech/power

# Android 电源配置文件

电池使用信息根据系统各模块的用电统计和 `power_profile.xml` 中响应模块耗电量配置联合计算出来的。

## 电池使用情况统计信息

系统的 `BatteryStats 服务` 在运行期间会不断收集各模块的用电信息，WLAN 芯片组、手机无线装置、蓝牙、GPS、显示屏和 CPU 的状态发生改变（开/关、空闲/全功耗、低/高亮度等）时收集各模块的信息，采用两种方法：

*   推送：各模块主动上报数据到 `BatteryStats 服务` 
*   拉取： `BatteryStats 服务`  主动从各模块中获取数据

当多个应用消耗公共资源时，系统会自动分摊电量消耗（不一定是均摊）。

 `BatteryStats 服务`  中的信息每 30分钟 一次备份到磁盘中。

## 电源配置文件中的值

配置文件：[platform/frameworks/base/core/res/res/xml/power_profile.xml](https://android.googlesource.com/platform/frameworks/base/+/master/core/res/res/xml/power_profile.xml)

`BatteryStats 服务`  会计算每个应用耗电量，并为之排名。计算方法为： CPU 时间乘以在特定速度运行 CPU 所需的毫安量。



# 电源管理

Android 提供以下增强电池续航时间的功能：

-   [应用限制](https://source.android.com/devices/tech/power/app_mgmt#app-restrictions)。平台可以提示哪些应用会对电池续航时间产生不利影响，以便用户可以对这些应用施加限制，防止它们消耗资源。默认情况下，应用不会在后台受到限制。
-   [应用待机模式](https://source.android.com/devices/tech/power/app_mgmt#app-standby)。平台会使未使用的应用进入应用待机模式，从而暂时限制此类应用访问网络，并延迟其同步和作业。
-   [低电耗模式](https://source.android.com/devices/tech/power/platform_mgmt#doze)。用户长时间没有使用设备（处于静止状态且屏幕关闭）时，平台会使设备进入深度休眠状态（DOZE状态）。当设备屏幕关闭但仍处于移动状态时，Android 7.0 及更高版本还会启用低电耗模式，以触发一系列轻度优化。
-   [豁免](https://source.android.com/devices/tech/power/mgmt#exempt-apps)。默认情况下，预加载的系统应用和云消息传递服务通常能够获得豁免，不会进入应用待机模式和低电耗模式。应用开发者可以使用 Intent 将这些设置应用于其应用。用户可以在“设置”菜单中设置被除外的应用，使其无需进入应用待机和低电耗节电模式。

 

## 设置被除外的应用

您可以设置被除外的应用，使其不受低电耗模式和应用待机模式的影响。除外功能可能适用于下列使用情形：

-   使用除 [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging/) (FCM) 以外的云消息传递平台的设备制造商。
-   使用非 FCM 云消息传递平台的运营商
-   使用非 FCM 云消息传递平台的第三方应用

默认情况下，豁免的应用会在“设置”>“应用和通知”>“特殊应用权限”>“电池优化”中列出。该列表用于豁免应用，使其不会进入低电耗模式和应用待机模式。为使用户清楚知道哪些应用已被除外，“设置”菜单**必须**显示所有被除外的应用。

用户可以依次转到“设置”>“应用和通知”>“APP-NAME”>“电池”>“电池优化”，然后选择要关闭（或重新开启）优化的应用，以此来手动设置被除外的应用。不过，用户无法取消系统映像中默认除外的任何应用或服务的除外状态。