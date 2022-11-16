
#（ZT）UNIX本地套接字的使用
进程间通信的一种方式是使用UNIX套接字，人们在使用这种方式时往往用的不是网络套接字，而是一种称为本地套接字的方式。这样做可以避免为黑客留下后门。

创建
使用套接字函数socket创建，不过传递的参数与网络套接字不同。域参数应该是PF_LOCAL或者PF_UNIX，而不能用PF_INET之类。本地套接字的通讯类型应该是SOCK_STREAM或SOCK_DGRAM，协议为默认协议。例如：
```java
int sockfd;
sockfd = socket(PF_LOCAL, SOCK_STREAM, 0);
```

绑定
创建了套接字后，还必须进行绑定才能使用。不同于网络套接字的绑定，本地套接字的绑定的是struct sockaddr_un结构。struct sockaddr_un结构有两个参数：sun_family、sun_path。sun_family只能是AF_LOCAL或AF_UNIX，而sun_path是本地文件的路径。通常将文件放在/tmp目录下。例如：

```java
struct sockaddr_un sun;
sun.sun_family = AF_LOCAL;
strcpy(sun.sun_path, filepath);
bind(sockfd, (struct sockaddr*)&sun, sizeof(sun));
```
监听
本地套接字的监听、接受连接操作与网络套接字类似。

连接
连接到一个正在监听的套接字之前，同样需要填充struct sockaddr_un结构，然后调用connect函数。

连接建立成功后，我们就可以像使用网络套接字一样进行发送和接受操作了。甚至还可以将连接设置为非阻塞模式，这里就不赘述了。

## 关键语句
### C程序
#### 服务端：
```
1)  server_fd = socket_local_server (SOCKET_NAME_XXH, ANDROID_SOCKET_NAMESPACE_ABSTRACT, SOCK_STREAM);
2)  s_fdListen = listen(server_fd, 4);
3)  while((socket = accept(server_fd, NULL, NULL)) > 0)
```

#### 客户端：
```
1)  fd = socket_local_client( SOCKET_NAME_XXH , ANDROID_SOCKET_NAMESPACE_ABSTRACT, SOCK_STREAM);
2)  write(fd, "hello", 5);
```


### JAVA 
#### 客户端：
```
1)  localSocket = new LocalSocket();
2)  localSocket.connect(new LocalSocketAddress(socketAddress));
3)  OutputStream os = localSocket.getOutputStream();
```


### Namespace:

```
LocalSocketAddress.Namespace  ABSTRACT  A socket in the Linux abstract namespace   
LocalSocketAddress.Namespace  FILESYSTEM  A socket named with a normal filesystem path.  
LocalSocketAddress.Namespace  RESERVED  A socket in the Android reserved namespace in /dev/socket. 
```


# java to java

## Java Client
```java
class ClientConnect {
    private static final String TAG = "ClientConnect";
    private static final String name = "com.repackaging.localsocket";
    private LocalSocket Client = null;
    private PrintWriter os = null;
    private BufferedReader is = null;
    private int timeout = 30000;

    public void connect(){
        try {
            Client = new LocalSocket();
            Client.connect(new LocalSocketAddress(name));
            Client.setSoTimeout(timeout);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void send(String[] data) {
        try {
            os = new PrintWriter(Client.getOutputStream());
            for(int i = 0 ; i < data.length ; i ++){
                os.println(data[0]);
            }
            os.println(FLAG);
            os.flush();
            Log.d(TAG,"send");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String recv() {
        Log.d(TAG,"recv");
        String result = null;
        try {
            is = new BufferedReader(new InputStreamReader(Client.getInputStream()));
            result = is.readLine();
            Log.d(TAG, result);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
        }
        return result;
    }

    public void close() {
        try {
            is.close();
            os.close();
            Client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

```

调用代码：
```java
ClientConnect client = new ClientConnect();
client.connect();
client.send(data);
result = client.recv();
client.close();
```

## Java Server
```java
class ServerThread implements Runnable {

    @Override
    public void run() {
        LocalServerSocket server = null;
        BufferedReader mBufferedReader = null;
        PrintWriter os = null;
        LocalSocket connect = null;
        String readString =null;
        try {
            server = new LocalServerSocket("com.repackaging.localsocket");        
            while (true) {
                connect = server.accept();
                Credentials cre = connect.getPeerCredentials();
                Log.i(TAG,"accept socket uid:"+cre.getUid());
                mBufferedReader = new BufferedReader(new InputStreamReader
                        (connect.getInputStream()));
                while((readString=mBufferedReader.readLine())!=null){
                    if(readString.equals("finish")) break;
                    Log.d(TAG,readString);
                }
                os = new PrintWriter(connect.getOutputStream());
                os.println("allow");
                os.flush();
                Log.d(TAG,"send allow");
            }    
        } catch (IOException e) {
            e.printStackTrace();
        }
        finally{
            try {
                mBufferedReader.close();
                os.close();
                connect.close();
                server.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

```

