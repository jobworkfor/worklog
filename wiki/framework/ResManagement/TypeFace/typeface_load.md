

`TypeFace`载入流程
----------------------------------------------------------------------------------------------------

###
frameworks/base/core/java/com/android/internal/os/WrapperInit.java
```java
    public static void main(String[] args) {
...
            // Mimic Zygote preloading.
            ZygoteInit.preload();
...
    }
```

###
frameworks/base/core/java/com/android/internal/os/ZygoteInit.java

```java
    static void preload() {
        Log.d(TAG, "begin preload");
...
        preloadClasses();
...
    }
```

###
frameworks/base/core/java/com/android/internal/os/ZygoteInit.java

```java
    private static void preloadClasses() {
...
            // PRELOADED_CLASSES = "/system/etc/preloaded-classes";
            is = new FileInputStream(PRELOADED_CLASSES);
...
        Log.i(TAG, "Preloading classes...");
...
            // line in frameworks/base/preloaded-classes
            while ((line = br.readLine()) != null) {
...
                    // Load and explicitly initialize the given class. Use
                    // Class.forName(String, boolean, ClassLoader) to avoid repeated stack lookups
                    // (to derive the caller's class-loader). Use true to force initialization, and
                    // null for the boot classpath class-loader (could as well cache the
                    // class-loader of this class in a variable).
                    Class.forName(line, true, null);
...
            }
            Log.i(TAG, "...preloaded " + count + " classes in "
                    + (SystemClock.uptimeMillis()-startTime) + "ms.");
...
```

> java中class.forName和classLoader都可用来对类进行加载。前者除了将类的.class文件加载到jvm中之外，还会对类进行解释，执行类中的static块。
而classLoader只干一件事情，就是将.class文件加载到jvm中，不会执行static中的内容,只有在newInstance才会去执行static块。
Class.forName(name, initialize, loader)带参函数也可控制是否加载static块。并且只有调用了newInstance()方法采用调用构造函数，创建类的对象。





Reference
----------------------------------------------------------------------------------------------------

* [ttc格式字体解包修改详细图文教程](http://www.mei521.com/?p=20070)
* [TrueType TTC格式详解](http://blog.csdn.net/kwfly/article/details/50909066)
* [TrueType Specification](https://www.microsoft.com/en-us/Typography/SpecificationsOverview.aspx)





