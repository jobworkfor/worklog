# [KLEN-6430](http://jira.blackshark.com/browse/KLEN-6430) 【MIUI】K项目测试：电源键亮屏慢，时间点6:40（FR:无规律重现）

相关问题：

1. [KLEN-7123](http://jira.blackshark.com/browse/KLEN-7123)
2. [KLEN-7079](http://jira.blackshark.com/browse/KLEN-7079) 
3. [KLEN-5864](http://jira.blackshark.com/browse/KLEN-5864) 
4. [MOBS-9056](http://jira.blackshark.com/browse/MOBS-9056) 



http://jenkins.blackshark.com/view/OndemandBuild/job/ODVB/2482/



```cpp
    // http://androidxref.blackshark.com:8088/sm8250/xref/frameworks/base/services/core/java/com/android/server/power/PowerManagerService.java#1703
    finishWakefulnessChangeIfNeededLocked:1701, PowerManagerService (com.android.server.power)["02-06 20:55:04.896251"]
    1688    private void finishWakefulnessChangeIfNeededLocked() {
    1689        if (mWakefulnessChanging && mDisplayReady) {
    1690            if (mWakefulness == WAKEFULNESS_DOZING
    1691                    && (mWakeLockSummary & WAKE_LOCK_DOZE) == 0) {
    1692                return; // wait until dream has enabled dozing
    1693            }
    1694            if (mWakefulness == WAKEFULNESS_DOZING || mWakefulness == WAKEFULNESS_ASLEEP) {
    1695                logSleepTimeoutRecapturedLocked();
    1696            }
    1697            // MIUI MOD: START
    1699            if (mWakefulness == WAKEFULNESS_AWAKE && mPreWakefulness != WAKEFULNESS_HANGUP) {
    1700                Trace.asyncTraceEnd(Trace.TRACE_TAG_POWER, TRACE_SCREEN_ON, 0);
        				// 此处的latencyMs依赖mLastWakeTime的值
    1701>               final int latencyMs = (int) (SystemClock.uptimeMillis() - mLastWakeTime);
    1702                if (latencyMs >= SCREEN_ON_LATENCY_WARNING_MS) {
    1703                    Slog.w(TAG, "Screen on took " + latencyMs + " ms");
    1704                }
    1705            }
    1706            // END
    1707            mWakefulnessChanging = false;
    1708            // MIUI ADD: START
    1709            if (!mScreenProjectionEnabled
    1710                    || mWakefulness != WAKEFULNESS_HANGUP) {
    1711                mNotifier.onWakefulnessInHangUp(false);
    1712            }
    1713            // END
    1714            mNotifier.onWakefulnessChangeFinished();
    1715        }
    1716    }
updatePowerStateLocked:1770, PowerManagerService (com.android.server.power)
onStateChanged:2699, PowerManagerService$1 (com.android.server.power)
run:1813, DisplayPowerController$4 (com.android.server.display)
handleCallback:883, Handler (android.os)
dispatchMessage:100, Handler (android.os)
loop:227, Looper (android.os)
run:67, HandlerThread (android.os)
run:45, ServiceThread (com.android.server)

"post: mOnStateChangedRunnable"
sendOnStateChangedWithWakelock:1690, DisplayPowerController (com.android.server.display)
updatePowerState:1207, DisplayPowerController (com.android.server.display)
access$600:90, DisplayPowerController (com.android.server.display)
handleMessage:2017, DisplayPowerController$DisplayControllerHandler (com.android.server.display)
dispatchMessage:107, Handler (android.os)
loop:227, Looper (android.os)
run:67, HandlerThread (android.os)
run:45, ServiceThread (com.android.server)

        "send msg: MSG_UPDATE_POWER_STATE"
        sendUpdatePowerStateLocked:694, DisplayPowerController (com.android.server.display)
        requestPowerState:671, DisplayPowerController (com.android.server.display)
        requestPowerState:2441, DisplayManagerService$LocalService (com.android.server.display)
        updateDisplayPowerStateLocked:2595, PowerManagerService (com.android.server.power)
    updatePowerStateLocked:1764, PowerManagerService (com.android.server.power)
    wakeUpNoUpdateLocked:1453, PowerManagerService (com.android.server.power)["02-06 20:55:04.122027"]
    1495    private boolean wakeUpNoUpdateLocked(long eventTime, @WakeReason int reason, String details,
    1496            int reasonUid, String opPackageName, int opUid) {
    1497        if (DEBUG_SPEW) {
    1498            Slog.d(TAG, "wakeUpNoUpdateLocked: eventTime=" + eventTime + ", uid=" + reasonUid);
    1499        }
    1500
    1501        if (eventTime < mLastSleepTime || mWakefulness == WAKEFULNESS_AWAKE
    1502                || !mBootCompleted || !mSystemReady || mForceSuspendActive) {
    1503            return false;
    1504        }
    1505
    1506        Trace.asyncTraceBegin(Trace.TRACE_TAG_POWER, TRACE_SCREEN_ON, 0);
    1507
    1508        Trace.traceBegin(Trace.TRACE_TAG_POWER, "wakeUp");
    1509        // MIUI ADD: START
    1510        if (mPolicy instanceof com.android.server.policy.PhoneWindowManager) {
    1511            ((com.android.server.policy.PhoneWindowManager) mPolicy).wakingUp(details);
    1512        }
    1513        // END
    1514        try {
    1515            Slog.i(TAG, "Waking up from "
    1516                    + PowerManagerInternal.wakefulnessToString(mWakefulness)
    1517                    + " (uid=" + reasonUid
    1518                    + ", reason=" + PowerManager.wakeReasonToString(reason)
    1519                    + ", details=" + details
    1520                    + ")...");
    1521
                    // 此处依赖eventTime
    1522>           mLastWakeTime = eventTime;
    1523            mLastWakeReason = reason;
    1524            setWakefulnessLocked(WAKEFULNESS_AWAKE, reason, eventTime);
    1525
    1526            mNotifier.onWakeUp(reason, details, reasonUid, opPackageName, opUid);
    1527            userActivityNoUpdateLocked(
    1528                    eventTime, PowerManager.USER_ACTIVITY_EVENT_OTHER, 0, reasonUid);
    1529        } finally {
    1530            Trace.traceEnd(Trace.TRACE_TAG_POWER);
    1531        }
    1532        return true;
    1533    }
wakeUpInternal:1490, PowerManagerService (com.android.server.power)
access$4700:120, PowerManagerService (com.android.server.power)
wakeUp:4554, PowerManagerService$BinderService (com.android.server.power)
wakeUp:1210, PowerManager (android.os)
wakeUp:4741, PhoneWindowManager (com.android.server.policy)
wakeUpFromPowerKey:4725, PhoneWindowManager (com.android.server.policy)
interceptPowerKeyDown:1056, PhoneWindowManager (com.android.server.policy)
interceptKeyBeforeQueueing:4093, PhoneWindowManager (com.android.server.policy)
callSuperInterceptKeyBeforeQueueing:261, MiuiPhoneWindowManager (com.android.server.policy)
interceptKeyBeforeQueueingInternal:1174, BaseMiuiPhoneWindowManager (com.android.server.policy)
    protected int interceptKeyBeforeQueueingInternal(KeyEvent event, int policyFlags, boolean isScreenOn) {
        if (!mSystemBooted) {
            // If we have not yet booted, don't let key events do anything.
            return 0;
        }

        int keyCode = event.getKeyCode();
        final boolean down = event.getAction() == KeyEvent.ACTION_DOWN;
        final int repeatCount = event.getRepeatCount();
        final boolean isInjected = (policyFlags & WindowManagerPolicy.FLAG_INJECTED) != 0;
        final boolean keyguardActive = mMiuiKeyguardDelegate != null && (isScreenOn
                ? mMiuiKeyguardDelegate.isShowingAndNotHidden()
                : mMiuiKeyguardDelegate.isShowing());

        Slog.w("BaseMiuiPhoneWindowManager", "keyCode:" + keyCode + " down:" + down
                 + " eventTime:" + event.getEventTime() + " downTime:" + event.getDownTime()
                 + " policyFlags:" + Integer.toHexString(policyFlags)
                 + " flags:" + Integer.toHexString(event.getFlags())
                 + " deviceId:" + event.getDeviceId() +" isScreenOn:" + isScreenOn
                 + " keyguardActive:" + keyguardActive +" repeatCount:" + repeatCount);
	}
interceptKeyBeforeQueueing:247, MiuiPhoneWindowManager (com.android.server.policy)
interceptKeyBeforeQueueing:169, InputManagerCallback (com.android.server.wm)
interceptKeyBeforeQueueing:2265, InputManagerService (com.android.server.input)
[system_server]
```







