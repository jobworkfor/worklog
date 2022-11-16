usb notification 的声音
======================

```
hello:/ # dumpsys notification
Current Notification Manager state:
  Notification List:
    NotificationRecord(0x040ea5a0: pkg=android user=UserHandle{-1} id=17040425 tag=null importance=3 key=-1|android|17040425|null|1000: Notification(pri=-2 contentView=null vibrate=null sound=content://settings/system/notification_sound tick defaults=0x0 flags=0x2 color=0xff607d8b vis=PUBLIC))
      uid=1000 userId=-1
      icon=Icon(typ=RESOURCE pkg=android id=0x010806fc) / android:drawable/stat_sys_adb
      pri=-2
      key=-1|android|17040425|null|1000
      seen=false
      groupKey=-1|android|17040425|null|1000
      contentIntent=PendingIntent{a737559: PendingIntentRecord{67f9bd8 android startActivity}}
      deleteIntent=null
->    tickerText=USB charging this device
      contentView=null
      defaults=0x00000000 flags=0x00000002
      sound=content://settings/system/notification_sound
      audioStreamType=-1
      audioAttributes=AudioAttributes: usage=5 content=4 flags=0x0 tags= bundle=null
      color=0xff607d8b
      vibrate=null
      led=0x00000000 onMs=0 offMs=0
      extras={
        android.title=String
        android.text=String
        android.appInfo=ApplicationInfo (ApplicationInfo{fda31ee android})
        android.originatingUserId=Integer (-1)
      }
```


/frameworks/base/core/res/res/values/strings.xml
```
<string name="usb_charging_notification_title">USB charging this device</string>
```

/frameworks/base/services/usb/java/com/android/server/usb/UsbDeviceManager.java
```
com.android.server.usb.UsbDeviceManager.UsbHandler.updateUsbNotification(){
    id = com.android.internal.R.string.usb_charging_notification_title;
    if (id != mUsbNotificationId) {
        if (id != 0) {
            CharSequence title = r.getText(id);
            if (value==1) {
                usbPromptUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION); <-1-
            }
            Notification notification = new Notification.Builder(mContext)
                    .setTicker(title)
                    .setSound(usbPromptUri)
                    .build();
            mNotificationManager.notifyAsUser(null, id, notification, UserHandle.ALL); <-2-
        }
    }
}
```

`-1->`
/frameworks/base/media/java/android/media/RingtoneManager.java
```
android.media.RingtoneManager.getDefaultUri(){
    } else if ((type & TYPE_NOTIFICATION) != 0) {
        return Settings.System.DEFAULT_NOTIFICATION_URI;
    }
}
```

`-2->`
/frameworks/base/core/java/android/app/NotificationManager.java
```
android.app.NotificationManager.notifyAsUser(){
    service.enqueueNotificationWithTag(pkg, mContext.getOpPackageName(), tag, id,
            copy, idOut, user.getIdentifier());
}
```

/frameworks/base/services/core/java/com/android/server/notification/NotificationManagerService.java
```
com.android.server.notification.NotificationManagerService.enqueueNotificationInternal(){
    mHandler.post(new EnqueueNotificationRunnable(userId, r));
}

com.android.server.notification.NotificationManagerService.EnqueueNotificationRunnable.run(){
    buzzBeepBlinkLocked(r);
}

com.android.server.notification.NotificationManagerService.buzzBeepBlinkLocked(){
    final boolean useDefaultSound = (notification.defaults & Notification.DEFAULT_SOUND) != 0 ||
                   Settings.System.DEFAULT_NOTIFICATION_URI.equals(notification.sound);

    if (mUidBeep.get(mCallingUid, true)) {
        if (useDefaultSound) {
            soundUri = Settings.System.DEFAULT_NOTIFICATION_URI;
        } else if (notification.sound != null) {
            soundUri = notification.sound;
        }
    }

    final IRingtonePlayer player = mAudioManager.getRingtonePlayer();
    player.playAsync(soundUri, record.sbn.getUser(), looping, audioAttributes);
}
```


/frameworks/base/core/java/android/provider/Settings.java
```
public static final String AUTHORITY = "settings";
```

/frameworks/base/packages/SettingsProvider/AndroidManifest.xml
```
<provider android:name="SettingsProvider"
          android:authorities="settings"/>
```

/frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java
```
@Override
public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
    // /frameworks/base/core/java/android/provider/Settings.java
    // NOTIFICATION_SOUND_CACHE = "notification_sound_cache";
    cacheName = Settings.System.NOTIFICATION_SOUND_CACHE;
    final File cacheFile = new File(
            getRingtoneCacheDir(UserHandle.getCallingUserId()), cacheName);
    return ParcelFileDescriptor.open(cacheFile, ParcelFileDescriptor.parseMode(mode));
}

private File getRingtoneCacheDir(int userId) {
    final File cacheDir = new File(Environment.getDataSystemDeDirectory(userId), "ringtones");
}
```

/frameworks/base/core/java/android/os/Environment.java
```
public static File getDataSystemDeDirectory(int userId) {
    return buildPath(getDataDirectory(), "system_de", String.valueOf(userId));
}
```

假设用户id是0,那么存储声音的文件路径为: `/data/system_de/0/ringtones/notification_sound_cache`



关于`dumpsys notification`
----------------------------------------------------------------------------------------------------
其实现函数为

/frameworks/base/services/core/java/com/android/server/notification/NotificationManagerService.java
```
@Override
protected void dump(FileDescriptor fd, PrintWriter pw, String[] args) {
    dumpImpl(pw, filter);
}

com.android.server.notification.NotificationManagerService.dumpImpl(){
    pw.print("Current Notification Manager state"); <-1-
    if (filter.filtered) {
        pw.print(" (filtered to "); pw.print(filter); pw.print(")");
    }
    pw.println(':');
    ...
}
```

对应的dump输出为
```
hello:/ # dumpsys notification
Current Notification Manager state: <-1-
  Notification List:
    NotificationRecord(0x040ea5a0: pkg=android user=UserHandle{-1} id=17040425 tag=null importance=3 key=-1|android|17040425|null|1000: Notification(pri=-2 contentView=null vibrate=null sound=content://settings/system/notification_sound tick defaults=0x0 flags=0x2 color=0xff607d8b vis=PUBLIC))
      uid=1000 userId=-1
      icon=Icon(typ=RESOURCE pkg=android id=0x010806fc) / android:drawable/stat_sys_adb
      pri=-2
...
```

由此推广，其他可以dump的service都会有一个dump()方法来实现dump的内容，比如：

/frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java
```
com.android.server.am.ActivityManagerService.dump(){
    dumpActivitiesLocked(fd, pw, args, opti, true, dumpClient, dumpPackage);
}

com.android.server.am.ActivityManagerService.dumpActivitiesLocked(){
    pw.println("ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)");
    ...
}
```

> `dumpsys service_name`命令中，其service_name可以通过`service list`命令来查询