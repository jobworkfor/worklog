android声音通道的切换
===================

在进行通道切换时，为什么会在原通道上设置一回在去设置新的通道

一、Application framework
----------------------------------------------------------------------------------------------------

在Application framework层级是app层的code，是通过Android.media提供的API来与audio硬件进行交互动作，这部分的代码是通过audio JNI来调用native代码从而达到影响硬件的效果；

二、JNI
----------------------------------------------------------------------------------------------------

JNI部分的代码是位于 frameworks/base/core/jni/和frameworks/base/media/jni 目录下的；

三、Native framework
----------------------------------------------------------------------------------------------------

四、Binder IPC
----------------------------------------------------------------------------------------------------

Binder IPC通信是跨进程通信的手段，audio的这部分代码位于frameworks/av/media/libmedia目录下，并且命名都是以I开头的；

五、Media Server
----------------------------------------------------------------------------------------------------

Audio Service是隶属Media Server的，其代码位于 frameworks/av/services/audioflinger，它是真正的与HAL层的实现进行交互的；

六、HAL
----------------------------------------------------------------------------------------------------

HAL层定义了Audio Service调用的标准接口，不同的硬件必须根据自己的情况来实现这个接口来让硬件在android中正常的工作，所以可以在不影响应用层系统调用的情况下，更换不同的硬件。大大减少了系统耦合性；

七、Kernel Driver
----------------------------------------------------------------------------------------------------

