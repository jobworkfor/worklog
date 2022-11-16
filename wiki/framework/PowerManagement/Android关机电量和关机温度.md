# 修改Android关机电量和关机温度

## 前言

Android系统默认是电量为0关机的，如果要修改成还有5%电量就关机怎么办？（吐槽一下：其实修改成5%关机也没什么意义，因为即便还有电量，开机后系统也会再次被关闭），不过确实有这样的需求，废话少说，这里简单分析怎么改：

## 分析

电池这一块自然少不了Android BatteryService，在adb shell中敲入：

````bash
dumpsys battery
````

输出如下：

````bash
Current Battery Service state:
 AC powered: false
 USB powered: true
 status: 2
 health: 2
 present: true
 level: 54
 scale: 100
 voltage:3856
 temperature: 300
 technology: LiFe
````


其中的level就是电量等级，temperature是摄氏温度，不过少了小数点，是30度。BatteyService中决定关机的就两个，一个level，一个temperature

mBatteryLevel，就是系统的电压等级，最大值是SCALE，也就是100，修改后 低电关机相关的代码如下：

````java
// @./frameworks/base/services/java/com/android/server/BatteryService.java
private final void shutdownIfNoPower() {
        // shut down gracefully if our battery is critically low and we are not powered.
        // wait until the system has booted before attempting to display the shutdown dialog.
        if (mBatteryLevel < 5 && !isPowered() && ActivityManagerNative.isSystemReady()) {
            Intent intent = new Intent(Intent.ACTION_REQUEST_SHUTDOWN);
            intent.putExtra(Intent.EXTRA_KEY_CONFIRM, false);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            mContext.startActivity(intent);
        }
    }

    private final void shutdownIfOverTemp() {
        // shut down gracefully if temperature is too high (> 68.0C)
        // wait until the system has booted before attempting to display the shutdown dialog.
        if (mBatteryTemperature > 680 && ActivityManagerNative.isSystemReady()) {
            Intent intent = new Intent(Intent.ACTION_REQUEST_SHUTDOWN);
            intent.putExtra(Intent.EXTRA_KEY_CONFIRM, false);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            mContext.startActivity(intent);
        }
    }
````

关机的原理是通过发送关机对话框的Intent来实现的，而不是调用ShutdownThread或是4.1的PowerManager
来实现的，这里确实体现了Android的灵活之处。
  关于BatteryService参数的更新，目前知道是通过uevent机制和sysfs进行交互更新的，这一块还需要进一步跟进一下。