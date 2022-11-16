VibratorService Readme
======================


VibratorService运行在`system_server`进程中，应用通过`frameworks/base/core/java/android/os/IVibratorService.aidl`来
调用其开放的API，aidl定义的接口如下：
```cpp
21/** {@hide} */
22interface IVibratorService
23{
24    boolean hasVibrator();
25    boolean hasAmplitudeControl();
26    void vibrate(int uid, String opPkg, in VibrationEffect effect, int usageHint, IBinder token);
27    void cancelVibrate(IBinder token);
28}
```
> http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/core/java/android/os/IVibratorService.aidl#22


vibrate()调用流程
----------------------------------------------------------------------------------------------------

* == system_server ==
* [private void startOtherServices()](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/java/com/android/server/SystemServer.java#761)
    * [ServiceManager.addService("vibrator", vibrator);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/java/com/android/server/SystemServer.java#874)

* APP call vibrate(...) API
* [public void vibrate(int uid, String opPkg, VibrationEffect effect, int usageHint,](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/VibratorService.java#485)
    * [Vibration vib = new Vibration(token, effect, usageHint, uid, opPkg);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/VibratorService.java#534)
    * [startVibrationLocked(vib);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/VibratorService.java#539)
        * [startVibrationInnerLocked(vib);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/VibratorService.java#648)
            * [<b>doVibratorOn(oneShot.getDuration(), oneShot.getAmplitude(), vib.uid, vib.usageHint);</b>](#1)
                * [<b>vibratorOn(millis);</b>](#2)
                * [native static void vibratorOn(long milliseconds);](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/VibratorService.java#144)
                * [static void vibratorOn(JNIEnv* /* env */, jobject /* clazz */, jlong timeout_ms)](http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/jni/com_android_server_VibratorService.cpp#110)
                    * [<b>Status retStatus = halCall(&V1_0::IVibrator::on, timeout_ms).withDefault(Status::UNKNOWN_ERROR);</b>](#3)
                        * [<b>int32_t ret = mDevice->vibrator_on(mDevice, timeout_ms);</b>](#4)
                        * [static int vibra_on(vibrator_device_t* vibradev __unused, unsigned int timeout_ms)](http://androidxref.blackshark.com:8088/sm8150/xref/hardware/libhardware/modules/vibrator/vibrator.c#88)
                            * [return sendit(timeout_ms);](http://androidxref.blackshark.com:8088/sm8150/xref/hardware/libhardware/modules/vibrator/vibrator.c#91)
                                * [snprintf(value, sizeof(value), "%u", timeout_ms);](http://androidxref.blackshark.com:8088/sm8150/xref/hardware/libhardware/modules/vibrator/vibrator.c#84)
                                * [return write_value(THE_DEVICE="/sys/class/timed_output/vibrator/enable", value);](http://androidxref.blackshark.com:8088/sm8150/xref/hardware/libhardware/modules/vibrator/vibrator.c#85)
                                    * [fd = TEMP_FAILURE_RETRY(open(file, O_WRONLY));](http://androidxref.blackshark.com:8088/sm8150/xref/hardware/libhardware/modules/vibrator/vibrator.c#55)
                                    * [written = TEMP_FAILURE_RETRY(write(fd, value, to_write));](http://androidxref.blackshark.com:8088/sm8150/xref/hardware/libhardware/modules/vibrator/vibrator.c#61)

----------------------------------------------------------------------------------------------------

### <a id=1></a>mH.postDelayed

通过Vibration对象的effect成员来确定当前震动的模式。
```cpp
654    @GuardedBy("mLock")
655    private void startVibrationInnerLocked(Vibration vib) {
656        Trace.traceBegin(Trace.TRACE_TAG_VIBRATOR, "startVibrationInnerLocked");
657        try {
658            mCurrentVibration = vib;
659            if (vib.effect instanceof VibrationEffect.OneShot) {
660                Trace.asyncTraceBegin(Trace.TRACE_TAG_VIBRATOR, "vibration", 0);
661                VibrationEffect.OneShot oneShot = (VibrationEffect.OneShot) vib.effect;
662->              doVibratorOn(oneShot.getDuration(), oneShot.getAmplitude(), vib.uid, vib.usageHint);
663                mH.postDelayed(mVibrationEndRunnable, oneShot.getDuration());
664            } else if (vib.effect instanceof VibrationEffect.Waveform) {
665                // mThread better be null here. doCancelVibrate should always be
666                // called before startNextVibrationLocked or startVibrationLocked.
667                Trace.asyncTraceBegin(Trace.TRACE_TAG_VIBRATOR, "vibration", 0);
668                VibrationEffect.Waveform waveform = (VibrationEffect.Waveform) vib.effect;
669                mThread = new VibrateThread(waveform, vib.uid, vib.usageHint);
670                mThread.start();
671            } else if (vib.effect instanceof VibrationEffect.Prebaked) {
672                Trace.asyncTraceBegin(Trace.TRACE_TAG_VIBRATOR, "vibration", 0);
673                long timeout = doVibratorPrebakedEffectLocked(vib);
674                if (timeout > 0) {
675                    mH.postDelayed(mVibrationEndRunnable, timeout);
676                }
677            } else {
678                Slog.e(TAG, "Unknown vibration type, ignoring");
679            }
680        } finally {
681            Trace.traceEnd(Trace.TRACE_TAG_VIBRATOR);
682        }
683    }
```
> http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/VibratorService.java#662


### <a id=2></a>vibratorOn(millis)
```cpp
918    private void doVibratorOn(long millis, int amplitude, int uid, int usageHint) {
919        Trace.traceBegin(Trace.TRACE_TAG_VIBRATOR, "doVibratorOn");
920        try {
921            synchronized (mInputDeviceVibrators) {
922                if (amplitude == VibrationEffect.DEFAULT_AMPLITUDE) {
923                    amplitude = mDefaultVibrationAmplitude;
924                }
925                if (DEBUG) {
926                    Slog.d(TAG, "Turning vibrator on for " + millis + " ms" +
927                            " with amplitude " + amplitude + ".");
928                }
929                noteVibratorOnLocked(uid, millis);
930                final int vibratorCount = mInputDeviceVibrators.size();
931                if (vibratorCount != 0) {
932                    final AudioAttributes attributes =
933                            new AudioAttributes.Builder().setUsage(usageHint).build();
934                    for (int i = 0; i < vibratorCount; i++) {
935                        mInputDeviceVibrators.get(i).vibrate(millis, attributes);
936                    }
937                } else {
938                    // Note: ordering is important here! Many haptic drivers will reset their
939                    // amplitude when enabled, so we always have to enable frst, then set the
940                    // amplitude.
941->                  vibratorOn(millis);
942                    doVibratorSetAmplitude(amplitude);
943                }
944            }
945        } finally {
946            Trace.traceEnd(Trace.TRACE_TAG_VIBRATOR);
947        }
948    }
```
> http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/java/com/android/server/VibratorService.java#941


### <a id=3></a>halCall()
```cpp
57// Helper used to transparently deal with the vibrator HAL becoming unavailable.
58template<class R, class I, class... Args0, class... Args1>
59Return<R> halCall(Return<R> (I::* fn)(Args0...), Args1&&... args1) {
60    // Assume that if getService returns a nullptr, HAL is not available on the
61    // device.
62    static sp<I> sHal = I::getService();
63    static bool sAvailable = sHal != nullptr;
64
65    if (!sAvailable) {
66        return NullptrStatus<R>();
67    }
68
69    // Return<R> doesn't have a default constructor, so make a Return<R> with
70    // STATUS::EX_NONE.
71    using ::android::hardware::Status;
72    Return<R> ret{Status::fromExceptionCode(Status::EX_NONE)};
73
74    // Note that ret is guaranteed to be changed after this loop.
75    for (int i = 0; i < NUM_TRIES; ++i) {
76        ret = (sHal == nullptr) ? NullptrStatus<R>()
77                : (*sHal.*fn)(std::forward<Args1>(args1)...);
78
79        if (ret.isOk()) {
80            break;
81        }
82
83        ALOGE("Failed to issue command to vibrator HAL. Retrying.");
84        // Restoring connection to the HAL.
85        sHal = I::tryGetService();
86    }
87    return ret;
88}
...
110static void vibratorOn(JNIEnv* /* env */, jobject /* clazz */, jlong timeout_ms)
111{
112    Status retStatus = halCall(&V1_0::IVibrator::on, timeout_ms).withDefault(Status::UNKNOWN_ERROR);
113    if (retStatus != Status::OK) {
114        ALOGE("vibratorOn command failed (%" PRIu32 ").", static_cast<uint32_t>(retStatus));
115    }
116}
```
> http://androidxref.blackshark.com:8088/sm8150/xref/frameworks/base/services/core/jni/com_android_server_VibratorService.cpp#112

halCall是个模板方法，调用方法为`V1_0::IVibrator::on`。
```cpp
19interface IVibrator {
20  /**
21   * Turn on vibrator
22   *
23   * This function must only be called after the previous timeout has expired or
24   * was canceled (through off()).
25   * @param timeout_ms number of milliseconds to vibrate.
26   * @return vibratorOnRet whether vibrator command was successful or not.
27   */
28  on(uint32_t timeoutMs) generates (Status vibratorOnRet);
```
> http://androidxref.blackshark.com:8088/sm8150/xref/hardware/interfaces/vibrator/1.0/IVibrator.hal#19

hal service采用了defaultPassthroughServiceImplementation方式，调用到`/hardware/libhardware/modules/vibrator/vibrator.c`
```cpp
24int main() {
25#ifdef ARCH_ARM_32
26    android::hardware::ProcessState::initWithMmapSize((size_t)8192);
27#endif
28    return defaultPassthroughServiceImplementation<IVibrator>();
29}
30
```

### <a id=4></a>mDevice->vibrator_on
```cpp
36// Methods from ::android::hardware::vibrator::V1_0::IVibrator follow.
37Return<Status> Vibrator::on(uint32_t timeout_ms) {
38    int32_t ret = mDevice->vibrator_on(mDevice, timeout_ms);
39    if (ret != 0) {
40        ALOGE("on command failed : %s", strerror(-ret));
41        return Status::UNKNOWN_ERROR;
42    }
43    return Status::OK;
44}
```
> http://androidxref.blackshark.com:8088/sm8150/xref/hardware/interfaces/vibrator/1.0/default/Vibrator.cpp#38

mDevice的定义如下：

```cpp
37typedef struct vibrator_device {
38    /**
39     * Common methods of the vibrator device.  This *must* be the first member of
40     * vibrator_device as users of this structure will cast a hw_device_t to
41     * vibrator_device pointer in contexts where it's known the hw_device_t references a
42     * vibrator_device.
43     */
44    struct hw_device_t common;
45
46    /** Turn on vibrator
47     *
48     * This function must only be called after the previous timeout has expired or
49     * was canceled (through vibrator_off()).
50     *
51     * @param timeout_ms number of milliseconds to vibrate
52     *
53     * @return 0 in case of success, negative errno code else
54     */
55    int (*vibrator_on)(struct vibrator_device* vibradev, unsigned int timeout_ms);
56
57    /** Turn off vibrator
58     *
59     * Cancel a previously-started vibration, if any.
60     *
61     * @return 0 in case of success, negative errno code else
62     */
63    int (*vibrator_off)(struct vibrator_device* vibradev);
64} vibrator_device_t;
```
> http://androidxref.blackshark.com:8088/sm8150/xref/hardware/libhardware/include/hardware/vibrator.h#37
