Settings.Global.putInt流程
=========================

流程說明
----------------------------------------------------------------------------------------------------

### Settings.Global.putInt()开始

==process:com.android.settings==

```java
/home/dd/dev/workspace/android/android/aosp/packages/apps/Settings/src/com/android/settings/development/DevelopmentSettings.java
->          Settings.Global.putInt(getActivity().getContentResolver(),
                    Settings.Global.STAY_ON_WHILE_PLUGGED_IN,
                    mKeepScreenOn.isChecked() ?
                            (BatteryManager.BATTERY_PLUGGED_AC | BatteryManager.BATTERY_PLUGGED_USB
                                    | BatteryManager.BATTERY_PLUGGED_WIRELESS) : 0);
```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/core/java/android/provider/Settings.java
        public static boolean putInt(ContentResolver cr, String name, int value) {
->          return putString(cr, name, Integer.toString(value));
        }
```

```java
        public static boolean putString(ContentResolver resolver,
                String name, String value) {
->          return putStringForUser(resolver, name, value, null, false, UserHandle.myUserId());
        }
```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/core/java/android/provider/Settings.java
        public static boolean putStringForUser(@NonNull ContentResolver resolver,
                @NonNull String name, @Nullable String value, @Nullable String tag,
                boolean makeDefault, @UserIdInt int userHandle) {
->          return sNameValueCache.putStringForUser(resolver, name, value, tag,
                    makeDefault, userHandle);
        }
```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/core/java/android/provider/Settings.java
        public boolean putStringForUser(ContentResolver cr, String name, String value,
                String tag, boolean makeDefault, final int userHandle) {
            try {
                Bundle arg = new Bundle();
                arg.putString(Settings.NameValueTable.VALUE, value);
                arg.putInt(CALL_METHOD_USER_KEY, userHandle);
                if (tag != null) {
                    arg.putString(CALL_METHOD_TAG_KEY, tag);
                }
                if (makeDefault) {
                    arg.putBoolean(CALL_METHOD_MAKE_DEFAULT_KEY, true);
                }
                IContentProvider cp = mProviderHolder.getProvider(cr);      // @getProvider
->              cp.call(cr.getPackageName(), mCallSetCommand, name, arg);
            } catch (RemoteException e) {
                Log.w(TAG, "Can't set key " + name + " in " + mUri, e);
                return false;
            }
            return true;
        }
```
上面这步重要，完成如下三个工作：
1. 封装出一个数据载体`Bundle arg`
2. 获取到ContentProvider对象
3. 调用ContentProvider的API实现数据存储

```java
    @Override
    public Bundle call(String callingPkg, String method, String request, Bundle args)
            throws RemoteException {
        Parcel data = Parcel.obtain();
        Parcel reply = Parcel.obtain();
        try {
            data.writeInterfaceToken(IContentProvider.descriptor);

            data.writeString(callingPkg);
            data.writeString(method);
            data.writeString(request);
            data.writeBundle(args);

->          mRemote.transact(IContentProvider.CALL_TRANSACTION, data, reply, 0);

            DatabaseUtils.readExceptionFromParcel(reply);
            Bundle bundle = reply.readBundle();
            return bundle;
        } finally {
            data.recycle();
            reply.recycle();
        }
    }
```
由`@getProvider`脚注可知provider坐落在`frameworks/base/packages/SettingsProvider/`中，查看其`AndroidManifest.xml`
发现该code运行在`system_server`进程中，调试`system_server`获取相关信息

==process:system_server==

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/core/java/android/content/ContentProviderNative.java
    public boolean onTransact(int code, Parcel data, Parcel reply, int flags)
            throws RemoteException {
                case CALL_TRANSACTION:
                {
                    data.enforceInterface(IContentProvider.descriptor);

                    String callingPkg = data.readString();  //  callingPkg: "com.android.settings"
                    String method = data.readString();      //  method: "PUT_global"
                    String stringArg = data.readString();   //  stringArg: "stay_on_while_plugged_in"
                    Bundle args = data.readBundle();        //  args: "Bundle[mParcelledData.dataSize=56]"

->                  Bundle responseBundle = call(callingPkg, method, stringArg, args);

                    reply.writeNoException();
                    reply.writeBundle(responseBundle);
                    return true;
                }

```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/core/java/android/content/ContentProvider.java
        @Override
        public Bundle call(
                String callingPkg, String method, @Nullable String arg, @Nullable Bundle extras) {
            Bundle.setDefusable(extras, true);
            final String original = setCallingPackage(callingPkg);
            try {
->              return ContentProvider.this.call(method, arg, extras);
            } finally {
                setCallingPackage(original);
            }
        }
