PackageMangerService Corner Features
====================================


Launcher uninstall icon visibility
----------------------------------------------------------------------------------------------------
* [<b>supportsDrop(Context context, Object info)</b>](#supportsDrop)

----------------------------------------------------------------------------------------------------

`com.android.launcher3.DropTargetBar#setup`方法将`mUninstallDropTarget`对象添加到`com.android.launcher3.dragndrop.DragController#mListeners`中，
`mUninstallDropTarget`在`com.android.launcher3.DropTargetBar#onFinishInflate`方法中被赋值：
```cpp
    protected void onFinishInflate() {
        super.onFinishInflate();

        // Get the individual components
        mDeleteDropTarget = (ButtonDropTarget) findViewById(R.id.delete_target_text);
        mAppInfoDropTarget = (ButtonDropTarget) findViewById(R.id.info_target_text);
->      mUninstallDropTarget = (ButtonDropTarget) findViewById(R.id.uninstall_target_text);

        mDeleteDropTarget.setDropTargetBar(this);
        mAppInfoDropTarget.setDropTargetBar(this);
        mUninstallDropTarget.setDropTargetBar(this);

        // Initialize with hidden state
        setAlpha(0f);
    }
```

`R.id.uninstall_target_text`被定义在`packages/apps/Launcher3/res/layout/drop_target_bar_horz.xml`中。
该布局在`packages/apps/Launcher3/res/layout-port/launcher.xml`中被引入：
```cpp
packages/apps/Launcher3/res/layout-port/launcher.xml
        <include
            android:id="@+id/drop_target_bar"
            layout="@layout/drop_target_bar_horz" />
```

在`packages/apps/Launcher3/src/com/android/launcher3/Launcher.java`中的初始化为：
```cpp
    private void setupViews() {
        // Get the search/delete/uninstall bar
        mDropTargetBar = (DropTargetBar) mDragLayer.findViewById(R.id.drop_target_bar);
    }
```

当长按并开始拖动图标时，调用`UninstallDropTarget.supportsDrop`方法来判断是否显示卸载图标，调用栈如下：
```cpp
"main@5173" prio=5 tid=0x1 nid=NA runnable
  java.lang.Thread.State: RUNNABLE
	  at com.android.launcher3.UninstallDropTarget.supportsDrop(UninstallDropTarget.java:43)
	  at com.android.launcher3.UninstallDropTarget.supportsDrop(UninstallDropTarget.java:38)
	  at com.android.launcher3.ButtonDropTarget.onDragStart(ButtonDropTarget.java:204)
	  at com.android.launcher3.dragndrop.DragController.startDeferredDrag(DragController.java:293)
	  at com.android.launcher3.dragndrop.DragController.startDrag(DragController.java:275)
	  at com.android.launcher3.Workspace.beginDragShared(Workspace.java:2351)
	  at com.android.launcher3.Workspace.beginDragShared(Workspace.java:2302)
	  at com.android.launcher3.Workspace.startDrag(Workspace.java:2291)
	  at com.android.launcher3.Launcher.onLongClick(Launcher.java:3145)
	  at android.view.View.performLongClickInternal(View.java:5714)
	  at android.view.View.performLongClick(View.java:5672)
	  at android.widget.TextView.performLongClick(TextView.java:9415)
	  at com.android.launcher3.CheckLongPressHelper$CheckForLongPress.run(CheckLongPressHelper.java:41)
	  at android.os.Handler.handleCallback(Handler.java:751)
	  at android.os.Handler.dispatchMessage(Handler.java:95)
	  at android.os.Looper.loop(Looper.java:154)
	  at android.app.ActivityThread.main(ActivityThread.java:6119)
	  at java.lang.reflect.Method.invoke(Method.java:-1)
	  at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:886)
	  at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:776)
```

### UninstallDropTarget.supportsDrop
```cpp
    public static boolean supportsDrop(Context context, Object info) {
        if (Utilities.ATLEAST_JB_MR2) {
            UserManager userManager = (UserManager) context.getSystemService(Context.USER_SERVICE);
            Bundle restrictions = userManager.getUserRestrictions();
            if (restrictions.getBoolean(UserManager.DISALLOW_APPS_CONTROL, false)
                    || restrictions.getBoolean(UserManager.DISALLOW_UNINSTALL_APPS, false)) {
                return false;
            }
        }

        Pair<ComponentName, Integer> componentInfo = getAppInfoFlags(info);
        return componentInfo != null && (componentInfo.second & AppInfo.DOWNLOADED_FLAG) != 0;
    }
```

