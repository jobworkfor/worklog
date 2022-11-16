# UsbService README

## 简介

Framework中管理USB功能的类是`com/android/server/usb/UsbService.java`，该类提供了切换usb模式，授权等方法。一般来说，外部app都是通过IPC到该类来实现USB的相关功能。

## 功能流程

### USB事件监听

Kernal 与 Framework层交互 UEventObserver；插入与拔出USB设备，事件监听以及上报.UEventObserver

#### 流程概要

| 序号  | 文件名                                           | 方法名                          | 方法体                                     | 说明                                                         |
| ----- | ------------------------------------------------ | ------------------------------- | ------------------------------------------ | ------------------------------------------------------------ |
|       | [system_server]                                  |                                 |                                            |                                                              |
| 1     | com/android/server/usb/UsbDeviceManager.java:362 | UsbDeviceManager()              | mUEventObserver = new UsbUEventObserver(); | 创建UsbUEventObserver对象，并启动监听                        |
| 1.1   | android/os/UEventObserver.java:99                | getThread()                     | sThread = new UEventThread();              | 创建UEventThread对象，并start该thread                        |
| 2.1   | android/os/UEventObserver.java:189               | run()                           | String message = nativeWaitForNextEvent(); | 获取usb事件                                                  |
| 2.2   | android/os/UEventObserver.java:194               | run()                           | sendEvent(message);                        | 分发usb事件信息                                              |
| 2.3   | android/os/UEventObserver.java:217               | run()                           | observer.onUEvent(event);                  | 通知com.android.server.usb.UsbDeviceManager.UsbUEventObserver对象usb事件 |
| 2.3.1 | com/android/server/usb/UsbDeviceManager.java:599 | updateState(String state)       | sendMessageDelayed(MSG_UPDATE_STATE);      |                                                              |
| 3     | com/android/server/usb/UsbDeviceManager.java:817 | handleMessage(MSG_UPDATE_STATE) | updateUsbNotification(false);              | 显示notification                                             |

#### 具体说明

3

