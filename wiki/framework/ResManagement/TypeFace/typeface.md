

简述
----------------------------------------------------------------------------------------------------

正好碰到了关于TrueType字体中TTC解析的问题,网上找了一圈,结合自己找到的部分资料、实际操作和自己对TrueType的认识浅述相关内容。

TTC文件的本质

TTC文件可以简单的理解为多个TrueType文件的合并。

TTC头文件

对TrueType字体有过了解的人基本上应该都知道TrueType头包含字体中相关Table的信息,而TTC是多个TrueType字体的集合,显然有个总的包含关于本TTC文件包含的TrueType个数等相关信息方面对包含的TrueType头信息进行检索。 
TTC头信息包含内容如下所述(上述信息可参考Mirosoft提供的TTF标准文档,本文后面有该文档下载地址)

1. TTCTag(4个字节)
2. Version(4个字节)
3. DirectoryCount(4个字节)
4. TableDirectory[DirectoryCount] (每一TableDirectory为4个字节)
下面结合simsun.ttc(如果系统为Windows可到下面目录中找到C:\Windows\Fonts)简述其头部包含的内容 
使用任意16进制文件查看器可以发现该文件16进制信息为:

1. 0x74 0x74 0x63 0x66(TTCTag ASCII为ttcf)
2. 0x00 0x02 0x00 0x00(Version信息)
3. 0x00 0x00 0x00 0x02(DirectoryCount值为2表示TTC包含两种TTF字体文件)
4. 0x00 0x00 0x00 0x20(TableDirectory[0] 第一种TTF字体的TTF头相对文件头的偏移位置信息)
5. 0x00 0x00 0x01 0x8C(TableDirectory[1] 第二种TTF文件的TTF头相对文件头的偏移位置信息)
TTC文件解包和合并工具简介

解包即是将TTC文件打开将里面的TTF文件全部信息提取出来
合并即是将多个TTF文件合并为一个TTC文件
TTCTools

该工具未找到官方网址,自己随便找个地方下载即可。其中包含解包和合并工具,具体使用说明请参考下载文件里面的Readme.txt,windows系统专用。

FontForge

开源项目,该工具非常强大,适合制作字体人士及相关研究人员使用,使用非常简单,具体请参看对应说明书,提供多平台支持。 
工具下载地址:http://fontforge.github.io/en-US/

AFDKO

Adobe公司出品,自带的otf2otc与otc2otf这两个工具也可完成TTC文件解包和合并任务,为多个平台提供支持。 
工具下载地址:http://http://www.adobe.com/devnet/opentype/afdko/eula.html

参考资料

https://www.microsoft.com/en-us/Typography/SpecificationsOverview.aspx 
该网址包含TrueType标准和OpenType说明书下载信息,其中关于TTC文件格式的具体描述在TrueType标准的第三章。





```
adb root
adb remount
adb push W:\work\freezed-ZSUI_DEV_APK_20161011\out\target\product\le_zl1\system\framework\arm64\boot.art /system/framework/arm64/boot.art
adb push W:\work\freezed-ZSUI_DEV_APK_20161011\out\target\product\le_zl1\system\framework\arm64\boot.oat /system/framework/arm64/boot.oat
adb push W:\work\freezed-ZSUI_DEV_APK_20161011\out\target\product\le_zl1\system\framework\arm\boot.art /system/framework/arm/boot.art
adb push W:\work\freezed-ZSUI_DEV_APK_20161011\out\target\product\le_zl1\system\framework\arm\boot.oat /system/framework/arm/boot.oat
adb push W:\work\freezed-ZSUI_DEV_APK_20161011\out\target\product\le_zl1\system\framework\services.jar /system/framework/services.jar



adb push W:\work\freezed-ZSUI_DEV_APK_20161011\out\target\product\le_zl1\system\framework\arm\ /system/framework/arm/
adb push W:\work\freezed-ZSUI_DEV_APK_20161011\out\target\product\le_zl1\system\framework\arm64\ /system/framework/arm64/

adb remount
adb push out/target/product/le_zl1/system/framework/arm/boot.art /system/framework/arm/boot.art &&\
adb push out/target/product/le_zl1/system/framework/arm/boot.oat /system/framework/arm/boot.oat &&\
adb push out/target/product/le_zl1/system/framework/arm64/boot.art /system/framework/arm64/boot.art &&\
adb push out/target/product/le_zl1/system/framework/arm64/boot.oat /system/framework/arm64/boot.oat &&\
adb shell stop && adb shell start


adb push out/target/product/le_zl1/system/framework/arm/boot.oat /system/framework/arm/boot.oat 
adb push out/target/product/le_zl1/system/framework/arm/boot.art /system/framework/arm/boot.art 
adb push out/target/product/le_zl1/system/framework/arm64/boot.oat /system/framework/arm64/boot.oat 
adb push out/target/product/le_zl1/system/framework/arm64/boot.art /system/framework/arm64/boot.art 


adb push out/target/product/generic_x86_64/system/framework/framework.jar /system/framework/framework.jar


setprop persist.zygote.async_preload false

adb remount
adb push out/target/product/le_zl1/system/framework/arm/* /system/framework/arm/
adb push out/target/product/le_zl1/system/framework/arm64/* /system/framework/arm64/
adb reboot

```


