# Android:进程UID定义


当在adb shell中查询当前进程情况时(ps),可以看到app应用都分配了一个user属性，
如app_37分配给了自己创建的应用com.andy.androidtest，在不卸载这个应用之前，这个属性是保持不变的。
非系统的应用都是以app开头命名，之后的编号就是uid（确切的说是uid-10000）。

    # ps
    ps
    USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME
    root      1     0     312    220   c009b74c 0000ca4c S /init
    ...
    app_37    598   33    132460 19900 ffffffff afd0eb08 S com.andy.androidtest
    

通过下面的代码我们可以枚举所有在运行的process的uid等属性：

    private RunningAppProcessInfo getForegroundApp()
    {
        RunningAppProcessInfo result = null, info = null;
    
        if (mActivityManager == null)
            mActivityManager = (ActivityManager) mContext
                    .getSystemService(Context.ACTIVITY_SERVICE);
        List<RunningAppProcessInfo> l = mActivityManager
                .getRunningAppProcesses();
        Iterator<RunningAppProcessInfo> i = l.iterator();
        while (i.hasNext())
        {
            info = i.next();
            Log.v(TAG,"running app process:"+String.valueOf(info.uid)+" "+info.processName);
            if (info.importance == RunningAppProcessInfo.IMPORTANCE_FOREGROUND
                    && !isRunningService(info.processName))
            {
                result = info;
                //Log.v(TAG,"running app:"+info.processName);
                break;
            }
        }
        return result;
    }

输出结果：

    10-25 08:41:16.766: V/ANDROIDTEST(598): running app process:10037 com.andy.androidtest
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10025 com.android.launcher
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10028 com.svox.pico
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10010 com.android.defcontainer
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10002 android.process.media
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10012 com.android.quicksearchbox
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10022 com.android.music
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10007 com.android.protips
    10-25 08:41:16.774: V/ANDROIDTEST(598): running app process:10023 jp.co.omronsoft.openwnn
    10-25 08:41:16.785: V/ANDROIDTEST(598): running app process:1000 system
    10-25 08:41:16.785: V/ANDROIDTEST(598): running app process:1001 com.android.phone
    10-25 08:41:16.785: V/ANDROIDTEST(598): running app process:10030 com.android.email
    10-25 08:41:16.785: V/ANDROIDTEST(598): running app process:10015 com.android.mms
    10-25 08:41:16.795: V/ANDROIDTEST(598): running app process:10009 com.android.alarmclock
    10-25 08:41:16.795: V/ANDROIDTEST(598): running app process:10000 android.process.acore
    10-25 08:41:16.795: V/ANDROIDTEST(598): running app process:1000 com.android.settings

