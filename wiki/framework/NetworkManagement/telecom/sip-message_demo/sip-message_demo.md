# MESSAGE消息
## 头字段填写说明

```
Call-id：                 必选
CSeq：                   必选
From：                   必选
To：                       必选
Max-Forwards： 必选
Via：                      必选
常用的可选参数：指定的消息体
```

## 消息实例
发送MESSAGE请求消息给192.168.2.48的6010端口，参考消息如下（带了“Hello”的消息体）：
```
MESSAGE sip:1897778888@192.168.2.48:6010 SIP/2.0
Call-ID: 8e12c17121ac4121bf927f6fd8013358@192.168.2.89
From: <sip:01052237300@192.168.2.89>;tag=-0037-708c9a5cba8dd878
To: <sip:1897778888@192.168.2.89>
CSeq: 1 MESSAGE
Via: SIP/2.0/UDP 192.168.2.89:14010;branch=z9hG4bK--22bd7222
Max-Forwards: 30
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: <sip:192.168.2.89:14010>
Content-Type: text/plain
Content-Length: 5

Hello
```

收到来自192.168.2.48的6010端口的返回消息，参考消息如下（修改了消息体的内容，变成了“Hello amigo”）：
```
 SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.2.89:14010;branch=z9hG4bK--22bd7222
From: <sip:01052237300@192.168.2.89>;tag=-0037-708c9a5cba8dd878
To: <sip:1897778888@192.168.2.89>;tag=-002-3c18e810ab17c76f
Call-ID: 8e12c17121ac4121bf927f6fd8013358@192.168.2.89
CSeq: 1 MESSAGE
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: <sip:192.168.2.48:54010>
Content-Type: text/plain
Content-Length: 11

Hello amigo
```

# REGISTER消息

1）头字段填写说明
```
Call-id：                 必选
Cseq：                   必选
From：                   必选
To：                       必选
Max-Forwards： 必选
Via：                      必选
Contact：              必选
Authorization：   必选
Expires：               常用可选头
```

2）非鉴权注册消息实例
在该实例中192.168.2.161机器发送注册消息给192.168.2.89服务器，发送消息实例如下：
```
 REGISTER sip:192.168.2.89 SIP/2.0
Via: SIP/2.0/UDP 192.168.2.161:10586
Max-Forwards: 70
From: <sip:01062237496@192.168.2.89>;tag=ca04c1391af3429491f2c4dfbe5e1b2e;epid=4f2e395931
To: <sip:01062237496@192.168.2.89>
Call-ID: da56b0fab5c54398b16c0d9f9c0ffcf2@192.168.2.161
CSeq: 1 REGISTER
Contact: <sip:192.168.2.161:10586>;methods="INVITE, MESSAGE, INFO, SUBSCRIBE, OPTIONS, BYE, CANCEL, NOTIFY, ACK, REFER"
User-Agent: RTC/1.2.4949 (BOL SIP Phone 1005)
Event: registration
Allow-Events: presence
Content-Length: 0
```

