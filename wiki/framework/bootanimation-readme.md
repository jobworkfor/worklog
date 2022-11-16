# bootanimation readme

## 目录位置
work/SM8250_Q_DEV_BSUI_20190923/miui/frameworks/base/cmds/bootanimation

## 主干流程


```cpp
[bootanimation_main.cpp] sp<BootAnimation> boot = new BootAnimation();
|-  [BootAnimation.cpp] BootAnimation()
|-  BootAnimation::onFirstRef() {run("BootAnimation", PRIORITY_DISPLAY);}
|-  BootAnimation::readyToRun() {mZip = zipFile;}
`-  BootAnimation::threadLoop() {r = movie();}
    `-  BootAnimation::movie() {
            eglSwapBuffers(mDisplay, mSurface);
        }

```



## 附录
### 如何使用`glDrawTexiOES`
```cpp
glGenTextures(...)
glBindTexture(...)
...
glTexImage2D(...)
GLint crop[4] = { 0, h, w, -h };
...
glTexParameteriv(GL_TEXTURE_2D, GL_TEXTURE_CROP_RECT_OES, crop);
...
glDrawTexiOES(...)
```

### refs
https://www.khronos.org/opengl/wiki/Category:Core_API_Reference