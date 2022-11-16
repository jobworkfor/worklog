

```
[AudioTrack(java)]
->new AudioTrack()
    [android_media_AudioTrack]
`   >native_setup()
        [AudioTrack(native)]
    `   >new AudioTrack()
    `   >set()
         `createTrack_l()
            [AudioSystem]
        `   >getOutpurForAttr()
                [AudioPolicyManager]
            `   >getOutpurForAttr()
                    [Engine]





```

```
[AudioFlinger]
->openOutput()
openOutput_l()
    [Threads]
`   >new MixerThread()
    `onFirstRef()
     `threadLoop()
      `prepareTracks_l()
        [AudioMixer]
    `   >setBufferProvider()
    `   >enable()
    `   >setParameter()
    threadLoop_mix()
    `   >process()
    threadLoop_write()
            [audio_hw.c]
        `   >out_write()
                [Tinyalsa_pcm.c]
            `   >pcm_write()
    threadLoop_removeTracks()
    threadLoop_exit()
```