```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java
    public Bundle call(String method, String name, Bundle args) {
        final int requestingUserId = getRequestingUserId(args);
        switch (method) {
            case Settings.CALL_METHOD_PUT_GLOBAL: {
                String value = getSettingValue(args);
                String tag = getSettingTag(args);
                final boolean makeDefault = getSettingMakeDefault(args);
->              insertGlobalSetting(name, value, tag, makeDefault, requestingUserId, false);
                break;
            }
```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java
    private boolean insertGlobalSetting(String name, String value, String tag,
            boolean makeDefault, int requestingUserId, boolean forceNotify) {
        if (DEBUG) {
            Slog.v(LOG_TAG, "insertGlobalSetting(" + name + ", " + value  + ", "
                    + ", " + tag + ", " + makeDefault + ", " + requestingUserId
                    + ", " + forceNotify + ")");
        }
->      return mutateGlobalSetting(name, value, tag, makeDefault, requestingUserId,
                MUTATION_OPERATION_INSERT, forceNotify, 0);
    }
```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java
    private boolean mutateGlobalSetting(String name, String value, String tag,
            boolean makeDefault, int requestingUserId, int operation, boolean forceNotify,
            int mode) {
        // Perform the mutation.
        synchronized (mLock) {
            switch (operation) {
                case MUTATION_OPERATION_INSERT: {
->                  return mSettingsRegistry.insertSettingLocked(SETTINGS_TYPE_GLOBAL,
                            UserHandle.USER_SYSTEM, name, value, tag, makeDefault,
                            getCallingPackage(), forceNotify, CRITICAL_GLOBAL_SETTINGS);
                }
```

```java
com.android.providers.settings.SettingsProvider.SettingsRegistry.insertSettingLocked
        public boolean insertSettingLocked(int type, int userId, String name, String value,
                String tag, boolean makeDefault, String packageName, boolean forceNotify,
                Set<String> criticalSettings) {
            final int key = makeKey(type, userId);

            boolean success = false;
            SettingsState settingsState = peekSettingsStateLocked(key);
            if (settingsState != null) {
                success = settingsState.insertSettingLocked(name, value,
                        tag, makeDefault, packageName);
            }

            if (success && criticalSettings != null && criticalSettings.contains(name)) {
                settingsState.persistSyncLocked();
            }

            if (forceNotify || success) {
                notifyForSettingsChange(key, name);
            }
            return success;
        }

```


```java
    public boolean insertSettingLocked(String name, String value, String tag,
            boolean makeDefault, String packageName) {
        if (TextUtils.isEmpty(name)) {
            return false;
        }

        Setting oldState = mSettings.get(name);
        String oldValue = (oldState != null) ? oldState.value : null;
        String oldDefaultValue = (oldState != null) ? oldState.defaultValue : null;
        Setting newState;

        if (oldState != null) {
            if (!oldState.update(value, makeDefault, packageName, tag, false)) {
                return false;
            }
            newState = oldState;
        } else {
            newState = new Setting(name, value, makeDefault, packageName, tag);
            mSettings.put(name, newState);
        }

        addHistoricalOperationLocked(HISTORICAL_OPERATION_UPDATE, newState);

        updateMemoryUsagePerPackageLocked(packageName, oldValue, value,
                oldDefaultValue, newState.getDefaultValue());

->      scheduleWriteIfNeededLocked();

        return true;
    }
```
此处会先把要修改值都放在mSettings容器中，里面有所有settings global的值，最后在scheduleWriteIfNeededLocked()方法中
将所有的值都写到`settings_global.xml`文件中。

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/SettingsState.java
    private void scheduleWriteIfNeededLocked() {
        // If dirty then we have a write already scheduled.
        if (!mDirty) {
            mDirty = true;
->          writeStateAsyncLocked();
        }
    }