当注册成功（回送200 OK）时，服务器发送的res消息参考如下：
```
 SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.2.161:10586
From: <sip:01062237496@192.168.2.89>;tag=ca04c1391af3429491f2c4dfbe5e1b2e;epid=4f2e395931
To: <sip:01062237496@192.168.2.89>;tag=-00834-14d0805b62bc026d
Call-ID: da56b0fab5c54398b16c0d9f9c0ffcf2@192.168.2.161
CSeq: 1 REGISTER
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: sip:192.168.2.161:10586
Content-Length: 0
Expires: 3600
```
3）鉴权注册消息实例
当需要鉴权注册时，当请求端192.168.2.161使用BOL或xlite等发送注册消息给192.168.2.89服务器时，服务器对192.168.2.161发送“401 Unauthorized”信息给请求端，提示请求段需要带上鉴权信息重新注册，请求端带上鉴权信息后（带有“Authorization”头字段）重新向服务器注册，服务器验证鉴权头的正确性，如果鉴权成功，给请求端发送200 OK消息。若失败，继续发送401消息。
第一步：请求端（192.168.2.161）发送REGISTER消息，参考消息如下：
```
 REGISTER sip:192.168.2.89 SIP/2.0
Via: SIP/2.0/UDP 192.168.2.161:8021
Max-Forwards: 70
From: <sip:01062237493@192.168.2.89>;tag=efca469543ce4788a6a6a2c7b66cd01f;epid=de4504430d
To: <sip:01062237493@192.168.2.89>
Call-ID: c88a247a74b54a8c9e676bdde3bba6c9@192.168.2.161
CSeq: 1 REGISTER
Contact: <sip:192.168.2.161:8021>;methods="INVITE, MESSAGE, INFO, SUBSCRIBE, OPTIONS, BYE, CANCEL, NOTIFY, ACK, REFER"
User-Agent: RTC/1.2.4949 (BOL SIP Phone 1005)
Event: registration
Allow-Events: presence
Content-Length: 0
```
第二步：服务器端（192.168.2.89）检查到需要鉴权，给请求端发送401结果码，并带上“WWW-Authenticate”头信息，参考消息如下：
```
 SIP/2.0 401 Unauthorized
Via: SIP/2.0/UDP 192.168.2.161:8021
From: <sip:01062237493@192.168.2.89>;tag=efca469543ce4788a6a6a2c7b66cd01f;epid=de4504430d
To: <sip:01062237493@192.168.2.89>;tag=-001893-38ba013ba3dde36e
Call-ID: c88a247a74b54a8c9e676bdde3bba6c9@192.168.2.161
CSeq: 1 REGISTER
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: <sip:192.168.2.89:14010>
Content-Length: 0
WWW-Authenticate: Digest realm="192.168.2.89", qop="auth", nonce="e17d377c3d2d9c343e26576a7fd04738481dfc10", opaque="", stale=FALSE, algorithm=MD5
```
第三步：请求端（192.168.2.161）通过“Authorization”头字段带上鉴权头信息，发送一个新的REGISTER消息，参考消息如下：
```
 REGISTER sip:192.168.2.89 SIP/2.0
Via: SIP/2.0/UDP 192.168.2.161:8021
Max-Forwards: 70
From: <sip:01062237493@192.168.2.89>;tag=efca469543ce4788a6a6a2c7b66cd01f;epid=de4504430d
To: <sip:01062237493@192.168.2.89>
Call-ID: c88a247a74b54a8c9e676bdde3bba6c9@192.168.2.161
CSeq: 2 REGISTER
Contact: <sip:192.168.2.161:8021>;methods="INVITE, MESSAGE, INFO, SUBSCRIBE, OPTIONS, BYE, CANCEL, NOTIFY, ACK, REFER"
User-Agent: RTC/1.2.4949 (BOL SIP Phone 1005)
Authorization: Digest username="01062237493", realm="192.168.2.89", qop=auth, algorithm=MD5, uri="sip:192.168.2.89", nonce="e17d377c3d2d9c343e26576a7fd04738481dfc10", nc=00000001, cnonce="12660455546344082314666316435946", response="f57e47ce03162293b9ced07362ce2b79"
Event: registration
Allow-Events: presence
Content-Length: 0
```
第四步：服务器端（192.168.2.89）验证鉴权信息的合法性，若验证成功，发送200 OK消息，参考消息如下：
```
 SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.2.161:8021
From: <sip:01062237493@192.168.2.89>;tag=efca469543ce4788a6a6a2c7b66cd01f;epid=de4504430d
To: <sip:01062237493@192.168.2.89>;tag=-001894-a5eb977c8969aa51
Call-ID: c88a247a74b54a8c9e676bdde3bba6c9@192.168.2.161
CSeq: 2 REGISTER
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: sip:192.168.2.161:8021
Content-Length: 0
Expires: 3600
```

# SUBSCRIBE消息
1）头字段填写说明
```
Call-id：                 必选
CSeq：                   必选
From：                    必选
To：                        必选
Max-Forwards： 必选
Via：                       必选
Expires：                常用可选头
```
2）消息实例
请求端（192.168.2.161）给服务器端（192.168.2.89）发送SUBSCRIBE消息，参考消息如下：
```
 SUBSCRIBE sip:01062237498@192.168.2.89:5060 SIP/2.0
Via: SIP/2.0/UDP 192.168.2.161:32092;branch=z9hG4bK-d87543-ec03ee3e022acf28-1--d87543-;rport
Max-Forwards: 70
Contact: <sip:01062237498@192.168.2.161:32092>
To: "01062237498"<sip:01062237498@192.168.2.89:5060>
From: "01062237498"<sip:01062237498@192.168.2.89:5060>;tag=e01c2548
Call-ID: NDQzMGE1MDMzYWU0NjRiYzMxMGY3NGUxMjBhMjBkNTQ.
CSeq: 1 SUBSCRIBE
Expires: 300
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, NOTIFY, MESSAGE, SUBSCRIBE, INFO
User-Agent: eyeBeam release 1011d stamp 40820
Event: message-summary
Content-Length: 0
```
服务器端（192.168.2.89）发送回执的200 OK信息，参考消息如下：
```
 SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.2.161:32092;branch=z9hG4bK-d87543-ec03ee3e022acf28-1--d87543-;rport
From: "01062237498"<sip:01062237498@192.168.2.89:5060>;tag=e01c2548
To: "01062237498"<sip:01062237498@192.168.2.89:5060>
Call-ID: NDQzMGE1MDMzYWU0NjRiYzMxMGY3NGUxMjBhMjBkNTQ.
CSeq: 1 SUBSCRIBE
Content-Length: 0
```

