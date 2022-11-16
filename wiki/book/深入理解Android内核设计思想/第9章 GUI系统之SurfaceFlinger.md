# 第9章 GUI系统之SurfaceFlinger

GUI（Graphical User Interface）即图形用户界面。优秀的GUI具备如下几个特性：

* 流畅性
* 友好性：合理搭配的视觉元素
* 可扩展性：方便开发者添加界面和交互方式

## 9.1 OpenGL ES与EGL

SurfaceFlinger 通过使用 OpenGL ES 提供的 API 来实现功能，需要理解的概念有：

* EGL：通过读取 egl.cfg 配置文件，动态加载 libagl（软件实现） 或 libhgl（硬件实现） 库。
* OpenGL ES：是一个通用函数库，不同平台上需要被“本地化”（与具体平台的窗口系统建立关联）才能正常工作。OpenGL是一个接口协议，既可以用软件实现，也可以用硬件实现。
* DisplayHardware
* Gralloc：一个驱动设备，管理帧缓冲区的分配和释放。
* Composer：负责图层合成和产生和控制 VSync 信号。
* FramebufferNativeWindow
