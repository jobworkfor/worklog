

Call Process
----------------------------------------------------------------------------------------------------
调用命令
```
base=/system
export CLASSPATH=$base/framework/pm.jar
exec app_process $base/bin com.android.commands.pm.Pm "$@"
```

所在进程
```
root      2066  1035  494984 44096 futex_wait 7ffef4261c48 S app_process
```

Install
----------------------------------------------------------------------------------------------------

frameworks/base/cmds/pm/src/com/android/commands/pm/Pm.java

```
public int run(String[] args) throws RemoteException {
        if ("install".equals(op)) {
            return runInstall();
        }
}
```




<div id="article_content" class="article_content tracking-ad" data-mod="popu_307" data-dsm="post">

<p>http://www.cnblogs.com/JianXu/p/5380882.html</p>
<p></p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t0" target="_blank"></a>
1.pm命令介绍</h2>
<p></p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
pm工具为包管理（package manager）的简称</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
可以使用pm工具来执行应用的安装和查询应用宝的信息、系统权限、控制应用</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
pm工具是Android开发与测试过程中必不可少的工具，shell命令格式如下：</p>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm &lt;command&gt;</p>
</blockquote>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t1" target="_blank"></a>
2.包名信息查询</h2>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
shell模式下：</p>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm list packages [options] [FILTER]</p>
<p style="margin:10px auto">打印所有的已经安装的应用的包名，如果设置了文件过滤则值显示包含过滤文字的内容</p>
</blockquote>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:462px">
<tbody>
<tr>
<td valign="top" width="61" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">参数</p>
</td>
<td valign="top" width="399" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">描述</p>
</td>
</tr>
<tr>
<td valign="top" width="61" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-f</td>
<td valign="top" width="399" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
显示每个包的文件位置</td>
</tr>
<tr>
<td valign="top" width="61" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-d</td>
<td valign="top" width="399" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
使用过滤器，只显示禁用的应用的包名</td>
</tr>
<tr>
<td valign="top" width="61" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-e</td>
<td valign="top" width="399" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
使用过滤器，只显示可用的应用的包名</td>
</tr>
<tr>
<td valign="top" width="61" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-s</td>
<td valign="top" width="399" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
使用过滤器，只显示系统应用的包名</td>
</tr>
<tr>
<td valign="top" width="61" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-3</td>
<td valign="top" width="399" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
使用过滤器，只显示第三方应用的包名</td>
</tr>
<tr>
<td valign="top" width="61" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-i</td>
<td valign="top" width="399" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
查看应用的安装者</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h1 style="margin:10px 0px; font-size:28px; border-bottom-width:1px; border-bottom-style:dashed; border-bottom-color:rgb(204,204,204); padding:3px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t2" target="_blank"></a>
二、权限信息查询</h1>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t3" target="_blank"></a>
1.权限基础</h2>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
权限的组成：权限的名称，属于的权限组，保护级别</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
例如:</p>
<div class="cnblogs_code" style="border:1px solid rgb(204,204,204); padding:5px; overflow:auto; margin:5px 0px; line-height:19.5px; font-family:'Courier New'!important; background-color:rgb(245,245,245)">
<pre style="margin-top:0px; margin-bottom:0px; white-space:pre-wrap; word-wrap:break-word; font-family:'Courier New'!important">&lt;permission android:description=<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">string resource</span><span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">
android:icon</span>=<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">drable resource</span><span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">
android:label</span>=<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">string resource</span><span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">
android:name</span>=<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">string</span><span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">
android:permissionGroup</span>=<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">string</span><span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">
android:protectionLevel</span>=[<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">normal</span><span style="line-height:1.5!important">"</span>|<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">dangerous</span><span style="line-height:1.5!important">"</span>|<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">signature</span><span style="line-height:1.5!important">"</span>|<span style="line-height:1.5!important">"</span><span style="line-height:1.5!important">signatureOrSystem</span><span style="line-height:1.5!important">"</span>]/&gt;</pre>
</div>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:718px">
<tbody>
<tr>
<td valign="top" width="130" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">protectionLevel</p>
</td>
<td valign="top" width="586" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="130" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
normal</td>
<td valign="top" width="586" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
表示权限是低风险的，不会对系统，用户或其他应用程序造成危害</td>
</tr>
<tr>
<td valign="top" width="130" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
dangerous</td>
<td valign="top" width="586" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
表示权限是高风险的，系统将可能要球用户输入相关信息，才会授予此权限</td>
</tr>
<tr>
<td valign="top" width="130" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
signature</td>
<td valign="top" width="586" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
表示只有当应用程序所用数字签名与声明引用权限的应用程序所用签名相同时，才能将权限授予给它</td>
</tr>
<tr>
<td valign="top" width="130" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
signatureOrSystem</td>
<td valign="top" width="586" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
需要签名或者系统级应用（放置在/system/app目录下）才能赋予权限</td>
</tr>
<tr>
<td valign="top" width="130" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
system</td>
<td valign="top" width="586" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
系统级应用（放置在/system/app目录下）才能赋予权限</td>
</tr>
<tr>
<td valign="top" width="130" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
自定义权限</td>
<td valign="top" width="586" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
应用自行定义的权限</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t4" target="_blank"></a>
2.权限查询</h2>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
shell模式下：</p>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm list permission-groups</p>
<p style="margin:10px auto">#打印所有已知的权限组</p>
<p style="margin:10px auto">pm list permissions [options] [GROUP]</p>
<p style="margin:10px auto">#打印权限</p>
</blockquote>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
参数可以组合使用例如：pm list permissions –g -d</p>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:400px">
<tbody>
<tr>
<td valign="top" width="50" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">参数</p>
</td>
<td valign="top" width="350" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="50" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-g</td>
<td valign="top" width="350" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
按组进行列出权限</td>
</tr>
<tr>
<td valign="top" width="50" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-f</td>
<td valign="top" width="350" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印所有信息</td>
</tr>
<tr>
<td valign="top" width="50" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-s</td>
<td valign="top" width="350" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
简短的摘要</td>
</tr>
<tr>
<td valign="top" width="50" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-d</td>
<td valign="top" width="350" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
只有危险的权限列表</td>
</tr>
<tr>
<td valign="top" width="50" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-u</td>
<td valign="top" width="350" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
只有权限的用户将看到列表&nbsp;<br>
用户自定义权限</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t5" target="_blank"></a>
3.授权与取消</h2>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
注意：目标apk的minSdkVersion、targetSdkVersion也必需为23及以上</p>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:690px">
<tbody>
<tr>
<td valign="top" width="265" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">子命令</p>
</td>
<td valign="top" width="423" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="265" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
grant &lt;package_name&gt; &lt;permission&gt;</td>
<td valign="top" width="423" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
授予应用权限许可。必需android6.0（API级别23）以上的设备</td>
</tr>
<tr>
<td valign="top" width="265" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
revoke &lt;package_name&gt; &lt;permission&gt;</td>
<td valign="top" width="423" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
撤销应用权限。必需android6.0（API级别23）以上的设备</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
例如：</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
需要注意的是所谓的授权是指你的apk里面已有的权限进行授权，相当于启用的概念</p>
<div class="cnblogs_code" style="border:1px solid rgb(204,204,204); padding:5px; overflow:auto; margin:5px 0px; line-height:19.5px; font-family:'Courier New'!important; background-color:rgb(245,245,245)">
<pre style="margin-top:0px; margin-bottom:0px; white-space:pre-wrap; word-wrap:break-word; font-family:'Courier New'!important">adb shell pm grant &lt;packageName&gt;<span style="line-height:1.5!important"> android.permission.READ_CONTACTS
</span><span style="line-height:1.5!important">#</span><span style="line-height:1.5!important">授权( 取消权限同理)</span></pre>
</div>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h1 style="margin:10px 0px; font-size:28px; border-bottom-width:1px; border-bottom-style:dashed; border-bottom-color:rgb(204,204,204); padding:3px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t6" target="_blank"></a>
三、其他信息查询</h1>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t7" target="_blank"></a>
1.测试包与apk路径查询</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm</p>
</blockquote>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:523px">
<tbody>
<tr>
<td valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">子命令</p>
</td>
<td valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">参数</p>
</td>
<td valign="top" width="255" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td rowspan="3" align="center" valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
list instrymentation</td>
<td valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
无参数</td>
<td valign="top" width="255" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
列出所有的instrumentation测试包</td>
</tr>
<tr>
<td valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-f</td>
<td valign="top" width="255" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
列出apk文件位置</td>
</tr>
<tr>
<td valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
&lt;target_package&gt;</td>
<td valign="top" width="255" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
列出某个app的测试包</td>
</tr>
<tr>
<td valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
path &lt;package&gt;</td>
<td valign="top" width="133" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
&lt;package&gt;</td>
<td valign="top" width="255" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印指定包名的apk路径</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
例如：</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
adb shell pm list instrumentation</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
adb shell pm list instrumentation TARGET_PACKAGE</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
adb shell pm path PACKAGE_NAME</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t8" target="_blank"></a>
2.系统功能与支持库查询</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm</p>
</blockquote>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:400px">
<tbody>
<tr>
<td valign="top" width="100" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">子命令</p>
</td>
<td valign="top" width="300" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="100" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
list feature</td>
<td valign="top" width="300" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印系统的所有功能&nbsp;<br>
列出所有硬件相关信息</td>
</tr>
<tr>
<td valign="top" width="100" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
list libraries</td>
<td valign="top" width="300" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印当前设备所支持的所有库</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
例如：</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
adb shell pm list feature</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t9" target="_blank"></a>
3.打印包的系统状态信息</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm dump PACKAGE</p>
<p style="margin:10px auto">打印给定的包的系统状态</p>
</blockquote>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:450px">
<tbody>
<tr>
<td valign="top" width="212" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">打印内容</p>
</td>
<td valign="top" width="236" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="212" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
DUMP OF SERVICE package</td>
<td valign="top" width="236" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印服务信息</td>
</tr>
<tr>
<td valign="top" width="212" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
DUMP OF SERVICE activity</td>
<td valign="top" width="236" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印activity信息</td>
</tr>
<tr>
<td valign="top" width="212" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
DUMP OF SERVICE meminfo</td>
<td valign="top" width="236" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印当前内存使用信息</td>
</tr>
<tr>
<td valign="top" width="212" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
DUMP OF SERVICE procstats</td>
<td valign="top" width="236" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印系统内存使用与一段时间内存汇总</td>
</tr>
<tr>
<td valign="top" width="212" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
DUMP OF SERVICE usagestats</td>
<td valign="top" width="236" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印服务器使用状态信息</td>
</tr>
<tr>
<td valign="top" width="212" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
DUMP OF SERVICE batterystats</td>
<td valign="top" width="236" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
打印电池状态信息</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
例如：</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
adb shell pm dump PACKAGE_NAME</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h1 style="margin:10px 0px; font-size:28px; border-bottom-width:1px; border-bottom-style:dashed; border-bottom-color:rgb(204,204,204); padding:3px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t10" target="_blank"></a>
四、安装与卸载</h1>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t11" target="_blank"></a>
1.安装</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm install [-lrtsfd] [-i PACKAGE] [PATH]</p>
<p style="margin:10px auto">通过指定路径安装apk到手机中(与adb install不同的是adb install安装的.apk是在你的电脑上，而pm install安装的apk是存储在你的手机中)</p>
</blockquote>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:664px">
<tbody>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">参数</p>
</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-l</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
锁定应用程序</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-r</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
重新安装应用，且保留应用数据</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-t</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
允许测试apk被安装</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-i &lt;INSTALLER_PACKAGE_NAME&gt;</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
指定安装包的包名</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-s</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
安装到sd卡</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-f</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
安装到系统内置存储中（默认安装位置）</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-d</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
允许降级安装（同一应用低级换高级）</td>
</tr>
<tr>
<td valign="top" width="232" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-g</td>
<td valign="top" width="430" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
授予应用程序清单中列出的所有权限（只有6.0系统可用）</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
首先将test.apk文件push到手机目录中比如/data/local/tmp</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
adb shell pm install /data/local/tmp/test.apk&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; #安装</p>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
adb shell pm install –r /data/local/tmp/test.apk&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; #重新安装</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t12" target="_blank"></a>
2.卸载</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm uninstall [options] &lt;PACKAGE&gt;</p>
<p style="margin:10px auto">#卸载应用</p>
</blockquote>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:432px">
<tbody>
<tr>
<td valign="top" width="82" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">参数</p>
</td>
<td valign="top" width="348" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="82" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
-k</td>
<td valign="top" width="348" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
卸载应用且保留数据与缓存（如果不加-k则全部删除）</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h1 style="margin:10px 0px; font-size:28px; border-bottom-width:1px; border-bottom-style:dashed; border-bottom-color:rgb(204,204,204); padding:3px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t13" target="_blank"></a>
五、控制命令</h1>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t14" target="_blank"></a>
1.清除应用数据</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm clear &lt;PACKAGE_NAME&gt;</p>
</blockquote>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t15" target="_blank"></a>
2.禁用和启用应用</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm</p>
</blockquote>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
只有系统应用才可以用，第三方应用不行</p>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:717px">
<tbody>
<tr>
<td valign="top" width="368" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">子命令</p>
</td>
<td valign="top" width="347" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="368" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
enable &lt;PACKAGE_OR_COMPONENT&gt;</td>
<td valign="top" width="347" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
使package或component可用</td>
</tr>
<tr>
<td valign="top" width="368" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
disenable &lt;PACKAGE_OR_COMPONENT&gt;</td>
<td valign="top" width="347" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
使package或component不可用（直接就找不到应用了）</td>
</tr>
<tr>
<td valign="top" width="368" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
disenable-user [options] &lt;PACKAGE_OR_COMPONENT&gt;</td>
<td valign="top" width="347" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
使package或component不可用（会显示已停用）</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t16" target="_blank"></a>
3.隐藏与恢复应用</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm</p>
</blockquote>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
被隐藏应用在应用管理中变得不可见，桌面图标也会消失</p>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:524px">
<tbody>
<tr>
<td valign="top" width="242" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">子命令</p>
</td>
<td valign="top" width="280" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="242" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
hide PACKAGE_OR_COMPONENT</td>
<td valign="top" width="280" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
隐藏package或component</td>
</tr>
<tr>
<td valign="top" width="242" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
unhide PACKAGE_OR_CONPONENT</td>
<td valign="top" width="280" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
恢复可见package或component</td>
</tr>
</tbody>
</table>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
&nbsp;</p>
<h2 style="margin-top:10px; margin-bottom:3px; font-size:21px; line-height:1.5; font-family:georgia,Verdana,Helvetica,Arial"><a name="t17" target="_blank"></a>
4.控制应用的默认安装位置</h2>
<blockquote style="border:2px solid rgb(239,239,239); padding:5px 10px; margin-top:10px; margin-bottom:10px; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; background:none">
<p style="margin:10px auto">pm</p>
</blockquote>
<p style="margin:10px auto; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px">
需要root权限</p>
<table border="0" cellspacing="0" cellpadding="2" style="border:1px solid silver; border-collapse:collapse; word-break:break-word; font-family:georgia,Verdana,Helvetica,Arial; font-size:13px; line-height:19.5px; width:600px">
<tbody>
<tr>
<td valign="top" width="226" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">子命令</p>
</td>
<td valign="top" width="372" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
<p align="center" style="margin:10px auto">说明</p>
</td>
</tr>
<tr>
<td valign="top" width="226" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
set-install-location &lt;LOCATION&gt;</td>
<td valign="top" width="372" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
更改默认的安装位置：&nbsp;<br>
0：自动-让系统决定最好的位置&nbsp;<br>
1：内部存储-安装在内部设备上的存储&nbsp;<br>
2：外部存储-安装在外部媒体&nbsp;<br>
注：只用于调试，不要瞎搞</td>
</tr>
<tr>
<td valign="top" width="226" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
get-install-localtion</td>
<td valign="top" width="372" style="font-size:13px; font-family:georgia,Verdana,Helvetica,Arial; word-break:break-all; border:1px solid silver; border-collapse:collapse; padding:3px">
返回当前的安装位置&nbsp;<br>
0&nbsp;<br>
1&nbsp;<br>
2&nbsp;<br>
对应上面的数字说明</td>
</tr>
</tbody>
</table>