sFallbackFonts

```
    for (int i = 0; i < fontConfig.families.size(); i++) {
        FontListParser.Family f = fontConfig.families.get(i);
        if (i == 0 || f.name == null) {
            familyList.add(makeFamilyFromParsed(f, bufferForPath));
        }
    }
    sFallbackFonts = familyList.toArray(new FontFamily[familyList.size()]);
```

解析出fonts.xml后，其中第一个字体和没名字的字体都是默认字体，会添加到sFallbackFonts对象中。




```
#0  SkFindAndPlaceGlyph::ProcessPosText<DrawOneGlyph&> (textEncoding=SkPaint::kGlyphID_TextEncoding, text=0x7ffed9f979a0 "C5\275C\377\377\377\377", byteLength=4, offset=..., matrix=..., pos=0x7ffed9a17480, scalarsPerPosition=2, textAlignment=SkPaint::kRight_Align, cache=0x7ffed9a17480, processOneGlyph=...) at external/skia/src/core/SkFindAndPlaceGlyph.h:590
#1  0x00007ffef47e4b3b in SkDraw::drawPosText (this=0x7fffb5562568, text=0x7ffed9f979a0 "C5\275C\377\377\377\377", byteLength=4, pos=0x7ffed9a17480, scalarsPerPosition=2, offset=..., paint=...) at external/skia/src/core/SkDraw.cpp:1669
#2  0x00007ffef47a7c26 in SkBitmapDevice::drawPosText (this=<optimized out>, draw=..., text=0x7ffed9f979a0, len=4, xpos=0x7ffed9f99d50, scalarsPerPos=-643730304, offset=..., paint=...) at external/skia/src/core/SkBitmapDevice.cpp:357
#3  0x00007ffef47cd170 in SkCanvas::onDrawPosText (this=<optimized out>, text=<optimized out>, byteLength=<optimized out>, pos=<optimized out>, paint=...) at external/skia/src/core/SkCanvas.cpp:2539
#4  0x00007ffef47cdb85 in SkCanvas::drawPosText (this=0x7ffed9f99400, text=<optimized out>, byteLength=4, pos=0x7ffed9a17480, paint=...) at external/skia/src/core/SkCanvas.cpp:2614
#5  0x00007ffef5b33223 in android::SkiaCanvas::drawGlyphs (this=0x7ffed9a12a80, text=0x7ffed9f979a0, positions=0x7ffed9f99d50, count=<optimized out>, paint=..., x=0, y=17, boundsLeft=5.60519386e-45, boundsTop=0, boundsRight=0, boundsBottom=0, totalAdvance=30) at frameworks/base/libs/hwui/SkiaCanvas.cpp:764
#6  0x00007ffef5adc47a in android::DrawTextFunctor::operator() (this=<optimized out>, start=<optimized out>, end=<optimized out>) at frameworks/base/libs/hwui/hwui/Canvas.cpp:135
#7  0x00007ffef5adbfb8 in android::MinikinUtils::forFontRun<android::DrawTextFunctor> (layout=..., paint=<optimized out>, f=...) at frameworks/base/libs/hwui/hwui/MinikinUtils.h:73
#8  0x00007ffef5adbda8 in android::Canvas::drawText (this=this@entry=0x7ffed9a12a80, text=0x7ffed9a17480, text@entry=0x7ffeda45eb18, start=<optimized out>, count=<optimized out>, contextCount=<optimized out>, x=<optimized out>, x@entry=0, y=<optimized out>, y@entry=17, bidiFlags=<optimized out>, origPaint=..., typeface=<optimized out>) at frameworks/base/libs/hwui/hwui/Canvas.cpp:182
#9  0x00007ffef773720d in android::CanvasJNI::drawTextString (env=0x7ffef343e240, canvasHandle=140732549638784, text=0x7fffb5562d38, start=0, end=<optimized out>, x=0, y=17, bidiFlags=2, paintHandle=140732549874464, typefaceHandle=140732980124576) at frameworks/base/core/jni/android_graphics_Canvas.cpp:496
#10 0x0000000074c40b1a in ?? ()
#11 0x0000000000000002 in ?? ()
#12 0x00007ffed9a4c320 in ?? ()
#13 0x00007ffef349dba0 in ?? ()
#14 0x0000000000000000 in ?? ()
```

