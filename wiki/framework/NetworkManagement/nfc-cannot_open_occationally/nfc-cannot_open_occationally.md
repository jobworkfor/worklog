

# 

Hi, Harry, Fenia,

经过LOG分 析，发 现NFC卡顿的地 方发 生在check firmware里。
由于check firmware会 比较firmware modified的time， 只有第一次刷完机的时候，firmware时 间会有变化，才会进doDownload。
所以工厂报的问题都是，刚刷完版本，在第一次开机的时候，有概率发 现不 能打 开NFC。重 启之后不能 重现。
idol4/NEON 都报过类似问题。
由于当时没有开机，有问题的log， 所以 这个 问题 一直没有办法解决。

经过仔细分析，我们注释掉： 
```
checkFirmware {
 ......
if (prev_fw_modtime == modtime) {
    //return;
}
......
}
```

让手机在每次开机时都去做一次doDownload的 动作，增大了重现概率。
目前重现过一次NFC不 能打 开的 情 况，并 且抓 取了 完整的开机log。

经过分析：
```
void NfcAdaptation::DownloadFirmware ()  {
    mHalCoreInitCompletedEvent.lock();
    ALOGD("%s: send CORE_INIT", func);
    HalWrite(cmd_init_nci_size , cmd_init_nci);
    mHalCoreInitCompletedEvent.wait();      
    //有问题的情况，wait调用有延时，在mHalCoreInitCompletedEvent.signal发出来之后，才被调用，导致再也没有地方去发mHalCoreInitCompletedEvent signal
    mHalInitCompletedEvent.lock ();
    ALOGD ("%s: try init HAL", func);
}
```

附，OK和NOK的log， 请尽快帮忙分析一下。

Surong, PANG




# Root Cause



# Solution

Hi Surong,
 
如刚才 电 话，根 据log来看， 存在 较难 重现 的core init没有响 应的 情 况，由 于没 有超 时处 理机 制， 所以 会停在这个地方。
 
建议去 掉checkfirmware的动作 （也 就是nfc off的时候 的firmware升 级），在mmi测试的 时候 来做 升 级。
 
之前这 个建 议也 提给 你们 惠州 和宁 波 了，可 以内 部同步下。
 
谢谢！
 
Best Regards,
Harry Chen
