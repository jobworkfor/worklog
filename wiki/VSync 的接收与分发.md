# VSync 的接收与分发

## 内容简介

安卓 APP UI 的每一帧的刷新都会向 SurfaceFlinger 请求一次 VSync，Choreographer.FrameDisplayEventReceiver 对象负责上层 VSync 的请求和监听，当收到 SF 的 VSync 上报后，在 FrameDisplayEventReceiver.onVsync() 方法中处理 APP UI 的刷新动作。

本文描述了 APP 如何与 SF 建立 VSync 通信机制以及 SF 如何将 VSync 上报到 APP 进程两个主要流程，其关键 API 如下：

通信机制建立流程：

* createDisplayEventConnection() ：在 SF 进程中创建 APP 端的专属通信对象 EventThreadConnection。

* stealReceiveChannel()：连通 APP 进程和 SF 进程各自的 BitTube 对象。

APP 请求 VSync 并上报流程：

* requestNextVsync()：wait-notify 机制，唤醒等待在 mCondition 上的 EventThread 线程。
* dispatchEvent()：SF 通过 BitTube 对象将 VSync 上报到 APP 进程。

下面具体说明这两个流程。

## 模块关系

建立 APP 与 SF 的通信机制、APP 向 SF 请求 VSync、SF 向 APP 上报 VSync，这些动作涉及 APP 和 SurfaceFlinger 两个进程，使用了 Binder 和 BitTube(socketpair) 两种 IPC 通信方式。在初始化 APP 时先通过 Binder 方式建立 BitTube 连接，然后 SF 通过 BitTube 对象向 APP 发送 VSync 信号，如下图所示：

<pre>
<img src="res/VSync的接收与分发03.svg" />
</pre>



上图涉及两个进程（app 进程和 surfaceflinger 进程），三层逻辑（app java 层，app native 层，surfaceflinger 层），用图标记号标注了两条流程。绿色高亮是重要的类，蓝色高亮是重要的方法和类变量，他们最终的目的是建立起从 SF 到 APP 的 VSync 上报通道（<font color=red>记号2.5</font>-><font color=red>记号2.6</font>-><font color=red>记号2.7</font>）。下面从模块角度出发，大致描述这两个执行流程。

### 建立 SF 中 APP 的专属连接

* 当启动 APP 时，Choreographer 对象被创建出来，该对象是线程相关的，被保存到 ThreadLocal 对象中。Choreographer 构造函数中，创建出 FrameDisplayEventReceiver 对象，FrameDisplayEventReceiver 构造函数中会调用 nativeInit(<font color=red>记号1.1</font>) 方法发起 SF 中的初始化。
* nativeInit(<font color=red>记号1.1</font>) 是一个 JNI 调用，在 native 对应的实现函数中，创建出 NativeDisplayEventReceiver 对象（native 对象），在其父类 DisplayEventDispatcher 的构造函数中，会初始化其成员变量 DisplayEventDispatcher::mReceiver，在 DisplayEventReceiver 的构造函数中，通过 Binder IPC 调用到 SurfaceFlinger::createDisplayEventConnection(<font color=red>记号1.2</font>) 方法，其目的是在 SF 进程中创建 APP 专属的通信对象。
* 在 SF 进程中，SurfaceFlinger::createDisplayEventConnection(<font color=red>记号1.2</font>) 方法根据 Client 传入的参数 ISurfaceComposer::VsyncSource 的类型确定是由 mSfConnectionHandle 还是由 mAppConnectionHandle 来处理当前连接。mSfConnectionHandle 和 mAppConnectionHandle 这两个对象是在 SF 进程初始化时被创建的，APP 调用 SurfaceFlinger::createDisplayEventConnection(<font color=red>记号1.2</font>) 时，已经初始化完毕。
* APP 传入 vsyncSource 的值为 eVsyncSourceApp，故由 mAppConnectionHandle 来处理当前连接，通过 mAppConnectionHandle 获取到对应的 EventThread 对象后，调用 eventThread->createEventConnection(<font color=red>记号1.3</font>) 方法创建出 APP 客户端的专属 EventThreadConnection <font color=red>记号1.4</font> 对象。该对象的成员变量 mChannel 就是与 APP 端的 socketpair 连接。mChannel 是 gui::BitTube 类的对象，gui::BitTube 是 socketpair 的包装类。
* SurfaceFlinger::createDisplayEventConnection(<font color=red>记号1.2</font>) 执行完成后，返回 SF 中 EventThreadConnection <font color=red>记号1.4</font> 对象的 Binder Proxy 端，保存到 DisplayEventReceiver 对象的 mEventConnection <font color=red>记号1.5</font> 成员变量中。此时，SF 中为 APP 创建了一个对应的 BitTube 对象，但还不能和 APP 通信。
* 在 APP 进程中，如果 DisplayEventReceiver::mEventConnection 对象创建成功，则先创建一个负责与 SF 进程通信的 BitTube 对象，保存到 DisplayEventReceiver::mDataChannel <font color=red>记号1.7</font> 中，然后调用其 stealReceiveChannel(<font color=red>记号1.6</font>) 方法打通与 SF 的连接，该方法是个 IPC 调用，服务端对应实现方法为：EventThreadConnection::stealReceiveChannel()。
* 在 SF 进程中，EventThreadConnection::stealReceiveChannel() 方法调用其 BitTube 对象的 setReceiveFd()/setSendFd(<font color=red>记号1.9</font>) 方法打通与 APP 进程的连接。至此，APP 与 SF 的通信机制建立完毕。
* 最后，APP 进程的 JNI 调用返回 NativeDisplayEventReceiver 对象在 Native 的地址（<font color=red>记号1.10</font>），保存在 Java 层 FrameDisplayEventReceiver 对象的 mReceiverPtr 变量中。

