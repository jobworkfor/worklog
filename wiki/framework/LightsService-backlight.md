背光调节
=======


基本流程
----------------------------------------------------------------------------------------------------
### SystemUI调节亮度
```
@startprocess

==systemui==
> vendor/blackshark/app/SystemUI/src/com/android/systemui/settings/BrightnessController.java
    private static final String DEFALUT_SYS_BRIGHTNESS_FILE = "/sys/class/backlight/panel0-backlight/brightness";
    public void onChanged(ToggleSlider toggleSlider, boolean tracking, boolean automatic,
            int value, boolean stopTracking) {
        if (mIsVrModeEnabled) {
        } else if (!mAutomatic) {
->          setBrightness(val);


==settings==
> \packages\apps\Settings\src\com\android\settings\BrightnessSeekBarPreference.java
public void onProgressChanged(SeekBar seekBar, int progress, boolean fromTouch) {
    if (!mAutomatic) {
        final int val = getAdjustAdj(progress + mMinimumBacklight);
->      setBrightness(val);


==framework==
> frameworks/base/services/core/java/com/android/server/display/DisplayPowerController.java
    private void updatePowerState() {
        // Apply manual brightness.
        // Use the current brightness setting from the request, which is expected
        // provide a nominal default value for the case where auto-brightness
        // is not ready yet.
        if (brightness < 0) {
            if (mUseManualBrightnessSplineConfig) {
-issue->        float adjustedTarget = mScreenManualBrightnessSpline.interpolate((float)mPowerRequest.screenBrightness);
                brightness = clampScreenBrightness(Math.round(adjustedTarget));
            }else {
                brightness = clampScreenBrightness(mPowerRequest.screenBrightness);
            }
        }

        if (!mPendingScreenOff) {
            boolean wasOrWillBeInVr = (state == Display.STATE_VR || oldState == Display.STATE_VR);
            if ((state == Display.STATE_ON
                    && mSkipRampState == RAMP_STATE_SKIP_NONE
                    || state == Display.STATE_DOZE && !mBrightnessBucketsInDozeConfig)
                    && !wasOrWillBeInVr) {
                int[] ret = mDisplayPowerControllerInjector.getRate(brightness, mPowerRequest,mPowerState,
                                mAppliedAutoBrightness,autoBrightnessAdjustmentChanged,
                                autoBrightnessEnabled, mScreenBrightnessRangeMaximum);
->              animateScreenBrightness(ret[0], ret[1]);


> frameworks/base/services/core/java/com/android/server/lights/LightsService.java
        private void setLightLocked(int color, int mode, int onMS, int offMS, int brightnessMode) {
            if (shouldBeInLowPersistenceMode()) {
                brightnessMode = BRIGHTNESS_MODE_LOW_PERSISTENCE;
            } else if (brightnessMode == BRIGHTNESS_MODE_LOW_PERSISTENCE) {
                brightnessMode = mLastBrightnessMode;
            }

            if (!mInitialized || color != mColor || mode != mMode || onMS != mOnMS ||
                    offMS != mOffMS || mBrightnessMode != brightnessMode) {
                if (DEBUG) Slog.v(TAG, "setLight #" + mId + ": color=#"
                        + Integer.toHexString(color) + ": brightnessMode=" + brightnessMode);
                mInitialized = true;
                mLastColor = mColor;
*               mColor = color;
                mMode = mode;
                mOnMS = onMS;
                mOffMS = offMS;
                mBrightnessMode = brightnessMode;
                Trace.traceBegin(Trace.TRACE_TAG_POWER, "setLight(" + mId + ", 0x"
                        + Integer.toHexString(color) + ")");
                mPerfMan.notify(HawkeyeErrno.EMS_LCD_SET_BACKLIGHT_BEGIN);
                try {
->                  setLight_native(mId, color, mode, onMS, offMS, brightnessMode);
                } finally {
                    mPerfMan.notify(HawkeyeErrno.EMS_LCD_SET_BACKLIGHT_END);
                    Trace.traceEnd(Trace.TRACE_TAG_POWER);
                }
            }
        }

==jni==
> /frameworks/base/services/core/jni/com_android_server_lights_LightsService.cpp
static void c(
        JNIEnv* /* env */,
        jobject /* clazz */,
        jint light,
        jint colorARGB,
        jint flashMode,
        jint onMS,
        jint offMS,
        jint brightnessMode) {
    {
        android::base::Timer t;
->      Return<Status> ret = hal->setLight(type, state);
        processReturn(ret, type, state);
        if (t.duration() > 50ms) ALOGD("Excessive delay setting light");
    }
}

static const JNINativeMethod method_table[] = {
    { "setLight_native", "(IIIIII)V", (void*)setLight_native },
};



==hal==
> hardware/interfaces/light/2.0/ILight.hal
interface ILight {
    setLight(Type type, LightState state) generates (Status status);
};


> hardware/qcom/display/liblight/lights.c
static int
set_light_backlight(struct light_device_t* dev,
        struct light_state_t const* state)
{
    if (!err) {
        if (!access(LCD_FILE, F_OK)) {
            ...
        } else if (!access(LCD_FILE2, F_OK)){
log>        ALOGI("file2 brightness %d\n", brightness);
->          err = write_int(LCD_FILE2, brightness);
        }
    }
}

==driver==
> kernel/msm-4.9/drivers/video/backlight/backlight.c
static ssize_t brightness_store(struct device *dev,
        struct device_attribute *attr, const char *buf, size_t count)
{
    int rc;
    struct backlight_device *bd = to_backlight_device(dev);
    unsigned long brightness;
    rc = kstrtoul(buf, 0, &brightness);
    if (rc)
        return rc;
    bd->usr_brightness_req = brightness;
->  brightness = (brightness <= bd->thermal_brightness_limit) ?
                bd->usr_brightness_req :
                bd->thermal_brightness_limit;
    rc = backlight_device_set_brightness(bd, brightness);
    return rc ? rc : count;
}
static DEVICE_ATTR_RW(brightness);

@endprocess
```

程序分层
----------------------------------------------------------------------------------------------------


### HAL
/hardware/qcom/display/liblight/lights.c
```
static struct hw_module_methods_t lights_module_methods = {
    .open =  open_lights,
};
struct hw_module_t HAL_MODULE_INFO_SYM = {
    .tag = HARDWARE_MODULE_TAG,
    .version_major = 1,
    .version_minor = 0,
    .id = LIGHTS_HARDWARE_MODULE_ID,
    .name = "lights Module",
    .author = "Google, Inc.",
    .methods = &lights_module_methods,
};
```


