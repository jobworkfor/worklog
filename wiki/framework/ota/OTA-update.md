# OTA升级原理

## ota 基本原理

OTA（Over－the－Air Technology）空中下载技术
现在ota 基本是AB 分区的 ，在系统正常运行的时候进行升级，升级之后启动对应的升级之后的分区。 之前最早的时候只有一个分区， 是recovery 升级，就本质而言，都类似，因此下面介绍recovery source code

终端ota 升级流程

```css
* 1.1 系统运行时获取升级包，可以从服务端下载，也可以直接拷贝到SD卡中
  * 1.2 获取升级包路径，验证签名，通过installPackage接口升级
* 1.3 系统重启进入Recovery模式
  * 1.4 在install.cpp进行升级操作
    * 1.5 try_update_binary执行升级脚本
      * 1.6 finish_recovery，重启
```

### 1.1 获取升级包

`device` 可以设计如何从服务器获取 `update.zip` 升级包，因为每一个公司的服务器不同， 升级的 `apk` 设计也不一样，目的就是获取 `update.zip` 差分升级包。然后进入`Recovery`，继续后续升级流程。

### 1.2 installPackage 接口升级

下面verifyPackage 校验文件，签名，如果不对抛出异常，实际在recovery阶段还是会进行校验升级文件
frameworks/base/core/java/android/os/RecoverySystem.java@verifyPackage

```java
197    /**
198     * Verify the cryptographic signature of a system update package
199     * before installing it.  Note that the package is also verified
200     * separately by the installer once the device is rebooted into
201     * the recovery system.  This function will return only if the
202     * package was successfully verified; otherwise it will throw an
203     * exception.
204     *
205     * Verification of a package can take significant time, so this
206     * function should not be called from a UI thread.  Interrupting
207     * the thread while this function is in progress will result in a
208     * SecurityException being thrown (and the thread's interrupt flag
209     * will be cleared).
210     *
211     * @param packageFile  the package to be verified
212     * @param listener     an object to receive periodic progress
213     * updates as verification proceeds.  May be null.
214     * @param deviceCertsZipFile  the zip file of certificates whose
215     * public keys we will accept.  Verification succeeds if the
216     * package is signed by the private key corresponding to any
217     * public key in this file.  May be null to use the system default
218     * file (currently "/system/etc/security/otacerts.zip").
219     *
220     * @throws IOException if there were any errors reading the
221     * package or certs files.
222     * @throws GeneralSecurityException if verification failed
223     */
 public static void verifyPackage(File packageFile,---》升级文件名字
                                     ProgressListener listener,
                                     File deviceCertsZipFile)
        throws IOException, GeneralSecurityException {
        final long fileLen = packageFile.length();

        final RandomAccessFile raf = new RandomAccessFile(packageFile, "r");
        try {
            final long startTimeMillis = System.currentTimeMillis();
            if (listener != null) {
                listener.onProgress(0);---->进度监听
            }

            // Parse the signature------》解析签名
            PKCS7 block =
                new PKCS7(new ByteArrayInputStream(eocd, commentSize+22-signatureStart, signatureStart));

            // Take the first certificate from the signature (packages
            // should contain only one).
            X509Certificate[] certificates = block.getCertificates();
            if (certificates == null || certificates.length == 0) {
                throw new SignatureException("signature contains no certificates");
            }
            X509Certificate cert = certificates[0];
            PublicKey signatureKey = cert.getPublicKey();

            // Check that the public key of the certificate contained
            // in the package equals one of our trusted public keys.
            boolean verified = false;
            //deviceCertsZipFile  ----->签名文件
            HashSet<X509Certificate> trusted = getTrustedCerts(
                deviceCertsZipFile == null ? DEFAULT_KEYSTORE : deviceCertsZipFile);
            for (X509Certificate c : trusted) {
                if (c.getPublicKey().equals(signatureKey)) {
                    verified = true;
                    break;
                }
            }
            if (!verified) {
                throw new SignatureException("signature doesn't match any trusted key");
            }

            // The signature cert matches a trusted key.  Now verify that
            // the digest in the cert matches the actual file data.
            raf.seek(0);
   
........
            final boolean interrupted = Thread.interrupted();
            if (listener != null) {
                listener.onProgress(100);
            }

            if (interrupted) {
                throw new SignatureException("verification was interrupted");
            }

            if (verifyResult == null) {
                throw new SignatureException("signature digest verification failed");
            }
        } finally {
            raf.close();
        }

        // Additionally verify the package compatibility.
        if (!readAndVerifyPackageCompatibilityEntry(packageFile)) {
            throw new SignatureException("package compatibility verification failed");---->抛出异常
        }
    }
```

