## 准备工作
### RIL层事件注册过程

#### /mnt/dev/workspace/idol4/frameworks/opt/telephony/src/java/com/android/internal/telephony/PhoneFactory.java
```java
/**
 * FIXME replace this with some other way of making these
 * instances
 */
public static void makeDefaultPhone(Context context) {
    synchronized (sLockProxyPhones) {
        ...
        sPhoneNotifier = new DefaultPhoneNotifier();
        ...
        for (int i = 0; i < numPhones; i++) {
            PhoneBase phone = null;
            int phoneType = TelephonyManager.getPhoneType(networkModes[i]);
            if (phoneType == PhoneConstants.PHONE_TYPE_GSM) {
                phone = TelephonyPluginDelegate.getInstance().makeGSMPhone(context,
                        sCommandsInterfaces[i], sPhoneNotifier, i);
            }
            Rlog.i(LOG_TAG, "Creating Phone with type = " + phoneType + " sub = " + i);

            sProxyPhones[i] = TelephonyPluginDelegate.getInstance().makePhoneProxy(phone);
        }
        ...
    }
}
```

* 构造一个`DefaultPhoneNotifier`对象
* 构造对应Type的`Phone`对象
* 为`Phone`对象创建一个`PhoneProxy`对象

#### /mnt/dev/workspace/idol4/frameworks/opt/telephony/src/java/com/android/internal/telephony/gsm/GSMPhone.java

```java
public
GSMPhone(Context context, CommandsInterface ci,
        PhoneNotifier notifier, boolean unitTestMode, int phoneId) {
    super("GSM", notifier, context, ci, unitTestMode, phoneId);

    mCi.setPhoneType(PhoneConstants.PHONE_TYPE_GSM);
    mCT = new GsmCallTracker(this);

    mSST = TelephonyPluginDelegate.getInstance().makeGsmServiceStateTracker(this);
    mDcTracker = TelephonyPluginDelegate.getInstance().makeDcTracker(this);

    mCi.registerForAvailable(this, EVENT_RADIO_AVAILABLE, null);
    ...

    log("GSMPhone: constructor: sub = " + mPhoneId);
}
```

* 通过`mCi`(由`RIL.java`实现)对象设置Phone类型
* 构造`GsmCallTracker`对象`mCT`。
    * GSMCallTracker实现了电话的拨打（Dial）、接听/拒绝(accept/reject)、挂断（hangup）、保持（hold）、切换以及电话会议等功能，
    * 负责查询Modem当前有多少路通话，维护电话状态等功能。
    * GSMCallTracker中包含了GsmConnection、RegistrantList、 GSMCall和Phone.State等类的对象实例。
    * 在GSMCallTracker构造函数中向RIL类实例注册了RegistrantList，当通话状态及射频Radio状态变化时，就会通知GSMCallTracker。
* 构造`GsmServiceStateTracker`对象`mSST`
* 构造`DcTrackerBase`对象`mDcTracker`
* 向`ril`注册各种监听器

#### frameworks/opt/telephony/src/java/com/android/internal/telephony/PhoneBase.java
```java
protected PhoneBase(String name, PhoneNotifier notifier, Context context, CommandsInterface ci,
        boolean unitTestMode, int phoneId) {
    ...
    mUiccController = UiccController.getInstance();
    mUiccController.registerForIccChanged(this, EVENT_ICC_CHANGED, null);
    ...
}
```

* 这里构造了`UiccController`对象`mUiccController`。
* 注册了`SIM`卡事件监听器


#### frameworks/opt/telephony/src/java/com/android/internal/telephony/gsm/GsmCallTracker.java
```java
GsmCallTracker (GSMPhone phone) {
    this.mPhone = phone;
    mCi = phone.mCi;

    mCi.registerForCallStateChanged(this, EVENT_CALL_STATE_CHANGE, null);

    mCi.registerForOn(this, EVENT_RADIO_AVAILABLE, null);
    mCi.registerForNotAvailable(this, EVENT_RADIO_NOT_AVAILABLE, null);
}
```

