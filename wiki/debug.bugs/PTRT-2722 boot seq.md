# PTRT-2722【大桌面：锁屏：重启后显示异常】重启手机后，先显示桌面再显示锁屏界面（FR：必现）

http://jira.blackshark.com/browse/PTRT-2722

## 结论

bootanimation 的问题，启动过程中 bootanimation crash

```
01-19 18:29:05.028  2048  2048 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-19 18:29:05.028  2048  2048 F DEBUG   : Build fingerprint: 'blackshark/PAR-A0/patriot:12/PTRT2111050CN00DPX/V12.0.1.0.RBICNBS:userdebug/test-keys'
01-19 18:29:05.028  2048  2048 F DEBUG   : Revision: '0'
01-19 18:29:05.028  2048  2048 F DEBUG   : ABI: 'arm64'
01-19 18:29:05.028  2048  2048 F DEBUG   : Timestamp: 1970-01-19 18:29:04.068410777+0800
01-19 18:29:05.028  2048  2048 F DEBUG   : Process uptime: 0s
01-19 18:29:05.028  2048  2048 F DEBUG   : Cmdline: /system/bin/bootanimation
01-19 18:29:05.028  2048  2048 F DEBUG   : pid: 1277, tid: 1443, name: BootAnimation  >>> /system/bin/bootanimation <<<
01-19 18:29:05.028  2048  2048 F DEBUG   : uid: 1000
01-19 18:29:05.028  2048  2048 F DEBUG   : signal 6 (SIGABRT), code -1 (SI_QUEUE), fault addr --------
01-19 18:29:05.028  2048  2048 F DEBUG   : Abort message: 'Pointer tag for 0x2900000001 was truncated, see 'https://source.android.com/devices/tech/debug/tagged-pointers'.'
01-19 18:29:05.028  2048  2048 F DEBUG   :     x0  0000000000000000  x1  00000000000005a3  x2  0000000000000006  x3  000000795295d550
01-19 18:29:05.028  2048  2048 F DEBUG   :     x4  8080808080808080  x5  8080808080808080  x6  8080808080808080  x7  8080808080808080
01-19 18:29:05.028  2048  2048 F DEBUG   :     x8  00000000000000f0  x9  c42491b4136412b2  x10 0000000000000000  x11 ffffff80ffffffdf
01-19 18:29:05.028  2048  2048 F DEBUG   :     x12 0000000000000001  x13 0000000000184e6f  x14 003482fe3c9cd000  x15 0000000000000048
01-19 18:29:05.028  2048  2048 F DEBUG   :     x16 00000079dc377d30  x17 00000079dc3516a0  x18 000000794f526000  x19 00000000000004fd
01-19 18:29:05.028  2048  2048 F DEBUG   :     x20 00000000000005a3  x21 00000000ffffffff  x22 b400007950acc950  x23 00000000ffff3cb0
01-19 18:29:05.028  2048  2048 F DEBUG   :     x24 000000795295e000  x25 b400007950a64418  x26 0000000002faf080  x27 00000064cddeea29
01-19 18:29:05.028  2048  2048 F DEBUG   :     x28 00000064cddee863  x29 000000795295d5d0
01-19 18:29:05.029  2048  2048 F DEBUG   :     lr  00000079dc3019fc  sp  000000795295d530  pc  00000079dc301a28  pst 0000000000001000
01-19 18:29:05.029  2048  2048 F DEBUG   : backtrace:
01-19 18:29:05.029  2048  2048 F DEBUG   :       #00 pc 000000000008aa28  /apex/com.android.runtime/lib64/bionic/libc.so (abort+168) (BuildId: d518382d7a1a085da68f588917bb7fe5)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #01 pc 0000000000047c4c  /apex/com.android.runtime/lib64/bionic/libc.so (free+108) (BuildId: d518382d7a1a085da68f588917bb7fe5)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #02 pc 000000000000e440  /system/lib64/libutils.so (android::FileMap::~FileMap()+28) (BuildId: 16796d84bdcf185b2112267dbd820c19)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #03 pc 000000000000a3e0  /system/bin/bootanimation (android::BootAnimation::initTexture(android::FileMap*, int*, int*)+80) (BuildId: fd8e862214104f8cc4242df07c6a635e)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #04 pc 000000000000c070  /system/bin/bootanimation (android::BootAnimation::movie()+3428) (BuildId: fd8e862214104f8cc4242df07c6a635e)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #05 pc 000000000000aec4  /system/bin/bootanimation (android::BootAnimation::threadLoop()+152) (BuildId: fd8e862214104f8cc4242df07c6a635e)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #06 pc 000000000001358c  /system/lib64/libutils.so (android::Thread::_threadLoop(void*)+264) (BuildId: 16796d84bdcf185b2112267dbd820c19)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #07 pc 0000000000012de8  /system/lib64/libutils.so (thread_data_t::trampoline(thread_data_t const*)+408) (BuildId: 16796d84bdcf185b2112267dbd820c19)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #08 pc 00000000000efb64  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+264) (BuildId: d518382d7a1a085da68f588917bb7fe5)
01-19 18:29:05.029  2048  2048 F DEBUG   :       #09 pc 000000000008c35c  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: d518382d7a1a085da68f588917bb7fe5)
01-19 18:29:05.048  1834  1919 E RILQ    : (0/1834): RIL[0][(1834,1919)] get_ecc_property_name: ecc list name : ril.ecclist.
01-19 18:29:05.049  1869  2109 E RILQ    : (1/1869): RIL[1][(1869,2109)] qcril_data_get_dds_sub_info: DSD Client unavailable
```

因为开机动画过早退出，导致后台变化呈现到前台。当第二段动画只有一帧时，不会crash，附件动画替换开机动画后该问题可以pass。

## 调试点

### HOME启动，ImageWallpaper，bootanim，StatusBar在启动过程中的位置

````java
android.intent.category.HOME|ImageWallpaper|starting phase|bootanim|StatusBar
````

Failed Log

