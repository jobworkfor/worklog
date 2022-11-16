# AsyncChannel

## 概述

AsyncChannel 是两个不同的Handler 的传递消息通道，这两个Handler 有可能是在同一个进程，也有可能是在不同的进程，如果是在不同的进程则需要借助Binder 的IPC 机制进行通信。

Messenger 与handler 相关联，Messenger将消息发送给对应的Handler去处理，Messenger =new Messenger(handler),如果handler 来自其他进程，那么 handler 必须来自通过AIDL 转化的Service, Messenger =new Messenger(service),可以这么理解AsyncChannel,就是借助Messenger 机制,让不同的handler之间进行通信。

AsyncChannel 提供客户端/服务端的通信模式，主要有两种应用场景：

## 与已知客户端通信

服务端和客户端相互通信，服务端需要知道那些客户端向它发送请求，它收到客户端请求后，并和客户端建立连接，最后通过replyToMessage将反馈消息发送给客户端。可以连接为双向连接。

以GsmDataConnectionTracker 所在的Handler 和 DataConnection 所在Handler 的通信为例。
  GsmDataConnectionTracker 利用DataConnectionAc(AsyncChannel的派生类），向DataConnection 发送请求，建立通信通道。
  int status = dcac.fullyConnectSync(mPhone.getContext(), this, conn.getHandler());
  status 表示通信通道是否建立成功，如果成功，就可以相互发送具体的消息了。
  fullyConnectSync 建立的是进程内的Handler 通信，首先初始化与连接相关的对象，如srcMessenger,DestMessager，对于同一进程的handler 通信，如果与连接相关的对象初始化完成了，那就说明双方的连接是没有问题了，只需要及建立通信通道。
  public int fullyConnectSync(Context srcContext, Handler srcHandler, Handler dstHandler) {
     int status = connectSync(srcContext, srcHandler, dstHandler);
     if (status == STATUS_SUCCESSFUL) {
       Message response = sendMessageSynchronously(CMD_CHANNEL_FULL_CONNECTION);
       status = response.arg1;
     }
     return status;
   }
   public int connectSync(Context srcContext, Handler srcHandler, Handler dstHandler) {
     return connectSync(srcContext, srcHandler, new Messenger(dstHandler));
   }
   public int connectSync(Context srcContext, Handler srcHandler, Messenger dstMessenger) {
     if (DBG) log("halfConnectSync srcHandler to the dstMessenger E");
 
     // We are connected
     connected(srcContext, srcHandler, dstMessenger);
 
     if (DBG) log("halfConnectSync srcHandler to the dstMessenger X");
     return STATUS_SUCCESSFUL;
   }
   public void connected(Context srcContext, Handler srcHandler, Messenger dstMessenger) {
     if (DBG) log("connected srcHandler to the dstMessenger E");
 
     // Initialize source fields
     mSrcContext = srcContext;
     mSrcHandler = srcHandler;
     mSrcMessenger = new Messenger(mSrcHandler);
 
     // Initialize destination fields
     mDstMessenger = dstMessenger;
 
     if (DBG) log("connected srcHandler to the dstMessenger X");
   }
  如果初始化成功就发送 CMD_CHANNEL_FULL_CONNECTION，的消息，这个消息被发送到 AsyncChannel 中的 SyncMessenger，SyncMessenger（同步Messenger) 维护着一个消息栈和消息发送线程（HandlerThread)。
   private static Message sendMessageSynchronously(Messenger dstMessenger, Message msg) {
       SyncMessenger sm = SyncMessenger.obtain();
       try {
         if (dstMessenger != null && msg != null) {
           msg.replyTo = sm.mMessenger;
           synchronized (sm.mHandler.mLockObject) {
             dstMessenger.send(msg);
             sm.mHandler.mLockObject.wait();
           }
         } else {
           sm.mHandler.mResultMsg = null;
         }
       } catch (InterruptedException e) {
         sm.mHandler.mResultMsg = null;
       } catch (RemoteException e) {
         sm.mHandler.mResultMsg = null;
       }
       Message resultMsg = sm.mHandler.mResultMsg;
       sm.recycle();
       return resultMsg;
     }
  从以上代码可以看出 对于发送的消息的replyTo 变成了SynMessenger 的 messenger(与SysnMessenger 的HandlerThread的Handler）。也就是说GsmDataConnectionTracker的消息通过SyncMessenger 发送到DataConnection的Handler,GsmDataConnectionTracker通过DataConnectionAc所建立的Handler （srcMessenger),就没有起作用。GsmDataConnectionTracker通过DataConnectionAc所建立的DestMessenger(目的Handler)还是起作用的。
  DataConnection 在接收到 CMD_CHANNEL_FULL_CONNECTION,后，创建自己的AsyncChannle ,通过 AsyncChannle 与 GsmDataConnectionTracker的DataConnectionAc的SyncMessenger的HandlerThread的Handler 建立连接，然后向HanlderThread的Handler 发送CMD_CHANNEL_FULLY_CONNECTED消息，并说明通信通道建立成功，HandlerThread的Handler 收到这个消息后，将这个消息转换成SyncMessenger的 resultMessage,并将resultMessage 交给 GsmDataConnectionTracker，那么GsmDataConnectionTracker就直到通信通道是连接成功的，它就可以发送其他具体的数据消息了。
  DataConnection 的 DcDefaultState处理 CMD_CHANNEL_FULL_CONNECTION
  case AsyncChannel.CMD_CHANNEL_FULL_CONNECTION: {
          if (mAc != null) {
             if (VDBG) log("Disconnecting to previous connection mAc=" + mAc);
             mAc.replyToMessage(msg, AsyncChannel.CMD_CHANNEL_FULLY_CONNECTED,
                 AsyncChannel.STATUS_FULL_CONNECTION_REFUSED_ALREADY_CONNECTED);
           } else {
             mAc = new AsyncChannel();
             mAc.connected(null, getHandler(), msg.replyTo);
             if (VDBG) log("DcDefaultState: FULL_CONNECTION reply connected");
             mAc.replyToMessage(msg, AsyncChannel.CMD_CHANNEL_FULLY_CONNECTED,
                 AsyncChannel.STATUS_SUCCESSFUL, mId, "hi");
           }
           break;
         }
  
  SyncMessenger 处理消息
   @Override
       public void handleMessage(Message msg) {
         mResultMsg = Message.obtain();
         mResultMsg.copyFrom(msg);
         synchronized(mLockObject) {
           mLockObject.notify();
         }
       }
  这个应用场景的模式就是客户端和服务端都持有AsyncChannel 对象，客户端通过自己的AsynChannel 和服务端的Handler 建立连接，并发送 CMD_CHANNEL_FULL_CONNECTION到自己的AsyncChannel 的SyncMessenger中，SyncMessenger 将消息转发到服务端的Handler,也就是说客户端向服务端发送消息是通过自己的AsyncChannel 的SyncMessenger 转发的。服务端收到消息后，首先通过自己的AsyncChannel 和客户端的SyncMessenger 建立连接，然后将反馈消息，发送给SyncMessenger,由SynMessenger 转发给客户端。
  当然以上描述只说明了利用AsyncChannel 建立通信通道的过程，发送具体的消息的过程也是和上面描述的一样。

 

