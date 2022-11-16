
```cpp

== com.android.settings ==
service.clearUsbDebuggingKeys();

== system_server ==
mDeviceManager.clearUsbDebuggingKeys();
    mHandler.sendEmptyMessage(UsbDebuggingHandler.MESSAGE_ADB_CLEAR);

public void handleMessage(Message msg=MESSAGE_ADB_CLEAR)
    deleteKeyFile();
        File keyFile = getUserKeyFile();
            File adbDir = new File(dataDir, ADB_DIRECTORY="misc/adb");
                return new File(adbDir, ADB_KEYS_FILE="adb_keys");
                    keyFile.delete();
```