Audio驱动是与硬件进行交互，并且实现HAL层的接口供上层正常调用，这里，厂商可以选择ALSA,OSS以及自定义的音频驱动； （NOTE：如果选择ALSA，android建议使用 external/tinyalsa目录下的实现）； 接下来就来说说通话时音频通道的切换，但是往下看之前必须知道，对于Audio Path的切换，android有一策略管理器来帮我们分配好输入输出的设备，比如当手机播放音乐时，从Speaker播放出来，这时候插入耳机的话会从耳机设备输出；但是有时候我们想要自己去指定的话，就是我们接下来要说的了； 我们在通话时，要是开免提，实际上也就是Audio Path切换到了Speaker，也就是外方喇叭；代码中的话调用一个函数即可，这是强制切换audio Path，不遵从系统的分配：
```
AudioManager audioManager = (AudioManager) context.getSystemService(Context.AUDIO_SERVICE); audioManager.setSpeakerphoneOn(true);
```
中间过程简单不说，最终是调用到了JNI，android_media_AudioSystem中的android_media_AudioSystem_setForceUse()函数，来看下其具体实现：
```
android_media_AudioSystem_setForceUse(JNIEnv *env, jobject thiz, jint usage, jint config)
{
    return check_AudioSystem_Command(AudioSystem::setForceUse(static_cast <audio_policy_force_use_t>(usage),
                                                           static_cast <audio_policy_forced_cfg_t>(config)));
}
```
显而易见，它是调用了AudioSystem.cpp的setForceUse()函数，check_AudioSystem_Command()不说，重点看看audio_policy_force_use_t和audio_policy_forced_cfg_t这两个结构体： 
audio_policy_force_use_t 说明的是当前的Audio环境 
audio_policy_forced_cfg_t 表示audio的输入输出设备 
它们是专门为setForceUse所用的；
```
/* usages used for audio_policy->set_force_use() */ 
typedef enum { 
AUDIO_POLICY_FORCE_FOR_COMMUNICATION, //表示的是通话过程中 
AUDIO_POLICY_FORCE_FOR_MEDIA, //媒体
AUDIO_POLICY_FORCE_FOR_RECORD, //录音
AUDIO_POLICY_FORCE_FOR_DOCK, 
AUDIO_POLICY_FORCE_FOR_SYSTEM, 
AUDIO_POLICY_FORCE_USE_CNT, 
AUDIO_POLICY_FORCE_USE_MAX = AUDIO_POLICY_FORCE_USE_CNT - 1, 
} audio_policy_force_use_t; 

 /* device categories used for audio_policy->set_force_use() */ 
typedef enum {
    AUDIO_POLICY_FORCE_NONE, 
    AUDIO_POLICY_FORCE_SPEAKER, 
    AUDIO_POLICY_FORCE_HEADPHONES, 
    AUDIO_POLICY_FORCE_BT_SCO, 
    AUDIO_POLICY_FORCE_BT_A2DP, 
    AUDIO_POLICY_FORCE_WIRED_ACCESSORY, 
    AUDIO_POLICY_FORCE_BT_CAR_DOCK, 
    AUDIO_POLICY_FORCE_BT_DESK_DOCK, 
    AUDIO_POLICY_FORCE_ANALOG_DOCK, 
    AUDIO_POLICY_FORCE_DIGITAL_DOCK, 
    AUDIO_POLICY_FORCE_NO_BT_A2DP, 
    /* A2DP sink is not preferred to speaker or wired HS */   
    AUDIO_POLICY_FORCE_SYSTEM_ENFORCED, 
    AUDIO_POLICY_FORCE_CFG_CNT, 
    AUDIO_POLICY_FORCE_DEFAULT = AUDIO_POLICY_FORCE_NONE, 
} audio_policy_forced_cfg_t; 
```
这时候我们就应该知道，当我想要在通话时打开Speaker，传递的参数就是usage和config分别是AUDIO_POLICY_FORCE_FOR_COMMUNICATION和AUDIO_POLICY_FORCE_SPEAKER了，这两个参数从上层一直到底层，还是很简单的； 
接着往下看就是调用的AudioSystem.cpp的setForceUse()函数了:
```
status_t AudioSystem::setForceUse(audio_policy_force_use_t usage, audio_policy_forced_cfg_t config) 
{ 
    SLOGE("setForceUse() usage = %d, config = %d" ,usage , config);
    if (aps == 0) return PERMISSION_DENIED; return aps->setForceUse(usage, config); 
} 
```
get_audio_policy_service()函数不做过多解释，就是通过Native的ServiceManager来获取audio policy的Service代理对象，从而实现与audio policy的进程间通讯；
```
 ....... 
 binder = sm->getService(String16("media.audio_policy"));
```
接下来就是调用frameworks/av/services/audioflinger/AudioPolicyService.cpp的setForceUse()函数了；
```
status_t AudioPolicyService::setForceUse(audio_policy_force_use_t usage, audio_policy_forced_cfg_t config) 
{ 
    if (mpAudioPolicy == NULL) { 
        return NO_INIT; 
    } 
    if (!settingsAllowed()) { 
        return PERMISSION_DENIED; 
    } 
    if (usage < 0 || usage >= AUDIO_POLICY_FORCE_USE_CNT) { 
        return BAD_VALUE; 
    } 
    if (config < 0 || config >= AUDIO_POLICY_FORCE_CFG_CNT) { 
        return BAD_VALUE; 
    } 
    Mutex::Autolock _l(mLock); 
    mpAudioPolicy->set_force_use(mpAudioPolicy, usage, config); 
    return NO_ERROR; 
} 
```
这个mpAudioPolicy是什么呢？它的set_force_use函数在哪里实现呢？这两个问题需要了解就OK了； 首先mpAudioPolicy它是一个指针，在AudioServicePolicy.cpp的构造函数中被赋值，来看看其赋值过程：
```
...... 
const struct hw_module_t *module; 
...... 
rc = hw_get_module(AUDIO_POLICY_HARDWARE_MODULE_ID, &module); 
...... 
rc = audio_policy_dev_open(module, &mpAudioPolicyDev); 
...... 
rc = mpAudioPolicyDev->create_audio_policy(mpAudioPolicyDev,&aps_ops,this, &mpAudioPolicy);
 ...... 
```
首先AUDIO_POLICY_HARDWARE_MODULE_ID值是：
```
   #define AUDIO_POLICY_HARDWARE_MODULE_ID "audio_policy" 
```
其次module是一个指针，指向的是一个hw_module_t结构体类型，它的作用是调用系统的哪个audio policy module，这个module可以是原始的，也可以由厂商自定义的
```
typedef struct hw_module_t { 
/** tag must be initialized to HARDWARE_MODULE_TAG */ 
    uint32_t tag; 
    uint16_t module_api_version; 
    #define version_major module_api_version 
    uint16_t hal_api_version; 
    #define version_minor hal_api_version 
    /** Identifier of module */ 
    const char *id; 
    const char *name; 
    const char *author; 
    /** Modules methods */ 
    struct hw_module_methods_t* methods; 
    /** module's dso */ 
    void* dso; 
    /** padding to 128 bytes, reserved for future use */ 
    uint32_t reserved[32-7]; 
} hw_module_t; 
```
再来看看是如何给module赋值的: hardware.c
```
int hw_get_module(const char *id, const struct hw_module_t **module) 
{ 
    return hw_get_module_by_class(id, NULL, module); 
} 
```
看看hw_get_module_by_class方法的实现： hardware.c
```
int hw_get_module_by_class(const char *class_id, const char *inst, const struct hw_module_t **module) { 
    int status; 
    int i; const struct hw_module_t *hmi = NULL; 
    char prop[PATH_MAX]; char path[PATH_MAX]; 
    char name[PATH_MAX]; 
    if (inst) 
        snprintf(name, PATH_MAX, "%s.%s", class_id, inst);
    else
        strlcpy(name, class_id, PATH_MAX);
    /* * Here we rely on the fact that calling dlopen multiple times on
       * the same .so will simply increment a refcount (and not load
       * a new copy of the library).
       * We also assume that dlopen() is thread-safe. 
    */ 

    /* Loop through the configuration variants looking for a module */
    for (i=0 ; i<HAL_VARIANT_KEYS_COUNT+1 ; i++)
    {
        if (i < HAL_VARIANT_KEYS_COUNT) { 
            if (property_get(variant_keys[i], prop, NULL) == 0) { 
                continue; 
            } 
            snprintf(path, sizeof(path), "%s/%s.%s.so", HAL_LIBRARY_PATH2, name, prop); 
            if (access(path, R_OK) == 0)
                break;
            snprintf(path, sizeof(path), "%s/%s.%s.so", HAL_LIBRARY_PATH1, name, prop);
            if (access(path, R_OK) == 0)
                break;
        }
        else { 
            snprintf(path, sizeof(path), "%s/%s.default.so", HAL_LIBRARY_PATH1, name);
            if (access(path, R_OK) == 0)
                break; 
            } 
    } 
    status = -ENOENT; 
    if (i < HAL_VARIANT_KEYS_COUNT+1) { 
    /* load the module, if this fails, we're doomed, and we should not try
     * to load a different variant.
     */ 
    status = load(class_id, path, module); 
    } 
    return status; 
} 
```
方法是找到指定的库文件并且加载；不做详细介绍；这里会得到audio_policy.default.so；这个库正是编译hardware/libhardware_legacy/audio出来的； 再跳回到AudioPolicyService的构造函数中来；接下来 ： 
```
rc = audio_policy_dev_open(module, &mpAudioPolicyDev); 
```

