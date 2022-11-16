# DUMP信息统计算法汇总

## 概要

Android系统提供了查看功耗使用情况信息的功能，其数据来源有两个：

*   电池使用情况打点信息
*   电源配置文件

### 电池使用情况统计信息

### 电源配置文件中的值

设备制造商必须提供组件的电源配置文件（ [platform/frameworks/base/core/res/res/xml/power_profile.xml](https://android.googlesource.com/platform/frameworks/base/+/master/core/res/res/xml/power_profile.xml)），该配置文件定义了组件的电流消耗值以及该组件在一段时间内大概消耗的电量。一个[典型](https://android.googlesource.com/platform/frameworks/base/+/master/core/res/res/xml/power_profile.xml)的配置内容如下：

````xml
<?xml version="1.0" encoding="utf-8"?>
...
<device name="Android">
  ...
  <item name="ambient.on">0.1</item>  <!-- ~100mA -->
  <item name="screen.on">0.1</item>  <!-- ~100mA -->
  ...
  <item name="gps.voltage">0</item>
</device>
````

## 相关代码



## 软件排行榜



## 参考

*   https://www.intmath.com/help/send-math-email-syntax.php
*   https://www.cnblogs.com/hellokitty2/p/12253075.html















































[back to content](../../index.md)