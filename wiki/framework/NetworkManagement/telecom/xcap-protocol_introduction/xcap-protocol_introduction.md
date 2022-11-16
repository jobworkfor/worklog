# XCAP 协议

XML配置访问协议（XCAP）The XML Configuration Access Protocol，是一种应用层协议，它允许一个客户端来读，写，修改和删除应用程序配置数据存储在服务器上的XML格式。(相关文档：rfc4825-XCAP 协议标准文档 )

XCAP映射XML文件子树和元素属性到HTTP URIs，使这些组件可以直接使用HTTP协议的客户端访问。

## 引言

如名字所示，XCAP是一种配置访问协议。它使用XML文档格式来存储应用程序的配置数据，允许客户端读取、写入及修改配置数据。

XCAP映射XML文档的子树和元素属性到HTTP URL，所以这些组件可以通过HTTP直接获取。XCAP是一种映射XML文档和文档属性到HTTP URL的一种惯例，一个资源的修改如何影响其他资源的规则，数据验证的约束，访问资源时相关的授权策略。因为这种结构，普通HTTP能够用来操作数据。

## 应用程序

在很多通信应用程序中，如VoIP，IM和presence，需要网络服务器去获取个性化用户信息给服务请求的进程。这些个性化用户信息存在于网络中，但由终端用户自己管理。这些管理可通过各种获取终端完成，包括web，无线手机，或pc应用程序。个性化用户信息的例子包括presence，授权策略和presence lists。Presence lists一个观察者需要的一些用户的presence。一种获取列表的presence信息的方法是订阅代表presence list的资源。在这种情况下，资源列表服务器（Resource List Server，RLS）需要获取这个列表来处理自身的SIP订阅请求。另一种获取用户presence list的方法是单独订阅每个用户。在这种情况下，可以使用一个服务器来方便地存储list，当客户端启动时，它从服务器获取list。这允许用户从不同的终端获取他们的资源列表。

## 操作概述

每个利用XCAP的应用程序可以指定应用程序的用法。这种应用程序的用法定义了被应用程序使用的数据的XML模式，和其他关键信息片段。XCAP的首要任务就是允许客户端读、写、修改、创建和删除数据片段。这些操作支持使用HTTP 1.1。

一个XCAP服务器扮演了一组XML文档的仓库。每个应用程序都有一组文档，每个应用程序的每个用户也都有一组文档。为了访问这些文档中的一个文档的某一组件，XCAP定义了一个算法来构建能够指向那个组件的URL。组件指示了文档里的所有元素或属性。因此，XCAP使用的HTTP URL指向文档或XML文档本身的一块信息。一个遵守此处定义的命名惯例和验证约束的HTTP资源就叫做`XCAP资源`。

因为XCAP资源也是HTTP资源，它们可以使用HTTP方法获取。使用HTTP GET获取`XCAP资源`，用HTTP PUT创建或修改，HTTP DELETE删除资源。与HTTP关联的资源的属性，如实体标签，也被应用到XCAP资源。实体标签在XCAP里非常有用，因为它们允许执行一组条件操作。

一个XCAP资源不过是XML文档，XML文档里的元素，关联到元素的属性。每个HTTP GET、PUT、DELETE方法能够执行到属于一个用户的特定应用的资源。

映射XCAP资源到HTTP URI可下面方式完成：
```
<?xmlversion="1.0"encoding="ISO-8859-1"?>
<xcap-caps>
    <users>
        <user1>hgs@cs.columbia.edu</user1>
        <user2>mss2103@cs.columbia.edu</user2>
    </users>
</xcap-caps>
```
获取<user1>的HTTP URI看起来是这样的：

|Part1|Part2|Part3|
|-|-|-|
|HTTP Method|XCAP Root/Application(k)/user(m)/document(i)/~~/xcap-caps/users/user1|HTTP(version)|
|GET/PUT/DELETE|XML里描述资源的真实路径|HTTP 1.0/1.1|

### Part2详解：
服务器检索被访问的应用程序，按照XCAP Root/Application(k)。如前面提到的，每个应用程序和每个应用程序的用户有它们自己的目录。所以整个系统是以层次化的结构存储的，以XCAP ROOT作为顶层，应用程序作为这个根的直接子节点，用户构成应用程序的子节点，每个用户目录下有一组XML文件。每个XML文件里面，所有元素有一个根节点，每个元素可以有一些属性。

上面的路径尝试在XCAP服务器上获取应用程序k下的用户m的i文档。目前为止的这个路径（`Application(k)/user(m)/document(i)`）叫做文档选择器。"`~~`"叫路径分隔符，它分隔了文档选择器和节点选择器。路径之后的就是节点选择器，所以上面请求的节点选择器是“`xcap-caps/users/user1`”，这告诉服务器，从文档i的根节点`<xcap-caps>`开始，在`<xcap-caps>`里找到`<users>`，在`<users>`里找到`<user1>`。当目标被定位到时，可执行指定的方法（`GET`, `PUT`, `DELETE`）。

如果节点选择器为空，则HTTP的方法将被应用到选定的文档上。

## 总结：
1. XCAP是一种能够映射HTTP URL到服务器上的XML内部结构的协议，这些XML文档保存每个应用程序里的每个用户的个性化信息。
2. 一个符合XCAP的URL由三部分组成，第一部分叫文档选择器，与普通HTTP URL类似，用于定位XML文档，路径结构是：Application/User/Document；第二部分是路径分隔符：`~~`；第三部分叫节点选择器，使用XPath表达式来定位XML的元素、属性等。
3. XCAP服务器可以用HTTP协议直接访问，对于定位到的XML元素、属性等，可用HTTP GET方法查询值，HTTP PUT创建或修改，用HTTP DELETE删除。