# java as the server, native as a client

Android是建立在Linux之上的OS，在涉及到安全、网络协议、文件加密等功能时，往往需要通过C语言调用底层API来实现，而如何发出指令让C端执行我们想要的功能，并且在执行之后有返回结果呢，这就需要打通Java端进程和C端进程，使之能高效地通信。这样，C端进程用于实现功能，Java端进程负责UI、功能的触发及结果处理就可以了。

对于*nix系统来说，“一切皆为文件”，Socket也不例外，Socket按照收发双方的媒介来说有三种类型：1，通过网络端口；2，通过文件系统；3，通过内存映射文件。具体说来，三种类型均可以用来作为IPC的Socket：1，通过本地回环接口(即LoopBack)127.0.0.1来收发数据；2，通过文件作为收发数据的中转站；3，在内存中开辟一块区域作为收发数据的中转站，此区域仍然使用文件读写API进行访问。LocalSocket支持方式2和方式3，从效率的角度来说，显然是方式3效率最高，那么下面我们就使用LocalSocket来演示如何实现Java端进程与C端进程之间的IPC。

以下的demo是Java端作为server，C端作为client；实际场景中可能更多的是Java端作为client，而C端作为server。

## java as the server

```java
package main.activity;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import android.app.Activity;
import android.net.LocalServerSocket;
import android.net.LocalSocket;
import android.os.Bundle;
import android.util.Log;

/**
 * @author pengyiming
 * @note 启动localSocketServer
 *
 */

public class LocalSocketServerActivity extends Activity
{
    /* 数据段begin */
    private final String TAG = "server";
    
    private ServerSocketThread mServerSocketThread;
    /* 数据段end */
    
    /* 函数段begin */
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        
        mServerSocketThread = new ServerSocketThread();
        mServerSocketThread.start();
    }
    
    @Override
    protected void onDestroy()
    {
        super.onDestroy();
        
        mServerSocketThread.stopRun();
    }
    /* 函数段end */
    
    /* 内部类begin */
    private class ServerSocketThread extends Thread
    {
        private boolean keepRunning = true;
        private LocalServerSocket serverSocket;
        
        private void stopRun()
        {
            keepRunning = false;
        }
        
        @Override
        public void run()
        {
            try
            {
                serverSocket = new LocalServerSocket("pym_local_socket");
            }
            catch (IOException e)
            {
                e.printStackTrace();
                
                keepRunning = false;
            }
            
            while(keepRunning)
            {
                Log.d(TAG, "wait for new client coming !");
                
                try
                {
                    LocalSocket interactClientSocket = serverSocket.accept();
                    
                    //由于accept()在阻塞时，可能Activity已经finish掉了，所以再次检查keepRunning
                    if (keepRunning)
                    {
                        Log.d(TAG, "new client coming !");
                        
                        new InteractClientSocketThread(interactClientSocket).start();
                    }
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                    
                    keepRunning = false;
                }
            }
            
            if (serverSocket != null)
            {
                try
                {
                    serverSocket.close();
                }
                catch (IOException e)
                {
                    e.printStackTrace();
                }
            }
        }
    }
    
    private class InteractClientSocketThread extends Thread
    {
        private LocalSocket interactClientSocket;
        
        public InteractClientSocketThread(LocalSocket interactClientSocket)
        {
            this.interactClientSocket = interactClientSocket;
        }
        
        @Override
        public void run()
        {
            StringBuilder recvStrBuilder = new StringBuilder();
            InputStream inputStream = null;
            try
            {
                inputStream = interactClientSocket.getInputStream();
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                char[] buf = new char[4096];
                int readBytes = -1;
                while ((readBytes = inputStreamReader.read(buf)) != -1)
                {
                    String tempStr = new String(buf, 0, readBytes);
                    recvStrBuilder.append(tempStr);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
                
                Log.d(TAG, "resolve data error !");
            }
            finally
            {
                if (inputStream != null)
                {
                    try
                    {
                        inputStream.close();
                    }
                    catch (IOException e)
                    {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
    /* 内部类end */
}
```

