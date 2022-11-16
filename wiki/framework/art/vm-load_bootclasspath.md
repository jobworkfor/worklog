# `Dalvik`加载java类

本文基于源码：[android 2.3.7](http://androidxref.com/2.3.7/)

## Android init.rc BOOTCLASSPATH
<pre style="background: #555555; color: #ffffff">
BOOTCLASSPATH定义了Java库所在的路径，在虚拟机加载Java库时使用。
</pre>
`BOOTCLASSPATH`不添加`jar`包路径，系统启动后将无法找到自定义JAVA层系统服务的相关类，这是由于自定义系统服务jar包是`Dalvik`所需的基本库文件。如果不添加相关路径会报如下错误：

    W/dalvikvm( 2582): Unable to resolve superclass of Lcom/android/server/yourdir/yourService; (1633)
    W/dalvikvm( 2582): Link of class 'Lcom/android/server/yourdir/yourService;' failed
    D/dalvikvm( 2582): DexOpt: unable to opt direct call 0x276b at 0x258 in Lcom/android/server/ServerThread;.run

### init.rc

[/system/core/rootdir/init.rc](http://androidxref.com/2.3.7/xref/system/core/rootdir/init.rc)
```c
# setup the global environment
    ...
    export BOOTCLASSPATH /system/framework/core.jar:/system/framework/bouncycastle.jar:/system/framework/ext.jar:/system/framework/framework.jar:/system/framework/android.policy.jar:/system/framework/services.jar:/system/framework/core-junit.jar
```

### Init.c

[/dalvik/vm/Init.c](http://androidxref.com/2.3.7/xref/dalvik/vm/Init.c#1010)
```c
/*
 * Set defaults for fields altered or modified by arguments.
 * Globals are initialized to 0 (a/k/a NULL or false).
 */
static void setCommandLineDefaults()
{
    ...
    envStr = getenv("BOOTCLASSPATH");
    if (envStr != NULL)
        gDvm.bootClassPathStr = strdup(envStr);
    else
        gDvm.bootClassPathStr = strdup(".");
    ...
}
```



### Class.c

[/dalvik/vm/oo/Class.c](http://androidxref.com/2.3.7/xref/dalvik/vm/oo/Class.c#304)
```c
/*
 * Initialize the bootstrap class loader.
 *
 * Call this after the bootclasspath string has been finalized.
 */
bool dvmClassStartup(void)
{
    ...
    /*
     * Process the bootstrap class path.  This means opening the specified
     * DEX or Jar files and possibly running them through the optimizer.
     */
    assert(gDvm.bootClassPath == NULL);
    processClassPath(gDvm.bootClassPathStr, true);

    if (gDvm.bootClassPath == NULL)
        return false;

    return true;
}
```


[/dalvik/vm/oo/Class.c](http://androidxref.com/2.3.7/xref/dalvik/vm/oo/Class.c#528)
```c
/*
 * Convert a colon-separated list of directories, Zip files, and DEX files
 * into an array of ClassPathEntry structs.
 *
 * During normal startup we fail if there are no entries, because we won't
 * get very far without the basic language support classes, but if we're
 * optimizing a DEX file we allow it.
 *
 * If entries are added or removed from the bootstrap class path, the
 * dependencies in the DEX files will break, and everything except the
 * very first entry will need to be regenerated.
 */
static ClassPathEntry* processClassPath(const char* pathStr, bool isBootstrap)
{
    ClassPathEntry* cpe = NULL;
    cpe = (ClassPathEntry*) calloc(count+1, sizeof(ClassPathEntry));

    while (cp < end) {
        if (*cp == '\0') {
            /* leading, trailing, or doubled ':'; ignore it */
        } else {
            if (!prepareCpe(&tmp, isBootstrap)) {
                /* drop from list and continue on */
                free(tmp.fileName);
            } else {
                ...
            }
        }
    }
}
```
[/dalvik/vm/oo/Class.c](http://androidxref.com/2.3.7/xref/dalvik/vm/oo/Class.c#477)
```c
/*
 * Prepare a ClassPathEntry struct, which at this point only has a valid
 * filename.  We need to figure out what kind of file it is, and for
 * everything other than directories we need to open it up and see
 * what's inside.
 */
static bool prepareCpe(ClassPathEntry* cpe, bool isBootstrap)
{
    if (dvmJarFileOpen(cpe->fileName, NULL, &pJarFile, isBootstrap) == 0) { ... }
    if (dvmRawDexFileOpen(cpe->fileName, NULL, &pRawDexFile, isBootstrap) == 0){ ... }
}
```


## Android 类实现探索-系统基础类
http://neilux.iteye.com/blog/1292449

## Dalvik 分析之准备篇
http://blog.csdn.net/virtualpower/article/details/5660966

## Dalvik 分析 - Class加载篇
http://blog.csdn.net/virtualpower/article/details/5715277



[ART执行类方法解析流程](https://blog.csdn.net/zhu929033262/article/details/75093012)

[Android Art Hook 技术方案](https://blog.csdn.net/L173864930/article/details/45035521)