主要功能清空上一次 UNCRYPT_PACKAGE_FILE, 校验过后，进入系统的recovery 引导模式
frameworks/base/core/java/android/os/ RecoverySystem.java@installPackage

```dart
    /**
     * If the package hasn't been processed (i.e. uncrypt'd), set up
     * UNCRYPT_PACKAGE_FILE and delete BLOCK_MAP_FILE to trigger uncrypt during the
     * reboot.
     *
     * @param context      the Context to use
     * @param packageFile  the update package to install.  Must be on a
     * partition mountable by recovery.
     * @param processed    if the package has been processed (uncrypt'd).
     *
     * @throws IOException if writing the recovery command file fails, or if
     * the reboot itself fails.
     *
     * @hide
     */
    @SystemApi
    @RequiresPermission(android.Manifest.permission.RECOVERY)
    public static void installPackage(Context context, File packageFile, boolean processed)
            throws IOException {
        synchronized (sRequestLock) {
            LOG_FILE.delete();
            // Must delete the file in case it was created by system server.
            UNCRYPT_PACKAGE_FILE.delete();  ----》 清空UNCRYPT_PACKAGE_FILE

            String filename = packageFile.getCanonicalPath();---》 获取升级文件名字
            Log.w(TAG, "!!! REBOOTING TO INSTALL " + filename + " !!!");

            // If the package name ends with "_s.zip", it's a security update.
            boolean securityUpdate = filename.endsWith("_s.zip");
            // If the package is on the /data partition, the package needs to
            // be processed (i.e. uncrypt'd). The caller specifies if that has
            // been done in 'processed' parameter.
            if (filename.startsWith("/data/")) {
                if (processed) {
                    if (!BLOCK_MAP_FILE.exists()) {
                        Log.e(TAG, "Package claimed to have been processed but failed to find "
                                + "the block map file.");
                        throw new IOException("Failed to find block map file");
                    }
                } else {
                    FileWriter uncryptFile = new FileWriter(UNCRYPT_PACKAGE_FILE);
                    try {
                        uncryptFile.write(filename + "\n");
                    } finally {
                        uncryptFile.close();
                    }
                    // UNCRYPT_PACKAGE_FILE needs to be readable and writable
                    // by system server.
                    if (!UNCRYPT_PACKAGE_FILE.setReadable(true, false)
                            || !UNCRYPT_PACKAGE_FILE.setWritable(true, false)) {
                        Log.e(TAG, "Error setting permission for " + UNCRYPT_PACKAGE_FILE);
                    }

                    BLOCK_MAP_FILE.delete();
                }

                // If the package is on the /data partition, use the block map
                // file as the package name instead.
                filename = "@/cache/recovery/block.map";
            }
            final String filenameArg = "--update_package=" + filename + "\n";
            final String localeArg = "--locale=" + Locale.getDefault().toLanguageTag() + "\n";
            final String securityArg = "--security\n";

            String command = filenameArg + localeArg;
            if (securityUpdate) {
                command += securityArg;
            }

            RecoverySystem rs = (RecoverySystem) context.getSystemService(
                    Context.RECOVERY_SERVICE);
            if (!rs.setupBcb(command)) { ----》设定重启参数 --->bootCommand
                throw new IOException("Setup BCB failed");
            }
            // Having set up the BCB (bootloader control block), go ahead and reboot
            PowerManager pm = (PowerManager) context.getSystemService(Context.POWER_SERVICE);
            String reason = PowerManager.REBOOT_RECOVERY_UPDATE;

            // On TV, reboot quiescently if the screen is off
            if (context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_LEANBACK)) {
                WindowManager wm = (WindowManager) context.getSystemService(Context.WINDOW_SERVICE);
                if (wm.getDefaultDisplay().getState() != Display.STATE_ON) {
                    reason += ",quiescent";
                }
            }
            pm.reboot(reason);----> 引导系统进入recovery模式
            throw new IOException("Reboot failed (no permissions?)");
        }
    }
```

frameworks/base/core/java/android/os/ RecoverySystem.java@bootCommand

