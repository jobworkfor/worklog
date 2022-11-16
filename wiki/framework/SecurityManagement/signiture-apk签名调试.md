## 问题描述

```
sfb-apk:399:SYSTEM/app/HTMLViewer/
sfb-apk:399:SYSTEM/app/HTMLViewer/HTMLViewer.apk
sfb-apk:432:key=build/target/product/security/releasekey,common.SPECIAL_CERT_STRINGS=('PRESIGNED', 'EXTERNAL')
    signing: HTMLViewer.apk                                    (build/target/product/security/releasekey)

   ERROR: Failed to run signapk.jar: return code 1:
[main] INFO com.xiaomi.keycenter.agent.client.KeycenterAgentClient - create KeycenterAgentClient instance
[main] WARN com.xiaomi.common.perfcounter.PerfCounterProvider - Failed to load job name config file:/.JOBNAME.
[main] WARN com.xiaomi.common.perfcounter.PerfCounterProvider - Failed to open perf counter config file:/perfcounter.properties, use the default value, step:300, push_on:true
java.security.SignatureException: Signer #1 failed
 at com.android.signapk.ApkSignerV2.generateApkSignatureSchemeV2Block(ApkSignerV2.java:416)
 at com.android.signapk.ApkSignerV2.generateApkSigningBlock(ApkSignerV2.java:364)
 at com.android.signapk.ApkSignerV2.sign(ApkSignerV2.java:232)
 at com.android.signapk.SignApk.main(SignApk.java:1147)
Caused by: java.security.SignatureException: Failed to verify generated SHA256withRSA signature using public key from certificate
 at com.android.signapk.ApkSignerV2.generateSignerBlock(ApkSignerV2.java:542)
 at com.android.signapk.ApkSignerV2.generateApkSignatureSchemeV2Block(ApkSignerV2.java:412)
 ... 3 more
Caused by: java.security.SignatureException: Signature did not verify
 at com.android.signapk.ApkSignerV2.generateSignerBlock(ApkSignerV2.java:535)
 ... 4 more
 
reason:
在target-file.zip文件中的 META/apkcerts.txt文件搜到这一行.
1194:    name="HTMLViewer.apk" certificate="build/target/product/security/releasekey.x509.pem" private_key="build/target/product/security/releasekey.pk8"
HTMLViewer.apk对应的是releasekey, 但是脚本tools/releasetools/sign_target_files_apks.py 里面没有对应的一个转换.
 
 
fix:
http://gerrit.blackshark.com:8080/#/c/130189/2/tools/releasetools/sign_target_files_apks.py.
tools/releasetools/sign_target_files_apks.py
918	927	       OPTIONS.key_map.update({
919		-          devkeydir + "/testkey":  d + "/releasekey",
920		-          devkeydir + "/devkey":   d + "/releasekey",
928	+          devkeydir + "/testkey":      d + "/releasekey",
929	+          devkeydir + "/devkey":       d + "/releasekey",
930	+          devkeydir + "/releasekey":   d + "/releasekey",
921	931	           devkeydir + "/media":    d + "/media",
922	932	           devkeydir + "/shared":   d + "/shared",
923	933	           devkeydir + "/platform": d + "/platform",
924	934	           "device/qcom/sepolicy/generic/vendor/timeservice" + "/timeservice_app_cert" : d + "/timese
rvice",
```





### 查看签名信息