```

```java
    private void writeStateAsyncLocked() {
        final long currentTimeMillis = SystemClock.uptimeMillis();

        if (mWriteScheduled) {
            ...
        } else {
            mLastNotWrittenMutationTimeMillis = currentTimeMillis;
->          Message message = mHandler.obtainMessage(MyHandler.MSG_PERSIST_SETTINGS);
            mHandler.sendMessageDelayed(message, WRITE_SETTINGS_DELAY_MILLIS);
            mWriteScheduled = true;
        }
    }
```

```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/SettingsState.java
    private final class MyHandler extends Handler {
        public static final int MSG_PERSIST_SETTINGS = 1;

        public MyHandler(Looper looper) {
            super(looper);
        }

        @Override
        public void handleMessage(Message message) {
            switch (message.what) {
                case MSG_PERSIST_SETTINGS: {
                    Runnable callback = (Runnable) message.obj;
->                  doWriteState();
                    if (callback != null) {
                        callback.run();
                    }
                }
                break;
            }
        }
    }
```

```java
    private void doWriteState() {
        boolean wroteState = false;
        final int version;
        final ArrayMap<String, Setting> settings;

        synchronized (mLock) {
            version = mVersion;
            settings = new ArrayMap<>(mSettings);
            mDirty = false;
            mWriteScheduled = false;
        }

        synchronized (mWriteLock) {
            if (DEBUG_PERSISTENCE) {
                Slog.i(LOG_TAG, "[PERSIST START]");
            }

            AtomicFile destination = new AtomicFile(mStatePersistFile);     @mStatePersistFile： /data/system/users/0/settings_global.xml
            FileOutputStream out = null;
            try {
                out = destination.startWrite();

                XmlSerializer serializer = Xml.newSerializer();
                serializer.setOutput(out, StandardCharsets.UTF_8.name());
                serializer.setFeature("http://xmlpull.org/v1/doc/features.html#indent-output",
                        true);
                serializer.startDocument(null, true);
                serializer.startTag(null, TAG_SETTINGS);
                serializer.attribute(null, ATTR_VERSION, String.valueOf(version));

                final int settingCount = settings.size();
                for (int i = 0; i < settingCount; i++) {
                    Setting setting = settings.valueAt(i);

                    writeSingleSetting(mVersion, serializer, setting.getId(), setting.getName(),
                            setting.getValue(), setting.getDefaultValue(), setting.getPackageName(),
                            setting.getTag(), setting.isDefaultFromSystem());

                    if (DEBUG_PERSISTENCE) {
                        Slog.i(LOG_TAG, "[PERSISTED]" + setting.getName() + "="
                                + setting.getValue());
                    }
                }

                serializer.endTag(null, TAG_SETTINGS);
                serializer.endDocument();
->              destination.finishWrite(out);

                wroteState = true;

                if (DEBUG_PERSISTENCE) {
                    Slog.i(LOG_TAG, "[PERSIST END]");
                }
            } catch (Throwable t) {
                Slog.wtf(LOG_TAG, "Failed to write settings, restoring backup", t);
                destination.failWrite(out);
            } finally {
                IoUtils.closeQuietly(out);
            }
        }

        if (wroteState) {
            synchronized (mLock) {
                addHistoricalOperationLocked(HISTORICAL_OPERATION_PERSIST, null);
            }
        }
    }
```

此处将settings中所有的值转成xml格式数据，写入`/data/system/users/0/settings_global.xml`文件

## 存储位置

综上，settings数据保存在xml文件中，支持多用户，涉及文件如下：

````bash
127|sailfish:/data/system/users/0 # ls -l
-rw------- 1 system system 12655 2021-11-08 22:00 settings_global.xml
-rw------- 1 system system 12084 2021-11-06 07:08 settings_secure.xml
-rw------- 1 system system  5285 2021-11-08 20:18 settings_system.xml
````


`@xxx`脚注说明
----------------------------------------------------------------------------------------------------
### @getProvider mProviderHolder.getProvider()获取IContentProvider
```java
/home/dd/dev/workspace/android/android/aosp/frameworks/base/core/java/android/provider/Settings.java
        public IContentProvider getProvider(ContentResolver contentResolver) {
            synchronized (mLock) {
                if (mContentProvider == null) {
->                  mContentProvider = contentResolver
                            .acquireProvider(mUri.getAuthority());
                }
                return mContentProvider;
            }
        }