# INVITE消息

1）头字段填写说明
```
必选头域如下：
Call-id
Contact
CSeq
From
To
Max-Forwards
Via
Supported
Allow
常用可选头域：
Accept
Authorization
Content-length
Content-type
Record-Route
Route
Require
Proxy-Authorization
Proxy-require
P-asserted-identity
P-prefered-identity
Privacy
```

2）非鉴权INVITE消息实例
在这个实例中，笔者在本机（192.168.2.161）上使用BOL注册了17899998888号码，呼叫01062230001号码时发送INVITE消息给服务器（192.168.2.89）的软交换，发送INVITE消息参考如下：
```
 INVITE sip:01062230001@192.168.2.89 SIP/2.0
Via: SIP/2.0/UDP 192.168.2.161:9545
Max-Forwards: 70
From: "Administrator" <sip:17899998888@192.168.2.89>;tag=2dc6e1000081463ba14f7db4e50b8643;epid=d6b5434cef
To: <sip:01062230001@192.168.2.89>
Call-ID: 31e72e80d5b04f52aba6cb8be8f3c0c0@192.168.2.161
CSeq: 1 INVITE
Contact: <sip:192.168.2.161:9545>
User-Agent: RTC/1.2
Content-Type: application/sdp
Content-Length: 691

v=0
o=- 0 0 IN IP4 192.168.2.161
s=session
c=IN IP4 192.168.2.161
b=CT:1000
t=0 0
m=audio 56284 RTP/AVP 97 111 112 6 0 8 4 5 3 101
k=base64:fGmazgf5GXZfJxZ27G9A7rxA4B7KX0pHrjYELKphPog
a=rtpmap:97 red/8000
a=rtpmap:111 SIREN/16000
a=fmtp:111 bitrate=16000
a=rtpmap:112 G7221/16000
a=fmtp:112 bitrate=24000
a=rtpmap:6 DVI4/16000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:4 G723/8000
a=rtpmap:5 DVI4/8000
a=rtpmap:3 GSM/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=encryption:optional
m=video 61432 RTP/AVP 34 31
k=base64:W5uTU8sIQjJVPWyRF31GZouVwAHFtE1cAmblK+mvDdI
a=recvonly
a=rtpmap:34 H263/90000
a=rtpmap:31 H261/90000
a=encryption:optional
```

其中m行表示支持的媒体编码，其中“m=audio 56284 RTP/AVP 97 111 112 6 0 8 4 5 3 101”指明了几种支持的音频媒体类型，“m=video 61432 RTP/AVP 34 31”指明了几种支持的视频媒体类型。软交换服务器（192.168.2.89）接收到INVITE消息后，即刻发送了100 trying消息，如下所示：
```
SIP/2.0 100 Trying
Via: SIP/2.0/UDP 192.168.2.161:9545
From: "Administrator" <sip:17899998888@192.168.2.89>;tag=2dc6e1000081463ba14f7db4e50b8643;epid=d6b5434cef
To: <sip:01062230001@192.168.2.89>
Call-ID: 31e72e80d5b04f52aba6cb8be8f3c0c0@192.168.2.161
CSeq: 1 INVITE
Content-Length: 0
```