编译`minikin`
```
intermediates=out/host/linux-x86/obj/EXECUTABLES/hyphtool_intermediates, mm -j32
```


###
/frameworks/base/core/jni/android_graphics_Canvas.cpp

```
/**
    text  The text to be drawn
    start The index of the first character in text to draw
    end   (end - 1) is the index of the last character in text to draw
    x     The x-coordinate of the origin of the text being drawn
    y     The y-coordinate of the baseline of the text being drawn
    bidiFlags           Bidirection of text, LTR or RTL
    paintHandle         The paint used for the text (e.g. color, size, style)
    typefaceHandle      Type face handle
*/
static void drawTextString(JNIEnv* env, jobject, jlong canvasHandle, jstring text,
                           jint start, jint end, jfloat x, jfloat y, jint bidiFlags,
                           jlong paintHandle, jlong typefaceHandle) {
    Paint* paint = reinterpret_cast<Paint*>(paintHandle);
    Typeface* typeface = reinterpret_cast<Typeface*>(typefaceHandle);
    const int count = end - start;
    const jchar* jchars = env->GetStringChars(text, NULL);
    get_canvas(canvasHandle)->drawText(jchars + start, 0, count, count, x, y,
                                       bidiFlags, *paint, typeface);
    env->ReleaseStringChars(text, jchars);
}
```

* jstring text -> jchar* jchars
    * typedef uint16_t jchar; /* unsigned 16 bits */

* get_canvas(canvasHandle)->drawText(jchars + start, 0, count, count, x, y, bidiFlags, *paint, typeface);
    * count = end - start;


### 


/frameworks/base/libs/hwui/hwui/Canvas.cpp
```
void Canvas::drawText(const uint16_t* text, int start, int count, int contextCount,
        float x, float y, int bidiFlags, const Paint& origPaint, Typeface* typeface) {
    // minikin may modify the original paint
    Paint paint(origPaint);

    Layout layout;
    MinikinUtils::doLayout(&layout, &paint, bidiFlags, typeface, text, start, count, contextCount);

    size_t nGlyphs = layout.nGlyphs();
    std::unique_ptr<uint16_t[]> glyphs(new uint16_t[nGlyphs]);
    std::unique_ptr<float[]> pos(new float[nGlyphs * 2]);

    x += MinikinUtils::xOffsetForTextAlign(&paint, layout);

    MinikinRect bounds;
    layout.getBounds(&bounds);
    if (!drawTextAbsolutePos()) {
        bounds.offset(x, y);
    }

    // Set align to left for drawing, as we don't want individual
    // glyphs centered or right-aligned; the offset above takes
    // care of all alignment.
    paint.setTextAlign(Paint::kLeft_Align);

    DrawTextFunctor f(layout, this, glyphs.get(), pos.get(),
            paint, x, y, bounds, layout.getAdvance());
    MinikinUtils::forFontRun(layout, &paint, f);
}
```