### VSync 的请求与上报

* APP 每刷新一帧界面都需要向 SF 申请一个 VSync 信号，APP 这边调用 nativeScheduleVsync(<font color=red>记号2.1</font>) 接口将控制权从 JAVA 层转到 Native 层。在 JNI 的实现接口中将 JAVA 传下来的地址（mReceiverPtr <font color=red>记号1.10</font>）转换成  NativeDisplayEventReceiver 的 sp 指针对象。
* 通过 sp\<NativeDisplayEventReceiver> 指针调用其成员变量 mEventConnection 的 requestNextVsync(<font color=red>记号2.2</font>) 方法向 SF 请求一个 VSync。requestNextVsync() 是一个 Binder IPC 接口，对应的实现方法为 EventThreadConnection::requestNextVsync()。
* 在 SF 进程的 EventThreadConnection::requestNextVsync() 方法中，会调用 EventThread 对象中的成员方法 mCondition.notify_all(<font color=red>记号2.3</font>) 来唤醒等待在 mCondition <font color=red>记号2.4</font> 上的 "app" 线程。"app" 线程唤醒后先从等待队列中取出 VSync 事件对象，然后调用 SF 进程中的 BitTube::sendObjects(<font color=red>记号2.5</font>) 方法将 VSync 事件（<font color=red>记号2.6</font>）发送给 APP 端的 BitTube 对象中。
* APP 进程通过 epoll 的方式（<font color=red>记号2.7</font>）监听 BitTube 上的事件，此时监听到 SF 传过来的 VSync 事件，触发 epoll 的回调处理方法 DisplayEventDispatcher::handleEvent(<font color=red>记号2.8</font>)，最后通过 JNI 回调到 JAVA 层的  FrameDisplayEventReceiver.onVsync(<font color=red>记号2.9</font>) 方法。
* 在 onVsync(<font color=red>记号2.9</font>) 方法中上层 APP 执行 View 的测量，布局和渲染动作。

## 类关系图

本流程相关类之间的静态关系如下图所示：

<pre>
<img src="res/VSync的接收与分发02.svg" />
</pre>



上图中，深蓝色背景的类跑在 SF 进程中，绿色高亮是重点成员变量。具体说明如下：