## 与匿名客户端通信

服务端和客户端相互通信，服务端不需要知道哪些客户端向它发送请求，它只需要去处理客户端发送过来的消息，不许要和客户端建立连接，可以理解为单向连接。

 

以MobileDataStateTracker所在的Handler 和 DataConnectionTracker 所在Handler 进行通信为例来进行说明。
   GsmDataConnectionTracker 的构造函数中，会发送一个 广播。
   protected void broadcastMessenger() {
     Intent intent = new Intent(ACTION_DATA_CONNECTION_TRACKER_MESSENGER);
     intent.putExtra(EXTRA_MESSENGER, new Messenger(this));
     mPhone.getContext().sendBroadcast(intent);
   }
   这个广播会被 MobileDataStateTracker 所接收。
   else if (intent.getAction().
           equals(DataConnectionTracker.ACTION_DATA_CONNECTION_TRACKER_MESSENGER)) {
         if (VDBG) log(mApnType + " got ACTION_DATA_CONNECTION_TRACKER_MESSENGER");
         mMessenger = intent.getParcelableExtra(DataConnectionTracker.EXTRA_MESSENGER);
         AsyncChannel ac = new AsyncChannel();
         ac.connect(mContext, MobileDataStateTracker.this.mHandler, mMessenger);
  从代码中可以看出，初始化了一个 AsyncChannel ,将 MobileDataStateTracker 的Handler 和 DataConnectionTracker所在的Handler 连接起来。
   public void connect(Context srcContext, Handler srcHandler, Messenger dstMessenger) {
     if (DBG) log("connect srcHandler to the dstMessenger E");
 
     // We are connected
     connected(srcContext, srcHandler, dstMessenger);
 
     // Tell source we are half connected
     replyHalfConnected(STATUS_SUCCESSFUL);
 
     if (DBG) log("connect srcHandler to the dstMessenger X");
   }
   private void replyHalfConnected(int status) {
     Message msg = mSrcHandler.obtainMessage(CMD_CHANNEL_HALF_CONNECTED);
     msg.arg1 = status;
     msg.obj = this;
     msg.replyTo = mDstMessenger;
     mSrcHandler.sendMessage(msg);
   }
  与连接相关的对象初始化完成后， MobileDataStateTracker就收到了 MD_CHANNEL_HALF_CONNECTED，信息，并且处理。代码中的 mSrcHandler就是 MobileDataStateTracker
 所在的Handler.
   public void handleMessage(Message msg) {
       switch (msg.what) {
         case AsyncChannel.CMD_CHANNEL_HALF_CONNECTED:
           if (msg.arg1 == AsyncChannel.STATUS_SUCCESSFUL) {
             if (VDBG) {
               mMdst.log("MdstHandler connected");
             }
             mMdst.mDataConnectionTrackerAc = (AsyncChannel) msg.obj;
           } else {
             if (VDBG) {
               mMdst.log("MdstHandler %s NOT connected error=" + msg.arg1);
             }
           }
           break;
         case AsyncChannel.CMD_CHANNEL_DISCONNECTED:
           if (VDBG) mMdst.log("Disconnected from DataStateTracker");
           mMdst.mDataConnectionTrackerAc = null;
           break;
         default: {
           if (VDBG) mMdst.log("Ignorning unknown message=" + msg);
           break;
         }
       }
   这样。 mDataConnectionTrackerAc ，就被初始化为，已经建立了连接的AsyncChannel 对象，两个Handler 的通信通道建立了（AsyncChannel对象建立）。当 MobileDataStateTracker执行setUserDataEnable的时候。
   public void setUserDataEnable(boolean enabled) {
     if (DBG) log("setUserDataEnable: E enabled=" + enabled);
     final AsyncChannel channel = mDataConnectionTrackerAc;
     if (channel != null) {
       channel.sendMessage(CMD_SET_USER_DATA_ENABLE, enabled ? ENABLED : DISABLED);
       mUserDataEnabled = enabled;
     }
     if (VDBG) log("setUserDataEnable: X enabled=" + enabled);
   }
   这个channel 就是刚才 连接完成后获得的 mDataConnectionTrackerAc ，于是马上向 DataConnectionTracker 发送 CMD_SET_USER_DATA_ENABLE的请求，
   之前 AsyncChannel 的 mDstMessenger 已经初始化了，消息会直接发送给 DataConnectionTracker，DataConnectionTracker没有给MobileDataStateTracker任何反馈信息，直接处理了该消息。
  以上两个应用场景都是用同一个进程内的连个Handler 来说明的。简单地说，两个Handler通信(想象成服务端和客户端）的初始化工作包括两方面
  <1> 初始化连接对象，如mSrcMessenger,mDestmessenger,msrcHandler 等，如果这些初始化没有问题，说明 两个Handler 之间的连接没有问题。
  <2> 建立通信通道，建立通道的消息被服务端handler 处理后，就像客户端的Handler 发送消息，说明连接状态是成功的，比如发送 CMD_CHANNEL_FULL_CONNECTION，MD_CHANNEL_HALF_CONNECTED等消息，让客户端知道通信通道是否已经建立成功。
  如果 客户端的handler 不想同服务端的handler 进行通信了，那么就发送中断连接的消息。
  对于两个不同进程的Handler 进行通信，在进行连接的时候，需要借助Binder 的AIDL机制绑定远程的Service,如
  public int connectSrcHandlerToPackageSync(
       Context srcContext, Handler srcHandler, String dstPackageName, String dstClassName) {
     if (DBG) log("connect srcHandler to dst Package & class E");
 
     mConnection = new AsyncChannelConnection();
 
     /* Initialize the source information */
     mSrcContext = srcContext;
     mSrcHandler = srcHandler;
     mSrcMessenger = new Messenger(srcHandler);
 
     /*
     \* Initialize destination information to null they will
     \* be initialized when the AsyncChannelConnection#onServiceConnected
     \* is called
     */
     mDstMessenger = null;
 
     /* Send intent to create the connection */
     Intent intent = new Intent(Intent.ACTION_MAIN);
     intent.setClassName(dstPackageName, dstClassName);
     boolean result = srcContext.bindService(intent, mConnection, Context.BIND_AUTO_CREATE);
     if (DBG) log("connect srcHandler to dst Package & class X result=" + result);
     return result ? STATUS_SUCCESSFUL : STATUS_BINDING_UNSUCCESSFUL;
   }

 

 

 