```
此处mUri的值为："content://settings/global"，此处不细究mUri在哪里赋值的了，本文主要说明`Settings.Global.putInt`最终的数据去向。忽略所有旁枝末节。

全文搜索`android:authorities="settings"`关键字，不难知道其Provider是`frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/SettingsProvider.java`
打开该文件发现有如下"表"的定义:
```java
    private static final String TABLE_SYSTEM = "system";
    private static final String TABLE_SECURE = "secure";
    private static final String TABLE_GLOBAL = "global";
```


### @mStatePersistFile
```bash
05-27 20:10:28.307  1545  1545 D bob_log_tag:  	_ [SettingsState - line:208]   mStatePersistFile: /data/system/users/0/settings_global.xml  pid: 1545  thread: main  thisha: 56d426b
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsState.<init>(SettingsState.java:216)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsProvider$SettingsRegistry.ensureSettingsStateLocked(SettingsProvider.java:2333)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsProvider$SettingsRegistry.ensureSettingsForUserLocked(SettingsProvider.java:2305)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsProvider$SettingsRegistry.peekSettingsStateLocked(SettingsProvider.java:2587)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsProvider$SettingsRegistry.getSettingsNamesLocked(SettingsProvider.java:2272)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsProvider$SettingsRegistry.syncSsaidTableOnStart(SettingsProvider.java:2254)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsProvider$SettingsRegistry.<init>(SettingsProvider.java:2152)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- com.android.providers.settings.SettingsProvider.onCreate(SettingsProvider.java:325)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- android.content.ContentProvider.attachInfo(ContentProvider.java:1917)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- android.content.ContentProvider.attachInfo(ContentProvider.java:1892)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- android.app.ActivityThread.installProvider(ActivityThread.java:6239)
05-27 20:10:28.309  1545  1545 D bob_log_tag:  	|-- android.app.ActivityThread.installContentProviders(ActivityThread.java:5805)
05-27 20:10:28.311  1545  1545 D bob_log_tag:  	|-- android.app.ActivityThread.installSystemProviders(ActivityThread.java:6414)
05-27 20:10:28.311  1545  1545 D bob_log_tag:  	|-- com.android.server.am.ActivityManagerService.installSystemProviders(ActivityManagerService.java:12147)
05-27 20:10:28.311  1545  1545 D bob_log_tag:  	|-- com.android.server.SystemServer.startOtherServices(SystemServer.java:788)
05-27 20:10:28.311  1545  1545 D bob_log_tag:  	|-- com.android.server.SystemServer.run(SystemServer.java:391)
05-27 20:10:28.311  1545  1545 D bob_log_tag:  	|-- com.android.server.SystemServer.main(SystemServer.java:267)
05-27 20:10:28.311  1545  1545 D bob_log_tag:  	|-- java.lang.reflect.Method.invoke(Native Method)
05-27 20:10:28.312  1545  1545 D bob_log_tag:  	|-- com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:438)
05-27 20:10:28.312  1545  1545 D bob_log_tag:  	|-- com.android.internal.os.ZygoteInit.main(ZygoteInit.java:787)
05-27 20:10:28.312  1545  1545 D bob_log_tag:  	@
```

上面调用栈为`mStatePersistFile`变量的初始化过程


小结
----------------------------------------------------------------------------------------------------

`Settings.Global.putInt(ContentResolver cr, String name, int value)`方法将键值对保存到`/data/system/users/0/settings_global.xml`文件中。
该文件路径是通过用户名来拼合起来的，所以该方法支持多用户。

保存的原始内容如下：
```xml
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<settings version="148">
  <setting id="41" name="low_battery_sound_timeout" value="0" package="android" defaultValue="0" defaultSysSet="true" />
  <setting id="32" name="car_undock_sound" value="/system/media/audio/ui/Undock.ogg" package="android" defaultValue="/system/media/audio/ui/Undock.ogg" defaultSysSet="true" />
  ...
```