- FrameDisplayEventReceiver 类（<font color=red>记号1</font>）是 APP 端 JAVA 层与 Native 的分界线，其成员变量 mReceiverPtr 保存了 Native 层 NativeDisplayEventReceiver 对象的地址。上层请求 VSync 时都需要将 mReceiverPtr 传给 Native 层。
- android::Looper 类（<font color=red>记号2</font>）是安卓标准的 Handler，Message，Looper 机制，APP 利用 Looper 对象 epoll 监听的能力监听 BitTube 对象。
- DisplayEventReceiver 类（<font color=red>记号3</font>）用于监听 SF 的各种事件回调，其成员变量 mDataChannel 是与 SF 通信的 BitTube 对象，底层使用 socketpair 方式实现跨进程通信。
- EventThreadConnection 类（<font color=red>记号4</font>）是每个连接到 SF 进程的 APP 的专属连接对象，其成员变量 mChannel 与 APP 端的 BitTube 对象互通。APP 通过 Binder IPC 调用其 requestNextVsync() 方法，然后 SF 通过 mChannel 将 VSync 上报给 APP 进程。
- SurfaceFlinger类（<font color=red>记号5</font>）是 SF 的主体实现类，在初始化时会创建 mAppConnectionHandle 和 mSfConnectionHandle 两个对象，分别处理对 APP 或 SF 事件感兴趣的客户端。
- EventThread类（<font color=red>记号6</font>）在构建 mAppConnectionHandle 时被创建出来，其成员 mThread 代表处理 APP 事件的子线程。每当 APP 客户端与 SF 建立 VSync 事件连接时，都会保存到该对象的 mDisplayEventConnections 成员中。VSync 事件只会发送给该集合中的客户端成员。

## 执行流程 - SF 初始化

VSync 的收发流程中，有一些变量在启动 SF 时被创建，下图主要描述了两个初始化点：帧率重载初始化和 mAppConnectionHandle 的初始化。

<pre>
<img src="res/VSync的接收与分发04.svg" />
</pre>


上图执行流程说明如下：

* 该流程描述了启动 surfaceflinger 时做的动作，到 SurfaceFlinger::processDisplayAdded() 方法的执行路径（<font color=red>记号1</font>）为：main_surfaceflinger.cpp::main() -> SurfaceFlinger::init() -> HWComposer::setCallback() -> ...  -> SurfaceFlinger::processDisplayAdded()。processDisplayAdded() 是来自 Hwc2::impl::Composer HAL 的回调，携带了底层 display 硬件相关信息。

* SurfaceFlinger::processDisplayAdded() 方法中，调用 SurfaceFlinger::setupNewDisplayDeviceInternal() 方法初始化当前系统的 DisplayDevice 对象，setupNewDisplayDeviceInternal() 方法中将为当前 display 设备创建一个刷新率配置对象 -- scheduler::RefreshRateConfigs::Config。scheduler::RefreshRateConfigs::Config 是一个静态配置对象，与系统状态无关，其成员变量 enableFrameRateOverride <font color=red>记号2</font> 的值取自系统属性 ro.surface_flinger.enable_frame_rate_override，系统默认为 false。

* 接着根据当前系统状态，将静态配置转换为 RefreshRateConfigs 对象，其成员变量 mSupportsFrameRateOverride 是是否支持帧率重载的开关，由于 scheduler::RefreshRateConfigs::Config.enableFrameRateOverride <font color=red>记号2</font> 为 false，所以当前系统不支持帧率重载。

* 回到 SurfaceFlinger::processDisplayAdded() 方法，继续调用 SurfaceFlinger::initScheduler(<font color=red>记号3</font>) 方法，在该方法中先创建出 Scheduler 对象，然后调用其 Scheduler::createConnection(<font color=red>记号4</font>) 方法创建 mAppConnectionHandle。

* 在 Scheduler::createConnection(<font color=red>记号4</font>) 中，调用 Scheduler::makeThrottleVsyncCallback() 方法构建一个 EventThread::ThrottleVsyncCallback 回调方法对象（<font color=red>记号5</font>），类型为 std::function<bool(nsecs_t, uid_t)>，是帧率重载的具体实现方法，当 EventThread 中 VSync 处理线程上报 VSync 时会调用该方法来控制帧率。当前系统配置不支持帧率重载，该方法是一个空实现。

* 回到 Scheduler::createConnection(<font color=red>记号4</font>) ，下面会创建出 EventThread 对象（<font color=red>记号5</font>），在其构造函数中启动一个新线程用来处理 VSync 事件，线程名为 "app"。

