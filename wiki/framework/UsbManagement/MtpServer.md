# MtpServer

PC send object via mtp
----------------------------------------------------------------------------------------------------

#### 流程概要

| 序号  | 文件名                                      | 方法名                                    | 方法体                                                    | 说明                      |
| ----- | ------------------------------------------- | ----------------------------------------- | --------------------------------------------------------- | ------------------------- |
|       | [android.process.media]                     |                                           |                                                           |                           |
|       | PC send file to device                      |                                           |                                                           |                           |
| 1     | /frameworks/av/media/mtp/MtpServer.cpp:213  | void MtpServer::run()                     | if (handleRequest()) {                                    |                           |
| 1.1   | /frameworks/av/media/mtp/MtpServer.cpp:364  | bool MtpServer::handleRequest()           | MtpOperationCode operation = mRequest.getOperationCode(); |                           |
| 1.2   | /frameworks/av/media/mtp/MtpServer.cpp:450  | bool MtpServer::handleRequest()           | response = doSendObject();                                | MTP_OPERATION_SEND_OBJECT |
| 1.2.1 | /frameworks/av/media/mtp/MtpServer.cpp:1191 | MtpResponseCode MtpServer::doSendObject() | ret = write(mfr.fd, mData.getData(), initialData);        |                           |

#### 具体说明

1.2.1

````java
1191MtpResponseCode MtpServer::doSendObject() {
...
1237    if (initialData > 0) {
1238        ret = write(mfr.fd, mData.getData(), initialData);
1239    }
````

1.2

````java
361bool MtpServer::handleRequest() {
381    ALOGV("got command %s (%x)", MtpDebug::getOperationCodeName(operation), operation);
383    switch (operation) {
449        case MTP_OPERATION_SEND_OBJECT:
450            response = doSendObject();
````

1.1

````java
361bool MtpServer::handleRequest() {
364    MtpOperationCode operation = mRequest.getOperationCode();
````

1

````java
167void MtpServer::run() {
213        if (handleRequest()) {
214            if (!dataIn && mData.hasData()) {
215                mData.setOperationCode(operation);
216                mData.setTransactionID(transaction);
217                ALOGV("sending data:");
````




Reference
----------------------------------------------------------------------------------------------------
* [Android之 MTP框架和流程分析](http://www.cnblogs.com/skywang12345/p/3474206.html)
* [Android之MTP框架和流程分析(二)](http://lvzg2005.blog.51cto.com/2015450/1563137/)
* https://www.cnblogs.com/kings-boke/p/4467599.html
