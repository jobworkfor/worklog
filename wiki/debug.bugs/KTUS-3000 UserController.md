# KTUS-3000【大桌面：桌面点击图标】重启手机后，等待10分钟点击桌面图标仍然提示“重启后请等待应用响应”（FR：仅一次

http://jira.blackshark.com/browse/KTUS-3000

## 结论

vold log中raid出错，Failed to install fscrypt key to /data/raid: I/O error，需要bsp继续分析。

````c
10-27 11:58:14.783  2401  2416 D StorageManagerService: unlockUserKey: 0 isFileEncryptedNativeOrEmulated: true hasToken: false hasSecret: true
10-27 11:58:14.784   866  1055 D vold    : fscrypt_unlock_user_key 0 serial=0
10-27 11:58:14.784   866  1055 D vold    : Skipping non-key miuser_backup
10-27 11:58:14.784   866  1055 D vold    : Trying user CE key /data/misc/vold/user_keys/ce/0/current
10-27 11:58:14.787   866  1055 D vold    : Successfully retrieved key
10-27 11:58:14.789   866  1055 D vold    : Installed fscrypt key with ref fe01931d68a14e8f460b49f67465b141 to /data
10-27 11:58:14.789   866  1055 D vold    : Added fscrypt-provisioning key for fe01931d68a14e8f460b49f67465b141 to session keyring

// raid 报错，导致无法解锁cd加密
10-27 11:58:14.789   866  1055 E vold    : Failed to install fscrypt key to /data/raid: I/O error
10-27 11:58:14.789   866  1055 E vold    : Couldn't read key for 0
10-27 11:58:14.789  2401  3663 I am_uid_running: 10233
````

## LOG关键字

### `User 0|I uc|Starting phase`

````c
01-02 06:27:25.992   901   901 D vold    : Installed de key for user 0
01-02 06:27:25.992   901   901 D vold    : fscrypt_prepare_user_storage for volume null, user 0, serial 0, flags 1
01-02 06:27:31.908  2229  2229 I SystemServiceManager: Starting phase 100
10-27 01:14:49.599  2229  2229 I SystemServiceManager: Starting phase 600
10-27 01:14:49.727  2229  2229 I SystemServiceManager: Calling onStartUser 0
10-27 01:14:49.912  2229  2229 I uc_send_user_broadcast: [0,android.intent.action.USER_FOREGROUND]
10-27 01:14:49.912  2229  2229 I uc_send_user_broadcast: [0,android.intent.action.USER_SWITCHED]
10-27 01:14:53.236  2229  3258 I ActivityTaskManager: user 0 is still locked. Cannot load recents
10-27 01:14:56.184  2229  2570 I SystemServiceManager: Starting phase 1000
    
10-27 01:14:56.274  2229  2570 I ActivityManager: User 0 state changed from BOOTING to RUNNING_LOCKED

10-27 01:14:56.322   901   901 D vold    : Installed fscrypt key with ref 28709b01f69c1399c6aeaf5cc9f635f8 to /data
10-27 01:14:56.323   901   901 D vold    : Added fscrypt-provisioning key for 28709b01f69c1399c6aeaf5cc9f635f8 to session keyring
10-27 01:14:56.323   901   901 D vold    : Installed fscrypt key with ref 28709b01f69c1399c6aeaf5cc9f635f8 to /data/raid
10-27 01:14:56.323   901   901 D vold    : Added fscrypt-provisioning key for 28709b01f69c1399c6aeaf5cc9f635f8 to session keyring
10-27 01:14:56.323   901   901 D vold    : Installed ce key for user 0
10-27 01:14:56.324  2229  2570 I uc_finish_user_unlocking: 0
10-27 01:14:56.324  2229  2570 W ActivityManager: UserLifecycleEvent 5 received without an active userJourneySession.
10-27 01:14:56.324  2229  2570 D ActivityManager: Started unlocking user 0
10-27 01:14:56.324  2229  2570 D ActivityManager: Unlocking user 0 progress 0
10-27 01:14:56.324  2229  2570 D ActivityManager: Unlocking user 0 progress 5

10-27 01:14:56.336   901   901 D vold    : fscrypt_prepare_user_storage for volume null, user 0, serial 0, flags 2
10-27 01:14:56.336   901   901 D vold    : Preparing: /data/system_ce/0
10-27 01:14:56.336   901   901 D vold    : Preparing: /data/misc_ce/0
10-27 01:14:56.337   901   901 D vold    : Preparing: /data/vendor_ce/0
    
10-27 01:14:57.169  2229  2567 I ActivityManager: User 0 state changed from RUNNING_LOCKED to RUNNING_UNLOCKING
10-27 01:14:57.173  2229  2567 D ActivityManager: Unlocking user 0 progress 20
10-27 01:14:57.174  2229  2669 I SystemServiceManager: Calling onUnlockingUser 0
10-27 01:14:57.182  2229  2669 D BluetoothManagerService: User 0 unlocked
10-27 01:14:57.281  2229  2669 I uc_finish_user_unlocked: 0

10-27 01:14:57.288  2229  2669 I ActivityManager: User 0 state changed from RUNNING_UNLOCKING to RUNNING_UNLOCKED
10-27 01:14:57.288  2229  2669 I am_user_state_changed: [0,3]
````

## 相关流程

````c
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	_ Started unlocking user  [UserProgressListener@onStarted(:2949)  null(14154:android.display)]
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.UserController$UserProgressListener.onStarted(UserController.java:2940)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.internal.util.ProgressReporter.notifyStarted(ProgressReporter.java:229)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.internal.util.ProgressReporter.start(ProgressReporter.java:210)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.UserController.finishUserUnlocking(UserController.java:573)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.UserController.unlockUserCleared(UserController.java:1726)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.UserController.maybeUnlockUser(UserController.java:1688)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.UserController.finishUserBoot(UserController.java:537)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.UserController.sendBootCompleted(UserController.java:2258)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.ActivityManagerService.finishBooting(ActivityManagerService.java:4989)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.am.ActivityManagerService.bootAnimationComplete(ActivityManagerService.java:5051)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.wm.WindowManagerService.performEnableScreen(WindowManagerService.java:3818)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.wm.WindowManagerService.access$1600(WindowManagerService.java:353)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.wm.WindowManagerService$H.handleMessage(WindowManagerService.java:5340)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- android.os.Handler.dispatchMessage(Handler.java:106)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- android.os.Looper.loopOnce(Looper.java:210)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- android.os.Looper.loop(Looper.java:299)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- android.os.HandlerThread.run(HandlerThread.java:67)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	|-- com.android.server.ServiceThread.run(ServiceThread.java:46)
10-27 01:21:06.146 14154 14195 D bob_log_tag:  	@
````

