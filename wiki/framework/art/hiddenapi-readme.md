# android P 隐藏API对系统APP的影响

android P限制了第三方APK对@hide API的调用，那么对系统APK有什么影响呢？

国内各大手机厂商对ROM进行各种定制，可以很容易绕过这些限制，那对于需要出海并且满足CTS要求的厂商有什么影响呢？

> **先说结论：**对系统厂商APK没有任何影响，依然可调用任何API

- 第三方APK，受hide限制
- 系统platform签名APK，不受限制
- 非platform签名APK，集成在system分区，又在hiddenapi-package-whitelist.xml，不受限制。(且**目前**不影响CTS)

# 一、对第三方APK、系统APK的影响

| SDK28                                                   | @hide 浅灰 | @hide 黑名单 | @systemapi           |
| ------------------------------------------------------- | ---------- | ------------ | -------------------- |
| **非platform签名**                                      |            |              |                      |
| /data/app                                               | 是，警告   | 否           | 是，需permisison权限 |
| /system/app                                             | 是，警告   | 否           | 是，需permisison权限 |
| /system/priv-app                                        | 是，警告   | 否           | 是，需permisison权限 |
| hiddenapi-package-whitelist.xml (/system/app、priv-app) | 是         | 是           | 是，需permisison权限 |
| **platform签名**                                        |            |              |                      |
| /data/app /system/app /system/priv-app                  | 是         | 是           | 是，需permisison权限 |

# 二、新增hiddenapi-package-whitelist.xml名单，能否通过CTS？

````xml
<!-- https://android.googlesource.com/platform/frameworks/base/+/master/data/etc/hiddenapi-package-whitelist.xml -->
<config>
  <hidden-api-whitelisted-app package="android.ext.services" />
  ...
</config>
````

实测无影响。
但不确定google后续CTS版本是否加强检查，**有风险**。

相关测试项：
CtsHiddenApiBlacklistApi27TestCases
CtsHiddenApiBlacklistCurrentApiTestCases
CtsHiddenApiBlacklistDebugClassTestCases
CtsHiddenApiKillswitchDebugClassTestCases
CtsHiddenApiKillswitchWhitelistTestCases
CtsHiddenApiKillswitchWildcardTestCases

# 三、Hide API限制原理

详细的原理牵扯到编译时、运行时，还是比较复杂的，下面仅从较宏观的角度阐明受限原理、加白原理。

**a.访问受限原理**
hiddenapi-light-greylist.txt包含的api，会在dex中对应的Method结构生成HiddenApiAccessFlags::kLightGreylist访问权限标记。

1. 生成正常framework dex
2. Hiddenapi工具根据hiddenapi-light-greylist.txt等配置文件对dex的access_flags进行修改
3. 新的带access标记的framework dex

ART通过access_flags判断是否可以调用：

```kotlin
  Action action = GetActionFromAccessFlags(member->GetHiddenApiAccessFlags());
  if (action == kAllow) {
    return action;
  }
```

**b.加白不受限原理**

构造ApplicationInfo时会判断platform签名、hide-package-whitelist，来确定HIDDEN_API_ENFORCEMENT的flag

```java
private boolean isAllowedToUseHiddenApis() {
return isSignedWithPlatformKey()
|| (isPackageWhitelistedForHiddenApis() && (isSystemApp() || isUpdatedSystemApp()));
}
```

ActivityManagerService中startProcessLocked()启动进程时会把是否检查hide api的flag传给zygote

```dart
@HiddenApiEnforcementPolicy int policy =app.info.getHiddenApiEnforcementPolicy();
int policyBits = (policy << Zygote.API_ENFORCEMENT_POLICY_SHIFT);
runtimeFlags |= policyBits;
```

fork新的app进程后，调用ZygoteHooks_nativePostForkChild( )，初始化art虚拟机参数hidden_api_policy_，设置不进行hide api检查的kNoChecks选项。