```java
     * Reboot into the recovery system with the supplied argument.
     * @param args to pass to the recovery utility.
     * @throws IOException if something goes wrong.
     */
    private static void bootCommand(Context context, String... args) throws IOException {
        LOG_FILE.delete();

        StringBuilder command = new StringBuilder();
        for (String arg : args) {
            if (!TextUtils.isEmpty(arg)) {
                command.append(arg);
                command.append("\n");
            }
        }

        // Write the command into BCB (bootloader control block) and boot from
        // there. Will not return unless failed.
        RecoverySystem rs = (RecoverySystem) context.getSystemService(Context.RECOVERY_SERVICE);
        rs.rebootRecoveryWithCommand(command.toString());

        throw new IOException("Reboot failed (no permissions?)");
    }
```

### 1.3 系统重启进入Recovery模式

 这个时候手机进入了重启，进入了recovery
 bootable/recovery/recovery.cpp

```cpp
int main(int argc, char **argv) {
    android::base::InitLogging(argv, &UiLogger);---->log 打印 终端
    .......
    case 'u': update_package = optarg; break;----》读取recovery 之前的参数，进入update 升级, 参考OPTIONS

    locale = load_locale_from_cache();---》从cache 读取update.zip 

    ui = new StubRecoveryUI();  ---->new 升级进度显示

    ui->SetBackground(RecoveryUI::NONE);------>升级进度条显示

    selinux_android_set_sehandle(sehandle);---->selinux

    device->StartRecovery();  ---》开始升级

    if(do_sdcard_mount_for_ufs() != 0) {----->sdcard mount

    if (!is_battery_ok()) {-----》检测电量

    status = install_package(update_package, &should_wipe_cache,------->进入了install_package

    finish_recovery();-----》升级完成，重启
}
```

bootable/recovery/recovery.cpp@OPTIONS

```cpp
static const struct option OPTIONS[] = {
  { "update_package", required_argument, NULL, 'u' },
  { "retry_count", required_argument, NULL, 'n' },
  { "wipe_data", no_argument, NULL, 'w' },
  { "wipe_cache", no_argument, NULL, 'c' },
  { "show_text", no_argument, NULL, 't' },
  { "sideload", no_argument, NULL, 's' },
  { "sideload_auto_reboot", no_argument, NULL, 'a' },
  { "just_exit", no_argument, NULL, 'x' },
  { "locale", required_argument, NULL, 'l' },
  { "shutdown_after", no_argument, NULL, 'p' },
  { "reason", required_argument, NULL, 'r' },
  { "security", no_argument, NULL, 'e'},
  { "wipe_ab", no_argument, NULL, 0 },
  { "wipe_package_size", required_argument, NULL, 0 },
  { "prompt_and_wipe_data", no_argument, NULL, 0 },
  { NULL, 0, NULL, 0 },
};
```

### 1.4 在install.cpp进行升级操作

 bootable/recovery/ install.cpp@install_package

```cpp
int install_package(const std::string& path, bool* wipe_cache, const std::string& install_file,
                    bool needs_mount, int retry_count) {
..........
    if (result != 0) {
    LOG(ERROR) << "failed to set up expected mounts for install; aborting";
    result = INSTALL_ERROR;
  } else {
    result = really_install_package(path, wipe_cache, needs_mount, &log_buffer, retry_count,
                                    &max_temperature);------>进入下一步的升级过程
  } 
......
  return result;
}
```

真正的升级在下面的函数中实现
 bootable/recovery/ install.cpp@really_install_package

```cpp
static int really_install_package(const std::string& path, bool* wipe_cache, bool needs_mount,
                                  std::vector<std::string>* log_buffer, int retry_count,
                                  int* max_temperature) {
  ui->SetBackground(RecoveryUI::INSTALLING_UPDATE);
  ui->Print("Finding update package...\n");
  // Give verification half the progress bar...
  ui->SetProgressType(RecoveryUI::DETERMINATE);
  ui->ShowProgress(VERIFICATION_PROGRESS_FRACTION, VERIFICATION_PROGRESS_TIME);
  LOG(INFO) << "Update location: " << path;

  // Map the update package into memory.
  ui->Print("Opening update package...\n");

  // Verify package.
  if (!verify_package(map.addr, map.length)) {----》校验update .zip 
    log_buffer->push_back(android::base::StringPrintf("error: %d", kZipVerificationFailure));
    return INSTALL_CORRUPT;
  }

  // Try to open the package.
  ZipArchiveHandle zip;
  int err = OpenArchiveFromMemory(map.addr, map.length, path.c_str(), &zip);
  if (err != 0) {
    LOG(ERROR) << "Can't open " << path << " : " << ErrorCodeString(err);
    log_buffer->push_back(android::base::StringPrintf("error: %d", kZipOpenFailure));

    CloseArchive(zip);
    return INSTALL_CORRUPT;
  }

  // Additionally verify the compatibility of the package.
  if (!verify_package_compatibility(zip)) {
    log_buffer->push_back(android::base::StringPrintf("error: %d", kPackageCompatibilityFailure));
    CloseArchive(zip);
    return INSTALL_CORRUPT;
  }

  // Verify and install the contents of the package.
  ui->Print("Installing update...\n");----->开始实际升级
  if (retry_count > 0) {
    ui->Print("Retry attempt: %d\n", retry_count);
  }
  ui->SetEnableReboot(false);
  int result = try_update_binary(path, zip, wipe_cache, log_buffer, retry_count, ----》 升级中max_temperature);
  ui->SetEnableReboot(true);---》 升级完成reboot 
  ui->Print("\n");

  CloseArchive(zip);
  return result;
}
```