它调用的是legacy_ap_dev_open()函数,不做详细介绍：audio_policy_hal.cpp
```
static int legacy_ap_dev_open(const hw_module_t* module, const char* name, hw_device_t** device) 
{ 
    struct legacy_ap_device *dev; 
    if (strcmp(name, AUDIO_POLICY_INTERFACE) != 0) 
        return -EINVAL; 
    dev = (struct legacy_ap_device *)calloc(1, sizeof(*dev)); 
    if (!dev) return -ENOMEM; 
    dev->device.common.tag = HARDWARE_DEVICE_TAG;
    dev->device.common.version = 0;
    dev->device.common.module = const_cast<hw_module_t*>(module);
    dev->device.common.close = legacy_ap_dev_close;
    dev->device.create_audio_policy = create_legacy_ap;
    dev->device.destroy_audio_policy = destroy_legacy_ap;
    *device = &dev->device.common; return 0;
} 
```
create_audio_policy()中的aps_ops参数指针代表的是，它是AudioPolicyService与外界交互的接口：
```
struct audio_policy_service_ops aps_ops = { 
    open_output : aps_open_output, 
    open_duplicate_output : aps_open_dup_output, 
    close_output : aps_close_output,
    suspend_output : aps_suspend_output,
    restore_output : aps_restore_output,
    open_input : aps_open_input,
    close_input : aps_close_input,
    set_stream_volume : aps_set_stream_volume,
    set_stream_output : aps_set_stream_output,
    set_parameters : aps_set_parameters,
    get_parameters : aps_get_parameters,
    start_tone : aps_start_tone,
    stop_tone : aps_stop_tone,
    set_voice_volume : aps_set_voice_volume,
    move_effects : aps_move_effects,
    load_hw_module : aps_load_hw_module,
    open_output_on_module : aps_open_output_on_module,
    open_input_on_module : aps_open_input_on_module,
};
```
知道了这些，接下来看create_audio_policy()： create_audio_policy()这个函数作用是创建一个用户自定义的policy_hal模块的接口，因为我们使用的是qcom的芯片，qcom有自己的一套，android原生有自己的一套，就依照原生的来看吧；其实都是差不多的； 刚刚上面分析的legacy_ap_dev_open()函数有这样一句：
```
...... 
dev->device.create_audio_policy = create_legacy_ap; 
...... 
```
那这样我们就来看看其create_legacy_ap()函数吧；我们只需要关注的是其中的那么几小段：
```
static int create_legacy_ap(const struct audio_policy_device *device, struct audio_policy_service_ops *aps_ops, void *service, struct audio_policy **ap)
{ 
    struct legacy_audio_policy *lap;
    ......
    lap = (struct legacy_audio_policy *)calloc(1, sizeof(*lap));
    ......
    lap->policy.set_force_use = ap_set_force_use;
    ......
    lap->service = service;
    lap->aps_ops = aps_ops;
    lap->service_client = new AudioPolicyCompatClient(aps_ops, service);
    ......
    lap->apm = createAudioPolicyManager(lap->service_client);
    ......
    *ap = &lap->policy;
    ......
}
```
就这样，AudioPolicyService.cpp的set_force_use()函数就调用到了这里： audio_policy_hal.cpp
```
 /* force using a specific device category for the specified usage */ 
 static void ap_set_force_use(struct audio_policy *pol, audio_policy_force_use_t usage, audio_policy_forced_cfg_t config)
 {
     struct legacy_audio_policy *lap = to_lap(pol);
     lap->apm->setForceUse((AudioSystem::force_use)usage, (AudioSystem::forced_config)config);
 }
```
从之前的create_legacy_ap()函数我们知道apm的由来，
```
  java lap->apm = createAudioPolicyManager(lap->service_client); 
```
createAudioPolicyManager()函数定义在AudioPolicyInterface.h接口中；
```
extern "C" 
AudioPolicyInterface* createAudioPolicyManager(AudioPolicyClientInterface *clientInterface); 
```
而这个createAudioPolicyManager()由硬件厂商实现，返回其AudioPolicyManager；qcom的实现是在AudioPolicyManagerALSA.cpp中；再往下不做具体分析了，主要是根据不同的策略来切换不同的Output和input设备以及其他一些操作；如果想进一步分析的话，还需要关注AudioPolicyManagerBase.cpp； 其实准确的总结起来是AudioPolicyService是一个壳子，这个壳子的重要关键就是audio_policy，真正的实现可以由厂商来自己实现，当然android也有，就是AudioPolicyManagerDefault


Reference
----------------------------------------------------------------------------------------------------
* [android声音通道的切换](http://blog.csdn.net/neverbefat/article/details/53407891)