可以看出,这些应用的process 的 uid是大于10000的，ps显示的结果中app_xx，xx部分就是pid减去10000的结果，是一一对应的关系。
这个10000定义在下列文件中的：AID_APP
http://androidxref.com/6.0.1_r10/xref/system/core/include/private/android_filesystem_config.h
```c
/* This is the master Users and Groups config for the platform.
 * DO NOT EVER RENUMBER
 */
#define AID_ROOT             0  /* traditional unix root user */
#define AID_SYSTEM        1000  /* system server */
#define AID_RADIO         1001  /* telephony subsystem, RIL */
#define AID_BLUETOOTH     1002  /* bluetooth subsystem */
#define AID_GRAPHICS      1003  /* graphics devices */
#define AID_INPUT         1004  /* input devices */
#define AID_AUDIO         1005  /* audio devices */
#define AID_CAMERA        1006  /* camera devices */
#define AID_LOG           1007  /* log devices */
#define AID_COMPASS       1008  /* compass device */
#define AID_MOUNT         1009  /* mountd socket */
#define AID_WIFI          1010  /* wifi subsystem */
#define AID_ADB           1011  /* android debug bridge (adbd) */
#define AID_INSTALL       1012  /* group for installing packages */
#define AID_MEDIA         1013  /* mediaserver process */
#define AID_DHCP          1014  /* dhcp client */
#define AID_SDCARD_RW     1015  /* external storage write access */
#define AID_VPN           1016  /* vpn system */
#define AID_KEYSTORE      1017  /* keystore subsystem */
#define AID_USB           1018  /* USB devices */
#define AID_DRM           1019  /* DRM server */
#define AID_MDNSR         1020  /* MulticastDNSResponder (service discovery) */
#define AID_GPS           1021  /* GPS daemon */
#define AID_UNUSED1       1022  /* deprecated, DO NOT USE */
#define AID_MEDIA_RW      1023  /* internal media storage write access */
#define AID_MTP           1024  /* MTP USB driver access */
#define AID_UNUSED2       1025  /* deprecated, DO NOT USE */
#define AID_DRMRPC        1026  /* group for drm rpc */
#define AID_NFC           1027  /* nfc subsystem */
#define AID_SDCARD_R      1028  /* external storage read access */
#define AID_CLAT          1029  /* clat part of nat464 */
#define AID_LOOP_RADIO    1030  /* loop radio devices */
#define AID_MEDIA_DRM     1031  /* MediaDrm plugins */
#define AID_PACKAGE_INFO  1032  /* access to installed package details */
#define AID_SDCARD_PICS   1033  /* external storage photos access */
#define AID_SDCARD_AV     1034  /* external storage audio/video access */
#define AID_SDCARD_ALL    1035  /* access all users external storage */
#define AID_LOGD          1036  /* log daemon */
#define AID_SHARED_RELRO  1037  /* creator of shared GNU RELRO files */
#define AID_SHELL         2000  /* adb and debug shell user */
#define AID_CACHE         2001  /* cache access */
#define AID_DIAG          2002  /* access to diagnostic resources */

/* The range 2900-2999 is reserved for OEM, and must never be
 * used here */
#define AID_OEM_RESERVED_START 2900
#define AID_OEM_RESERVED_END   2999

/* The 3000 series are intended for use as supplemental group id's only.
 * They indicate special Android capabilities that the kernel is aware of. */
#define AID_NET_BT_ADMIN  3001  /* bluetooth: create any socket */
#define AID_NET_BT        3002  /* bluetooth: create sco, rfcomm or l2cap sockets */
#define AID_INET          3003  /* can create AF_INET and AF_INET6 sockets */
#define AID_NET_RAW       3004  /* can create raw INET sockets */
#define AID_NET_ADMIN     3005  /* can configure interfaces and routing tables. */
#define AID_NET_BW_STATS  3006  /* read bandwidth statistics */
#define AID_NET_BW_ACCT   3007  /* change bandwidth statistics accounting */
#define AID_NET_BT_STACK  3008  /* bluetooth: access config files */
#define AID_EVERYBODY     9997  /* shared between all apps in the same profile */
#define AID_MISC          9998  /* access to misc storage */
#define AID_NOBODY        9999
#define AID_APP          10000  /* first app user */
#define AID_ISOLATED_START 99000 /* start of uids for fully isolated sandboxed processes */
#define AID_ISOLATED_END   99999 /* end of uids for fully isolated sandboxed processes */
#define AID_USER        100000  /* offset for uid ranges for each user */
#define AID_SHARED_GID_START 50000 /* start of gids for apps in each user to share */
#define AID_SHARED_GID_END   59999 /* start of gids for apps in each user to share */

static const struct android_id_info android_ids[] = {
    { "root",          AID_ROOT, },
    { "system",        AID_SYSTEM, },
    { "radio",         AID_RADIO, },
    { "bluetooth",     AID_BLUETOOTH, },
    { "graphics",      AID_GRAPHICS, },
    { "input",         AID_INPUT, },
    { "audio",         AID_AUDIO, },
    { "camera",        AID_CAMERA, },
    { "log",           AID_LOG, },
    { "compass",       AID_COMPASS, },
    { "mount",         AID_MOUNT, },
    { "wifi",          AID_WIFI, },
    { "adb",           AID_ADB, },
    { "install",       AID_INSTALL, },
    { "media",         AID_MEDIA, },
    { "dhcp",          AID_DHCP, },
    { "sdcard_rw",     AID_SDCARD_RW, },
    { "vpn",           AID_VPN, },
    { "keystore",      AID_KEYSTORE, },
    { "usb",           AID_USB, },
    { "drm",           AID_DRM, },
    { "mdnsr",         AID_MDNSR, },
    { "gps",           AID_GPS, },
    // AID_UNUSED1
    { "media_rw",      AID_MEDIA_RW, },
    { "mtp",           AID_MTP, },
    // AID_UNUSED2
    { "drmrpc",        AID_DRMRPC, },
    { "nfc",           AID_NFC, },
    { "sdcard_r",      AID_SDCARD_R, },
    { "clat",          AID_CLAT, },
    { "loop_radio",    AID_LOOP_RADIO, },
    { "mediadrm",      AID_MEDIA_DRM, },
    { "package_info",  AID_PACKAGE_INFO, },
    { "sdcard_pics",   AID_SDCARD_PICS, },
    { "sdcard_av",     AID_SDCARD_AV, },
    { "sdcard_all",    AID_SDCARD_ALL, },
    { "logd",          AID_LOGD, },
    { "shared_relro",  AID_SHARED_RELRO, },
    { "shell",         AID_SHELL, },
    { "cache",         AID_CACHE, },
    { "diag",          AID_DIAG, },
    { "net_bt_admin",  AID_NET_BT_ADMIN, },
    { "net_bt",        AID_NET_BT, },
    { "inet",          AID_INET, },
    { "net_raw",       AID_NET_RAW, },
    { "net_admin",     AID_NET_ADMIN, },
    { "net_bw_stats",  AID_NET_BW_STATS, },
    { "net_bw_acct",   AID_NET_BW_ACCT, },
    { "net_bt_stack",  AID_NET_BT_STACK, },
    { "everybody",     AID_EVERYBODY, },
    { "misc",          AID_MISC, },
    { "nobody",        AID_NOBODY, },
};
```