### 1.5 try_update_binary执行升级脚本

 bootable/recovery/install.cpp@try_update_binary

```cpp
// If the package contains an update binary, extract it and run it.
static int try_update_binary(const std::string& package, ZipArchiveHandle zip, bool* wipe_cache,
                             std::vector<std::string>* log_buffer, int retry_count,
                             int* max_temperature) {
  read_source_target_build(zip, log_buffer);

  int pipefd[2];
  pipe(pipefd);

  std::vector<std::string> args;
#ifdef AB_OTA_UPDATER
  int ret = update_binary_command(package, zip, "/sbin/update_engine_sideload", retry_count,
                                  pipefd[1], &args);
#else
  int ret = update_binary_command(package, zip, "/tmp/update-binary", retry_count, pipefd[1],
                                  &args);
#endif
  if (ret) {
    close(pipefd[0]);
    close(pipefd[1]);
    return ret;
  }

  // When executing the update binary contained in the package, the
  // arguments passed are:
  //
  //   - the version number for this interface
  //
  //   - an FD to which the program can write in order to update the
  //     progress bar.  The program can write single-line commands:
  //
  //        progress <frac> <secs>
  //            fill up the next <frac> part of of the progress bar
  //            over <secs> seconds.  If <secs> is zero, use
  //            set_progress commands to manually control the
  //            progress of this segment of the bar.
  //
  //        set_progress <frac>
  //            <frac> should be between 0.0 and 1.0; sets the
  //            progress bar within the segment defined by the most
  //            recent progress command.
  //
  //        ui_print <string>
  //            display <string> on the screen.
  //
  //        wipe_cache
  //            a wipe of cache will be performed following a successful
  //            installation.
  //
  //        clear_display
  //            turn off the text display.
  //
  //        enable_reboot
  //            packages can explicitly request that they want the user
  //            to be able to reboot during installation (useful for
  //            debugging packages that don't exit).
  //
  //        retry_update
  //            updater encounters some issue during the update. It requests
  //            a reboot to retry the same package automatically.
  //
  //        log <string>
  //            updater requests logging the string (e.g. cause of the
  //            failure).
  //
  //   - the name of the package zip file.
  //
  //   - an optional argument "retry" if this update is a retry of a failed
  //   update attempt.
  //

  // Convert the vector to a NULL-terminated char* array suitable for execv.
  const char* chr_args[args.size() + 1];
  chr_args[args.size()] = nullptr;
  for (size_t i = 0; i < args.size(); i++) {
    chr_args[i] = args[i].c_str();
  }

  pid_t pid = fork();
  if (pid == -1) {
    close(pipefd[0]);
    close(pipefd[1]);
    PLOG(ERROR) << "Failed to fork update binary";
    return INSTALL_ERROR;
  }

  if (pid == 0) {
    umask(022);
    close(pipefd[0]);
    execv(chr_args[0], const_cast<char**>(chr_args));--->使用子进程进行执行升级
    // Bug: 34769056
    // We shouldn't use LOG/PLOG in the forked process, since they may cause
    // the child process to hang. This deadlock results from an improperly
    // copied mutex in the ui functions.
    fprintf(stdout, "E:Can't run %s (%s)\n", chr_args[0], strerror(errno));
    _exit(EXIT_FAILURE);
  }
  close(pipefd[1]);

  std::atomic<bool> logger_finished(false);
  std::thread temperature_logger(log_max_temperature, max_temperature, std::ref(logger_finished));

  *wipe_cache = false;
  bool retry_update = false;

  char buffer[1024];
  FILE* from_child = fdopen(pipefd[0], "r");
  while (fgets(buffer, sizeof(buffer), from_child) != nullptr) {
    std::string line(buffer);
    size_t space = line.find_first_of(" \n");
    std::string command(line.substr(0, space));
    if (command.empty()) continue;

    // Get rid of the leading and trailing space and/or newline.
    std::string args = space == std::string::npos ? "" : android::base::Trim(line.substr(space));

    if (command == "progress") {
      std::vector<std::string> tokens = android::base::Split(args, " ");
      double fraction;
      int seconds;
      if (tokens.size() == 2 && android::base::ParseDouble(tokens[0].c_str(), &fraction) &&
          android::base::ParseInt(tokens[1], &seconds)) {
        ui->ShowProgress(fraction * (1 - VERIFICATION_PROGRESS_FRACTION), seconds);
      } else {
        LOG(ERROR) << "invalid \"progress\" parameters: " << line;
      }
    } else if (command == "set_progress") {--》在主进程中执行显示升级的progress
      std::vector<std::string> tokens = android::base::Split(args, " ");
      double fraction;
      if (tokens.size() == 1 && android::base::ParseDouble(tokens[0].c_str(), &fraction)) {
        ui->SetProgress(fraction);
      } else {
        LOG(ERROR) << "invalid \"set_progress\" parameters: " << line;
      }
    } else if (command == "ui_print") {
      ui->PrintOnScreenOnly("%s\n", args.c_str());
      fflush(stdout);
    } else if (command == "wipe_cache") {
      *wipe_cache = true;
    } else if (command == "clear_display") {
      ui->SetBackground(RecoveryUI::NONE);
    } else if (command == "enable_reboot") {
      // packages can explicitly request that they want the user
      // to be able to reboot during installation (useful for
      // debugging packages that don't exit).
      ui->SetEnableReboot(true);
    } else if (command == "retry_update") {
      retry_update = true;
    } else if (command == "log") {
      if (!args.empty()) {
        // Save the logging request from updater and write to last_install later.
        log_buffer->push_back(args);
      } else {
        LOG(ERROR) << "invalid \"log\" parameters: " << line;
      }
    } else {
      LOG(ERROR) << "unknown command [" << command << "]";
    }
  }
  fclose(from_child);

  int status;
  waitpid(pid, &status, 0);

  logger_finished.store(true);
  finish_log_temperature.notify_one();
  temperature_logger.join();

  if (retry_update) {
    return INSTALL_RETRY;
  }
  if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
    LOG(ERROR) << "Error in " << package << " (Status " << WEXITSTATUS(status) << ")";
    return INSTALL_ERROR;
  }

  return INSTALL_SUCCESS;
}
```