* mCi引用RIL对象，在这里注册了电话状态改变事件，视频电话状态改变事件，无线开关事件等。
* 由于RIL实现了CommandsInterface接口，并继承于BaseCommands抽象类，registerForCallStateChanged函数实现在RIL的父类BaseCommands中

BaseCommands中注册监听器的方法

    registerForCallStateChanged
    registerForCallWaitingInfo
    registerForCdmaOtaProvision
    registerForCdmaPrlChanged
    registerForCdmaSubscriptionChanged
    registerForCellInfoList
    registerForDataNetworkStateChanged
    registerForDisplayInfo
    registerForExitEmergencyCallbackMode
    registerForHardwareConfigChanged
    registerForIccRefresh
    registerForIccStatusChanged
    registerForImsNetworkStateChanged
    registerForInCallVoicePrivacyOff
    registerForInCallVoicePrivacyOn
    registerForLceInfo
    registerForLineControlInfo
    registerForNotAvailable
    registerForNumberInfo
    registerForOffOrNotAvailable
    registerForOn
    registerForRadioCapabilityChanged
    registerForRadioStateChanged
    registerForRedirectedNumberInfo
    registerForResendIncallMute
    registerForRilConnected
    registerForRingbackTone
    registerForSignalInfo
    registerForSrvccStateChanged
    registerForSubscriptionStatusChanged
    registerForT53AudioControlInfo
    registerForVoiceNetworkStateChanged
    registerForVoiceRadioTechChanged
    registerFoT53ClirlInfo

这里为RIL注册了一些消息事件，并指定GsmCallTracker来处理这些消息。

##### 消息通知原理

/mnt/dev/workspace/idol4/frameworks/opt/telephony/src/java/com/android/internal/telephony/BaseCommands.java

```java
@Override
public void registerForCallStateChanged(Handler h, int what, Object obj) {
    Registrant r = new Registrant (h, what, obj);

    mCallStateRegistrants.add(r);
}
```

* 该函数通过Handler及对应的事件消息来构造一个Registrant对象，
* 将Registrant对象注册到mCallStateRegistrants对象中，mCallStateRegistrants为RegistrantList类型变量，定义在RIL的父类BaseCommands中
* RegistrantList类首先将某个消息及处理该消息的Handler封装成Registrant对象，并将该对象保存到成员变量registrants动态数组中。

/mnt/dev/workspace/idol4/frameworks/base/core/java/android/os/RegistrantList.java

```java
public synchronized void
add(Registrant r)
{
    removeCleared();
    registrants.add(r);
}

private synchronized void
internalNotifyRegistrants (Object result, Throwable exception)
{
   for (int i = 0, s = registrants.size(); i < s ; i++) {
        Registrant  r = (Registrant) registrants.get(i);
        r.internalNotifyRegistrant(result, exception);
   }
}
```

* 对于电话状态改变事件，注册的Handle对象为GsmCallTracker，因此在电话状态改变事件到来时，GsmCallTracker将处理EVENT_CALL_STATE_CHANGE消息事件。

GsmCallTracker处理的消息如下：
```java
protected static final int EVENT_POLL_CALLS_RESULT             = 1;
protected static final int EVENT_CALL_STATE_CHANGE             = 2;
protected static final int EVENT_REPOLL_AFTER_DELAY            = 3;
protected static final int EVENT_OPERATION_COMPLETE            = 4;
protected static final int EVENT_GET_LAST_CALL_FAIL_CAUSE      = 5;

protected static final int EVENT_SWITCH_RESULT                 = 8;
protected static final int EVENT_RADIO_AVAILABLE               = 9;
protected static final int EVENT_RADIO_NOT_AVAILABLE           = 10;
protected static final int EVENT_CONFERENCE_RESULT             = 11;
protected static final int EVENT_SEPARATE_RESULT               = 12;
protected static final int EVENT_ECT_RESULT                    = 13;
protected static final int EVENT_EXIT_ECM_RESPONSE_CDMA        = 14;
protected static final int EVENT_CALL_WAITING_INFO_CDMA        = 15;
protected static final int EVENT_THREE_WAY_DIAL_L2_RESULT_CDMA = 16;
protected static final int EVENT_THREE_WAY_DIAL_BLANK_FLASH    = 20;
```

