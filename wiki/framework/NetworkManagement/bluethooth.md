

## 编译

````bash

time prebuilts/build-tools/linux-x86/bin/ninja -j 32 -f out/combined-qssi.ninja MiuiBluetooth
adb root && adb remount && adb push Y:\work\sm8250_os\out\target\product\qssi\system\app\MiuiBluetooth /system/app/ && adb shell "stop && start"

time prebuilts/build-tools/linux-x86/bin/ninja -j 32 -f out/combined-qssi.ninja framework
adb root && adb remount && adb push Y:\work\sm8250_os\out\target\product\qssi\system\framework /system/ && adb shell "stop && start"
````

## trace

初始化，MiuiFastConnectService将自己的callback注册到GattService中

````bash
== com.xiaomi.bluetooth ==
com.android.bluetooth.ble.app.MiuiFastConnectService.ServiceMessageHandler#handleMessage(MSG_START_BLE_SCAN) // MiuiFastConnectService.java#1221
	mBluetoothLeScanner.startScan(filters, scanSettings, mScanCallback);// MiuiFastConnectService.java#1261
		wrapper.startRegistration(); // android/bluetooth/le/BluetoothLeScanner.java#259
			mBluetoothGatt.registerScanner(this, mWorkSource);// BluetoothLeScanner.java#403
			
== com.android.bluetooth ==
registerScanner(IScannerCallback callback, WorkSource workSource)// GattService.java#472
	service.registerScanner(callback, workSource);// GattService.java#478
````

通知流程，从com.android.bluetooth -> com.xiaomi.bluetooth

````bash
== com.android.bluetooth ==
void onScanResult()// GattService.java#990
	app.callback.onScanResult(result);// com/android/bluetooth/gatt/GattService.java#1087

== com.xiaomi.bluetooth ==
annerCallback$Stub.onTransact(IScannerCallback.java:128)
    handler.post(new Runnable() {...}// frameworks/base/core/java/android/bluetooth/le/BluetoothLeScanner.java#509
        BluetoothLeScanner$BleScanCallbackWrapper$1.run()// BluetoothLeScanner.java#512
            sendMessageDelayObject(MSG_BLE_SCAN_DEVICE, callbackType, 0, result, 0, false);// MiuiFastConnectService.java#449
                -- sendmessage:MSG_BLE_SCAN_DEVICE --
                MiuiFastConnectService$ServiceMessageHandler.handleMessage(MSG_BLE_SCAN_DEVICE) // MiuiFastConnectService.java#1385
                    MiuiFastConnectService.handleScanCallBack() // MiuiFastConnectService.java#439
                        MiuiFastConnectService.handlFastConnectScanResult() // MiuiFastConnectService.java#355

````