01-26 10:31:46.765  5525  5525 D bob_log_tag: #00 pc 000000000000c3fc  /system/lib64/libutils.so (_ZN7android9CallStackC2EPKci+92)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #01 pc 0000000000010258  /system/lib64/libminikin.so
01-26 10:31:46.765  5525  5525 D bob_log_tag: #02 pc 000000000000bd68  /system/lib64/libharfbuzz_ng.so
01-26 10:31:46.765  5525  5525 D bob_log_tag: #03 pc 000000000000bd34  /system/lib64/libharfbuzz_ng.so (hb_face_get_upem+40)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #04 pc 000000000000dfbc  /system/lib64/libharfbuzz_ng.so (hb_font_create+116)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #05 pc 0000000000010170  /system/lib64/libminikin.so (_ZN7android15getHbFontLockedEPNS_11MinikinFontE+380)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #06 pc 0000000000018ad0  /system/lib64/libminikin.so (_ZN7android12getFontTableEPNS_11MinikinFontEj+48)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #07 pc 000000000000c5c8  /system/lib64/libminikin.so (_ZN7android10FontFamily7addFontEPNS_11MinikinFontE+80)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #08 pc 000000000002e050  /system/lib64/libhwui.so
01-26 10:31:46.765  5525  5525 D bob_log_tag: #09 pc 0000000000069568  /system/lib64/libc.so (pthread_once+200)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #10 pc 000000000002df68  /system/lib64/libhwui.so (_ZN7android8Typeface14resolveDefaultEPS0_+28)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #11 pc 000000000002d6b4  /system/lib64/libhwui.so (_ZN7android12MinikinUtils19prepareMinikinPaintEPNS_12MinikinPaintEPPNS_14FontCollectionEPKNS_5PaintEPNS_8TypefaceE+60)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #12 pc 000000000002d968  /system/lib64/libhwui.so (_ZN7android12MinikinUtils11measureTextEPKNS_5PaintEiPNS_8TypefaceEPKtmmmPf+120)
01-26 10:31:46.765  5525  5525 D bob_log_tag: #13 pc 00000000001145c0  /system/lib64/libandroid_runtime.so





/proc/self/cwd/frameworks/minikin/libs/minikin/HbFontCache.cpp:41
/proc/self/cwd/external/harfbuzz_ng/src/hb-face-private.hh:72
/proc/self/cwd/external/harfbuzz_ng/src/hb-face-private.hh:82
/proc/self/cwd/external/harfbuzz_ng/src/hb-font.cc:1136
/proc/self/cwd/frameworks/minikin/libs/minikin/HbFontCache.cpp:135
/proc/self/cwd/frameworks/minikin/libs/minikin/MinikinInternal.cpp:84
/proc/self/cwd/frameworks/minikin/libs/minikin/FontFamily.cpp:83 
/proc/self/cwd/frameworks/base/libs/hwui/hwui/Typeface.cpp:73
/proc/self/cwd/bionic/libc/bionic/pthread_once.cpp:71
/proc/self/cwd/frameworks/base/libs/hwui/hwui/Typeface.cpp:101
/proc/self/cwd/frameworks/base/libs/hwui/hwui/MinikinUtils.cpp:29
/proc/self/cwd/frameworks/base/libs/hwui/hwui/MinikinUtils.cpp:67
frameworks/base/core/jni/android/graphics/Paint.cpp:486




问题调用栈，当出现字体问题时，如下callstack没有正确载入字体头文件

###

/home/bob/dev/workspace/android/frameworks/base/core/java/com/android/internal/os/ZygoteInit.java
```
    static void preload() {
        ...
        preloadTextResources();
        ...
    }

    private static void preloadTextResources() {
        ...
        TextView.preloadFontCache();
    }
```



###

/home/bob/dev/workspace/android/frameworks/base/core/java/android/widget/TextView.java

```
    public static void preloadFontCache() {
        ...
        // We don't care about the result, just the side-effect of measuring.
        p.measureText("H");
    }
```

###

/home/bob/dev/workspace/android/frameworks/base/graphics/java/android/graphics/Paint.java
```
    public float measureText(String text) {
        ...
        return measureText(text, 0, text.length());
    }

    public float measureText(String text, int start, int end) {
        ...
        float w = nGetTextAdvances(mNativePaint, mNativeTypeface, text, start, end, start,
                end, mBidiFlags, null, 0);
        ...
    }
```


###

/frameworks/base/core/jni/android/graphics/Paint.cpp
```
    static jfloat getTextAdvances__StringIIIII_FI(...) {
        ...
        jfloat result = doTextAdvances(env, paint, typeface, textArray + contextStart,
                start - contextStart, end - start, contextEnd - contextStart, bidiFlags,
                advances, advancesIndex);
        ...
    }
```





















zsui_dev_apk_20161011_zl1.xml





Reference
----------------------------------------------------------------------------------------------------

* [ttc格式字体解包修改详细图文教程](http://www.mei521.com/?p=20070)
* [TrueType TTC格式详解](http://blog.csdn.net/kwfly/article/details/50909066)
* [TrueType Specification](https://www.microsoft.com/en-us/Typography/SpecificationsOverview.aspx)

Launcher3的字体为`sans-serif-condensed`

* [Android Tombstone 分析](http://www.cnblogs.com/CoderTian/p/5980426.html)
* [Android Native/Tombstone Crash Log 详细分析[原创] ](http://blog.sina.com.cn/s/blog_702c2db50102vc2h.html)