### java as a client.

```java
package main.activity;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

/**
 * @author pengyiming
 * @note 用于启动localSocketClient，向server发送心跳报文
 *
 */

public class LocalSocketClientActivity extends Activity
{
    /* 数据段begin */
    private final String TAG = "client";
    
    private HeartBeatThread mHeartBeatThread;
    
    public native int startHeartBeat();
    /* 数据段end */
    
    /* 函数段begin */
    static
    {
        System.loadLibrary("pymclient");
    }
    
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        
        mHeartBeatThread = new HeartBeatThread();
        mHeartBeatThread.start();
    }
    
    @Override
    protected void onDestroy()
    {
        super.onDestroy();
        
        mHeartBeatThread.stopRun();
    }
    /* 函数段end */
    
    /* 内部类begin */
    private class HeartBeatThread extends Thread
    {
        int ret;
        boolean keepRunning = true;
        
        public void stopRun()
        {
            keepRunning = false;
        }
        
        @Override
        public void run()
        {
            Log.d(TAG, "start heart beat!");
            
            while (keepRunning)
            {
                ret = startHeartBeat();
                
                Log.d(TAG, "ret = " + ret);
                
                if (ret != 0)
                {
                    break;
                }
                
                try
                {
                    sleep(1000);
                }
                catch (InterruptedException e)
                {
                    e.printStackTrace();
                }
            }
            
            Log.d(TAG, "stop heart beat!");
        }
    }
    /* 内部类end */
}
```

上述客户端代码启动了一个线程用于发送“心跳”报文，每隔1s构建一个新的LocalSocket，连接服务端并发送流数据，其核心就在于native方法的实现。值得一提的是，我最初使用原生socket函数，没想connect总是返回错误；后来在同事的提醒下，我参考了Android源码rild.c中socket_local_client的使用，并从socket_local_client.c中抽取出相应代码改写而成。