````java
class UsbDeviceManager > class UsbHandler > public void handleMessage(Message msg) {
            switch (msg.what) {
                case MSG_UPDATE_STATE:
                    updateUsbNotification(false);
````

2.3.1

````java
        public void updateState(String state) {
            removeMessages(MSG_UPDATE_STATE);
            if (connected == 1) removeMessages(MSG_FUNCTION_SWITCH_TIMEOUT);
            Message msg = Message.obtain(this, MSG_UPDATE_STATE);
            msg.arg1 = connected;
            msg.arg2 = configured;
            // debounce disconnects to avoid problems bringing up USB tethering
            // MIUI MOD : START
            // sendMessageDelayed(msg, (connected == 0) ? UPDATE_DELAY : 0);
->          sendMessageDelayed(msg, (connected == 0 && mSwitchFunction) ? UPDATE_DELAY : 0);
            // END
        }
````

2.3

````java
        private void sendEvent(String message) {
            if (!mTempObserversToSignal.isEmpty()) {
                final UEvent event = new UEvent(message);
                final int N = mTempObserversToSignal.size();
                for (int i = 0; i < N; i++) {
                    final UEventObserver observer = mTempObserversToSignal.get(i);
->                  observer.onUEvent(event);
                }
                mTempObserversToSignal.clear();
            }
        }

218    /*
219     * Listens for uevent messages from the kernel to monitor the USB state
220     */
221    private final class UsbUEventObserver extends UEventObserver {
222        @Override
223        public void onUEvent(UEventObserver.UEvent event) {
224            if (DEBUG) Slog.v(TAG, "USB UEVENT: " + event.toString());
225
226            String state = event.get("USB_STATE");
227            String accessory = event.get("ACCESSORY");
228            if (state != null) {
229->              mHandler.updateState(state);
230            } else if ("START".equals(accessory)) {
231                if (DEBUG) Slog.d(TAG, "got accessory start");
232                startAccessoryMode();
233            }
234        }
235    }
````

2.1 & 2.2

````java
        @Override
        public void run() {
            nativeSetup();

            while (true) {
->              String message = nativeWaitForNextEvent();
                if (message != null) {
                    if (DEBUG) {
                        Log.d(TAG, message);
                    }
->                  sendEvent(message);
                }
            }
        }
````

1.1

````java
    public final void startObserving(String match) {
        if (match == null || match.isEmpty()) {
            throw new IllegalArgumentException("match substring must be non-empty");
        }

->      final UEventThread t = getThread();
        t.addObserver(match, this);
    }

    private static UEventThread getThread() {
        synchronized (UEventObserver.class) {
            if (sThread == null) {
->              sThread = new UEventThread();
                sThread.start();
            }
            return sThread;
        }
    }
````

1[system_server]

````java
    public UsbDeviceManager(Context context, UsbAlsaManager alsaManager,
            UsbSettingsManager settingsManager) {
        // Watch for USB configuration changes
->      mUEventObserver = new UsbUEventObserver();
        mUEventObserver.startObserving(USB_STATE_MATCH);
        mUEventObserver.startObserving(USB_STATE_MATCH_SEC);
        mUEventObserver.startObserving(ACCESSORY_START_MATCH);
````

### 选择MTP选项

#### 流程概要

| 序号  | 文件名                                                       | 方法名                   | 方法体                                                      | 说明                                                      |
| ----- | ------------------------------------------------------------ | ------------------------ | ----------------------------------------------------------- | --------------------------------------------------------- |
|       | [com.android.settings]                                       |                          |                                                             |                                                           |
| 1     | android/hardware/usb/UsbManager.java                         | setCurrentFunctions()    | mService.setCurrentFunctions(functions);                    |                                                           |
|       | [system_server]                                              |                          |                                                             |                                                           |
| 2     | frameworks/base/core/java/android/hardware/usb/UsbManager.java:702 | setCurrentFunctions()    | mDeviceManager.setCurrentFunctions(functions);              |                                                           |
| 2.1   | com/android/server/usb/UsbDeviceManager.java:2075            | setCurrentFunctions()    | mHandler.sendMessage(MSG_SET_CURRENT_FUNCTIONS, functions); |                                                           |
|       | (MSG_SET_CURRENT_FUNCTIONS)                                  |                          |                                                             |                                                           |
| 3     | com/android/server/usb/UsbDeviceManager.java:921             | handleMessage()          | setEnabledFunctions(functions, false);                      |                                                           |
| 3.1   | com/android/server/usb/UsbDeviceManager.java:1521            | setEnabledFunctions()    | if (trySetEnabledFunctions(usbFunctions, forceRestart)) {   |                                                           |
| 3.1.1 | com/android/server/usb/UsbDeviceManager.java:1627            | trySetEnabledFunctions() | setUsbConfig(oemFunctions);                                 | 设置新USB配置之前都会先断开当前的链接，然后再设置新的配置 |

3.1.1

````java
class UsbDeviceManager > class UsbHandlerLegacy > private boolean trySetEnabledFunctions(long usbFunctions, boolean forceRestart) {
            String functions = null;
            if (usbFunctions != UsbManager.FUNCTION_NONE) {
                functions = UsbManager.usbFunctionsToString(usbFunctions);// functions: "mtp"
            }
            functions = applyAdbFunction(functions);
            String oemFunctions = applyOemOverrideFunction(functions);// functions: "mtp,adb"

            if ((!functions.equals(oemFunctions)
                    && !mCurrentOemFunctions.equals(oemFunctions)) // mCurrentOemFunctions: "diag,diag_mdm,qdss,qdss_mdm,serial_cdev,dpl,rmnet,adb"
                    || !mCurrentFunctionsStr.equals(functions)
                    || !mCurrentFunctionsApplied
                    || forceRestart) {
                Slog.i(TAG, "Setting USB config to " + functions);

                /**
                 * Kick the USB stack to close existing connections.
                 */
->              setUsbConfig(UsbManager.USB_FUNCTION_NONE);// UsbManager.USB_FUNCTION_NONE: "none"

                if (!waitForState(UsbManager.USB_FUNCTION_NONE)) { // sys.usb.state == "none"  wait for 50x60 ms
                    Slog.e(TAG, "Failed to kick USB config");
                    return false;
                }

                /**
                 * Set the new USB configuration.
                 */
->              setUsbConfig(oemFunctions);// oemFunctions: "mtp,adb"

                if (mBootCompleted
                        && (containsFunction(functions, UsbManager.USB_FUNCTION_MTP)
                        || containsFunction(functions, UsbManager.USB_FUNCTION_PTP))) {
                    /**
                     * Start up dependent services.
                     */
                    updateUsbStateBroadcastIfNeeded(getAppliedFunctions(mCurrentFunctions));
                }

                if (!waitForState(oemFunctions)) { // sys.usb.state == "mtp,adb"
                    Slog.e(TAG, "Failed to switch USB config to " + functions);
                    return false;
                }

                mCurrentFunctionsApplied = true;
            }
            return true;
````

3.1

````java
class UsbDeviceManager > class UsbHandlerLegacy > protected void setEnabledFunctions(long usbFunctions, boolean forceRestart) {
            /**
             * Try to set the enabled functions.
             */
            final long oldFunctions = mCurrentFunctions;
            final boolean oldFunctionsApplied = mCurrentFunctionsApplied;
->          if (trySetEnabledFunctions(usbFunctions, forceRestart)) { // usbFunctions: 4  forceRestart: true
                return;
            }

            /**
             * Didn't work.  Try to revert changes.
             * We always reapply the policy in case certain constraints changed such as
             * user restrictions independently of any other new functions we were
             * trying to activate.
             */
            if (oldFunctionsApplied && oldFunctions != usbFunctions) {
                Slog.e(TAG, "Failsafe 1: Restoring previous USB functions.");
                if (trySetEnabledFunctions(oldFunctions, false)) {
                    return;
                }
            }

            /**
             * Still didn't work.  Try to restore the default functions.
             */
            Slog.e(TAG, "Failsafe 2: Restoring default USB functions.");
            if (trySetEnabledFunctions(UsbManager.FUNCTION_NONE, false)) {
                return;
            }

            /**
             * Now we're desperate.  Ignore the default functions.
             * Try to get ADB working if enabled.
             */
            Slog.e(TAG, "Failsafe 3: Restoring empty function list (with ADB if enabled).");
            if (trySetEnabledFunctions(UsbManager.FUNCTION_NONE, false)) {
                return;
            }

            /**
             * Ouch.
             */
            Slog.e(TAG, "Unable to set any USB functions!");
````

3 MSG_SET_CURRENT_FUNCTIONS

````java
class UsbDeviceManager > class UsbHandler > public void handleMessage(Message msg) {
                case MSG_SET_CURRENT_FUNCTIONS:
                    long functions = (Long) msg.obj;
                    setEnabledFunctions(functions, false);
````

2.1sendMessage(MSG_SET_CURRENT_FUNCTIONS)

```java
    public void setCurrentFunctions(long functions) {
        } else if (functions == UsbManager.FUNCTION_MTP) {
            MetricsLogger.action(mContext, MetricsEvent.ACTION_USB_CONFIG_MTP);
        ...
        mHandler.sendMessage(MSG_SET_CURRENT_FUNCTIONS, functions);
    }
```

2[system_server]

````java
    @Override
    public void setCurrentFunctions(long functions) {
        mContext.enforceCallingOrSelfPermission(android.Manifest.permission.MANAGE_USB, null);
        Preconditions.checkArgument(UsbManager.areSettableFunctions(functions)); // 如果非Settable Functions，将抛出异常
        Preconditions.checkState(mDeviceManager != null);
->      mDeviceManager.setCurrentFunctions(functions);
    }
````

1[com.android.settings]

````java
setCurrentFunctions:718, UsbManager (android.hardware.usb)
class UsbManager > public void setCurrentFunctions(long functions) {
        try {
            if (...) {
                mService.setCurrentFunctions(functions);

setCurrentFunctions:87, UsbBackend (com.android.settings.connecteddevice.usb)
onClick:275, UsbModeChooserActivity$2 (com.android.settings.connecteddevice.usb)
onItemClick:312, AlertControllerWrapper$AlertParams$3 (com.miui.internal.variable)
performItemClick:330, AdapterView (android.widget)
performItemClick:1224, AbsListView (android.widget)
run:3235, AbsListView$PerformClick (android.widget)
run:4191, AbsListView$3 (android.widget)
handleCallback:883, Handler (android.os)
dispatchMessage:100, Handler (android.os)
loop:227, Looper (android.os)
main:7544, ActivityThread (android.app)
invoke:-1, Method (java.lang.reflect)
run:548, RuntimeInit$MethodAndArgsCaller (com.android.internal.os)
main:960, ZygoteInit (com.android.internal.os)
````

### 点击通知栏“正在通过USB充电”

1[system_server]

````java

// com/android/systemui/statusbar/phone/StatusBar.java
class StatusBar > class NotificationClicker > onClick() > new OnDismissAction() > onDismiss() > new Runnable() > run() {
                                    try {
                                        intent.send(null, 0, null, null, null, null,
                                                options != null ? options.toBundle() : getActivityOptions());
                                        Logger.fullI(TAG, "click notification, sending intent, key=" + sbn.getKey());
                                        
[system_server]
interface IActivityManager > class Stub > onTransact() {
          int _result = this.sendIntentSender(_arg0, _arg1, _arg2, _arg3, _arg4, _arg5, _arg6, _arg7);

````

2[com.android.settings]

````java
// com/android/settings/connecteddevice/usb/UsbModeChooserActivity.java
class UsbModeChooserActivity > protected void onCreate(@Nullable Bundle savedInstanceState) {
        initDialog();
````

### USB Service的启动

1

````java
class SystemServer > private void startOtherServices() {
            if (mPackageManager.hasSystemFeature(PackageManager.FEATURE_USB_HOST)
                    || mPackageManager.hasSystemFeature(
                    PackageManager.FEATURE_USB_ACCESSORY)
                    || isEmulator) {
                // Manage USB host and device support
                traceBeginAndSlog("StartUsbService");
                mSystemServiceManager.startService(USB_SERVICE_CLASS);
                traceEnd();
            }
````

2

````java
class UsbService > class Lifecycle
        @Override
        public void onStart() {
            mUsbService = new UsbService(getContext());
            publishBinderService(Context.USB_SERVICE, mUsbService); // Context.USB_SERVICE: "usb"
        }

        @Override
        public void onBootPhase(int phase) {
            if (phase == SystemService.PHASE_ACTIVITY_MANAGER_READY) {
                mUsbService.systemReady();
            } else if (phase == SystemService.PHASE_BOOT_COMPLETED) {
                mUsbService.bootCompleted();
            }
        }
````

### 获取service

````java
 UsbManager usbManager = (UsbManager) getSystemService(Context.USB_SERVICE);
 HashMap<Strinng,UsbDevice> deviceHashMap = usbManager.getDeviceList() ;
````