### 1.6 finish_recovery，重启

 升级完成后保存Log  ，reboot

```cpp
int main(int argc, char **argv) {
    ..........升级完成...... 
    // Save logs and clean up before rebooting or shutting down.
    finish_recovery(); 
    .....
}
```

## 2 制作update.zip AB 分区

本部分主要介绍，如何制作ota 升级包

* 全量升级包
* 增量升级包

### 2.1 全量升级包

```bash
source build/envsetup.sh
lunch <target-config>
make otapackage -j8
```

全量升级包路径:`out/target/product/sdm845/sdm845-ota-eng.zip`
 在build 完成后，产生制作增量升级的source files ， 文件路径是：
 `out/target/product/sdm845/obj/PACKAGING/target_files_intermediates/dm845-target_files-eng.zip`

### 2.2 增量升级包

 `/build/tools/releasetools/ota_from_target_files –v –-block -p out/host/ linux-x86 -k build/target/product/security/testkey -i path_to_target_files_v1.zip path_to_target_files_v2.zip update.zip`
 其中 ：path_to_target_files_v1.zip与path_to_target_files_v2.zip就是上面做全量包时候产生的文件target_files

**备注1**
 上面的制作方式，只是在 android 部分，如果包含了第三方文件怎么版本。例如 高通的bp 中的modem bt 等等做差分。
 高通bp 差分包之前需要做的事情，就是把bp build 完整，然后copy 生成的bin 到android的ration  目录下。 然后执行2.1, 2.2  部分就可以了

mkdir RADIO 文件夹 在/device/qcom/<target>/.
copy non-HLOS.mbn, tz.mbn, rpm.mbn,  等等到 RADIO 文件夹