## native as a client
```h
/* DO NOT EDIT THIS FILE - it is machine generated */
#include <jni.h>
/* Header for class main_activity_LocalSocketClientActivity */

#ifndef _Included_main_activity_LocalSocketClientActivity
#define _Included_main_activity_LocalSocketClientActivity
#ifdef __cplusplus
extern "C" {
#endif

/* socket命名空间(见cutils/sockets.h) */
#define ANDROID_SOCKET_NAMESPACE_ABSTRACT 0
#define ANDROID_SOCKET_NAMESPACE_RESERVED 1
#define ANDROID_SOCKET_NAMESPACE_FILESYSTEM 2

/* socket类型 */
#define SOCK_STREAM      1
#define SOCK_DGRAM       2
#define SOCK_RAW         3
#define SOCK_RDM         4
#define SOCK_SEQPACKET   5
#define SOCK_PACKET      10

/* 清0宏 */
#define MEM_ZERO(pDest, destSize) memset(pDest, 0, destSize)

/* 错误码定义 */
#define NO_ERR 0
#define CREATE_ERR -1
#define CONNECT_ERR -2
#define LINUX_MAKE_ADDRUN_ERROR -3
#define NO_LINUX_MAKE_ADDRUN_ERROR -4
#define CLOSE_ERR -5

/* 是否使用linux的本地socket命令空间 */
#define HAVE_LINUX_LOCAL_SOCKET_NAMESPACE "linux_local_socket_namespace"

#undef main_activity_LocalSocketClientActivity_MODE_PRIVATE
#define main_activity_LocalSocketClientActivity_MODE_PRIVATE 0L
#undef main_activity_LocalSocketClientActivity_MODE_WORLD_READABLE
#define main_activity_LocalSocketClientActivity_MODE_WORLD_READABLE 1L
#undef main_activity_LocalSocketClientActivity_MODE_WORLD_WRITEABLE
#define main_activity_LocalSocketClientActivity_MODE_WORLD_WRITEABLE 2L
#undef main_activity_LocalSocketClientActivity_MODE_APPEND
#define main_activity_LocalSocketClientActivity_MODE_APPEND 32768L
#undef main_activity_LocalSocketClientActivity_MODE_MULTI_PROCESS
#define main_activity_LocalSocketClientActivity_MODE_MULTI_PROCESS 4L
#undef main_activity_LocalSocketClientActivity_BIND_AUTO_CREATE
#define main_activity_LocalSocketClientActivity_BIND_AUTO_CREATE 1L
#undef main_activity_LocalSocketClientActivity_BIND_DEBUG_UNBIND
#define main_activity_LocalSocketClientActivity_BIND_DEBUG_UNBIND 2L
#undef main_activity_LocalSocketClientActivity_BIND_NOT_FOREGROUND
#define main_activity_LocalSocketClientActivity_BIND_NOT_FOREGROUND 4L
#undef main_activity_LocalSocketClientActivity_BIND_ABOVE_CLIENT
#define main_activity_LocalSocketClientActivity_BIND_ABOVE_CLIENT 8L
#undef main_activity_LocalSocketClientActivity_BIND_ALLOW_OOM_MANAGEMENT
#define main_activity_LocalSocketClientActivity_BIND_ALLOW_OOM_MANAGEMENT 16L
#undef main_activity_LocalSocketClientActivity_BIND_WAIVE_PRIORITY
#define main_activity_LocalSocketClientActivity_BIND_WAIVE_PRIORITY 32L
#undef main_activity_LocalSocketClientActivity_BIND_IMPORTANT
#define main_activity_LocalSocketClientActivity_BIND_IMPORTANT 64L
#undef main_activity_LocalSocketClientActivity_BIND_ADJUST_WITH_ACTIVITY
#define main_activity_LocalSocketClientActivity_BIND_ADJUST_WITH_ACTIVITY 128L
#undef main_activity_LocalSocketClientActivity_CONTEXT_INCLUDE_CODE
#define main_activity_LocalSocketClientActivity_CONTEXT_INCLUDE_CODE 1L
#undef main_activity_LocalSocketClientActivity_CONTEXT_IGNORE_SECURITY
#define main_activity_LocalSocketClientActivity_CONTEXT_IGNORE_SECURITY 2L
#undef main_activity_LocalSocketClientActivity_CONTEXT_RESTRICTED
#define main_activity_LocalSocketClientActivity_CONTEXT_RESTRICTED 4L
#undef main_activity_LocalSocketClientActivity_RESULT_CANCELED
#define main_activity_LocalSocketClientActivity_RESULT_CANCELED 0L
#undef main_activity_LocalSocketClientActivity_RESULT_OK
#define main_activity_LocalSocketClientActivity_RESULT_OK -1L
#undef main_activity_LocalSocketClientActivity_RESULT_FIRST_USER
#define main_activity_LocalSocketClientActivity_RESULT_FIRST_USER 1L
#undef main_activity_LocalSocketClientActivity_DEFAULT_KEYS_DISABLE
#define main_activity_LocalSocketClientActivity_DEFAULT_KEYS_DISABLE 0L
#undef main_activity_LocalSocketClientActivity_DEFAULT_KEYS_DIALER
#define main_activity_LocalSocketClientActivity_DEFAULT_KEYS_DIALER 1L
#undef main_activity_LocalSocketClientActivity_DEFAULT_KEYS_SHORTCUT
#define main_activity_LocalSocketClientActivity_DEFAULT_KEYS_SHORTCUT 2L
#undef main_activity_LocalSocketClientActivity_DEFAULT_KEYS_SEARCH_LOCAL
#define main_activity_LocalSocketClientActivity_DEFAULT_KEYS_SEARCH_LOCAL 3L
#undef main_activity_LocalSocketClientActivity_DEFAULT_KEYS_SEARCH_GLOBAL
#define main_activity_LocalSocketClientActivity_DEFAULT_KEYS_SEARCH_GLOBAL 4L
/*
 * Class:     main_activity_LocalSocketClientActivity
 * Method:    startHeartBeat
 * Signature: ()I
 */
JNIEXPORT jint JNICALL Java_main_activity_LocalSocketClientActivity_startHeartBeat
  (JNIEnv *, jobject);

#ifdef __cplusplus
}
#endif
#endif
```

客户端native方法实现：


