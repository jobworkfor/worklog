
由Messaging应用发起的调用
```
"Thread-2@5486" prio=5 tid=0x6f nid=NA runnable
  java.lang.Thread.State: RUNNABLE
	  at android.os.Parcel.readException(Parcel.java:1885)
	  at android.webkit.IWebViewUpdateService$Stub$Proxy.waitForAndGetProvider(IWebViewUpdateService.java:201)
	  at android.webkit.WebViewFactory.getWebViewContextAndSetProvider(WebViewFactory.java:328)
	  at android.webkit.WebViewFactory.getProviderClass(WebViewFactory.java:398)
	  at android.webkit.WebViewFactory.getProvider(WebViewFactory.java:211)
	  - locked <0x15a2> (a java.lang.Object)
	  at android.webkit.WebView.getFactory(WebView.java:2467)
	  at android.webkit.WebView.findAddress(WebView.java:1738)
	  at android.text.util.Linkify.gatherMapLinks(Linkify.java:569)
	  at android.text.util.Linkify.addLinks(Linkify.java:261)
	  at com.android.messaging.common.view.CooperationTextView.initLinkify(CooperationTextView.java:117)
	  at com.android.messaging.BugleApplication$2.run(BugleApplication.java:214)
	  at java.lang.Thread.run(Thread.java:764)
```


符合webview app的标准
```
@startuml
participant WebViewUpdater as WU
WU->WU:findPreferredWebViewPackage()
activate WU
  WU->WU:getValidWebViewPackagesAndInfos()
  activate WU
    WU->WU:isValidProvider()
    activate WU
      WU->WU:validityResult()
        activate WU
          WU x-> WU:if(...)return VALIDITY_INCORRECT_SDK_VERSION;
          WU x-> WU:if(...)return VALIDITY_INCORRECT_VERSION_CODE;
          WU x-> WU:if(...)return VALIDITY_INCORRECT_SIGNATURE;
          WU x-> WU:if(...)return VALIDITY_NO_LIBRARY_FLAG;
          WU -> WU:return VALIDITY_OK;
        deactivate WU
    deactivate WU
  deactivate WU
deactivate WU
@enduml
```