软交换服务器（192.168.2.89）查找被叫号码消息，并发送INVITE消息给被叫的地址，接收到被叫的100 trying消息，而后接收到180 Ringing消息，软交换服务器给主叫方也发送180 Ringing消息，告知被叫已振铃，发送消息如下：（第一行可不关注，是笔者公司的底层打出的消息）：
[16:15:59] ===SIPTransaction Send SIP message (455 bytes) to 192.168.2.161:9545
```
SIP/2.0 180 Ringing
Via: SIP/2.0/UDP 192.168.2.161:9545
From: "Administrator" <sip:17899998888@192.168.2.89>;tag=2dc6e1000081463ba14f7db4e50b8643;epid=d6b5434cef
To: <sip:01062230001@192.168.2.89>;tag=-006773-7d10081ef45af150
Call-ID: 31e72e80d5b04f52aba6cb8be8f3c0c0@192.168.2.161
CSeq: 1 INVITE
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: <sip:192.168.2.89:14010>
Content-Length: 0
```
软交换服务器（192.168.2.89）接收到被叫的INVITE消息的200 OK消息，给主叫方也发送200 OK消息，消息参考如下：
```
SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.2.89:14010;branch=z9hG4bK--50c44f35
From: <sip:17899998888@192.168.2.89>;tag=-002221-d749165cdfed2151
To: <sip:01062230001@192.168.2.89>;tag=6b3e0000bf5c0000
Call-ID: fdfa416f8779a8701af1086b07879a65@192.168.2.89
CSeq: 1 INVITE
Contact: <sip:192.168.2.161:5060>
Content-Type: application/sdp
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Content-Length: 118

v=0
o=- 1 1 IN IP4 192.168.2.161
s=-
t=0 0
m=audio 19194 RTP/AVP 8
c=IN IP4 192.168.2.161
a=rtpmap:8 PCMA/8000
```
3）签权INVITE消息实例

# ACK消息
1）头字段填写说明
```
必选头域如下：
Call-id
Cseq
From
To
Max-Forwords
Via
常用可选头域：
Content-Length
Content-Type
Route
```

2）消息实例

在“4、INVITE消息”中讲到了主叫方接收到INVITE消息的200 消息后，接着给主叫方发送ACK消息，消息参考如下：
```
ACK sip:192.168.2.89:14010 SIP/2.0
Via: SIP/2.0/UDP 192.168.2.161:9545
Max-Forwards: 70
From: "Administrator" <sip:17899998888@192.168.2.89>;tag=2dc6e1000081463ba14f7db4e50b8643;epid=d6b5434cef
To: <sip:01062230001@192.168.2.89>;tag=-006773-7d10081ef45af150
Call-ID: 31e72e80d5b04f52aba6cb8be8f3c0c0@192.168.2.161
CSeq: 1 ACK
User-Agent: RTC/1.2
Content-Length: 0
```

# BYE消息

1）头字段填写说明
```
必选头域如下：
Call-id
Cseq
From
To
Max-Forwards
Via
常用可选头域：
Content-Length
Content-Type
Route
Reason
```

2）消息实例
本实例笔者在本机（192.168.2.161）上注册了17899998888号码，呼叫01062230001号码时发送INVITE消息给服务器（192.168.2.89）的软交换，并与呼叫的号码建立通话后，主叫方主动挂断时，BYE消息如下所示：
```
 BYE sip:192.168.2.89:14010 SIP/2.0
Via: SIP/2.0/UDP 192.168.2.161:9545
Max-Forwards: 70
From: "Administrator" <sip:17899998888@192.168.2.89>;tag=2dc6e1000081463ba14f7db4e50b8643;epid=d6b5434cef
To: <sip:01062230001@192.168.2.89>;tag=-006773-7d10081ef45af150
Call-ID: 31e72e80d5b04f52aba6cb8be8f3c0c0@192.168.2.161
CSeq: 2 BYE
User-Agent: RTC/1.2
Content-Length: 0
```
服务器发送200 OK消息，参考实例如下：
```
SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.2.161:9545
From: "Administrator" <sip:17899998888@192.168.2.89>;tag=2dc6e1000081463ba14f7db4e50b8643;epid=d6b5434cef
To: <sip:01062230001@192.168.2.89>;tag=-006773-7d10081ef45af150
Call-ID: 31e72e80d5b04f52aba6cb8be8f3c0c0@192.168.2.161
CSeq: 2 BYE
Content-Length: 0
```
# PRACK消息

1）头字段填写说明
```
必选头域如下：
Call-id
Cseq
From
To
Max-Forwards
Via
RAck
常用可选头域：
Content-Type
Content-Length
```