```c
/* 头文件begin */
#include "main_activity_LocalSocketClientActivity.h"

#include <sys/socket.h>
#include <sys/un.h>
#include <stddef.h>
#include <string.h>
/* 头文件end */

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Class:     main_activity_LocalSocketClientActivity
 * Method:    startHeartBeat
 */
JNIEXPORT jint JNICALL Java_main_activity_LocalSocketClientActivity_startHeartBeat(JNIEnv * env, jobject object)
{
    int socketID;
    struct sockaddr_un serverAddr;
    char path[] = "pym_local_socket\0";
    int ret;

    socketID = socket_local_client(path, ANDROID_SOCKET_NAMESPACE_ABSTRACT, SOCK_STREAM);
    if (socketID < 0)
    {
        return socketID;
    }

    ret = close(socketID);
    if (ret < 0)
    {
        return CLOSE_ERR;
    }

    return NO_ERR;
}

/* 创建本地socket客户端 */
int socket_local_client(const char *name, int namespaceId, int type)
{
    int socketID;
    int ret;

    socketID = socket(AF_LOCAL, type, 0);
    if(socketID < 0)
    {
        return CREATE_ERR;
    }

    ret = socket_local_client_connect(socketID, name, namespaceId, type);
    if (ret < 0)
    {
        close(socketID);

        return ret;
    }

    return socketID;
}

/* 连接到相应的fileDescriptor上 */
int socket_local_client_connect(int fd, const char *name, int namespaceId, int type)
{
    struct sockaddr_un addr;
    socklen_t socklen;
    size_t namelen;
    int ret;

    ret = socket_make_sockaddr_un(name, namespaceId, &addr, &socklen);
    if (ret < 0)
    {
        return ret;
    }

    if(connect(fd, (struct sockaddr *) &addr, socklen) < 0)
    {
        return CONNECT_ERR;
    }

    return fd;
}

/* 构造sockaddr_un */
int socket_make_sockaddr_un(const char *name, int namespaceId, struct sockaddr_un *p_addr, socklen_t *socklen)
{
    size_t namelen;

    MEM_ZERO(p_addr, sizeof(*p_addr));
#ifdef HAVE_LINUX_LOCAL_SOCKET_NAMESPACE

    namelen  = strlen(name);

    // Test with length +1 for the *initial* '\0'.
    if ((namelen + 1) > sizeof(p_addr->sun_path))
    {
        return LINUX_MAKE_ADDRUN_ERROR;
    }
    p_addr->sun_path[0] = 0;
    memcpy(p_addr->sun_path + 1, name, namelen);

#else

    namelen = strlen(name) + strlen(FILESYSTEM_SOCKET_PREFIX);

    /* unix_path_max appears to be missing on linux */
    if (namelen > (sizeof(*p_addr) - offsetof(struct sockaddr_un, sun_path) - 1))
    {
        return NO_LINUX_MAKE_ADDRUN_ERROR;
    }

    strcpy(p_addr->sun_path, FILESYSTEM_SOCKET_PREFIX);
    strcat(p_addr->sun_path, name);

#endif

    p_addr->sun_family = AF_LOCAL;
    *socklen = namelen + offsetof(struct sockaddr_un, sun_path) + 1;

    return NO_ERR;
}

#ifdef __cplusplus
}
#endif
```

注意到100~101行比较特殊，是从`p_addr->sun_path[1]`开始拷贝本地域名，这就是之前为什么一直connect不上的原因，至于为什么偏移1个字节来拷贝本地域名，你可以在*nix系统下输入"man 7 unix"来找到原因。

先启动server，再启动client就可以看到结果了。对了，在成功创建并已自动连接后，我并未发送任何数据，其实发送数据就是写入文件，It's your trun now! 在close之前加入这段代码吧~

```c
int ret;
char buf[] = "hello";

ret = write(socketID, buf, strlen(buf));
```

## Note

##############################################
目的：实现本地 C程序与apk的socket通信。
原理：没有涉及到网络通信，所以使用Android封装的local socket要更简单
参考：系统源码RIL模块
整理：Andy.xie
###############################################

### C程序 服务端：

1. server_fd = socket_local_server (SOCKET_NAME_XXH, ANDROID_SOCKET_NAMESPACE_ABSTRACT, SOCK_STREAM);
2. s_fdListen = listen(server_fd, 4);
3. while((socket = accept(server_fd, NULL, NULL)) > 0)


### C 客户端：

1. fd = socket_local_client( SOCKET_NAME_XXH , ANDROID_SOCKET_NAMESPACE_ABSTRACT, SOCK_STREAM);
2. write(fd, "hello", 5);


### JAVA 客户端：

1. localSocket = new LocalSocket();
2. localSocket.connect(new LocalSocketAddress(socketAddress));
3. OutputStream os = localSocket.getOutputStream();


### Namespace:

LocalSocketAddress.Namespace  ABSTRACT  A socket in the Linux abstract namespace   
LocalSocketAddress.Namespace  FILESYSTEM  A socket named with a normal filesystem path.  
LocalSocketAddress.Namespace  RESERVED  A socket in the Android reserved namespace in /dev/socket. 


# References

* [Android中LocalSocket使用](http://www.cnblogs.com/bastard/archive/2012/10/09/2717052.html)




