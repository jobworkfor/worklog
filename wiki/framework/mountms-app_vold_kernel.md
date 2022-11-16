app，vold，kernel的通信
======================


app <-> vold
----------------------------------------------------------------------------------------------------

java层顺序调用
```
PackageHelper.getSecureContainerList
getMountService().getSecureContainerList()
mConnector.executeForList("asec", "list"), VoldResponseCode.AsecListResult)
executeForList(DEFAULT_TIMEOUT, cmd, args)

makeCommand(rawBuilder, logBuilder, sequenceNumber, cmd, args);
final String rawCmd = rawBuilder.toString();
```

下发命令给vold
```
synchronized (mDaemonLock) {
    if (mOutputStream == null) {
    } else {
        try {
            mOutputStream.write(rawCmd.getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
        }
    }
}
```

/system/vold/CommandListener.cpp
```
int CommandListener::AsecCmd::runCommand(SocketClient *cli, int argc, char **argv)
if (!strcmp(argv[1], "list")) {
    dumpArgs(argc, argv, -1);

    listAsecsInDirectory(cli, VolumeManager::SEC_ASECDIR_EXT); // "/mnt/secure/asec"
    listAsecsInDirectory(cli, VolumeManager::SEC_ASECDIR_INT); // "/data/app-asec"
} 
```

返回消息给app层
```
void CommandListener::AsecCmd::listAsecsInDirectory(SocketClient *cli, const char *directory) {
    while (!readdir_r(d, dent, &result) && result != NULL) {
        if (name_len > 5 && name_len < 260 &&
                !strcmp(&dent->d_name[name_len - 5], ".asec")) {
            cli->sendMsg(ResponseCode::AsecListResult, id, false);
        }
    }
}
```

ref: https://max.book118.com/html/2015/0327/13876433.shtm


