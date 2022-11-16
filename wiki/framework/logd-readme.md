
logd进程启动
----------------------------------------------------------------------------------------------------
```cpp
268on load_persist_props_action
269    load_persist_props
270    start logd
271    start logd-reinit
```
> http://127.0.0.1:8080/android-aosp/xref/system/core/rootdir/init.rc#268


```cpp
1 ->    service logd /system/bin/logd
2           socket logd stream 0666 logd logd
3           socket logdr seqpacket 0666 logd logd
4           socket logdw dgram+passcred 0222 logd logd
5           file /proc/kmsg r
6           file /dev/kmsg w
7           user logd
8           group logd system package_info readproc
9           writepid /dev/cpuset/system-background/tasks
10      
11->    service logd-reinit /system/bin/logd --reinit
12          oneshot
13          disabled
14          user logd
15          group logd
16          writepid /dev/cpuset/system-background/tasks
17      
18      on fs
19          write /dev/event-log-tags "# content owned by logd
20      "
21          chown logd logd /dev/event-log-tags
22          chmod 0644 /dev/event-log-tags
```
> http://127.0.0.1:8080/android-aosp/xref/system/core/logd/logd.rc

`load_persist_props_action`的触发在`init.rc`的`late-init`动作中。
```cpp
277# Mount filesystems and start core system services.
278on late-init
281    # Mount fstab in init.{$device}.rc by mount_all command. Optional parameter
282    # '--early' can be specified to skip entries with 'latemount'.
283    # /system and /vendor must be mounted by the end of the fs stage,
284    # while /data is optional.
285    trigger fs
...
302    # Load persist properties and override properties (if enabled) from /data.
303->  trigger load_persist_props_action
```
> http://127.0.0.1:8080/android-aosp/xref/system/core/rootdir/init.rc#278

`late-init`的触发在`init.cpp`中
```cpp
740    if (bootmode == "charger") {
741        am.QueueEventTrigger("charger");
742    } else {
743->      am.QueueEventTrigger("late-init");
744    }
```


Log Process
----------------------------------------------------------------------------------------------------
* [LIBLOG_ABI_PUBLIC int __android_log_print(int prio, const char* tag,](http://127.0.0.1:8080/android-aosp/xref/system/core/liblog/logger_write.c#491)
    * [return __android_log_write(prio, tag, buf);](http://127.0.0.1:8080/android-aosp/xref/system/core/liblog/logger_write.c#500)
        * [return __android_log_buf_write(LOG_ID_MAIN, prio, tag, msg);](http://127.0.0.1:8080/android-aosp/xref/system/core/liblog/logger_write.c#413)
            * [<b>return write_to_log(bufID, vec, 3);</b>](#write_to_log)
                * [<b>static int __write_to_log_init(log_id_t log_id, struct iovec* vec, size_t nr) {</b>](#__write_to_log_init)
                    * [__write_to_log_daemon(log_id, vec, nr);](http://127.0.0.1:8080/android-aosp/xref/system/core/liblog/logger_write.c#395)
                    
        

----------------------------------------------------------------------------------------------------
### <a id=write_to_log></a>write_to_log()
```cpp
416LIBLOG_ABI_PUBLIC int __android_log_buf_write(int bufID, int prio,
417                                              const char* tag, const char* msg) {
418  struct iovec vec[3];
419  char tmp_tag[32];
420
421  if (!tag) tag = "";
422
423  /* XXX: This needs to go! */
424  if (bufID != LOG_ID_RADIO) {
425    switch (tag[0]) {
426      case 'H':
427        if (strcmp(tag + 1, "HTC_RIL" + 1)) break;
428        goto inform;
429      case 'R':
430        /* Any log tag with "RIL" as the prefix */
431        if (strncmp(tag + 1, "RIL" + 1, strlen("RIL") - 1)) break;
432        goto inform;
433      case 'Q':
434        /* Any log tag with "QC_RIL" as the prefix */
435        if (strncmp(tag + 1, "QC_RIL" + 1, strlen("QC_RIL") - 1)) break;
436        goto inform;
437      case 'I':
438        /* Any log tag with "IMS" as the prefix */
439        if (strncmp(tag + 1, "IMS" + 1, strlen("IMS") - 1)) break;
440        goto inform;
441      case 'A':
442        if (strcmp(tag + 1, "AT" + 1)) break;
443        goto inform;
444      case 'G':
445        if (strcmp(tag + 1, "GSM" + 1)) break;
446        goto inform;
447      case 'S':
448        if (strcmp(tag + 1, "STK" + 1) && strcmp(tag + 1, "SMS" + 1)) break;
449        goto inform;
450      case 'C':
451        if (strcmp(tag + 1, "CDMA" + 1)) break;
452        goto inform;
453      case 'P':
454        if (strcmp(tag + 1, "PHONE" + 1)) break;
455      /* FALLTHRU */
456      inform:
457        bufID = LOG_ID_RADIO;
458        snprintf(tmp_tag, sizeof(tmp_tag), "use-Rlog/RLOG-%s", tag);
459        tag = tmp_tag;
460      /* FALLTHRU */
461      default:
462        break;
463    }
464  }
465
466#if __BIONIC__
467  if (prio == ANDROID_LOG_FATAL) {
468    android_set_abort_message(msg);
469  }
470#endif
471
472  vec[0].iov_base = (unsigned char*)&prio;
473  vec[0].iov_len = 1;
474  vec[1].iov_base = (void*)tag;
475  vec[1].iov_len = strlen(tag) + 1;
476  vec[2].iov_base = (void*)msg;
477  vec[2].iov_len = strlen(msg) + 1;
478
479->return write_to_log(bufID, vec, 3);
480}
```
> http://127.0.0.1:8080/android-aosp/xref/system/core/liblog/logger_write.c#479

### <a id=__write_to_log_init></a>write_to_log()
```cpp
39static int __write_to_log_init(log_id_t, struct iovec* vec, size_t nr);
40static int (*write_to_log)(log_id_t, struct iovec* vec,
41                           size_t nr) = __write_to_log_init;
```
> http://127.0.0.1:8080/android-aosp/xref/system/core/liblog/logger_write.c#40




