# Alarm 对功耗的影响

频繁的 `alarm` 唤醒，长时间的 `alarm timer` 持锁不放将导致功耗额外增加。了解alarm相关内容，有利于做功耗优化。

## Overview

對於系統功耗優化，時常可以看到alarm喚醒頻繁，或者alarm timer持鎖時間過長的問題，對於這樣的情況Android的各個版本也都有持續性的優化，對於alarm來說，簡而言之都是加強管控，儘可能減少喚醒，集中批量處理。

## AlarmManager

AlarmManager提供接口供應用根據自己的需求，來設置alarm以及對應的處理方法

frameworks/base/core/java/android/app/AlarmManager.java

### alarm目前有幾種類型

-   RTC_WAKEUP

```
    /**
     * Alarm time in {@link System#currentTimeMillis System.currentTimeMillis()}
     * (wall clock time in UTC), which will wake up the device when
     * it goes off.
     */
    public static final int RTC_WAKEUP = 0;
```

-   RTC

```
    /**
     * Alarm time in {@link System#currentTimeMillis System.currentTimeMillis()}
     * (wall clock time in UTC).  This alarm does not wake the
     * device up; if it goes off while the device is asleep, it will not be
     * delivered until the next time the device wakes up.
     */
    public static final int RTC = 1;
```

-   ELAPSED_REALTIME_WAKEUP

```
    /**
     * Alarm time in {@link android.os.SystemClock#elapsedRealtime
     * SystemClock.elapsedRealtime()} (time since boot, including sleep),
     * which will wake up the device when it goes off.
     */
    public static final int ELAPSED_REALTIME_WAKEUP = 2;
```

-   ELAPSED_REALTIME

```
    /**
     * Alarm time in {@link android.os.SystemClock#elapsedRealtime
     * SystemClock.elapsedRealtime()} (time since boot, including sleep).
     * This alarm does not wake the device up; if it goes off while the device
     * is asleep, it will not be delivered until the next time the device
     * wakes up.
     */
    public static final int ELAPSED_REALTIME = 3;
```

-   RTC_POWEROFF_WAKEUP

```
    /**
     * Alarm time in {@link System#currentTimeMillis System.currentTimeMillis()}
     * (wall clock time in UTC), which will wake up the device when
     * it goes off. And it will power on the devices when it shuts down.
     * Set as 5 to make it be compatible with android_alarm_type.
     * @hide
     */
    public static final int RTC_POWEROFF_WAKEUP = 5;
```

### 其特點用途如下

-   RTC和ELAPSED_REALTIME 的差異在於前者使用絕對時間，後者使用相對時間來設置
-   WAKEUP類型的alarm在超時時如果系統處於待機休眠狀態，則會喚醒系統，非WAKEUP類型的只能等到下一次系統喚醒的時候再被處理
-   RTC_POWEROFF_WAKEUP 基本就是用來給關機鬧鐘，或者定時開機用

## API

-   **set**(int type, long triggerAtMillis, PendingIntent operation)：設置一次性的
-   **setRepeating**(int type, long triggerAtMillis, long intervalMillis, PendingIntent operation)：設置可重複執行的
-   **setInexactRepeating**(int type, long triggerAtMillis, long intervalMillis, PendingIntent operation)：設置可重複執行的，並且沒有精確的時間要求
-   **cancel**(PendingIntent operation)
-   **cancel**(OnAlarmListener listener)

SET的调用流程如下：

````bash
setImpl()
    setImplLocked()
        setImplLocked()
            rescheduleKernelAlarmsLocked()
                setlocked()
                    set()
````





trace alarmtimer

4a057549d6044c2dea47e80f8369a76225ec9d90[m [1;34m<baolin.wang@linaro.org>[m [1;34m>[m alarmtimer: Add tracepoints for alarm timers [32m(Tue Nov 29 06:35:21 2016)[m [m