* 返回 Scheduler::createConnection(<font color=red>记号4</font>) 后，调用 Scheduler::createConnection() 将 EventThread 对象封装成 Scheduler::Connection 结构保存到 Scheduler::mConnections 对象（<font color=red>记号5</font>）中。Scheduler::mConnections 的类型为 std::unordered_map<ConnectionHandle, Connection>，当有 APP 客户端需要与 SF 建立连接时，会用 ConnectionHandle 作为键来索引 Connection 对象，进一步剥出 EventThread 对象来用。ConnectionHandle 是一个结构，就一个 std::uintptr_t 类型的成员，对应不同的 VSync 类型的值，如下：

  ````java
  // aosp_android-12.1.0_r2\frameworks\base\core\java\android\view\DisplayEventReceiver.java
  public abstract class DisplayEventReceiver {
      public static final int VSYNC_SOURCE_APP = 0;
      public static final int VSYNC_SOURCE_SURFACE_FLINGER = 1;
  ...
  ````

## 执行流程 - 建立连接

初始化完成后，系统有了 mAppConnectionHandle 对象，当 APP 要求与 SF 建立连接时，就使用该对象来建立连接，建立过程如下图所示：

<pre>
<img src="res/VSync的接收与分发01.svg" />
</pre>


上图执行流程说明如下：

* APP 进程启动后会创建 Choreographer 对象保存到 ThreadLocal 变量中，在 Choreographer 的构造函数中，创建出 FrameDisplayEventReceiver 对象（<font color=red>记号1</font>），该对象是 APP JAVA 层与 Native 层的分水岭，在 FrameDisplayEventReceiver 的构造函数中，调用 nativeInit() 方法创建 Native 层的 NativeDisplayEventReceiver 对象。Native 初始化完毕后将 NativeDisplayEventReceiver 对象在 Native 的地址保存到 DisplayEventReceiver.mReceiverPtr <font color=red>记号2</font>中。
* DisplayEventReceiver.nativeInit() 方法在 Native 层的实现为 android_view_DisplayEventReceiver.cpp 的 nativeInit() 过程调用，该方法中做两件事情，1. 创建 NativeDisplayEventReceiver 对象（<font color=red>记号3</font>）；2. 调用 NativeDisplayEventReceiver 对象的 initialize() 方法（<font color=red>记号5</font>）。先看 NativeDisplayEventReceiver 对象（<font color=red>记号3</font>）的创建，在其构造函数中调用父类 DisplayEventDispatcher 的构造。DisplayEventDispatcher 的构造中创建出 DisplayEventReceiver 对象（<font color=red>记号3-1</font>）。
* DisplayEventReceiver 构造中做两件事：1. 通过 Binder IPC 调用 createDisplayEventConnection(<font color=red>记号3-2</font>)，在 SF 进程中创建 APP 的专属连接对象 EventThreadConnection；2. 通过 Binder IPC 调用 stealReceiveChannel(<font color=red>记号4</font>)，连通 APP 进程和 SF 进程的 BitTube 对象。下面先看 createDisplayEventConnection() 调用。
* SF 进程中 createDisplayEventConnection(<font color=red>记号3-2</font>) 的实现方法为 SurfaceFlinger::createDisplayEventConnection()，该方法中，根据传入参数 vsyncSource 确定使用 mAppConnectionHandle <font color=red>记号3-3</font> 来建立 APP 的专属连接对象。然后通过 mAppConnectionHandle 在 Scheduler::mConnections 中索引到对应的 EventThread 对象（<font color=red>记号3-4</font>），接着调用 EventThread::createEventConnection() 方法创建 EventThreadConnection 对象。
* 在 EventThreadConnection 的构造函数中，初始化其成员变量 mChannel <font color=red>记号3-5</font> 该对象是 BitTube 类型，BitTube 构造函数中调用 init() 方法进行初始化，init() 方法中调用 linux 系统调用 socketpair(<font color=red>记号3-6</font>) 创建出 mReceiveFd 和 mSendFd 文件描述符。在 EventThreadConnection::onFirstRef() 方法中，将当前连接加入到 EventThread::mDisplayEventConnections 集合中，后续 VSync 只分发给该集合中的成员。此时 SF 还没有和 APP 连通。
* 支持，APP 专属 EventThreadConnection 连接对象创建完毕，下面就是完成 APP 与 SF 的互联，回到 APP 进程的 DisplayEventReceiver 构造函数中，先创建一个 BitTube 对象，保存到 DisplayEventReceiver::mDataChannel 变量中，接着 IPC 调用 stealReceiveChannel(<font color=red>记号4</font>) 方法，SF 进程对应的实现为 EventThreadConnection::stealReceiveChannel() 方法，该方法将 SF::BitTube::mReceiveFd 赋值给 APP::BitTube::mReceiveFd，将 SF::BitTube::mSendFd 复制一份再复制给 APP::BitTube::mSendFd，至此 APP 与 SF 完成了通信连接的建立。
* APP 与 SF 建立通信信道后，APP 还需要监听 SF 上报的消息，这通过 Looper 提供的 epoll 监听机制实现。回到 nativeInit() 函数，调用 DisplayEventDispatcher::initialize(<font color=red>记号5</font>) 方法，在 initialize() 方法中调用 mLooper->addFd(<font color=red>记号5-1</font>) 监听 BitTube 收消息事件，完成监听的初始化。

简而言之，本流程说明了由 Choreographer 对象在构造函数中发起的与 SF 建立 BitTube 连接的过程，APP 端通过 Looper 的 epoll 监听机制来触发对底层 VSync 上报信号的处理。

## 执行流程 - VSync 的收发

至此，java 层通过 DisplayEventReceiver 中的 nativeInit 函数，建立了 APP 和 SF 的通信连接，应用层通过 native 层 Looper 将 mReceiveFd 加入监听，随时响应 mSendFd 的写入。下面分析一个完整的 APP 请求 VSync 和 SF 上报 VSync 的流程，如下图所示：

<pre>
<img src="res/VSync的接收与分发05.svg" />
</pre>


上图执行流程说明如下：

* 当 APP 需要更新界面时，需要向 SF 请求一个 VSync，通过调用 FrameDisplayEventReceiver.nativeScheduleVsync(<font color=red>记号1-1</font>) 方法从 JAVA 层过度到 Native 层调用，通过 DisplayEventDispatcher::scheduleVsync() -> DisplayEventReceiver::requestNextVsync() -> mEventConnection->requestNextVsync(<font color=red>记号1-2</font>) 调用，跳转到 SF 进程。
* SF 进程中，requestNextVsync() 的实现方法为 EventThreadConnection::requestNextVsync()，接着调用其成员变量 mEventThread 的 EventThread::requestNextVsync() 方法，首先判断 EventThreadConnection 对象的状态，看看这个连接对象上是否已经有 VSync 请求了，如果没有（状态为 VSyncRequest::None）就将其状态修改为 VSyncRequest::Single，说明只请求一次 VSync 上报。修改完状态后调用 mCondition.notify_all(<font color=red>记号1-3</font>) 来唤醒等待在 mCondition 上的 VSync 处理线程 -- "app" 线程。
* EventThread 对象中 "app" 线程启动后调用 mCondition.wait(<font color=red>记号1-4</font>) 等待在 mCondition 上，此时被 mCondition.notify_all(<font color=red>记号1-3</font>) 唤醒，开始执行处理循环内代码。首先调用 EventThread::mPendingEvents 的 mPendingEvents.front(<font color=red>记号1-5</font>) 方法取出等待的 VSync 事件，然后从 EventThread::mDisplayEventConnections 取出需要接受 VSync 事件的客户端，最后调用 EventThread::dispatchEvent(<font color=red>记号1-7</font>) 方法将 VSync 发送到对应的客户端。
  * 客户端是否需要接受 VSync 的判断方法为 EventThread::shouldConsumeEvent(<font color=red>记号1-6</font>)，当前的判断条件为 EventThreadConnection 对象的状态是 VSyncRequest::Single 或者 VSyncRequest::Periodic。在判断 EventThreadConnection 状态的同时，还调用了帧率重载的实现方法 EventThread::throttleVsync(<font color=red>记号1-6-1</font>)，安卓通过控制 VSync 的上报频率来实现帧率重载。该方法在 EventThread 构造函数中被初始化，由于系统属性定义为不支持帧率重载，所以该方法为一个空实现。
* 继续 EventThread::dispatchEvent(<font color=red>记号1-7</font>) 方法调用，下面会逐个向符合条件的 EventThreadConnection 对象上报 VSync，其原理就是调用 EventThreadConnection::mChannel 的 BitTube::write(<font color=red>记号1-8</font>) 方法将 VSync 事件传送给 APP 端，write() 最终会调用到 linux 的系统调用 ::send(<font color=red>记号1-9</font>) 方法实现 socketpair 通信。
* 在上一小节中，APP 会调用 DisplayEventDispatcher::initialize() 方法实现对 BitTube 消息的 epoll 监听，回调函数为 DisplayEventDispatcher::handleEvent(<font color=red>记号2-1</font>)，此处收到 SF 的上报后执行两个动作：1. 调用 processPendingEvents(<font color=red>记号2-2</font>) 方法从 BitTube 中取出 VSync 事件；2. 调用 dispatchVsync(<font color=red>记号3-1</font>) 方法将 VSync 事件投递到 JAVA 层，实现 View 的后续动作。
* 先看 processPendingEvents(<font color=red>记号2-2</font>) 方法，该方法调用了 DisplayEventDispatcher::mReceiver 成员的 DisplayEventReceiver::getEvents() 方法，接着调用 DisplayEventReceiver::mDataChannel 成员的 BitTube::recvObjects(<font color=red>记号2-4</font>) 方法获取 SF 上报的 VSync 事件，与 SF 进程中的写入相对应，这里通过 linux 系统调用 ::recv(<font color=red>记号2-5</font>) 实现。
* 再看 dispatchVsync(<font color=red>记号3-1</font>) 方法，该方法通过 env->CallVoidMethod(<font color=red>记号3-2</font>) 回到到 JAVA 层的 DisplayEventReceiver.dispatchVsync() 方法，该方法中调用了 FrameDisplayEventReceiver.onVsync(<font color=red>记号3-3</font>) 方法，最后通过一层 Message 的转换调用到上层 doFrame(<font color=red>记号3-4</font>) 方法实现后续的界面更新操作。

简而言之，应用层请求 Vsync 的本质是唤醒 SF 进程中等待在 std::condition_variable 上的 VSync 处理线程，从当前 EventThread 对象的 mPendingEvents 中取出 Vsync 事件通过 BitTube 再上报给 APP 进程。

## 小结

本文描述了 APP 与 SF 的 VSync 通信机制，通信的大致步骤为：

1. APP 通过 Binder IPC 调用与 SF 建立 BitTube 连接
2. APP 调用 nativeScheduleVsync() 方法向 SF 请求 VSync 信号
3. SF VSync 处理线程被 wait-notify 机制唤醒后，通过 BitTube 向 APP 上报 VSync 信号

结合 APP UI 绘制的能力，绘制的业务流程如下：

1. 首先应用层想要绘制 UI，需要向 SF 请求一个 Vsync，APP 端通过 EventThreadConnection 的 Binder Proxy 端调用到 SurfaceFlinger 进程中 EventThread 的 requestNextVsync 函数实现。
2. EventThread 是用来处理多种显示相关的事件，比如 Vsync、Hotplug 和 ConfigChanged。SF 中有两个 EventThread，分别处理 ”app“ 相关和 ”appsf“ 相关的显示事件。
3. EventThreadConnection 代表 APP 进程到 SF 进程的一个专属连接，每一个上层的 ViewRootImpl 都对应一个 EventThreadConnection，每个 View 视图都需要 Vsync 来触发器绘制的相关工作。
4. EventThread 的内部管理一个线程，该线程就处理对底层 Vsync 的接收和对上层客户端的分发，该线程是一个死循环，当它没收到事件请求时会通过 C++ 条件变量调用 wait 陷入等待状态。
5. APP 请求 Vsync 的过程其实就是通过 notify 这个条件变量来唤醒 EventThread 内部这个线程，然后从 mPendingEvents 中获取到 Vsync 事件分发给感兴趣的客户端进程。