GsmCallTracker有三个成员变量：

* GsmCall ringingCall = new GsmCall(this) 前台Call，其中对应的Connection是ACTIVE,DIALING,ALERTING状态的，即激活状态
* GsmCall foregroundCall = new GsmCall(this) 后台Call，其中对应的Connection是HOLDING状态的，即保持状态
* GsmCall backgroundCall = new GsmCall(this) 来电Call，其中对应的Connection是INCOMING,WAITING状态的，即来电状态

### Phone层事件注册过程

在Phone进程启动的时，PhoneApp的onCreate函数首先被调用，PhoneApp会构造各种全局对象，同时也会注册一些事件。

/mnt/dev/workspace/idol4/packages/services/Telephony/src/com/android/phone/PhoneApp.java
```java
@Override
public void onCreate() {
    if (UserHandle.myUserId() == 0) {
        // We are running as the primary user, so should bring up the
        // global phone state.
        mPhoneGlobals = new PhoneGlobals(this);
        mPhoneGlobals.onCreate();
        ...
    }
}
```

/mnt/dev/workspace/idol4/packages/services/Telephony/src/com/android/phone/PhoneGlobals.java
```java
public void onCreate() {
    ...
    mCM = CallManager.getInstance();
    for (Phone phone : PhoneFactory.getPhones()) {
        mCM.registerPhone(phone);
    }
    ...
}
```

* 如果是双卡，`PhoneFactory.getPhones()`会返回两个phone对象。

/mnt/dev/workspace/idol4/frameworks/opt/telephony/src/java/com/android/internal/telephony/CallManager.java
```java
/**
 * Register phone to CallManager
 * @param phone to be registered
 * @return true if register successfully
 */
public boolean registerPhone(Phone phone) {
    ...
    mPhones.add(basePhone);
    ...
    registerForPhoneStates(basePhone);
}

private void registerForPhoneStates(Phone phone) {
    // New registration, create a new handler instance and register the phone.
    handler = new CallManagerHandler();
    mHandlerMap.put(phone, handler);

    // for common events supported by all phones
    // The mRegistrantIdentifier passed here, is to identify in the PhoneBase
    // that the registrants are coming from the CallManager.
    phone.registerForPreciseCallStateChanged(handler, EVENT_PRECISE_CALL_STATE_CHANGED,
            mRegistrantidentifier);
    phone.registerForDisconnect(handler, EVENT_DISCONNECT,
            mRegistrantidentifier);
    phone.registerForNewRingingConnection(handler, EVENT_NEW_RINGING_CONNECTION,
            mRegistrantidentifier);
    phone.registerForUnknownConnection(handler, EVENT_UNKNOWN_CONNECTION,
            mRegistrantidentifier);
    ...
}
```

* 此时的`Phone`类型为`GsmPhone`，其父类为`PhoneBase`。
* `CallManager`将其创建的`CallManagerHandler`对象注册到PhoneBase中，`GsmPhone`的时间便是由`CallManagerHandler`来处理的。