````logcat
01-19 11:44:02.912  1285  1285 I auditd  : type=1400 audit(0.0:170): avc: denied { read } for comm="BootAnimation" name="settings_global.xml" dev="dm-5" ino=14059 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 04:26:26.928  1341  1937 I am_proc_start: [0,2774,10147,com.miui.miwallpaper,service,{com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper}]
10-27 04:26:37.282  1207  1879 I sf_stop_bootanim: 49211
10-27 04:27:36.391  1341  3698 I am_kill : [0,3873,com.miui.aod,100,depends on provider com.android.systemui/.statusbar.notification.NotificationProvider in dying proc com.android.systemui (adj -10000)]
10-27 04:34:02.969  1341  2595 I input_interaction: Interaction with: 3247aff com.miui.home/com.miui.home.launcher.Launcher (server), 893b089 com.miui.miwallpaper.wallpaperservice.ImageWallpaper (server), PointerEventDispatcher0 (server), 
10-27 05:22:18.499 13434 13434 I auditd  : type=1400 audit(0.0:776): avc: denied { read } for comm="BootAnimation" name="settings_global.xml" dev="dm-5" ino=15989 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 05:22:37.472 13867 13913 I am_proc_start: [0,14180,10147,com.miui.miwallpaper,service,{com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper}]
10-27 05:22:49.672 13350 13858 I sf_stop_bootanim: 1009238
10-27 05:26:42.981 21282 21282 I BootAnimation: bootanimation launching ...
10-27 05:26:47.587 21282 21282 I auditd  : type=1400 audit(0.0:1439): avc: denied { read } for comm="BootAnimation" name="settings_global.xml" dev="dm-5" ino=17540 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 05:26:47.587 21282 21282 W BootAnimation: type=1400 audit(0.0:1439): avc: denied { read } for name="settings_global.xml" dev="dm-5" ino=17540 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 05:26:47.591 21282 21383 E BootAnimation: couldn't find audio_conf.txt
10-27 05:26:47.592 21282 21383 V BootAnimation: settings_global.xml open error 13
10-27 05:26:47.599 21282 21383 D BootAnimation: Use save memory method, maybe small fps in actual.
10-27 05:26:49.269 21282 21383 D BootAnimation: Use save memory method, maybe small fps in actual.
10-27 05:26:50.275 21282 21383 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 21383 (BootAnimation), pid 21282 (bootanimation)
10-27 05:26:50.630 21450 21450 F DEBUG   : Cmdline: /system/bin/bootanimation
10-27 05:26:50.630 21450 21450 F DEBUG   : pid: 21282, tid: 21383, name: BootAnimation  >>> /system/bin/bootanimation <<<
10-27 05:26:50.632 21450 21450 F DEBUG   :       #03 pc 000000000000a3e0  /system/bin/bootanimation (android::BootAnimation::initTexture(android::FileMap*, int*, int*)+80) (BuildId: fd8e862214104f8cc4242df07c6a635e)
10-27 05:26:50.632 21450 21450 F DEBUG   :       #04 pc 000000000000c070  /system/bin/bootanimation (android::BootAnimation::movie()+3428) (BuildId: fd8e862214104f8cc4242df07c6a635e)
10-27 05:26:50.632 21450 21450 F DEBUG   :       #05 pc 000000000000aec4  /system/bin/bootanimation (android::BootAnimation::threadLoop()+152) (BuildId: fd8e862214104f8cc4242df07c6a635e)
10-27 05:26:51.727 21410 21410 I SystemServiceManager: Starting phase 100
10-27 05:26:57.250 21410 21410 I SystemServiceManager: Starting phase 200
10-27 05:26:58.266 21410 21410 I SystemServerTiming: StartStatusBarManagerService
10-27 05:26:58.269 21410 21410 D SystemServerTiming: StartStatusBarManagerService took to complete: 3ms
10-27 05:26:59.364 21410 21410 I SystemServiceManager: Starting phase 480
10-27 05:26:59.400 21410 21410 I SystemServiceManager: Starting phase 500
10-27 05:27:00.129 21410 21410 I SystemServiceManager: Starting phase 520
10-27 05:27:00.957 21410 21410 I SystemServiceManager: Starting phase 550
10-27 05:27:01.123 21410 21410 V WallpaperManagerService: bindWallpaperComponentLocked: componentName=ComponentInfo{com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper}
10-27 05:27:01.482 21410 21455 D Boost   : hostingType=service, hostingName={com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper}, callerPackage=null, isSystem=true, isBoostNeeded=false.
10-27 05:27:01.482 21410 21455 I am_proc_start: [0,21716,10147,com.miui.miwallpaper,service,{com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper}]
10-27 05:27:01.483 21410 21455 I ActivityManager: Start proc 21716:com.miui.miwallpaper/u0a147 for service {com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper} caller=null
10-27 05:27:03.685 21410 21410 I SystemServiceManager: Starting phase 600
10-27 05:27:03.846 21410 21410 V WallpaperManagerService: bindWallpaperComponentLocked: componentName=ComponentInfo{com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper}
10-27 05:27:04.416 21410 21410 I ActivityTaskManager: START u0 {act=android.intent.action.MAIN cat=[android.intent.category.HOME] flg=0x10000100 cmp=com.miui.home/.launcher.Launcher (has extras)} from uid 0
10-27 05:27:07.099 22146 22228 W RecentsModel: getRunningTask   taskInfo=TaskInfo{userId=0 taskId=2 displayId=0 isRunning=true baseIntent=Intent { act=android.intent.action.MAIN cat=[android.intent.category.HOME] flg=0x10800100 cmp=com.miui.home/.launcher.Launcher } baseActivity=ComponentInfo{com.miui.home/com.miui.home.launcher.Launcher} topActivity=ComponentInfo{com.miui.home/com.miui.home.launcher.Launcher} origActivity=null realActivity=ComponentInfo{com.miui.home/com.miui.home.launcher.Launcher} numActivities=1 lastActiveTime=3679026 supportsSplitScreenMultiWindow=true supportsMultiWindow=true resizeMode=2 isResizeable=true token=WCT{android.window.IWindowContainerToken$Stub$Proxy@f29e3db} topActivityType=2 pictureInPictureParams=PictureInPictureParams( aspectRatio=null sourceRectHint=null hasSetActions=false isAutoPipEnabled=false isSeamlessResizeEnabled=true) displayCutoutSafeInsets=Rect(0, 80 - 0, 0) topActivityInfo=ActivityInfo{ea4ee78 com.miui.home.launcher.Launcher} launchCookies...
10-27 05:27:07.100 22146 22228 D RecentsImpl: onResumed className=com.miui.home.launcher.Launcher,mIsInAnotherPro=false,mIsStatusBarExpansion=false,isKeyguardLocked=true,mNavStubView=com.miui.home.recents.NavStubView{f43f9c7 V.E...... ........ 0,0-1080,35}
10-27 05:27:07.720 22146 22146 D Recent.RecentsContainer:     statusBars=Insets{left=0, top=80, right=0, bottom=0} max=null vis=false
10-27 05:27:07.861 22146 22146 D Recent.RecentsContainer:     statusBars=Insets{left=0, top=80, right=0, bottom=0} max=null vis=false
10-27 05:27:07.880 22146 22146 D RecentsImpl: onResumed className=com.miui.home.launcher.Launcher,mIsInAnotherPro=false,mIsStatusBarExpansion=false,isKeyguardLocked=true,mNavStubView=com.miui.home.recents.NavStubView{f43f9c7 V.E...... ........ 0,0-1080,35}
10-27 05:27:09.497 21410 22278 I system_server: Connection::Connection : windowName (6660902 com.miui.miwallpaper.wallpaperservice.ImageWallpaper (server))
10-27 05:27:09.497 21410 22278 I system_server: Connection::Connection : windowName (6660902 com.miui.miwallpaper.wallpaperservice.ImageWallpaper (server)),isMonitorApp(0)
10-27 05:27:09.656 21410 21438 D bob_log_tag:  	_   title: com.miui.miwallpaper.wallpaperservice.ImageWallpaper
10-27 05:27:09.783 22121 22121 I service_manager_slow: [72,statusbar]
10-27 05:27:10.424 21410 21836 I ActivityManager:                        com.miui.miwallpaper/.wallpaperservice.ImageWallpaper<=Proc{21410:system/1000}
10-27 05:27:10.963 22121 22121 E SystemServiceRegistry: 	at com.android.systemui.statusbar.policy.MiuiBatteryControllerImpl.init(MiuiBatteryControllerImpl.java:127)
10-27 05:27:10.963 22121 22121 E SystemServiceRegistry: 	at com.android.systemui.statusbar.phone.DozeParameters_Factory.get(DozeParameters_Factory.java:63)
10-27 05:27:10.963 22121 22121 E SystemServiceRegistry: 	at com.android.systemui.statusbar.phone.DozeParameters_Factory.get(DozeParameters_Factory.java:15)
10-27 05:27:12.211 22146 22214 D StatusBarController: handleMessage: flag 800000  disable true
10-27 05:27:12.211 22146 22146 D Launcher_WallpaperUtils: changeStatusBarMode:false
10-27 05:27:12.388 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.policy.MiuiBatteryControllerImpl$1@bfe6e8f
10-27 05:27:12.398 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.policy.KeyguardStateControllerImpl$UpdateMonitorCallback@47d64ab
10-27 05:27:12.594 22121 22174 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:94)
10-27 05:27:12.594 22121 22174 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:20)
10-27 05:27:12.594 22121 22174 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationSettingsHelper.canShowBadge(NotificationSettingsHelper.java:375)
10-27 05:27:12.594 22121 22174 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationProvider.query(NotificationProvider.java:121)
10-27 05:27:12.595 22121 22489 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:94)
10-27 05:27:12.595 22121 22489 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:20)
10-27 05:27:12.595 22121 22489 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationSettingsHelper.canShowBadge(NotificationSettingsHelper.java:375)
10-27 05:27:12.595 22121 22489 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationProvider.query(NotificationProvider.java:121)
10-27 05:27:12.606 22121 22193 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:94)
10-27 05:27:12.606 22121 22193 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:20)
10-27 05:27:12.606 22121 22193 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationSettingsHelper.canShowBadge(NotificationSettingsHelper.java:375)
10-27 05:27:12.606 22121 22193 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationProvider.query(NotificationProvider.java:121)
10-27 05:27:12.651 22121 22170 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:94)
10-27 05:27:12.651 22121 22170 E DatabaseUtils: 	at com.android.systemui.statusbar.policy.UserSwitcherController_Factory.get(UserSwitcherController_Factory.java:20)
10-27 05:27:12.651 22121 22170 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationSettingsHelper.canShowBadge(NotificationSettingsHelper.java:375)
10-27 05:27:12.651 22121 22170 E DatabaseUtils: 	at com.android.systemui.statusbar.notification.NotificationProvider.query(NotificationProvider.java:121)
10-27 05:27:12.676 22146 22230 D Launcher.Wallpaper: wallpaperInfo:DesktopWallpaperInfo{mColorMode=0, mStatusBarColorMode=0, mSearchBarColorMode=2, mScrollable=false}
10-27 05:27:12.684 22146 22146 D Launcher_WallpaperUtils: changeStatusBarMode:false
10-27 05:27:12.887 22121 22121 D KeyguardViewMediator: adjustStatusBarLocked: mShowing=true mOccluded=false isSecure=false force=false --> flags=0x1600000
10-27 05:27:12.960 22146 22214 D StatusBarController: handleMessage: flag 800000  disable false
10-27 05:27:13.003 22146 22146 D Launcher_WallpaperUtils: changeStatusBarMode:false
10-27 05:27:13.261 21239 22266 I sf_stop_bootanim: 1272827
10-27 05:27:13.300 21410 21437 I SystemServiceManager: Starting phase 1000
10-27 05:27:13.586 22121 22121 W ContextImpl: Calling a method in the system process without a qualified user: android.app.ContextImpl.bindService:1905 android.content.ContextWrapper.bindService:820 com.android.wifitrackerlib.WifiPasspointProvision.bindPasspointKeyService:297 com.android.wifitrackerlib.WifiPickerTracker.<init>:170 com.android.systemui.statusbar.policy.AccessPointControllerImpl$WifiPickerTrackerFactory.create:319 
10-27 05:27:13.907 22121 22518 W ContextImpl: Calling a method in the system process without a qualified user: android.app.ContextImpl.bindService:1905 android.content.ContextWrapper.bindService:820 com.qti.extphone.ExtTelephonyManager.connectService:131 com.android.systemui.statusbar.policy.MiuiFiveGServiceClient.connectService:275 com.android.systemui.statusbar.policy.MiuiFiveGServiceClient.access$1300:47 
10-27 05:27:13.914 22121 22121 V WifiManager: registerTrafficStateCallback: callback=com.android.systemui.statusbar.policy.MiuiWifiSignalController$WifiTrafficStateCallback@cf32802, executor=com.android.systemui.util.concurrency.ExecutorImpl@325c6e9
10-27 05:27:13.922 22121 22121 V WifiManager: registerScanResultsCallback: callback=com.android.systemui.statusbar.policy.NetworkControllerImpl$5@d44d513, executor=androidx.mediarouter.media.MediaRoute2Provider$$ExternalSyntheticLambda0@eecb350
10-27 05:27:13.946 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.BiometricUnlockController@7a3b6b9
10-27 05:27:14.174 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.KeyguardIndicationController$MiuiBaseKeyguardCallback@a780fe6
10-27 05:27:14.175 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.KeyguardIndicationController$4@bdb0927
10-27 05:27:14.206 22121 22121 D StatusBar: disable<e i a s b h r c s > disable2<q i n >
10-27 05:27:14.207 21410 22232 I StatusBarManagerService: registerStatusBar bar=com.android.internal.statusbar.IStatusBar$Stub$Proxy@12f40cb
10-27 05:27:14.300 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.policy.MiuiCarrierTextController$2@1028a17
10-27 05:27:14.458 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.KeyguardBottomAreaView$10@61c6b1e
10-27 05:27:15.536 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.MiuiNotificationPanelViewController$mKeyguardUpdateMonitorCallback$1@cbdb947
10-27 05:27:15.571 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.ScrimController$KeyguardVisibilityCallback@ddf8b5b
10-27 05:27:15.618 22121 22121 D StatusBar: mUserSetupObserver - DeviceProvisionedListener called for user 0
10-27 05:27:15.618 22121 22121 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: true
10-27 05:27:15.619 22121 22121 D StatusBar: mUserSetupObserver - DeviceProvisionedListener called for user 0
10-27 05:27:15.659 22121 22121 W ContextImpl: Calling a method in the system process without a qualified user: android.app.ContextImpl.startService:1826 android.content.ContextWrapper.startService:784 com.blackshark.gamedock.GameDockManager.initGameDock:215 com.android.systemui.statusbar.phone.StatusBar.makeStatusBarView:1441 com.android.systemui.statusbar.phone.StatusBar.createAndAddWindows:2938 
10-27 05:27:15.751 21410 21889 I system_server: Connection::Connection : windowName (7f31a65 StatusBar (server))
10-27 05:27:15.752 21410 21889 I system_server: Connection::Connection : windowName (7f31a65 StatusBar (server)),isMonitorApp(0)
10-27 05:27:15.796 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.notification.collection.coordinator.KeyguardCoordinator$6@7c7f634
10-27 05:27:15.833 22121 22121 D MiuiPhoneStatusBarPolicy: updateBluetooth: action = null
10-27 05:27:15.833 22121 22121 D MiuiPhoneStatusBarPolicy: hide bluetooth battery
10-27 05:27:15.833 22121 22121 D MiuiPhoneStatusBarPolicy: updateBluetooth: BluetoothFlowState = 0
10-27 05:27:15.834 22121 22121 D MiuiPhoneStatusBarPolicy: updateZenAndRinger: zenVisible = false ringerVisible = false
10-27 05:27:15.842 22121 22121 V WifiManager: registerSoftApCallback: callback=com.android.systemui.statusbar.policy.HotspotControllerImpl@56f5464, executor=android.os.HandlerExecutor@57596cd
10-27 05:27:15.844 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.KeyguardBouncer$1@691db82
10-27 05:27:15.845 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.KeyguardBouncer$2@5884293
10-27 05:27:15.845 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.StatusBarKeyguardViewManager$3@fff52d0
10-27 05:27:15.845 22121 22121 D KeyguardViewMediator: adjustStatusBarLocked: mShowing=true mOccluded=false isSecure=false force=false --> flags=0x1600000
10-27 05:27:15.846 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.StatusBar$5@7d1d2c9
10-27 05:27:15.853 22121 22121 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: true
10-27 05:27:15.853 22121 22121 D SystemUIBootTiming: StartServicescom.android.systemui.statusbar.phone.StatusBar took to complete: 2591ms
10-27 05:27:15.853 22121 22121 W SystemUIService: Initialization of com.android.systemui.statusbar.phone.StatusBar took 2591 ms
10-27 05:27:15.876 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.policy.MiuiHeadsUpPolicy$mKeyguardUpdateMonitorCallback$1@92bac8a
10-27 05:27:15.937 22121 22121 D SystemUIBootTiming: StartServicescom.android.systemui.statusbar.notification.InstantAppNotifier took to complete: 1ms
10-27 05:27:15.978 22121 22121 D StatusBar: disable<e i a s B!H!R!c s > disable2<q i n >
10-27 05:27:16.116 22121 22609 D KeyguardViewMediator: adjustStatusBarLocked: mShowing=true mOccluded=false isSecure=false force=false --> flags=0x1600000
10-27 05:27:16.617 22778 22930 I DC:AlarmHelper: setStatusBarIcon: false
10-27 05:27:16.783 22121 22121 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: true
10-27 05:27:16.795 22778 22930 I DC:AlarmHelper: setStatusBarIcon: false
10-27 05:27:16.988 22121 22121 I DepthController: Won't set zoom. Window not attached com.android.systemui.statusbar.phone.NotificationShadeWindowView{8063ff8 V.E...... ......I. 0,0-0,0}
10-27 05:27:16.997 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.KeyguardBottomAreaView$10@9551402
10-27 05:27:17.089 22121 22121 D MiuiKeyguardStatusBarView: updateIconsAndTextColors: dark = false, iconColor = -419430401, intensity = 0.0
10-27 05:27:17.090 22121 22121 D PanelView: setKeyguardBottomAreaVisibility statusBarState=0 goingToFullShade=false
10-27 05:27:17.090 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.NotificationPanelViewController$1@8a85c80
10-27 05:27:17.098 22121 22121 D MiuiKeyguardStatusBarView: updateIconsAndTextColors: dark = false, iconColor = -419430401, intensity = 0.0
10-27 05:27:17.191 22146 22146 W RecentsImpl: updateFsgWindowVisibilityState   isEnter=true   typeFrom=typefrom_keyguard   isOpen=true   mIsInAnotherPro=false   mIsStatusBarExpansion=false
10-27 05:27:17.192 22146 22146 W RecentsImpl: updateFsgWindowVisibilityState   isEnter=true   typeFrom=typefrom_keyguard   isOpen=true   mIsInAnotherPro=false   mIsStatusBarExpansion=false
10-27 05:27:17.414 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.phone.KeyguardBottomAreaView$10@9551402
10-27 05:27:17.415 22121 22121 E KeyguardUpdateMonitor: 	at com.android.systemui.statusbar.phone.KeyguardBottomAreaView.onAttachedToWindow(KeyguardBottomAreaView.java:457)
10-27 05:27:17.488 22121 22121 D MiuiKeyguardStatusBarView: updateIconsAndTextColors: dark = false, iconColor = -419430401, intensity = 0.0
10-27 05:27:17.491 22121 22121 D MiuiKeyguardStatusBarView: onChange: mShowCarrier = true
10-27 05:27:17.491 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.views.MiuiBatteryMeterView$1@6d72bff
10-27 05:27:17.529 22778 22778 I DC:AlarmHelper: setStatusBarIcon: false
10-27 05:27:17.646 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.views.MiuiBatteryMeterView$1@88e3e74
10-27 05:27:17.905 22121 22121 W ChoreographerMonitor: PerfMonitor choreDoFrame : time=920ms vsyncFrame=0 (title=animation action=android.animation.AnimationHandler$1 latency=1415ms) (title=animation action=com.android.systemui.statusbar.NotificationShadeDepthController$updateBlurCallback$1 latency=1414ms) (title=traversal action=android.view.ViewRootImpl$TraversalRunnable latency=1280ms) (title=traversal action=android.view.ViewRootImpl$TraversalRunnable latency=1842ms) (title=traversal action=android.view.ViewRootImpl$TraversalRunnable latency=1599ms) (title=traversal action=android.view.ViewRootImpl$TraversalRunnable latency=1063ms)
10-27 05:27:17.913 21410 21438 D bob_log_tag:  	_   title: StatusBar
10-27 05:27:17.924 21410 21438 D bob_log_tag:  	_   title: com.miui.miwallpaper.wallpaperservice.ImageWallpaper
10-27 05:27:17.925 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217728 miFodLayer 0x8000000
10-27 05:27:17.936 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:18.468 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.views.MiuiBatteryMeterView$1@c8a2f15
10-27 05:27:18.834 22121 22121 D MiuiPhoneStatusBarPolicy: updateBluetooth: action = null
10-27 05:27:18.834 22121 22121 D MiuiPhoneStatusBarPolicy: hide bluetooth battery
10-27 05:27:18.834 22121 22121 D MiuiPhoneStatusBarPolicy: updateBluetooth: BluetoothFlowState = 0
10-27 05:27:19.142 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.156 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.165 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.333 22121 22121 V ShadeControllerImpl: NotificationShadeWindow: com.android.systemui.statusbar.phone.NotificationShadeWindowView{8063ff8 V.E...... ......ID 0,0-1080,2400} canPanelBeCollapsed(): false
10-27 05:27:19.346 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.354 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.425 22121 22121 D KeyguardViewMediator: adjustStatusBarLocked: mShowing=true mOccluded=false isSecure=false force=false --> flags=0x1600000
10-27 05:27:19.491 22121 22121 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: false
10-27 05:27:19.493 22121 22121 D StatusBar: has Active Notifications is : false
10-27 05:27:19.494 22121 22121 D StatusBar: disable<e i a s B H R c s > disable2<q i n >
10-27 05:27:19.536 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.544 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.631 22121 22121 V KeyguardUpdateMonitor: *** register callback for com.android.systemui.statusbar.views.MiuiBatteryMeterView$1@4464369
10-27 05:27:19.643 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.677 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.710 21239 21239 D CompositionEngine: writeOutputDependentGeometryStateToHWC layer[StatusBar#0] set Z 134217729 miFodLayer 0x8000000
10-27 05:27:19.725 22121 22121 D MiuiKeyguardStatusBarView: updateIconsAndTextColors: dark = false, iconColor = -419430401, intensity = 0.0
10-27 05:27:19.836 22121 22121 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: false
10-27 05:27:19.839 22121 22121 D PanelView: setKeyguardBottomAreaVisibility statusBarState=1 goingToFullShade=false
10-27 05:27:19.845 22121 22121 D StatusBar: disable<e i a s B H R c s > disable2<q i n >
10-27 05:27:19.846 22121 22121 D StatusBar: disable<e i a s B H R c s > disable2<q i n >
10-27 05:27:19.868 22121 22121 D KeyguardViewMediator: adjustStatusBarLocked: mShowing=true mOccluded=false isSecure=false force=false --> flags=0x1600000
10-27 05:27:19.987 22121 22121 D KeyguardViewMediator: adjustStatusBarLocked: mShowing=true mOccluded=false isSecure=false force=false --> flags=0x1600000
10-27 05:27:20.222 22146 22146 W RecentsImpl: updateFsgWindowVisibilityState   isEnter=true   typeFrom=typefrom_keyguard   isOpen=true   mIsInAnotherPro=false   mIsStatusBarExpansion=false
10-27 05:27:20.332 22121 22121 W Looper  : PerfMonitor doFrame : time=111ms vsyncFrame=0 latency=632ms procState=-1 historyMsgCount=127 (msgIndex=1 wall=138ms seq=199 running=60ms runnable=6ms binder=70ms late=2600ms h=android.view.Choreographer$FrameHandler c=android.view.Choreographer$FrameDisplayEventReceiver) (msgIndex=83 wall=86ms seq=281 running=52ms runnable=2ms binder=36ms late=932ms h=android.os.Handler c=com.android.systemui.statusbar.NotificationListener$$ExternalSyntheticLambda4) (msgIndex=109 wall=176ms seq=307 running=40ms runnable=14ms binder=139ms late=404ms h=com.android.systemui.keyguard.KeyguardViewMediator$6 w=1) (msgIndex=115 wall=155ms seq=313 running=1ms runnable=1ms binder=155ms late=516ms h=android.os.Handler c=com.android.keyguard.MiuiDozeServiceHost$$ExternalSyntheticLambda2) (msgIndex=119 wall=55ms seq=317 running=6ms binder=51ms late=667ms h=com.android.keyguard.KeyguardUpdateMonitor$15 w=322)
10-27 05:27:20.351 22121 22121 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: false
10-27 05:27:20.365 22121 22121 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: false
````

AOSP Log

````logcat
09-27 07:14:38.973   939  1029 I am_proc_start: [0,1386,10085,com.android.systemui,service,{com.android.systemui/com.android.systemui.ImageWallpaper}]
09-27 07:14:42.453   520   535 I sf_stop_bootanim: 33181
09-30 06:03:05.562     1     1 I init    : Received control message 'start' for 'bootanim' from pid: 24244 (/system/bin/surfaceflinger)
09-30 06:03:05.573     1     1 I init    : starting service 'bootanim'...
09-30 06:03:10.314 24288 24320 I am_proc_start: [0,24435,10085,com.android.systemui,service,{com.android.systemui/com.android.systemui.ImageWallpaper}]
09-30 06:03:13.577     1     1 I init    : Service 'bootanim' (pid 24282) exited with status 0
09-30 06:03:13.726 24244 24379 I sf_stop_bootanim: 243535463
09-30 06:19:44.218   488   488 I ServiceManager: service 'statusbar' died
09-30 06:19:45.569     1     1 I init    : Received control message 'start' for 'bootanim' from pid: 26191 (/system/bin/surfaceflinger)
09-30 06:19:45.569     1     1 I init    : starting service 'bootanim'...
09-30 06:19:45.757 26229 26229 D BootAnimation: BootAnimationStartTiming start time: 255936485ms
09-30 06:19:45.757 26229 26229 D BootAnimation: BootAnimationPreloadTiming start time: 255936485ms
09-30 06:19:45.758 26229 26229 D BootAnimation: BootAnimationPreloadStopTiming start time: 255936485ms
09-30 06:19:45.817 26229 26231 D BootAnimation: BootAnimationShownTiming start time: 255936545ms
09-30 06:19:46.964 26234 26234 I SystemServiceManager: Starting phase 100
09-30 06:19:48.313 26234 26234 I SystemServer: StartStatusBarManagerService
09-30 06:19:48.314 26234 26234 D SystemServerTiming: StartStatusBarManagerService took to complete: 1ms
09-30 06:19:48.827 26234 26234 I SystemServiceManager: Starting phase 480
09-30 06:19:48.833 26234 26234 I SystemServiceManager: Starting phase 500
09-30 06:19:48.999 26234 26234 I SystemServiceManager: Starting phase 520
09-30 06:19:49.022 26234 26234 I SystemServiceManager: Starting phase 550
09-30 06:19:49.065 26234 26234 V WallpaperManagerService: bindWallpaperComponentLocked: componentName=ComponentInfo{com.android.systemui/com.android.systemui.ImageWallpaper}
09-30 06:19:49.103 26234 26263 I am_proc_start: [0,26392,10085,com.android.systemui,service,{com.android.systemui/com.android.systemui.ImageWallpaper}]
09-30 06:19:49.103 26234 26263 I ActivityManager: Start proc 26392:com.android.systemui/u0a85 for service {com.android.systemui/com.android.systemui.ImageWallpaper}
09-30 06:19:49.221 26234 26234 I SystemServiceManager: Starting phase 600
09-30 06:19:49.235 26234 26234 V WallpaperManagerService: bindWallpaperComponentLocked: componentName=ComponentInfo{com.android.systemui/com.android.systemui.ImageWallpaper}
09-30 06:19:49.479 26234 26234 I ActivityTaskManager: START u0 {act=android.intent.action.MAIN cat=[android.intent.category.HOME] flg=0x10000100 cmp=com.android.settings/.FallbackHome} from uid 0
09-30 06:19:49.687 26392 26392 D SystemUIBootTiming: StartServicescom.android.systemui.statusbar.CommandQueue$CommandQueueStart took to complete: 0ms
09-30 06:19:50.135 26234 26497 I ActivityManager:   ntv   ??   33566: bootanimation (   17,772K memtrack) (pid 26229) native
09-30 06:19:50.420 26392 26392 V WifiManager: registerTrafficStateCallback: callback=com.android.systemui.statusbar.policy.WifiSignalController$WifiTrafficStateCallback@8d8a02e, handler=null
09-30 06:19:50.523 26392 26392 D StatusBar: disable<e i a s b h r c s > disable2<q i n >
09-30 06:19:50.529 26234 26352 I StatusBarManagerService: registerStatusBar bar=com.android.internal.statusbar.IStatusBar$Stub$Proxy@e3ab4f7
09-30 06:19:50.818 26392 26392 D StatusBar: mUserSetupObserver - DeviceProvisionedListener called for user 0
09-30 06:19:50.821 26392 26392 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: true
09-30 06:19:50.821 26392 26392 D StatusBar: mUserSetupObserver - DeviceProvisionedListener called for user 0
09-30 06:19:50.907 26392 26392 V WifiManager: registerSoftApCallback: callback=com.android.systemui.statusbar.policy.HotspotControllerImpl@10ff9d2, handler=Handler (android.os.Handler) {c578aa3}
09-30 06:19:50.918 26392 26608 I SecurityController: 	at com.android.systemui.statusbar.policy.SecurityControllerImpl$CACertLoader.doInBackground(SecurityControllerImpl.java:415)
09-30 06:19:50.918 26392 26608 I SecurityController: 	at com.android.systemui.statusbar.policy.SecurityControllerImpl$CACertLoader.doInBackground(SecurityControllerImpl.java:411)
09-30 06:19:50.994 26392 26392 D SystemUIBootTiming: StartServicescom.android.systemui.statusbar.notification.InstantAppNotifier took to complete: 8ms
09-30 06:19:51.016 26392 26392 D StatusBar: disable<e i a s b h r c s > disable2<q i n >
09-30 06:19:51.543 26392 26392 D StatusBar: disable<e i a s b h r c s > disable2<q i n >
09-30 06:19:51.565 26234 26257 D bob_log_tag:  	_   title: StatusBar  [WindowSurfaceController@showSurface(:450)  null(26234:android.anim)]
09-30 06:19:52.020 26392 26392 V StatusBar: mStatusBarWindow: com.android.systemui.statusbar.phone.StatusBarWindowView{c81b598 V.E...... ......ID 0,0-1080,63} canPanelBeCollapsed(): false
09-30 06:19:52.110 26392 26392 D StatusBar: disable<e i a s b H!R!c s > disable2<q i n >
09-30 06:19:52.266 26392 26392 D StatusBar: updateQsExpansionEnabled - QS Expand enabled: true
09-30 06:19:52.273 26392 26392 D StatusBar: disable<e i a s b H R c s > disable2<q i n >
09-30 06:19:52.275 26392 26392 D StatusBar: disable<e i a s b H R c s > disable2<q i n >
09-30 06:19:52.275 26392 26392 D StatusBar: disable<e i a s b H R c s > disable2<q i n >
09-30 06:19:52.310 26392 26392 D StatusBar: disable<e i a s b H R c s > disable2<q i n >
09-30 06:19:52.318 26392 26392 D StatusBar: disable<e i a s b H R c s > disable2<q i n >
09-30 06:19:52.383 26392 26392 D StatusBar: disable<e i a s b H R c s > disable2<q i n >
09-30 06:19:52.443 26234 26257 D bob_log_tag:  	_   title: com.android.systemui.ImageWallpaper  [WindowSurfaceController@showSurface(:450)  null(26234:android.anim)]
09-30 06:19:52.457 26229 26229 D BootAnimation: BootAnimationStopTiming start time: 255943184ms
09-30 06:19:52.427     1     1 I init    : Service 'bootanim' (pid 26229) exited with status 0
09-30 06:19:52.657 26191 26325 I sf_stop_bootanim: 244147359
09-30 06:19:52.661 26234 26256 I SystemServiceManager: Starting phase 1000
09-30 06:19:53.590 26234 26352 I ActivityTaskManager: START u0 {act=android.intent.action.MAIN cat=[android.intent.category.HOME] flg=0x10000100 cmp=com.android.launcher3/.Launcher} from uid 0
````

### 启动过程中的进程启动

````
ActivityManager: Start proc|starting phase
````

Failed Log

````logcat
10-27 05:26:51.727 21410 21410 I SystemServiceManager: Starting phase 100
10-27 05:26:57.250 21410 21410 I SystemServiceManager: Starting phase 200
10-27 05:26:59.364 21410 21410 I SystemServiceManager: Starting phase 480
10-27 05:26:59.400 21410 21410 I SystemServiceManager: Starting phase 500
10-27 05:27:00.129 21410 21410 I SystemServiceManager: Starting phase 520
10-27 05:27:00.957 21410 21410 I SystemServiceManager: Starting phase 550
10-27 05:27:01.119 21410 21455 I ActivityManager: Start proc 21688:com.android.bluetooth/1002 for service {com.android.bluetooth/com.android.bluetooth.btservice.AdapterService} caller=null
10-27 05:27:01.483 21410 21455 I ActivityManager: Start proc 21716:com.miui.miwallpaper/u0a147 for service {com.miui.miwallpaper/com.miui.miwallpaper.wallpaperservice.ImageWallpaper} caller=null
10-27 05:27:02.035 21410 21455 I ActivityManager: Start proc 21753:WebViewLoader-armeabi-v7a/1037 [android.webkit.WebViewLibraryLoader$RelroFileCreator] for null caller=null
10-27 05:27:02.091 21410 21455 I ActivityManager: Start proc 21755:WebViewLoader-arm64-v8a/1037 [android.webkit.WebViewLibraryLoader$RelroFileCreator] for null caller=null
10-27 05:27:03.685 21410 21410 I SystemServiceManager: Starting phase 600
10-27 05:27:04.521 21410 21455 I ActivityManager: Start proc 21894:com.smartpolicy.core/1000 for added application com.smartpolicy.core caller=null
10-27 05:27:04.600 21410 21455 I ActivityManager: Start proc 21916:com.blackshark.HydraAlpha/1000 for added application com.blackshark.HydraAlpha caller=null
10-27 05:27:04.667 21410 21455 I ActivityManager: Start proc 21932:.qtidataservices/u0a152 for added application .qtidataservices caller=null
10-27 05:27:04.768 21410 21455 I ActivityManager: Start proc 21934:com.qti.phone/u0a178 for added application com.qti.phone caller=null
10-27 05:27:04.860 21410 21455 I ActivityManager: Start proc 21967:com.blackshark.exlight/1000 for added application com.blackshark.exlight caller=null
10-27 05:27:05.000 21410 21455 I ActivityManager: Start proc 21984:vendor.qti.qesdk.sysservice/1000 for added application vendor.qti.qesdk.sysservice caller=null
10-27 05:27:05.067 21410 21455 I ActivityManager: Start proc 21988:org.codeaurora.ims/u0a188 for added application org.codeaurora.ims caller=null
10-27 05:27:05.167 21410 21455 I ActivityManager: Start proc 22004:com.android.se/1068 for added application com.android.se caller=null
10-27 05:27:05.341 21410 21455 I ActivityManager: Start proc 22021:com.xiaomi.finddevice/6110 for added application com.xiaomi.finddevice caller=null
10-27 05:27:05.395 21410 21455 I ActivityManager: Start proc 22049:com.qualcomm.qti.devicestatisticsservice/u0a175 for added application com.qualcomm.qti.devicestatisticsservice caller=null
10-27 05:27:05.524 21410 21455 I ActivityManager: Start proc 22069:com.zeusis.HydraService/1000 for added application com.zeusis.HydraService caller=null
10-27 05:27:05.625 21410 21455 I ActivityManager: Start proc 22082:.qtidataservices/u0a159 for added application .qtidataservices caller=null
10-27 05:27:05.767 21410 21455 I ActivityManager: Start proc 22102:com.android.phone/1001 for added application com.android.phone caller=null
10-27 05:27:05.921 21410 21455 I ActivityManager: Start proc 22121:com.android.systemui/1000 for added application com.android.systemui caller=null
10-27 05:27:06.027 21410 21455 I ActivityManager: Start proc 22125:.dataservices/1001 for added application .dataservices caller=null
10-27 05:27:06.104 21410 21455 I ActivityManager: Start proc 22146:com.miui.home/u0a63 for top-activity {com.miui.home/com.miui.home.launcher.Launcher} caller=null
10-27 05:27:06.485 21410 22184 I ActivityManager: Start proc 22175:com.android.settings:remote/1000 for content provider {com.android.settings/com.android.settings.cloud.CloudSettingsProvider} caller=null
10-27 05:27:06.752 21410 21455 I ActivityManager: Start proc 22202:android.ext.services/u0a211 for service {android.ext.services/android.ext.services.autofill.InlineSuggestionRenderServiceImpl} caller=null
10-27 05:27:08.339 21410 21455 I ActivityManager: Start proc 22342:com.miui.weather2/u0a234 for content provider {com.miui.weather2/com.miui.weather2.providers.WeatherProvider} caller=null
10-27 05:27:09.278 21410 21455 I ActivityManager: Start proc 22385:com.xiaomi.finddevice:normal/6110 for service {com.xiaomi.finddevice/com.xiaomi.finddevice.v2.ui.FindDeviceNotificationReceiver} caller=null
10-27 05:27:11.485 21410 21455 I ActivityManager: Start proc 22550:com.android.smspush/u0a199 for service {com.android.smspush/com.android.smspush.WapPushManager} caller=null
10-27 05:27:13.283 21410 21455 I ActivityManager: Start proc 22654:.qtidataservices/u0a158 for service {vendor.qti.iwlan/vendor.qti.iwlan.QualifiedNetworksServiceImpl} caller=null
10-27 05:27:13.300 21410 21437 I SystemServiceManager: Starting phase 1000
10-27 05:27:13.786 21410 21455 I ActivityManager: Start proc 22690:com.android.settings/1000 for broadcast {com.android.settings/com.android.settings.connecteddevice.usb.UsbModeChooserReceiver} caller=null
10-27 05:27:15.126 21410 21455 I ActivityManager: Start proc 22754:com.miui.securitycore.remote/1000 for service {com.miui.securitycore/com.miui.xspace.service.XSpaceService} caller=null
10-27 05:27:15.258 21410 21455 I ActivityManager: Start proc 22778:com.android.deskclock/u0a119 for broadcast {com.android.deskclock/com.android.deskclock.AlarmInitReceiver} caller=null
10-27 05:27:16.274 21410 21455 I ActivityManager: Start proc 22900:com.miui.securitycenter.remote/1000 for content provider {com.miui.securitycenter/com.miui.networkassistant.provider.NetworkAssistantProvider} caller=null
10-27 05:27:16.560 21410 21455 I ActivityManager: Start proc 22935:com.miui.voiceassist/u0a100 for service {com.miui.voiceassist/com.xiaomi.voiceassistant.AssistInteractionService} caller=null
10-27 05:27:16.929 21410 21455 I ActivityManager: Start proc 22961:com.blackshark.ota/1000 for added application com.blackshark.ota caller=null
10-27 05:27:17.120 21410 21455 I ActivityManager: Start proc 22983:com.blackshark.push:push/u0a53 for added application com.blackshark.push:push caller=null
10-27 05:27:17.343 21410 21455 I ActivityManager: Start proc 23003:com.miui.contentcatcher/1000 for added application com.miui.contentcatcher caller=null
10-27 05:27:17.515 21410 21455 I ActivityManager: Start proc 23023:com.blackshark.search/u0a66 for added application com.blackshark.search caller=null
10-27 05:27:17.755 21410 21455 I ActivityManager: Start proc 23033:com.blackshark.msgtransfer/1000 for added application com.blackshark.msgtransfer caller=null
10-27 05:27:17.824 21410 21455 I ActivityManager: Start proc 23064:com.blackshark.performancemaster/1000 for added application com.blackshark.performancemaster caller=null
10-27 05:27:18.100 21410 21455 I ActivityManager: Start proc 23073:com.miui.daemon/1000 for added application com.miui.daemon caller=null
10-27 05:27:18.258 21410 21455 I ActivityManager: Start proc 23104:com.android.nfc/1027 for added application com.android.nfc caller=null
10-27 05:27:18.327 21410 21455 I ActivityManager: Start proc 23115:com.blackshark.gameevaluate/1000 for added application com.blackshark.gameevaluate caller=null
10-27 05:27:18.507 21410 21455 I ActivityManager: Start proc 23138:com.blackshark.gamewindowservice/1000 for added application com.blackshark.gamewindowservice caller=null
10-27 05:27:18.614 21410 21455 I ActivityManager: Start proc 23143:system/u0a39 for added application system caller=null
10-27 05:27:18.789 21410 21455 I ActivityManager: Start proc 23168:com.qualcomm.qti.services.systemhelper:systemhelper_service/u0a190 for added application com.qualcomm.qti.services.systemhelper:systemhelper_service caller=null
10-27 05:27:18.862 21410 21455 I ActivityManager: Start proc 23189:org.ifaa.aidl.manager/u0a155 for added application org.ifaa.aidl.manager caller=null
10-27 05:27:18.947 21410 21455 I ActivityManager: Start proc 23192:com.miui.voicetrigger/u0a129 for added application com.miui.voicetrigger caller=null
10-27 05:27:19.049 21410 21455 I ActivityManager: Start proc 23221:com.xiaomi.mircs/u0a61 for added application com.xiaomi.mircs caller=null
10-27 05:27:19.307 21410 21455 I ActivityManager: Start proc 23242:com.blackshark.sharkmonitor/1000 for added application com.blackshark.sharkmonitor caller=null
10-27 05:27:19.450 21410 21455 I ActivityManager: Start proc 23259:com.xiaomi.xmsfkeeper/u0a117 for added application com.xiaomi.xmsfkeeper caller=null
10-27 05:27:19.619 21410 21455 I ActivityManager: Start proc 23280:com.qualcomm.qti.workloadclassifier/u0a196 for added application com.qualcomm.qti.workloadclassifier caller=null
10-27 05:27:19.928 21410 21455 I ActivityManager: Start proc 23306:com.tencent.soter.soterserver/u0a160 for added application com.tencent.soter.soterserver caller=null
10-27 05:27:20.162 21410 21455 I ActivityManager: Start proc 23328:com.blackshark.analytics/u0a116 for added application com.blackshark.analytics caller=null
10-27 05:27:20.225 21410 21455 I ActivityManager: Start proc 23352:com.blackshark.mtsservice/1000 for added application com.blackshark.mtsservice caller=null
10-27 05:27:20.347 21410 21455 I ActivityManager: Start proc 23368:org.mipay.android.manager/u0a153 for added application org.mipay.android.manager caller=null
10-27 05:27:20.657 21410 21455 I ActivityManager: Start proc 23397:com.qualcomm.location/u0a192 for added application com.qualcomm.location caller=null
10-27 05:27:20.902 21410 21455 I ActivityManager: Start proc 23404:com.blackshark.bsliveassistant/1000 for added application com.blackshark.bsliveassistant caller=null
10-27 05:27:20.962 21410 21455 I ActivityManager: Start proc 23437:com.qualcomm.qti.services.secureui:sui_service/1000 for added application com.qualcomm.qti.services.secureui:sui_service caller=null
10-27 05:27:21.083 21410 21455 I ActivityManager: Start proc 23449:com.blackshark.zsappusagecollector/1000 for added application com.blackshark.zsappusagecollector caller=null
10-27 05:27:21.205 21410 21455 I ActivityManager: Start proc 23471:com.blackshark.gamesdkmanager/1000 for added application com.blackshark.gamesdkmanager caller=null
10-27 05:27:21.418 21410 21455 I ActivityManager: Start proc 23487:com.miui.face/1000 for added application com.miui.face caller=null
10-27 05:27:21.545 21410 21455 I ActivityManager: Start proc 23506:com.miui.analytics/u0a124 for service {com.miui.analytics/com.miui.analytics.onetrack.OneTrackService} caller=null
10-27 05:27:21.658 21410 21455 I ActivityManager: Start proc 23509:com.android.providers.media.module/u0a212 for service {com.android.providers.media.module/com.android.providers.media.fuse.ExternalStorageServiceImpl} caller=null
10-27 05:27:21.754 21410 21455 I ActivityManager: Start proc 23539:com.miui.personalassistant/u0a62 for service {com.miui.personalassistant/com.miui.personalassistant.overlay.AssistantOverlayService} caller=null
10-27 05:27:21.992 21410 21455 I ActivityManager: Start proc 23550:com.blackshark.shoulderkey/1000 for service {com.blackshark.shoulderkey/com.blackshark.shoulderkey.service.ShoulderKeyService} caller=null
10-27 05:27:22.193 21410 21455 I ActivityManager: Start proc 23578:com.xiaomi.metoknlp/u0a133 for service {com.xiaomi.metoknlp/com.xiaomi.location.metoknlp.MetokLocationService} caller=null
10-27 05:27:22.465 21410 21455 I ActivityManager: Start proc 23598:com.android.statementservice/u0a85 for broadcast {com.android.statementservice/com.android.statementservice.domain.DomainVerificationReceiverV1} caller=null
10-27 05:27:22.607 21410 21455 I ActivityManager: Start proc 23619:com.xiaomi.location.fused/1000 for service {com.xiaomi.location.fused/com.xiaomi.location.fused.FusedLocationService} caller=null
````

AOSP Log

````logcat
09-30 06:19:46.964 26234 26234 I SystemServiceManager: Starting phase 100
09-30 06:19:48.827 26234 26234 I SystemServiceManager: Starting phase 480
09-30 06:19:48.833 26234 26234 I SystemServiceManager: Starting phase 500
09-30 06:19:48.999 26234 26234 I SystemServiceManager: Starting phase 520
09-30 06:19:49.022 26234 26234 I SystemServiceManager: Starting phase 550
09-30 06:19:49.063 26234 26263 I ActivityManager: Start proc 26374:com.android.bluetooth/1002 for service {com.android.bluetooth/com.android.bluetooth.btservice.AdapterService}
09-30 06:19:49.103 26234 26263 I ActivityManager: Start proc 26392:com.android.systemui/u0a85 for service {com.android.systemui/com.android.systemui.ImageWallpaper}
09-30 06:19:49.221 26234 26234 I SystemServiceManager: Starting phase 600
09-30 06:19:49.268 26234 26263 I ActivityManager: Start proc 26428:WebViewLoader-armeabi-v7a/1037 [android.webkit.WebViewLibraryLoader$RelroFileCreator] for null
09-30 06:19:49.308 26234 26263 I ActivityManager: Start proc 26435:WebViewLoader-arm64-v8a/1037 [android.webkit.WebViewLibraryLoader$RelroFileCreator] for null
09-30 06:19:49.379 26234 26263 I ActivityManager: Start proc 26471:com.android.networkstack/1073 for service {com.android.networkstack/com.android.server.NetworkStackService}
09-30 06:19:49.632 26234 26539 I ActivityManager: Start proc 26512:com.qualcomm.qti.telephonyservice/u0a77 for added application com.qualcomm.qti.telephonyservice
09-30 06:19:49.709 26234 26263 I ActivityManager: Start proc 26558:com.android.phone/1001 for added application com.android.phone
09-30 06:19:49.784 26234 26263 I ActivityManager: Start proc 26582:com.android.settings/1000 for activity {com.android.settings/com.android.settings.FallbackHome}
09-30 06:19:49.934 26234 26263 I ActivityManager: Start proc 26622:android.ext.services/u0a42 for service {android.ext.services/android.ext.services.watchdog.ExplicitHealthCheckServiceImpl}
09-30 06:19:50.174 26234 26263 I ActivityManager: Start proc 26658:com.android.inputmethod.latin/u0a92 for service {com.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME}
09-30 06:19:50.919 26234 26263 I ActivityManager: Start proc 26747:com.android.cellbroadcastreceiver/u0a53 for broadcast {com.android.cellbroadcastreceiver/com.android.cellbroadcastreceiver.CellBroadcastReceiver}
09-30 06:19:51.277 26234 26263 I ActivityManager: Start proc 26802:android.process.acore/u0a38 for content provider {com.android.providers.blockednumber/com.android.providers.blockednumber.BlockedNumberProvider}
09-30 06:19:52.661 26234 26256 I SystemServiceManager: Starting phase 1000
09-30 06:19:52.739 26234 26263 I ActivityManager: Start proc 26871:com.android.deskclock/u0a91 for broadcast {com.android.deskclock/com.android.deskclock.AlarmInitReceiver}
09-30 06:19:53.481 26234 26263 I ActivityManager: Start proc 26918:com.android.nfc/1027 for added application com.android.nfc
09-30 06:19:53.543 26234 26263 I ActivityManager: Start proc 26926:com.android.se/1068 for added application com.android.se
09-30 06:19:53.554 26234 26263 I ActivityManager: Start proc 26965:com.qualcomm.qti.rcsbootstraputil/1001 for added application com.qualcomm.qti.rcsbootstraputil
09-30 06:19:53.628 26234 26263 I ActivityManager: Start proc 26974:com.android.externalstorage/u0a40 for broadcast {com.android.externalstorage/com.android.externalstorage.MountReceiver}
09-30 06:19:53.684 26234 26263 I ActivityManager: Start proc 27011:com.android.launcher3/u0a87 for service {com.android.launcher3/com.android.launcher3.notification.NotificationListener}
09-30 06:19:53.765 26234 26548 I ActivityManager: Start proc 27035:com.android.smspush/u0a66 for service {com.android.smspush/com.android.smspush.WapPushManager}
09-30 06:19:53.808 26234 26263 I ActivityManager: Start proc 27061:com.android.music/u0a97 for service {com.android.music/com.android.music.MediaPlaybackService}
09-30 06:19:53.851 26234 26263 I ActivityManager: Start proc 27081:com.android.printspooler/u0a59 for service {com.android.printspooler/com.android.printspooler.model.PrintSpoolerService}
09-30 06:19:53.868 26234 26263 I ActivityManager: Start proc 27096:android.process.media/u0a39 for broadcast {com.android.providers.downloads/com.android.providers.downloads.DownloadReceiver}
09-30 06:19:54.023 26234 26263 I ActivityManager: Start proc 27143:com.android.keychain/1000 for service {com.android.keychain/com.android.keychain.KeyChainService}
09-30 06:19:54.366 26234 26263 I ActivityManager: Start proc 27187:com.android.deskclock/u0a91 for broadcast {com.android.deskclock/com.android.alarmclock.AnalogAppWidgetProvider}
09-30 06:19:54.560 26234 26263 I ActivityManager: Start proc 27217:com.android.quicksearchbox/u0a99 for broadcast {com.android.quicksearchbox/com.android.quicksearchbox.SearchWidgetProvider}
09-30 06:19:54.735 26234 26263 I ActivityManager: Start proc 27245:com.android.dialer/u0a84 for broadcast {com.android.dialer/com.android.dialer.app.calllog.CallLogReceiver}
09-30 06:19:54.966 26234 26263 I ActivityManager: Start proc 27276:com.android.carrierconfig/u0a80 for service {com.android.carrierconfig/com.android.carrierconfig.DefaultCarrierConfigService}
09-30 06:19:54.986 26234 26263 I ActivityManager: Start proc 27295:com.android.calendar/u0a89 for broadcast {com.android.calendar/com.android.calendar.alerts.AlertReceiver}
09-30 06:19:55.110 26234 26263 I ActivityManager: Start proc 27323:com.android.contacts/u0a83 for broadcast {com.android.contacts/com.android.contacts.interactions.OnBootOrUpgradeReceiver}
09-30 06:19:55.360 26234 26263 I ActivityManager: Start proc 27356:com.android.dynsystem/1000 for broadcast {com.android.dynsystem/com.android.dynsystem.BootCompletedReceiver}
09-30 06:19:55.568 26234 26263 I ActivityManager: Start proc 27382:com.android.email/u0a96 for broadcast {com.android.email/com.android.email.service.EmailBroadcastReceiver}
09-30 06:19:55.745 26234 26263 I ActivityManager: Start proc 27416:com.android.managedprovisioning/u0a44 for broadcast {com.android.managedprovisioning/com.android.managedprovisioning.preprovisioning.BootReminder}
09-30 06:19:55.851 26234 26263 I ActivityManager: Start proc 27438:com.android.messaging/u0a63 for broadcast {com.android.messaging/com.android.messaging.receiver.BootAndPackageReplacedReceiver}
09-30 06:19:55.997 26234 26263 I ActivityManager: Start proc 27463:com.android.onetimeinitializer/u0a81 for broadcast {com.android.onetimeinitializer/com.android.onetimeinitializer.OneTimeInitializerReceiver}
09-30 06:19:56.114 26234 26263 I ActivityManager: Start proc 27490:com.android.packageinstaller/u0a48 for broadcast {com.android.packageinstaller/com.android.packageinstaller.TemporaryFileManager}
09-30 06:19:56.187 26234 26263 I ActivityManager: Start proc 27513:com.android.permissioncontroller/u0a50 for broadcast {com.android.permissioncontroller/com.android.packageinstaller.permission.service.LocationAccessCheck$SetupPeriodicBackgroundLocationAccessCheck}
09-30 06:19:56.288 26234 26263 I ActivityManager: Start proc 27535:com.android.providers.calendar/u0a49 for broadcast {com.android.providers.calendar/com.android.providers.calendar.CalendarReceiver}
09-30 06:19:56.448 26234 26263 I ActivityManager: Start proc 27561:com.android.settings/1000 for broadcast {com.android.settings/com.android.settings.fuelgauge.batterytip.AnomalyConfigReceiver}
09-30 06:19:56.569 26234 26263 I ActivityManager: Start proc 27583:com.android.traceur/u0a74 for broadcast {com.android.traceur/com.android.traceur.Receiver}
09-30 06:19:56.676 26234 26263 I ActivityManager: Start proc 27605:com.qualcomm.telephony/1000 for broadcast {com.qualcomm.atfwd/com.qualcomm.atfwd.AtFwdAutoboot}
09-30 06:19:56.768 26234 26263 I ActivityManager: Start proc 27628:com.qualcomm.embms/u0a75 for broadcast {com.qualcomm.embms/com.qualcomm.embms.EmbmsBootReceiver}
09-30 06:19:56.819 26234 26263 I ActivityManager: Start proc 27650:com.android.localtransport/1000 for service {com.android.localtransport/com.android.localtransport.LocalTransportService}
09-30 06:19:56.864 26234 26263 I ActivityManager: Start proc 27671:com.qualcomm.embms:remote/u0a75 for service {com.qualcomm.embms/com.qualcomm.embms.EmbmsService}
````

### 调用SurfaceControl.show()的窗口

代码修改：

````java
// Z:\work\workspace\studio_aosp\work\AOSP\sailfish-qp1a.191005.007.a3\frameworks\base\services\core\java\com\android\server\wm\WindowSurfaceController.java
class WindowSurfaceController {
    private boolean showSurface() {
        try {
            setShown(true);
            //---------------------------------------------------------

            final String __log_tag = "bob_log_tag";
            Log.d(__log_tag, " 	_ "
                    + "  title: " + title
                    + "  [WindowSurfaceController@showSurface(:450)  " + ActivityThread.currentProcessName()
                    + "(" + Process.myPid() + ":" + Thread.currentThread().getName() + ")]"
            );
            StackTraceElement[] stackTrace = new Throwable().getStackTrace();
            for (StackTraceElement element : stackTrace) {
                Log.d(__log_tag, " 	|-- " + element.toString());
            }
            Log.d(__log_tag, " 	@");

            //---------------------------------------------------------
            mSurfaceControl.show();
            return true;
        } catch (RuntimeException e) {
            Slog.w(TAG, "Failure showing surface " + mSurfaceControl + " in " + this, e);
        }

        mAnimator.reclaimSomeSurfaceMemory("show", true);

        return false;
    }
````

关键字

````
bob_log_tag:  	_   title|starting phase|bootanim
````

AOSP log

````log
09-27 07:14:42.453   520   535 I sf_stop_bootanim: 33181
09-30 06:03:05.562     1     1 I init    : Received control message 'start' for 'bootanim' from pid: 24244 (/system/bin/surfaceflinger)
09-30 06:03:05.573     1     1 I init    : starting service 'bootanim'...
09-30 06:03:13.577     1     1 I init    : Service 'bootanim' (pid 24282) exited with status 0
09-30 06:03:13.726 24244 24379 I sf_stop_bootanim: 243535463
09-30 06:19:45.569     1     1 I init    : Received control message 'start' for 'bootanim' from pid: 26191 (/system/bin/surfaceflinger)
09-30 06:19:45.569     1     1 I init    : starting service 'bootanim'...
09-30 06:19:45.757 26229 26229 D BootAnimation: BootAnimationStartTiming start time: 255936485ms
09-30 06:19:45.757 26229 26229 D BootAnimation: BootAnimationPreloadTiming start time: 255936485ms
09-30 06:19:45.758 26229 26229 D BootAnimation: BootAnimationPreloadStopTiming start time: 255936485ms
09-30 06:19:45.817 26229 26231 D BootAnimation: BootAnimationShownTiming start time: 255936545ms
09-30 06:19:46.964 26234 26234 I SystemServiceManager: Starting phase 100
09-30 06:19:48.827 26234 26234 I SystemServiceManager: Starting phase 480
09-30 06:19:48.833 26234 26234 I SystemServiceManager: Starting phase 500
09-30 06:19:48.999 26234 26234 I SystemServiceManager: Starting phase 520
09-30 06:19:49.022 26234 26234 I SystemServiceManager: Starting phase 550
09-30 06:19:49.221 26234 26234 I SystemServiceManager: Starting phase 600
09-30 06:19:50.040 26234 26257 D bob_log_tag:  	_   title: com.android.settings/com.android.settings.FallbackHome  [WindowSurfaceController@showSurface(:450)  null(26234:android.anim)]
09-30 06:19:50.135 26234 26497 I ActivityManager:   ntv   ??   33566: bootanimation (   17,772K memtrack) (pid 26229) native
09-30 06:19:51.565 26234 26257 D bob_log_tag:  	_   title: StatusBar  [WindowSurfaceController@showSurface(:450)  null(26234:android.anim)]
09-30 06:19:51.569 26234 26257 D bob_log_tag:  	_   title: NavigationBar0  [WindowSurfaceController@showSurface(:450)  null(26234:android.anim)]
09-30 06:19:52.443 26234 26257 D bob_log_tag:  	_   title: com.android.systemui.ImageWallpaper  [WindowSurfaceController@showSurface(:450)  null(26234:android.anim)]
09-30 06:19:52.457 26229 26229 D BootAnimation: BootAnimationStopTiming start time: 255943184ms
09-30 06:19:52.427     1     1 I init    : Service 'bootanim' (pid 26229) exited with status 0
09-30 06:19:52.657 26191 26325 I sf_stop_bootanim: 244147359
09-30 06:19:52.661 26234 26256 I SystemServiceManager: Starting phase 1000
````

Failed Log

````logcat
01-19 11:44:02.912  1285  1285 I auditd  : type=1400 audit(0.0:170): avc: denied { read } for comm="BootAnimation" name="settings_global.xml" dev="dm-5" ino=14059 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 04:26:37.282  1207  1879 I sf_stop_bootanim: 49211
10-27 05:22:18.499 13434 13434 I auditd  : type=1400 audit(0.0:776): avc: denied { read } for comm="BootAnimation" name="settings_global.xml" dev="dm-5" ino=15989 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 05:22:49.672 13350 13858 I sf_stop_bootanim: 1009238
10-27 05:26:42.981 21282 21282 I BootAnimation: bootanimation launching ...
10-27 05:26:47.587 21282 21282 I auditd  : type=1400 audit(0.0:1439): avc: denied { read } for comm="BootAnimation" name="settings_global.xml" dev="dm-5" ino=17540 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 05:26:47.587 21282 21282 W BootAnimation: type=1400 audit(0.0:1439): avc: denied { read } for name="settings_global.xml" dev="dm-5" ino=17540 scontext=u:r:bootanim:s0 tcontext=u:object_r:system_data_file:s0 tclass=file permissive=0
10-27 05:26:47.591 21282 21383 E BootAnimation: couldn't find audio_conf.txt
10-27 05:26:47.592 21282 21383 V BootAnimation: settings_global.xml open error 13
10-27 05:26:47.599 21282 21383 D BootAnimation: Use save memory method, maybe small fps in actual.
10-27 05:26:49.269 21282 21383 D BootAnimation: Use save memory method, maybe small fps in actual.
10-27 05:26:50.275 21282 21383 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 21383 (BootAnimation), pid 21282 (bootanimation)
10-27 05:26:50.630 21450 21450 F DEBUG   : Cmdline: /system/bin/bootanimation
10-27 05:26:50.630 21450 21450 F DEBUG   : pid: 21282, tid: 21383, name: BootAnimation  >>> /system/bin/bootanimation <<<
10-27 05:26:50.632 21450 21450 F DEBUG   :       #03 pc 000000000000a3e0  /system/bin/bootanimation (android::BootAnimation::initTexture(android::FileMap*, int*, int*)+80) (BuildId: fd8e862214104f8cc4242df07c6a635e)
10-27 05:26:50.632 21450 21450 F DEBUG   :       #04 pc 000000000000c070  /system/bin/bootanimation (android::BootAnimation::movie()+3428) (BuildId: fd8e862214104f8cc4242df07c6a635e)
10-27 05:26:50.632 21450 21450 F DEBUG   :       #05 pc 000000000000aec4  /system/bin/bootanimation (android::BootAnimation::threadLoop()+152) (BuildId: fd8e862214104f8cc4242df07c6a635e)
10-27 05:26:51.727 21410 21410 I SystemServiceManager: Starting phase 100
10-27 05:26:57.250 21410 21410 I SystemServiceManager: Starting phase 200
10-27 05:26:59.364 21410 21410 I SystemServiceManager: Starting phase 480
10-27 05:26:59.400 21410 21410 I SystemServiceManager: Starting phase 500
10-27 05:27:00.129 21410 21410 I SystemServiceManager: Starting phase 520
10-27 05:27:00.957 21410 21410 I SystemServiceManager: Starting phase 550
10-27 05:27:03.685 21410 21410 I SystemServiceManager: Starting phase 600
10-27 05:27:07.100 21410 21438 D bob_log_tag:  	_   title: GestureStub
10-27 05:27:07.178 21410 21438 D bob_log_tag:  	_   title: GestureStubRight
10-27 05:27:07.196 21410 21438 D bob_log_tag:  	_   title: GestureStubLeft
10-27 05:27:07.902 21410 21438 D bob_log_tag:  	_   title: com.miui.home/com.miui.home.launcher.Launcher
10-27 05:27:09.656 21410 21438 D bob_log_tag:  	_   title: com.miui.miwallpaper.wallpaperservice.ImageWallpaper
10-27 05:27:10.341 21410 21438 D bob_log_tag:  	_   title: Freeform-HotSpotView
10-27 05:27:10.343 21410 21438 D bob_log_tag:  	_   title: Freeform-OverLayView
10-27 05:27:13.261 21239 22266 I sf_stop_bootanim: 1272827
10-27 05:27:13.300 21410 21437 I SystemServiceManager: Starting phase 1000
10-27 05:27:16.360 21410 21425 D bob_log_tag:  	_   title: RoundCornerTop
10-27 05:27:16.361 21410 21425 D bob_log_tag:  	_   title: RoundCornerBottom
10-27 05:27:17.913 21410 21438 D bob_log_tag:  	_   title: StatusBar
10-27 05:27:17.924 21410 21438 D bob_log_tag:  	_   title: com.miui.miwallpaper.wallpaperservice.ImageWallpaper
10-27 05:27:17.927 21410 21438 D bob_log_tag:  	_   title: NotificationShade
10-27 05:27:19.698 21410 21438 D bob_log_tag:  	_   title: control_center
````



















## 相关流程