```csharp
common/build/ufs/bin/asic/NON-HLOS.bin modem.img
common/build/ufs/bin/BTFM.bin bluetooth.img
common/build/ufs/bin/asic/dspso.bin dsp.img
boot_images/QcomPkg/SDM845Pkg/Bin/845/LA/RELEASE/xbl.elf xbl.img
boot_images/QcomPkg/SDM845Pkg/Bin/845/LA/RELEASE/xbl_config.elf xbl_config.img
trustzone_images/build/ms/bin/WAXAANAA/tz.mbn tz.img
aop_proc/build/ms/bin/AAAAANAZO/aop.mbn aop.img
trustzone_images/build/ms/bin/WAXAANAA/hyp.mbn hyp.img
trustzone_images/build/ms/bin/WAXAANAA/keymaster64.mbn keymaster.img
trustzone_images/build/ms/bin/WAXAANAA/cmnlib.mbn cmnlib.img
trustzone_images/build/ms/bin/WAXAANAA/cmnlib64.mbn cmnlib64.img
LINUX/android/out/target/product/sdm845/abl.elf abl.img
trustzone_images/build/ms/bin/WAXAANAA/devcfg.mbn devcfg.img
common/core_qupv3fw/sdm845/rel/1.0/qupv3fw.elf qupfw.img
trustzone_images/build/ms/bin/WAXAANAA/storsec.mbn storsec.img
LINUX/android/out/target/product/sdm845/vbmeta.img vbmeta.img
LINUX/android/out/target/product/sdm845/dtbo.img dtbo.img
boot_images/QcomPkg/SDM845Pkg/Bin/845/LA/RELEASE/imagefv.elf ImageFv.img
```

对应关系：

```csharp
    NON-HLOS.bin /dev/block/bootdevice/by-name/modem
    BTFM.bin /dev/block/bootdevice/by-name/bluetooth
    dspso.bin /dev/block/bootdevice/by-name/dsp 
    mdtpsecapp.mbn /dev/block/bootdevice/by-name/mdtpsecapp
    mdtp.img /dev/block/bootdevice/by-name/mdtp
    xbl.elf /dev/block/bootdevice/by-name/xbl
    xbl_config.elf /dev/block/bootdevice/by-name/xbl_config
    tz.mbn /dev/block/bootdevice/by-name/tz
    aop.mbn /dev/block/bootdevice/by-name/aop
    hyp.mbn /dev/block/bootdevice/by-name/hyp
    keymaster64.mbn /dev/block/bootdevice/by-name/keymaster
    cmnlib.mbn /dev/block/bootdevice/by-name/cmnlib
    cmnlib64.mbn /dev/block/bootdevice/by-name/cmnlib64
    abl.elf /dev/block/bootdevice/by-name/abl
    devcfg.mbn /dev/block/bootdevice/by-name/devcfg
    qupv3fw.elf /dev/block/bootdevice/by-name/qupfw
    storsec.mbn /dev/block/bootdevice/by-name/storsec
    vbmeta.img /dev/block/bootdevice/by-name/vbmeta
    dtbo.img /dev/block/bootdevice/by-name/dtbo
    imagefv.elf /dev/block/bootdevice/by-name/ImageFv
make AB_OTA_PARTITIONS="abl aop bluetooth cmnlib64 cmnlib devcfg dsp hyp keymaster modem qupfw tz xbl boot system vendor xbl_config dtbo vbmeta storsec ImageFv" -j
```

**备注2:**
 如果升级差分包失败，考虑base版本是否fastboot 下面的路径版本
 `out/target/product/sdm845/obj/PACKAGING/target_files_intermediates`

## FAQ

### 通过ADB命令进行OTA升级

````bash
adb push ./update-xxxx.zip /data/update.zip
echo “–update_package=/data/update.zip” > /cache/recovery/command
reboot recovery
````

### Framework中OTA测试程序

````java
// http://androidxref.blackshark.com:8088/sm8250/xref/tools/tradefederation/core/src/com/android/tradefed/targetprep/SystemUpdaterDeviceFlasher.java#105
85    private boolean installUpdate(ITestDevice device, IDeviceBuildInfo deviceBuild)
86            throws DeviceNotAvailableException, TargetSetupError {
105->      String commands =
106                "echo --update_package > /cache/recovery/command &&" +
107                // FIXME would need to be "CACHE:" instead of "/cache/" for
108                // eclair devices
109                "echo /cache/update.zip >> /cache/recovery/command";
110        device.executeShellCommand(commands);
111        device.rebootIntoRecovery();
112        device.waitForDeviceAvailable();
113        return true;
114    }
115
````