```java
/* Event Constants */
protected static final int EVENT_RADIO_AVAILABLE             = 1;
/** Supplementary Service Notification received. */
protected static final int EVENT_SSN                         = 2;
protected static final int EVENT_SIM_RECORDS_LOADED          = 3;
protected static final int EVENT_MMI_DONE                    = 4;
protected static final int EVENT_RADIO_ON                    = 5;
protected static final int EVENT_GET_BASEBAND_VERSION_DONE   = 6;
protected static final int EVENT_USSD                        = 7;
protected static final int EVENT_RADIO_OFF_OR_NOT_AVAILABLE  = 8;
protected static final int EVENT_GET_IMEI_DONE               = 9;
protected static final int EVENT_GET_IMEISV_DONE             = 10;
protected static final int EVENT_GET_SIM_STATUS_DONE         = 11;
protected static final int EVENT_SET_CALL_FORWARD_DONE       = 12;
protected static final int EVENT_GET_CALL_FORWARD_DONE       = 13;
protected static final int EVENT_CALL_RING                   = 14;
protected static final int EVENT_CALL_RING_CONTINUE          = 15;

// Used to intercept the carrier selection calls so that
// we can save the values.
protected static final int EVENT_SET_NETWORK_MANUAL_COMPLETE    = 16;
protected static final int EVENT_SET_NETWORK_AUTOMATIC_COMPLETE = 17;
protected static final int EVENT_SET_CLIR_COMPLETE              = 18;
protected static final int EVENT_REGISTERED_TO_NETWORK          = 19;
protected static final int EVENT_SET_VM_NUMBER_DONE             = 20;
...
```

CallManager，Phone和RIL的关系为：

    CallManager -注册CallManagerHandler-> Phone -注册自身-> RIL

当RIL有消息上抛时，消息处理流程为：

    RIL -通过Phone自身通知-> Phone -通过CallManagerHandler通知-> CallManager

如：

`EVENT_CALL_RING`消息的注册流程为：


`EVENT_CALL_RING`消息的通知流程为：

### CallManager层事件注册过程

在启动PhoneApp时，会创建一个CallNotifier对象

#### /mnt/dev/workspace/idol4/packages/services/Telephony/src/com/android/phone/PhoneGlobals.java
```java
public void onCreate() {
    ...
    // Create the CallNotifer singleton, which handles
    // asynchronous events from the telephony layer (like
    // launching the incoming-call UI when an incoming call comes
    // in.)
    notifier = CallNotifier.init(this, callLogger, callStateMonitor, bluetoothManager);
    ...
}
```

对于CallNotifier对象，代码中的解释为：
```java
/**
 * Phone app module that listens for phone state changes and various other
 * events from the telephony layer, and triggers any resulting UI behavior
 * (like starting the Incoming Call UI, playing in-call tones,
 * updating notifications, writing call log entries, etc.)
 */
 public class CallNotifier extends Handler { ... }
```

参数中，涉及了三个对象，分别为
##### /mnt/dev/workspace/idol4/packages/services/Telephony/src/com/android/phone/CallLogger.java

```java
/**
 * Helper class for interacting with the call log.
 */
class CallLogger {
    // Logs a call to the call log based on the connection object passed in.
    public void logCall(Connection c, int callLogType) { ... }

    // Came as logCall(Connection,int) but calculates the call type from the connection object.
    public void logCall(Connection c) { ... }

    // Logs a call to the call from the parameters passed in.
    public void logCall(CallerInfo ci, String number, int presentation, int callType, long start, long duration) { // no-op }
}
```

##### /mnt/dev/workspace/idol4/packages/services/Telephony/src/com/android/phone/CallStateMonitor.java
```java
/**
 * Dedicated Call state monitoring class.  This class communicates directly with
 * the call manager to listen for call state events and notifies registered
 * handlers.
 * It works as an inverse multiplexor for all classes wanted Call State updates
 * so that there exists only one channel to the telephony layer.
 *
 * TODO: Add manual phone state checks (getState(), etc.).
 */
class CallStateMonitor extends Handler { ... }
```

