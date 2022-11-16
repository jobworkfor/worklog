Android音频系统
==============

基本概念
----------------------------------------------------------------------------------------------------

声卡分为`软声卡`和`硬声卡`，区分标志是声卡中是否有主处理芯片，`软声卡`一般只有一个音频解码芯片，控制操作（如：播放）
还是需要由CPU来调度的，`硬声卡`一手包办了。

典型声卡的三个部分
1. `Connectors`: 用于连接外放设备，如音响耳机等，一般也被叫做`jacks`
2. `Audio Circuits`: 声卡主体，负责信号放大，混音，A/D等
3. `Interface`: 连接计算机总线的单元，如PCI

linux中查看声卡命令：
```
generic_x86_64:/ # cat proc/asound/cards                                                                                                                                                                                               
 0 [Intel          ]: HDA-Intel - HDA Intel
                      HDA Intel at 0xfebc0000 irq 11
```

Android平台上的声音处理依赖于Linux系统的音频驱动实现，主要有两种驱动架构：
1. OSS (Open Sound System): 老的音频架构，对新音频特性支持不足
2. ALSA(Advanced Linux Sound Architecture): 开源，新生，兼容OSS。

### ALSA

Alsa主要的文件节点如下：
```
/proc/asound: Information Interface
/dev/snd/controlCX: Control Interface
/dev/snd/mixerCXDX: Mixer Interface
/dev/snd/pcmCXDX: PCM Interface
/dev/snd/midiCXDX: Raw MIDI Interface
/dev/snd/seq: Sequencer Interface
/dev/snd/timer: Timer Interface
```

### TinyAlsa for Android
Android 使用的是ALSA的裁剪版本（对于ARM，原工程过于浩繁）。 TinyAlsa的源码文件很少：
```
android/aosp/external/tinyalsa
├── Android.bp
├── include
│   └── tinyalsa
│       └── asoundlib.h
├── mixer.c
├── MODULE_LICENSE_BSD
├── NOTICE
├── pcm.c
├── README
├── tinycap.c
├── tinyhostless.c
├── tinymix.c
├── tinypcminfo.c
└── tinyplay.c
```

Android Audio 系统架构
----------------------------------------------------------------------------------------------------

### 分层理解
从一般角度出发，可以分成三个层次：User，Audio Driver，Hardware。其中User又可以进一步分层为：App，Framework，Audio Lib，HAL。
整个分层如下所示：
```

        App
        --------------
        Framework
User    --------------
        Audio Lib
        --------------
        HAL
----------------------------
Audio Driver
----------------------------
Hardware
```

#### App
音乐播放器的实现

#### Framework
涉及的相关类：
* AudioManager
* AudioService
* AudioSystem
* AudioTrack
* AudioRecorder

#### Libraries
Java类中具体功能的实际实现都是在此处。相关代码位置：`frameworks/av/media/libmedia`

AudioFlinger和AudioPolicyService也属于该层，代码位置：`frameworks/av/services/audioflinger`

#### HAL
被AudioFlinger直接访问。



FAQ
----------------------------------------------------------------------------------------------------
### Adndroid VoIP相关的开源应用有哪些 ？
imsdroid，sipdroid，csipsimple，linphone，WebRTC 等等

### 音频算法处理的开源库有哪些 ？
speex、ffmpeg，webrtc audio module（NS、VAD、AECM、AGC），等等

### Android提供了哪些音频开发相关的API？
* 音频采集：     MediaRecoder，AudioRecord
* 音频播放：     SoundPool，MediaPlayer，AudioTrack （它们之间的区别可以参考这篇文章）
* 音频编解码：    MediaCodec
* NDK API：     OpenSL ES