2）消息实例
如下是PRACK消息的参考实例：
```
PRACK sip:192.168.2.154:5060 SIP/2.0
CSeq: 2 PRACK
Call-ID: 0112114b0ca1d73c3fbdc7036e4672c8@huawei.com
Contact: <sip:01055554444@192.168.2.46>
Content-Length: 0
From: <sip:01055554444@192.168.2.154>;tag=6c789654
To: <sip:01062237400@192.168.2.154>;tag=0012-f1939f63004dbd16
Via: SIP/2.0/UDP 192.168.2.46;branch=z9hG4bK04982ba62
User-Agent: Huawei-MC820/1.0.0
Supported: 100rel
RAck: 1 1 INVITE
```

# INFO消息
1）头字段填写说明
```
必选头域如下：
Call-id
Cseq
From
To
Max-Forwards
Via
常用可选头域：
Content-Type
Content-Length
Route
```
2）消息实例
在笔者开发过程中，媒体服务器与软交换服务器之间的使用的是INFO消息交互，如下消息为软交换服务器向媒体服务器发送的INFO消息（请求开始录音），参考如下：
```
INFO sip:192.168.2.89:14010 SIP/2.0
Call-ID: 52f3d02182b72d37c48cea5dd013a401@192.168.2.89
From: <sip:msml@minicc:5090>;tag=013913-74fa8415d2902b1c
To: <sip:as@cintel.net.cn>;tag=-00708-b879297623d39362
CSeq: 1 INFO
Via: SIP/2.0/UDP 192.168.2.89:5090;branch=z9hG4bKf06b482d
Max-Forwards: 30
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: <sip:192.168.2.89:5090>
Content-Type: application/msml+xml
Content-Length: 164

<?xml version="1.0" encoding="US-ASCII"?>
<msml version="1.1">
<event name="app.startingRecord" id="conf:002221c6082350d233/dialog:PRLeg708">
</event>
</msml>
```
如下是媒体服务器回送的200  OK消息，消息参考如下：
```
SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.2.89:5090;branch=z9hG4bKf06b482d
From: <sip:msml@minicc:5090>;tag=013913-74fa8415d2902b1c
To: <sip:as@cintel.net.cn>;tag=-00708-b879297623d39362
Call-ID: 52f3d02182b72d37c48cea5dd013a401@192.168.2.89
CSeq: 1 INFO
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,REGISTER,INFO,UPDATE,PRACK,REFER,SUBSCRIBE,NOTIFY,MESSAGE
Contact: <sip:192.168.2.89:14010>
Content-Length: 0
```

# OPTIONS消息
1）头字段填写说明
```
必选头域如下：
Call-id
Cseq
From
To
Max-Forwords
Via
常用可选头域：
Accept
Allow
Supported
```

2）消息实例
参考实例如下所示：
```
OPTIONS sip:user@carrier.com SIP/2.0
Via: SIP/2.0/UDP cavendish.kings.cambridge.edu.uk; branch=z0hG4bK1834
Max-Forwards: 70
To: <sip:user@proxy.carrier.com>
From: J.C. Maxwell <sip:james.maxwell@kings.cambridge.edu.uk>; tag=34
Call-ID: 9352812@cavendish.kings.cambridge.edu.uk
CSeq: 1 OPTIONS
Content-Length: 0
```

# NOTIFY消息
参考消息实例如下所示：
```
NOTIFY sip:tyoung@parlour.elasticity.co.uk SIP/2.0
Via SIP/2.0/UDP cartouche.rosettastone.org:5060; branch=z9hG4bK3841323
Max-Forwards: 70
To: Thomas Young <sip:tyoung@elasticity.co.uk>; tag=1814
From: <sip:ptolemy@rosettastone.org>; tag=5363956k
Call-ID: 452k59252058dkfj34924lk34
CSeq: 3 NOTIFY
Contact: <sip:Ptolemy@cartouche.rosettastone.org>
Event: dialog
Subscription-State: active
Allow-Event: dialog
Content-Type: application/xml + dialog
Content-Length: 消息体长度

(xml格式的消息体 )
```

# REFER消息
参考消息实例如下所示：

```
REFER sip:m.rejewski@biuroszyfrow.pl SIP/2.0"
Via SIP/2.0/UDP lab34.bletchleypark.co.uk:5060; branch=z9hG4bK932039
Max-Forwards: 69
To: <sip:m.rejewski@biuroszyfrow.pl>; tag=ACEBDC
From: Alan Turing <sip:turing@bletchleypark.co.uk>; tag=213424
Call-ID: 3419fak3kFD23s1A9dkl
CSeq; 5412 REFER
Refer-To: <sip:info@scherbius-ritter.com>
Content-Length: 0
```