如注释说明，该类将自己注册到`CallManager`中以监听Call的事件。
```java
/**
 * Register for call state notifications with the CallManager.
 */
private void registerForNotifications() {
    //
    // TODO: The lines commented out here can be removed as their associated functionality in
    // other files is removed.
    //
    callManager.registerForNewRingingConnection(this, PHONE_NEW_RINGING_CONNECTION, null);
    callManager.registerForPreciseCallStateChanged(this, PHONE_STATE_CHANGED, null);
    callManager.registerForDisconnect(this, PHONE_DISCONNECT, null);
    callManager.registerForCdmaOtaStatusChange(this, EVENT_OTA_PROVISION_CHANGE, null);
    callManager.registerForDisplayInfo(this, PHONE_STATE_DISPLAYINFO, null);
    callManager.registerForSignalInfo(this, PHONE_STATE_SIGNALINFO, null);
    callManager.registerForInCallVoicePrivacyOn(this, PHONE_ENHANCED_VP_ON, null);
    callManager.registerForInCallVoicePrivacyOff(this, PHONE_ENHANCED_VP_OFF, null);
    callManager.registerForSuppServiceFailed(this, PHONE_SUPP_SERVICE_FAILED, null);
    callManager.registerForSuppServiceNotification(this, PHONE_SUPP_SERVICE_NOTIFY, null);
    //callManager.registerForRingbackTone(this, PHONE_RINGBACK_TONE, null);
    //callManager.registerForResendIncallMute(this, PHONE_RESEND_MUTE, null);
    //callManager.registerForPostDialCharacter(this, PHONE_ON_DIAL_CHARS, null);
    callManager.registerForTtyModeReceived(this, PHONE_TTY_MODE_RECEIVED, null);
}
```
???1. 当有`PHONE_NEW_RINGING_CONNECTION`类型消息到来时，意味着一个`RINGING`或`WAITING`的连接（`connection`）出现，此时`handleMessage`函数调用`onNewRingingConnection`来处理。后者先检查`Settings`里的设置是否可以接听电话；然后进行响铃（见`InCallTonePlayer`）和显示`InCallScreen`的`UI`，见`PhoneUtils.showIncomingCallUi()`和`PhoneApp.displayCallScreen()`两个函数。通话过程中的铃音提示由线程类`InCallTonePlayer`完成。
???2. 当有`PHONE_INCOMING_RING`类型的消息到来时，意味着RIL层受到Ring，此处播放铃音。它使用的是Ringer.ring()函数，它会创建一个线程去播放铃音,见Ringer.makeLooper函数。
3. 当有`PHONE_STATE_CHANGED`消息时，表明Phone的状态发生了改变，比如响铃后接通了电话，此时处理函数是onPhoneStateChanged，比如再次确认停止铃音、更新状态栏列的状态通知等。
4. 当有`PHONE_DISCONNECT`消息时，表明电话连接已挂断或RingCall断掉。其处理函数是onDisconnect。它清理现场诸如音频通道恢复、来电响铃的停止确认、对InCallScreen的UI清理、若有未接电话须在状态栏显示等。

##### /mnt/dev/workspace/idol4/packages/services/Telephony/src/com/android/phone/BluetoothManager.java
一个空实现类，暂时没有提供功能。

##### CallManager类的消息注册方法：
```java
registerForCallWaiting
registerForCdmaOtaStatusChange
registerForDisconnect
registerForDisplayInfo
registerForEcmTimerReset
registerForInCallVoicePrivacyOff
registerForInCallVoicePrivacyOn
registerForIncomingRing
registerForMmiComplete
registerForMmiInitiate
registerForNewRingingConnection
registerForOnHoldTone
registerForPhoneStates
registerForPostDialCharacter
registerForPreciseCallStateChanged
registerForResendIncallMute
registerForRingbackTone
registerForServiceStateChanged
registerForSignalInfo
registerForSubscriptionInfoReady
registerForSuppServiceFailed
registerForSuppServiceNotification
registerForTtyModeReceived
registerForUnknownConnection
registerPhone
```

### 电话状态改变事件处理