```bash
D:\MoGu\imgupack\2_pass\system\app\HTMLViewer\HTMLViewer.apk>keytool -printcert -file META-INF/CERT.RSA
所有者: EMAILADDRESS=buildfarm@blackshark.com, CN=blackshark, OU=CM, O=blackshark, L=ShangHai, ST=ShangHai, C=CN
发布者: EMAILADDRESS=buildfarm@blackshark.com, CN=blackshark, OU=CM, O=blackshark, L=ShangHai, ST=ShangHai, C=CN
序列号: d69a86fbca48c9bc
生效时间: Sat Sep 15 12:22:36 CST 2018, 失效时间: Wed Jan 31 12:22:36 CST 2046
证书指纹:
         SHA1: 02:E5:16:F0:4C:23:44:48:69:7C:CE:FE:E9:DE:56:B5:52:22:05:FD
         SHA256: C8:36:F2:F2:E9:48:5F:8A:81:7F:EC:A2:30:74:51:55:6A:83:E3:3F:45:D0:76:B6:2D:E3:C2:24:47:02:06:88
签名算法名称: SHA256withRSA
主体公共密钥算法: 2048 位 RSA 密钥
版本: 3

扩展:

#1: ObjectId: 2.5.29.35 Criticality=false
AuthorityKeyIdentifier [
KeyIdentifier [
0000: 8E 21 3C 7E FF 2A 24 F4   8E 59 20 9D 52 68 26 68  .!<..*$..Y .Rh&h
0010: E1 90 1C 7F                                        ....
]
]

#2: ObjectId: 2.5.29.19 Criticality=false
BasicConstraints:[
  CA:true
  PathLen:2147483647
]

#3: ObjectId: 2.5.29.14 Criticality=false
SubjectKeyIdentifier [
KeyIdentifier [
0000: 8E 21 3C 7E FF 2A 24 F4   8E 59 20 9D 52 68 26 68  .!<..*$..Y .Rh&h
0010: E1 90 1C 7F                                        ....
]
]
```

### 查看x509.pem的指纹

````bash
bob.shen@RMSH21:~/work/SM8350_R_DEV_BSUI_20200916$ openssl x509 -in build/target/product/security/testkey.x509.pem -noout -fingerprint
SHA1 Fingerprint=61:ED:37:7E:85:D3:86:A8:DF:EE:6B:86:4B:D8:5B:0B:FA:A5:AF:81

bob.shen@RMSH21:~/work/SM8350_R_DEV_BSUI_20200916$ openssl x509 -in build/target/product/security/ -noout -fingerprint
Android.bp                 fsverity-release.x509.der  networkstack.pk8           platform.x509.pem          shared.x509.pem            verity_key                 
Android.mk                 media.pk8                  networkstack.x509.pem      README                     testkey.pk8                verity.pk8                 
bsp_verity.pem             media.x509.pem             platform.pk8               shared.pk8                 testkey.x509.pem           verity.x509.pem  

bob.shen@RMSH21:~/work/SM8350_R_DEV_BSUI_20200916$ openssl x509 -in build/target/product/security/platform.x509.pem -noout -fingerprint
SHA1 Fingerprint=27:19:6E:38:6B:87:5E:76:AD:F7:00:E7:EA:84:E4:C6:EE:E3:3D:FA
````

### 查看签名版本

```bash
D:\MoGu\imgupack\2_pass\system\app\HTMLViewer>java -jar C:\tools\android-sdk\build-tools\29.0.2\lib\apksigner.jar verify -v HTMLViewer.pass.apk
Verifies
Verified using v1 scheme (JAR signing): true
Verified using v2 scheme (APK Signature Scheme v2): true
Verified using v3 scheme (APK Signature Scheme v3): true
Number of signers: 1
```

### Android使用apksigner对apk进行v2签名

```
（1）先找到电脑中25或者25以上版本的SDK的build-tools\版本号的目录，并把需要签名的安装包放在该目录下。
（2）使用zipalign将安装包对齐：打开cmd，将目录切换到sdk的build-tools\版本号的目录下，使用zipalign -v -p 4 input.apk output.apk进行对其操作，其中input.apk是需要签名的安装包，output.apk是对齐之后的的安装包。
（3）把对齐后的安装包apk文件放到build-tools\版本号下的lib文件下，使用apksigner对安装包进行签名：打开cmd，将目录切换至当前目录下，
    使用如下命令：java -jar apksigner.jar sign --ks kestore的路径 --out output.apk input.apk 然后会提示输入keystore的密码，输入后回车即可完成签名。
（4）检查是否签名成功：依旧在当前目录下打开cmd，然后输入如下命令：java -jar apksigner.jar verify -v my.apk。如果v1 scheme和v2 scheme的值都为true，即表示签名成功。
```

