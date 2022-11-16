Android SeLinux 需要知道的
========================

前言
----------------------------------------------------------------------------------------------------

从app到驱动，写完一个需求后，selinux死活的不让功能顺畅的运行，于是离开需求的开发，来了解selinux的本貌，记录于此文。


需要知道的概念
----------------------------------------------------------------------------------------------------

<pre>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="981px" version="1.1" content="&lt;mxfile userAgent=&quot;Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36&quot; version=&quot;8.6.5&quot; editor=&quot;www.draw.io&quot; type=&quot;browser&quot;&gt;&lt;diagram id=&quot;61752c5f-85da-54f6-fe78-506cdffe69ce&quot; name=&quot;Page-1&quot;&gt;7VtZb9s4EP41BnYfUkiUJdmPiZse2BQIYGy3+0hJtM0NLQoUndj765eUSF1kbNUrH2mrAg01FK/5Zr7h5ZE3W28/MpitvtAEkRFwku3Iez8C4gkD8UdKdqUkBH4pWDKclCK3Fszxv0gJHSXd4ATlrQ85pYTjrC2MaZqimLdkkDH60v5sQUm71QwukSGYx5CY0r9wwleldOI7tfwTwsuVbtl1VE4E46clo5tUtTcC3qJ4yuw11HWp7/MVTOhLQ+Tdj7wZo5SXqfV2hojUrVZbWe7DK7lVvxlKeZ8CoCzwDMlGDf0Bp5ut7BmKNwzznew1TTZEwFH2mO+0lopxIlmTO/LuXlaYo3kGY5n7IuxCyFZ8TVQ2JHiZinQseoaYECwwITNKKCsqE2pCQRwLec4ZfUKNnCScRkK/3p05ODXeZ8Q42jZEarAfEV0jzuQYVK43VopXhulN1PtLDbOrwVk1IA6UDCrLWlZV19oVCaVgu7I9Q9nvb2cDa3UAHbmTC+pobOjIUBBKk1vp43LYBOY5jts6ITBC5K5yRG1JKU3RPgXldMNi1QQIFelAtkS8hR5KWtRharGhJd+iJC1jiECOn9uEY9OcauGRYtHhCqSOHY/dju7L0ahCTQLo1HMDXgFbV1SqwKiowLEadS9o/auA1jORBVeF7E3QgRYcCW14oJ7hkA0syAZEqOUuEomlTMzvVWAp5aLGKmsPAzoDxBVf/hNySYBYhPhbVYDTzBZtguIZiEm7XmoSqWezJK8L1TFMOjFAme9yjtbt2J5RgmOZSCCHEcyRgYaYomQyGe8IFrCww5BEJX4PkRYYob6YEVmwM9BwimcgNDqONXXNsOZY0Ain/x8MNzC5TtDNXL1Sxld0SVNI7mvpXdsPGgpGW8y/KbFM/y3T74C0cqEetvumv5MvZaZ3kD1zwQdcTcWl/f+DON+pd7jhVIjqbj5Q6T1FI71Yd2qy7qQn6/am095YhKfHIvRPpu+inBklC/EHTKp+1aFUNSgkKn+vQ50btqKo6CrcNT7IZFTKXw+SoDNHdcf+3lh44HuRKHtwbAR0JyexqdKOtFm5Tf/WeZWL9zO4jk00rcaxGKV1QlYbknsGntAz2/MTxdSIoLdxjPK8iDoxF7oFTgzjFapmO0zPaX67/Tr73RQPPNUZICh2F8RVBDzHYs/1T+M1oOk1TttrQMtrDi8qThoWtW037X16sbg4/cVhpwLVdS+FatXDQVF1mw72rudk5y3i1ndvYHhvdIzo86jXaihdUNHtNSqmODligu/fQGiZnjO0jH/20KLPTa5iKlWdd/yKLYOjejmK0pTQ2GLS23wOjHLOYMwxTW3z4ACuJQWV/5sfPMy/iDo+Ufp0/bwGznk+ogNS88SOLoVggYm5dzfoTmrio0kyHll26SYg8obaM/XBJaOG95NHDXBVU1fT1k14znAYaKHccU+dnOkwsHtkdOxpoH+oouHOjCyn4Qa41dEDJIRu+GEKyxDDog+SvXShx1pkOYcAxZUDg/kymmMZuUDhoY4kvQXB2VfVTHFOIpJyUz0vPc8NG8XqUuZlhiAK/IGo0pt20PJMqgSexezCAajSelJfhvEEP+s4Xm2YfU5pghqnf41v9kStC92A8B2/pdjz3hI5yVT5R1yw6xsFLWYOLhatbPcbDId4ZFR5ROUaQj3yctXbcI2bi96gAic5ZvkhfSOw+EZ4Md94/YZIy9r7iD6nzyKkisqq6wwzKBuz+8/3SK/O19zwkr4W/sLs+zF77TrdWWYO5n6MSZfGtYAE5qtKY71XTua9qXiCooVl1wCiySLep9wrWUR1b0L6zpGLKONKZRfb4RZRnrlC/jOXZwFOafVd9IUR8zbKC5ry1n2rIJjNBqKvaXsWPQ58wxemFjy9IVzBXF3+gVha/EzhGlTjOgdVY72LdoRuxGv9e4LSxuofbXj3/wE=&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://www.draw.io/?client=1&amp;lightbox=1&amp;edit=_blank');}}})(this);" viewBox="0 0 981 462" style="cursor:pointer;max-width:100%;max-height:462px;"><defs/><g transform="translate(0.5,0.5)"><rect x="680" y="340" width="120" height="60" rx="9" ry="9" fill="#ffe6cc" stroke="#d79b00" pointer-events="none"/><g transform="translate(681.5,356.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="116" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 116px; white-space: normal; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">Linux security modules</div></div></foreignObject><text x="58" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Linux security modules</text></switch></g><rect x="520" y="340" width="120" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(566.5,363.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="26" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 26px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">DAC</div></div></foreignObject><text x="13" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">DAC</text></switch></g><path d="M 480 370 L 513.63 370" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 518.88 370 L 511.88 373.5 L 513.63 370 L 511.88 366.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 640 370 L 673.63 370" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 678.88 370 L 671.88 373.5 L 673.63 370 L 671.88 366.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="480" y="0" width="350" height="320" fill="#f5f5f5" stroke="#666666" pointer-events="none"/><g transform="translate(630.5,7.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="48" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 50px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;"><b>SELinux</b></div></div></foreignObject><text x="24" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">&lt;b&gt;SELinux&lt;/b&gt;</text></switch></g><path d="M 500 67 C 500 45.67 600 45.67 600 67 L 600 114 C 600 135.33 500 135.33 500 114 Z" fill="#ffffff" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 500 67 C 500 83 600 83 600 67" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(501.5,88.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="96" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 96px; white-space: normal; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">System security policy database</div></div></foreignObject><text x="48" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">System security policy database</text></switch></g><path d="M 680 75 L 606.37 75" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 601.12 75 L 608.12 71.5 L 606.37 75 L 608.12 78.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 673.63 105 L 620 105 L 600 105" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 678.88 105 L 671.88 108.5 L 673.63 105 L 671.88 101.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 770 120 L 770 143.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 770 148.88 L 766.5 141.88 L 770 143.63 L 773.5 141.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="680" y="60" width="120" height="60" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(684.5,76.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="110" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 112px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">Access vector cache<br />(AVC)<br /></div></div></foreignObject><text x="55" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Access vector cache&lt;br&gt;(AVC)&lt;br&gt;</text></switch></g><path d="M 710 150 L 710 126.37" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 710 121.12 L 713.5 128.12 L 710 126.37 L 706.5 128.12 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 770 210 L 770 233.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 770 238.88 L 766.5 231.88 L 770 233.63 L 773.5 231.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 800 180 L 853.63 180" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 858.88 180 L 851.88 183.5 L 853.63 180 L 851.88 176.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="680" y="150" width="120" height="60" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(681.5,166.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="116" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 116px; white-space: normal; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">Policy enforcement server</div></div></foreignObject><text x="58" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Policy enforcement server</text></switch></g><path d="M 710 240 L 710 216.37" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 710 211.12 L 713.5 218.12 L 710 216.37 L 706.5 218.12 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 770 300 L 770 333.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 770 338.88 L 766.5 331.88 L 770 333.63 L 773.5 331.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="680" y="240" width="120" height="60" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(686.5,249.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="106" height="40" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 108px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">SELinux abstraction<br />&amp;<br />LSM Hook</div></div></foreignObject><text x="53" y="26" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">SELinux abstraction&lt;br&gt;&amp;&lt;br&gt;LSM Hook</text></switch></g><rect x="860" y="150" width="120" height="60" fill="#d5e8d4" stroke="#82b366" pointer-events="none"/><g transform="translate(900.5,173.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="38" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 40px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">Log file</div></div></foreignObject><text x="19" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Log file</text></switch></g><path d="M 710 340 L 710 306.37" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 710 301.12 L 713.5 308.12 L 710 306.37 L 706.5 308.12 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 800 370 L 838.63 370" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 843.88 370 L 836.88 373.5 L 838.63 370 L 836.88 366.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 730 390 L 960 390 L 960 443 L 752.2 443 L 739.2 460 L 739.2 443 L 730 443 Z" fill="#fff2cc" stroke="#d6b656" stroke-miterlimit="10" transform="translate(0,425)scale(1,-1)translate(0,-425)" pointer-events="none"/><rect x="845" y="340" width="120" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(868.5,363.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="72" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 74px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;"><div>Access Inode</div></div></div></foreignObject><text x="36" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">&lt;div&gt;Access Inode&lt;/div&gt;</text></switch></g><path d="M 120 370 L 163.63 370" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 168.88 370 L 161.88 373.5 L 163.63 370 L 161.88 366.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="0" y="340" width="120" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(2.5,363.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="114" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 116px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;"><div>Process Access Files</div></div></div></foreignObject><text x="57" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">&lt;div&gt;Process Access Files&lt;/div&gt;</text></switch></g><path d="M 290 370 L 353.63 370" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 358.88 370 L 351.88 373.5 L 353.63 370 L 351.88 366.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="170" y="340" width="120" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(178.5,363.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="102" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 104px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;"><div><div><div>Invoke System Call</div></div></div></div></div></foreignObject><text x="51" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">[Not supported by viewer]</text></switch></g><rect x="360" y="340" width="120" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(368.5,363.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="102" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 104px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;"><div><div><div>Invoke System Call</div></div></div></div></div></foreignObject><text x="51" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">[Not supported by viewer]</text></switch></g><path d="M 320 460 L 320 320" fill="none" stroke="#6c8ebf" stroke-miterlimit="10" stroke-dasharray="3 3" pointer-events="none"/><g transform="translate(246.5,431.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="63" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 102, 204); line-height: 1.2; vertical-align: top; white-space: nowrap;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">User Space</div></div></foreignObject><text x="32" y="12" fill="#0066CC" text-anchor="middle" font-size="12px" font-family="Helvetica">User Space</text></switch></g><g transform="translate(331.5,431.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="72" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 102, 204); line-height: 1.2; vertical-align: top; white-space: nowrap;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;">Kernel Space</div></div></foreignObject><text x="36" y="12" fill="#0066CC" text-anchor="middle" font-size="12px" font-family="Helvetica">Kernel Space</text></switch></g></g></svg>
</pre>


### DAC和MAC

是linux提供的两种安全机制：
* DAC(Discretionary Access Control): 内核级别的Linux UID/GID机制
* MAC(Mandatory Access Control): 用户、进程或者文件的权限是由管理策略决定的，而不是由它们自主决定的。
  例如，我们可以设定这样的一个管理策略，不允许用户A将它创建的文件F授予用户B访问。
  这样无论用户A如何修改文件F的权限位，用户B都是无法访问文件F的。

### 安全策略文件

TEAC（Type Enforcement Access Control），简称TE文件。说明访问规则的地方


### 安全上下文

SEAndroid是一种基于安全策略的MAC安全机制。这种安全策略又是建立在对象的安全上下文的基础上的。这里所说的对象分为两种类型，一种称主体（Subject），一种称为客体（Object）。主体通常就是指进程，而客观就是指进程所要访问的资源，例如文件、系统属性等。

安全上下文实际上就是一个附加在对象上的标签（Tag）。这个标签实际上就是一个字符串，它由四部分内容组成，分别是SELinux用户、SELinux角色、类型、安全级别，每一个部分都通过一个冒号来分隔，格式为“user:role:type:sensitivity”。

在SEAndroid中，只定义了一个SELinux用户u，因此我们通过ps -Z和ls -Z命令看到的所有的进程和文件的安全上下文中的SELinux用户都为u。最为重要的字段是Type，整个上下文描述可以简记为`u:r:type:s`


安全级别最开始的目的是用来对美国政府分类文件进行访问控制的。在基于安全级别的MAC安全机制中，主体（subject）和客体（object）都关联有一个安全级别。其中，安全级别较高的主体可以读取安全级别较低的客体，而安全级别较低的主体可以写入安全级别较高的客体。前者称为“read down”，而后者称为“write up”。通过这种规则，可以允许数据从安全级别较低的主体流向安全级别较高的主体，而限制数据从安全级别较高的主体流向安全级别较低的主体，从而有效地保护了数据。注意，如果主体和客体的安全级别是相同的，那么主体是可以对客体进行读和写的。


### 类型

在SEAndroid中，我们通常将用来标注文件的安全上下文中的类型称为file_type，而用来标注进程的安全上下文的类型称为domain，并且每一个用来描述文件安全上下文的类型都将file_type设置为其属性，每一个用来进程安全上下文的类型都将domain设置为其属性。

Android系统四种类型的对象的安全上下文，分别是:
1. App进程        -> mac_permissions.xml
2. App数据文件    -> seapp_contexts
3. 系统文件     -> file_contexts
4. 系统属性     -> property_contexts


/system/sepolicy/mac_permissions.xml
```
<?xml version="1.0" encoding="utf-8"?>
<policy>

<!--
    * A signature is a hex encoded X.509 certificate or a tag defined in
      keys.conf and is required for each signer tag. The signature can
      either appear as a set of attached cert child tags or as an attribute.
    * A signer tag must contain a seinfo tag XOR multiple package stanzas.
    * Each signer/package tag is allowed to contain one seinfo tag. This tag
      represents additional info that each app can use in setting a SELinux security
      context on the eventual process as well as the apps data directory.
    * seinfo assignments are made according to the following rules:
      - Stanzas with package name refinements will be checked first.
      - Stanzas w/o package name refinements will be checked second.
      - The "default" seinfo label is automatically applied.

    * valid stanzas can take one of the following forms:

     // single cert protecting seinfo
     <signer signature="@PLATFORM" >
       <seinfo value="platform" />
     </signer>

     // multiple certs protecting seinfo (all contained certs must match)
     <signer>
       <cert signature="@PLATFORM1"/>
       <cert signature="@PLATFORM2"/>
       <seinfo value="platform" />
     </signer>

     // single cert protecting explicitly named app
     <signer signature="@PLATFORM" >
       <package name="com.android.foo">
         <seinfo value="bar" />
       </package>
     </signer>

     // multiple certs protecting explicitly named app (all certs must match)
     <signer>
       <cert signature="@PLATFORM1"/>
       <cert signature="@PLATFORM2"/>
       <package name="com.android.foo">
         <seinfo value="bar" />
       </package>
     </signer>
-->

    <!-- Platform dev key in AOSP -->
    <signer signature="@PLATFORM" >
      <seinfo value="platform" />
    </signer>

</policy>
```

文件mac_permissions.xml给不同签名的App分配不同的seinfo字符串，例如，在AOSP源码环境下编译并且使用平台签名的App获得的seinfo为“platform”，使用第三方签名安装的App获得的seinfo签名为"default"。 具体参考XML文件中的开头注释

这个seinfo描述的其实并不是安全上下文中的Type，它是用来在另外一个文件external/sepolicy/seapp_contexts中查找对应的Type的。

/system/sepolicy/seapp_contexts
```
# Input selectors:
#	isSystemServer (boolean)
#	isAutoPlayApp (boolean)
#	isOwner (boolean)
#	user (string)
#	seinfo (string)
#	name (string)
#	path (string)
#	isPrivApp (boolean)
# isSystemServer=true can only be used once.
# An unspecified isSystemServer defaults to false.
# isAutoPlayApp=true will match apps marked by PackageManager as AutoPlay
# isOwner=true will only match for the owner/primary user.
# isOwner=false will only match for secondary users.
# If unspecified, the entry can match either case.
# An unspecified string selector will match any value.
# A user string selector that ends in * will perform a prefix match.
# user=_app will match any regular app UID.
# user=_isolated will match any isolated service UID.
# isPrivApp=true will only match for applications preinstalled in
#       /system/priv-app.
# All specified input selectors in an entry must match (i.e. logical AND).
# Matching is case-insensitive.
#
# Precedence rules:
# 	  (1) isSystemServer=true before isSystemServer=false.
# 	  (2) Specified isAutoPlayApp= before unspecified isAutoPlayApp= boolean.
# 	  (3) Specified isOwner= before unspecified isOwner= boolean.
#	  (4) Specified user= string before unspecified user= string.
#	  (5) Fixed user= string before user= prefix (i.e. ending in *).
#	  (6) Longer user= prefix before shorter user= prefix.
#	  (7) Specified seinfo= string before unspecified seinfo= string.
#	      ':' character is reserved and may not be used.
#	  (8) Specified name= string before unspecified name= string.
#	  (9) Specified path= string before unspecified path= string.
# 	  (10) Specified isPrivApp= before unspecified isPrivApp= boolean.
#
# Outputs:
#	domain (string)
#	type (string)
#	levelFrom (string; one of none, all, app, or user)
#	level (string)
# Only entries that specify domain= will be used for app process labeling.
# Only entries that specify type= will be used for app directory labeling.
# levelFrom=user is only supported for _app or _isolated UIDs.
# levelFrom=app or levelFrom=all is only supported for _app UIDs.
# level may be used to specify a fixed level for any UID.
#
#
# Neverallow Assertions
# Additional compile time assertion checks can be added as well. The assertion
# rules are lines beginning with the keyword neverallow. Full support for PCRE
# regular expressions exists on all input and output selectors. Neverallow
# rules are never output to the built seapp_contexts file. Like all keywords,
# neverallows are case-insensitive. A neverallow is asserted when all key value
# inputs are matched on a key value rule line.
#

# only the system server can be in system_server domain
neverallow isSystemServer=false domain=system_server
neverallow isSystemServer="" domain=system_server

# system domains should never be assigned outside of system uid
neverallow user=((?!system).)* domain=system_app
neverallow user=((?!system).)* type=system_app_data_file

# anything with a non-known uid with a specified name should have a specified seinfo
neverallow user=_app name=.* seinfo=""
neverallow user=_app name=.* seinfo=default

# neverallow shared relro to any other domain
# and neverallow any other uid into shared_relro
neverallow user=shared_relro domain=((?!shared_relro).)*
neverallow user=((?!shared_relro).)* domain=shared_relro

# neverallow non-isolated uids into isolated_app domain
# and vice versa
neverallow user=_isolated domain=((?!isolated_app).)*
neverallow user=((?!_isolated).)* domain=isolated_app

# uid shell should always be in shell domain, however non-shell
# uid's can be in shell domain
neverallow user=shell domain=((?!shell).)*

# AutoPlay Apps must run in the autoplay_app domain
neverallow isAutoPlayApp=true domain=((?!autoplay_app).)*

isSystemServer=true domain=system_server
user=system seinfo=platform domain=system_app type=system_app_data_file
user=bluetooth seinfo=platform domain=bluetooth type=bluetooth_data_file
user=nfc seinfo=platform domain=nfc type=nfc_data_file
user=radio seinfo=platform domain=radio type=radio_data_file
user=shared_relro domain=shared_relro
user=shell seinfo=platform domain=shell type=shell_data_file
user=_isolated domain=isolated_app levelFrom=user
user=_app seinfo=platform domain=platform_app type=app_data_file levelFrom=user
user=_app isAutoPlayApp=true domain=autoplay_app type=autoplay_data_file levelFrom=all
user=_app isPrivApp=true domain=priv_app type=app_data_file levelFrom=user
user=_app domain=untrusted_app type=app_data_file levelFrom=user
```


权限修改
----------------------------------------------------------------------------------------------------
### 方法1: adb在线修改seLinux

Enforcing(表示已打开)，Permissive（表示已关闭）
```
getenforce;     //获取当前seLinux状态
setenforce 1;   //打开seLinux
setenforce 0;   //关闭seLinux
```

### 方法2: 从kernel中彻底关闭

修改`LINUX/android/kernel/arch/arm64/configs/xxx_defconfig`文件（xxx一般为手机产品名）， 去掉`CONFIG_SECURITY_SELINUX=y`的配置项

### 方法3: sepolicy中添加权限

#### 修改依据
通过指令cat /proc/kmsg | grep denied，或者kernel的Log中定位到标志性log。

#### 修改步骤

找相应的源类型.te文件，此文件可能的存放路径 (其中源类型见下方的标志性log格式) ：
```
  LINUX/android/external/sepolicy
  LINUX/android/device/qcom/sepolicy/common
```
标志性log 格式
```
avc: denied {操作权限} for pid=7201 comm="进程名" scontext=u:r:源类型:s0 tcontext=u:r:目标类型:s0 tclass=访问类型 permissive=0
```
在相应源类型.te文件，添加如下格式的一行语句：(结尾别忘了分号)
```
格式：allow  源类型 目标类型:访问类型 {操作权限};
```

#### 实例
Kernel Log
```
avc: denied {getattr read} for pid=7201 comm="xxx.xxx" scontext=u:r:system_app:s0 tcontext=u:r:shell_data_file:s0 tclass=dir permissive=0
```

在`system_app.te`文件中，添加下面语句：
```
allow system_app shell_data_file:dir {getattr read};
```


在te文件中，我们一般遇到的语法是这样的：
```
rule_name source_type target_type:class perm_set
```
解读为： 为source_type设置一个rule_name的规则，规则是对target_type的class 进行 perm_set的操作。


type的命令如下：
```
type type_id [alias alias_id,] [attribute_id]
```
将type_id（别名为alias）关联到attribute. 这样的话，方便用attribute来管理不同的type中包含相同的属性的部分。

class命令的格式为：
```
class class_name [ inherits common_name ] { permission_name ... }
```
inherits表示继承了common定义的权限，然后自己额外实现了permission_name的权限


### 一些特殊的配置文件

#### attributes
所有定义的attributes都在这个文件
```
/system/sepolicy/attributes
/device/qcom/sepolicy/common/attributes
```

#### access_vectors
对应了每一个class可以被允许执行的命令
```
/system/sepolicy/access_vectors
```

#### roles
Android中只定义了一个role，名字就是r，将r和attribute domain关联起来
/system/sepolicy/roles
```
role r;
role r types domain;
```

#### users

其实是将user与roles进行了关联，设置了user的安全级别，s0为最低级是默认的级别，mls_systemHigh是最高的级别

/system/sepolicy/users
```
user u roles { r } level s0 range s0 - mls_systemhigh;
```

#### security_classes
指的是上文命令中的class，个人认为这个class的内容是指在android运行过程中，程序或者系统可能用到的操作的模块
/system/sepolicy/security_classes

#### macros
系统定义的宏全在te_macros文件
```
/system/sepolicy/te_macros
/device/qcom/sepolicy/common/te_macros
```

#### *.te
一些配置的文件，包含了各种运行的规则
```
/system/sepolicy/*.te
/device/qcom/sepolicy/common/*.te
```

##### 在te文件中常见的四种命名的规则

* `allow`：赋予某项权限。
* `allowaudit`：audit含义就是记录某项操作。默认情况下是SELinux只记录那些权限检查失败的操作。allowaudit则使得权限检查成功的操作也被记录。注意，allowaudit只是允许记录，它和赋予权限没关系。赋予权限必须且只能使用allow语句。
* `dontaudit`：对那些权限检查失败的操作不做记录。
* `neverallow`：前面讲过，用来检查安全策略文件中是否有违反该项规则的allow语句。如例子5所示：


### selinux两种工作模式

* `permissive`：所有操作都被允许（即没有MAC），但是如果有违反权限的话，会记录日志
* `enforcing`：所有操作都会进行权限检查



如何排查并解决SEAndroid 的审计不通过

Android 5.0 之后，SEAndroid所有的部分均为Enforcing模式；如果当某个操作不被SEAndroid允许时，例如对文件进行write，该如何排查出信息，同时，在sepolicy中，添加上相应的allow语句，将权限开放出去；

1：SEAndroid不允许时，log记录在哪里？
SEAndroid的审计不通过时，log记录在dmesg 中，dmesg是kernel的log，如果想要获取该log，可以使用如下命令：
adb shell su -c dmesg    ----- 获取kernel log

2： 查看SEAndroid 不允许的log
SEAndroid 审计不通过的log，带有"avc:" 所以，用如下命令即可搜集到审计不同的log：

adb shell su -c demsg | grep 'avc:'  ---- 得到审计不通过的log信息

如果有审计不通过的，会得出如下类似的信息：
```
<5> type=1400 audit: avc:  denied  { read write } for  pid=177 comm="rmt_storage" name="mem" dev="tmpfs" ino=6004 scontext=u:r:rmt:s0
```

tcontext=u:object_r:kmem_device:s0 tclass=chr_file 不被允许的操作是：read 和write
访问者是：u:r:rmt:s0
被访问者是：u:object_r:kmem_device:s0
操作对象是：chr_file

相当于在sepolicy 策略语言中，缺乏这样的语句allow rmt kmem_device:chr_file {read write}

TIP:
pid=177 表示访问者所在的进程，comm中给的是一个提示，表示当这个denial发生时，什么正在运行；

3：如何消除这样的不通过
很简单，可以直接在sepolicy中加上这样的策略语句；
例如上处avc不通过，可以在/external/sepolicy/ 目录下，新建一个test.te
在test.te 中写入，allow rmt kmem_device:chr_file {read write},
重新编译策略语言，刷机即可；

但是当avc很多时，人工去看容易出错且慢，我们可以使用工具来完成这项工作；

selinux/policycoreutils/audit2allow环境搭建：
测试电脑的配置是：unbutu 12.04
step 1：在 ubuntu中安装policycoreutils
sudo apt-get install policycoreutils

step 2 : 使用audit2allow 工具完成策略语言的添加：
adb shell su -c dmesg | audit2allow

例如上诉avc语句就会输出：
```
#============= rmt ==============
allow rmt kmem_device:chr_file { read write };
```

TIP：
1： 要知道，audit2allow是policycoreutils中的工具之一
2：如果在ubuntu 14.04 或者更新的版本中，可以直接将策略语句插入到编译好的sepolicy中
命令如下：
```
adb shell su -c dmesg | audit2allow -p out/target/product/<device>/root/sepolicy
```



Android设置应用进程的安全上下文
----------------------------------------------------------------------------------------------------
理解了守护进程的安全上下文的创建过程后，我们再看看应用进程的安全上下文是如何创建的。应用进程是通过Zygote进程fork出来的，
但是不会调用exec。在前面介绍Zygote进程时我们已经知道了创建应用进程时会调用函数ForkAndSpecializeCommon()，
这个函数则通过调用seLinux_android_setcontext()函数来设置应用进程的安全上下文，如下所示：
```
rc =selinux_android_setcontext(uid,is_system_server,se_info_c_str,se_name_c_str);
selinux_android_setcontext()函数的代码如下：
int selinux_android_setcontext(uid_t uid, int isSystemServer,
               const char *seinfo, const char *pkgname)
{
char *orig_ctx_str = NULL, *ctx_str;
context_t ctx = NULL;
int rc = -1;
......
__selinux_once(once, seapp_context_init); // 调用一次seapp_context_init函数
rc = getcon(&ctx_str);        // 得到当前进程从Zygote进程继承的安全上下文
......
ctx = context_new(ctx_str);    // 以ctx_str为模板创建一个新的安全上下文
orig_ctx_str = ctx_str;
......
// 在SEAPP_DOMAIN中查找新的安全上下文
rc = seapp_context_lookup(SEAPP_DOMAIN, uid,isSystemServer, seinfo, pkgname, ctx);
...... // 检查新的安全上下文
if (strcmp(ctx_str, orig_ctx_str)) { // 如果新的安全上下文和原来的不相同
     rc = setcon(ctx_str);          // 为当前进程设置安全上下文。
     if (rc < 0)
         goto err;
}
 ......
return rc;
}
selinux_android_setcontext()函数首先调用了seapp_context_init()函数来装载“seapp_context”文件的内容。然后通过函数seapp_context_lookup()查找合适的安全上下文，最后调用setcon()函数来设置进程的安全上下文。我们先看看seapp_context_init()函数的代码：
static voidseapp_context_init(void)
{
    selinux_android_seapp_context_reload();
}
seapp_context_init()函数只是调用了selinux_android_seapp_context_reload()函数，代码如下：
intselinux_android_seapp_context_reload(void)
{
   ......
   while ((fp==NULL) &&seapp_contexts_file[i])
       fp =fopen(seapp_contexts_file[i++], "r"); // 打开文件
......  // 把文件的内容读进来并解析
}
selinux_android_seapp_context_reload()函数的作用是打开数组seapp_contexts_file中指定的文件，读取它的内容并解析，解析后的内容放到全局变量seapp_contexts中，这段解析比较长，也比较简单，我们就不逐行分析了，这里主要是希望了解所打开的文件的定义，如下所示：
static char const *const seapp_contexts_file[] = {
"/data/security/current/seapp_contexts",
"/seapp_contexts",
0 };
constseapp_contexts_file数组中定义了两个文件，/seapp_contexts是原始的文件，如果对这个文件的内容进行了修改，会保存到/data/security/current/seapp_contexts文件中，所以需要先检查这个文件是否存在。这个文件的内容是：
isSystemServer=truedomain=system
user=systemdomain=system_app type=system_data_file
user=bluetoothdomain=bluetooth type=bluetooth_data_file
user=nfc domain=nfctype=nfc_data_file
user=radiodomain=radio type=radio_data_file
user=_appdomain=untrusted_app type=app_data_file levelFrom=none
user=_appseinfo=platform domain=platform_app type=platform_app_data_file
user=_appseinfo=shared domain=shared_app type=platform_app_data_file
user=_appseinfo=media domain=media_app type=platform_app_data_file
user=_appseinfo=release domain=release_app type=platform_app_data_file
user=_isolateddomain=isolated_app
user=Shelldomain=shell type=shell_data_file
seapp_contexts文件定义了用户名和domain之间的联系。下面我们看看seapp_context_lookup()函数是如何根据这个文件的信息来得到应用的安全上下文的。
static intseapp_context_lookup(enum seapp_kind kind, uid_t uid, int isSystemServer,
              const char *seinfo, const char*pkgname, context_t ctx)
{
......
userid = uid / AID_USER;
appid = uid % AID_USER;
 // 通过uid在android_ids表中查找进程名，android_ids表中定义的系统应用
if (appid < AID_APP) {
     for (n = 0; n < android_id_count; n++) {
         if (android_ids[n].aid == appid) {
              username = android_ids[n].name;
              break;
         }
     }
     if (!username)
         goto err;
} else if (appid < AID_ISOLATED_START) { // 如果进程号小于AID_ISOLATED_START
     username = "_app";                     // 说明是普通进程，设置用户名为"_app"
     appid -= AID_APP;
} else {
     username = "_isolated";                // 沙箱进程，设置用户名为"_isolated"
     appid -= AID_ISOLATED_START;
}
if (appid >= CAT_MAPPING_MAX_ID || userid>= CAT_MAPPING_MAX_ID)
     goto err;
for (i = 0; i < nspec; i++) {  // 在seapp_contexts表中进行查找
     cur = seapp_contexts[i];
     if (cur->isSystemServer !=isSystemServer)  // 不处理systemserver进程
         continue;
 
     if (cur->user) {  // 先比较文件中的user项和进程的username
         if (cur->prefix) {
              if (strncasecmp(username,cur->user, cur->len-1))
                  continue;
         } else {
              if (strcasecmp(username, cur->user))
                  continue;
         }
     }
     if (cur->seinfo) {    // 再比较两者的seinfo是否相同
         if (!seinfo || strcasecmp(seinfo,cur->seinfo))
              continue;
     }
     if (cur->name) {      // seapp_contexts中没有哪行定义了name，所以这里不用比较
         if (!pkgname || strcasecmp(pkgname,cur->name))
              continue;
     }
     if (kind == SEAPP_TYPE &&!cur->type)  // 参数kind等于SEAPP_DOMAIN
         continue;
     else if (kind == SEAPP_DOMAIN &&!cur->domain)
         continue;         // 跳过文件中没有domain的项
 
     if (cur->sebool) {    // 如果文件中定义了sebool项(文件中也没有哪行定义它)
         ......
     }
     if (kind == SEAPP_TYPE) {
         if (context_type_set(ctx,cur->type))
              goto oom;
     } else if (kind == SEAPP_DOMAIN) {
         if (context_type_set(ctx,cur->domain)) // 设置安全上下文的域
              goto oom;
     }  
     ......  
}
```
seapp_context_lookup()函数首先根据进程的id得到进程的username，如果是系统进程，通过查找android_ids表可以得到进行用户名，如果是普通进程，通过判断id的大小来区分是普通的app（用户名为_app）还是沙箱应用（用户名为_isolated）。然后根据进程的用户名和seinfo在seapp_contexts表中进行查找对应的项，如果找到了，把找到的domain设置到安全上下文中就完成了。
现在又有了一个新问题，进程的seinfo是什么，进程又是从哪里获得值的？我们前面介绍了PackageManagerService中扫描apk文件时会调用方法scanPackageLI()，这个方法中有下面一段代码：
```
if (mFoundPolicyFile){
   SELinuxMMAC.assignSeinfoValue(pkg);
}
SELinuxMMAC 的assignSeinfoValue()方法就是用来设置应用的seinfo。我们看看assignSeinfoValue()方法的代码：
    public static voidassignSeinfoValue(PackageParser.Package pkg) {
        if(((pkg.applicationInfo.flags & ApplicationInfo.FLAG_SYSTEM) != 0) ||
           ((pkg.applicationInfo.flags&ApplicationInfo.FLAG_UPDATED_SYSTEM_APP) != 0)){
            for (Signature s :pkg.mSignatures) {
                if (s == null)
                    continue;
 
                if (sSigSeinfo.containsKey(s)) { // 查找sSigSeinfo表中的签名
                    Stringseinfo = pkg.applicationInfo.seinfo = sSigSeinfo.get(s);                   
                    return;      // 返回sSigSeinfo中对应的seinfo
                }
            }
            if(sPackageSeinfo.containsKey(pkg.packageName)) {
                String seinfo= pkg.applicationInfo.seinfo =
sPackageSeinfo.get(pkg.packageName);               
                return;         //根据包名来得到seinfo
            }
        }
        String seinfo =pkg.applicationInfo.seinfo = sSigSeinfo.get(null);      
    }
assignSeinfoValue()方法首先根据文件的签名在sSigSeinfo表中匹配相同签名的项，如果找到了相同的项，则返回对应的seinfo。否则再根据应用的包名在sPackageSeinfo表中进行匹配，找到相同的项则返回对应的seinfo。所以问题又变成了sSigSeinfo和sPackageSeinfo两张表中的内容从那里得到的。看看SELinuxMMAC中对这个两个全局变量进行初始化的方法readInstallPolicy方法就知道了，这个方法会对INSTALL_POLICY_FILE数组中定义的xml文件进行解析，解析的结果将保存到这两张表中。INSTALL_POLICY_FILE数组的内容如下：
    private static finalFile[] INSTALL_POLICY_FILE = {
        newFile(Environment.getDataDirectory(), "security/mac_permissions.xml"),
        newFile(Environment.getRootDirectory(),"etc/security/mac_permissions.xml"),
        null};
我们打开一个mac_permissions.xml文件看看，
<?xmlversion="1.0" encoding="utf-8"?>
<policy>
    <signer signature="......">
      <seinfo value="platform"/>
    </signer>
    <signer signature="......">
      <seinfo value="media" />
    </signer>
    <signer signature="......">
      <seinfo value="shared" />
    </signer>
    <signer signature="......">
      <seinfo value="release"/>
    </signer>
    <default>
      <seinfo value="default"/>
    </default>
</policy>
```
上面列出内容中签名项的内容太长，我们就省略了。这个文件的格式很好理解，实际上是给某个签名赋予了一个名称，seinfo用来表示这个名称。
因此应用进程获得安全上下文实际上是根据应用的签名先得到对应的seinfo的值，再通过比较seinfo和用户名得到domain的值。Domain是安全上下文中最关键的项，得到它就等于得到了安全上下文。
从这里也可以看到，Android对SELinux的策略的实现基本上是维持了以前的功能，对app的安全上下文只是根据以前的定义划分成四种类型，还没有进一步的对每个系统app的指定不同的安全上下文。

## Android Selinux中的宏

### init_daemon_domain

<pre>
<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIxNDUzIiBoZWlnaHQ9Ijk1NyIgdmlld0JveD0iLTAuNSAtMC41IDE0NTMgOTU3IiBjb250ZW50PSImbHQ7bXhmaWxlIGhvc3Q9JnF1b3Q7YXBwLmRpYWdyYW1zLm5ldCZxdW90OyBtb2RpZmllZD0mcXVvdDsyMDIxLTExLTA1VDA0OjM5OjIzLjMxMVomcXVvdDsgYWdlbnQ9JnF1b3Q7NS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85MS4wLjQ0NzIuMTY0IFNhZmFyaS81MzcuMzYmcXVvdDsgdmVyc2lvbj0mcXVvdDsxNS42LjgmcXVvdDsgZXRhZz0mcXVvdDstR1l5WHBhaWVUUnVWZnZKazYzeCZxdW90OyZndDsmbHQ7ZGlhZ3JhbSBpZD0mcXVvdDszTkZCSUVRRHVQTFFhN0J0SE1qVSZxdW90OyBuYW1lPSZxdW90O1BhZ2UtMSZxdW90OyZndDs3VnhyYzVzNEYvNDF6TFlmbk1IZ0MzdzBqdDN1YkhmN3R0bWR6WDdLeUNEYmJEQ2lJR3A3Zi8ycmN5UnVCbnhKNHFadW5jbkVRaEs2SEQzbk9SZHdOSE84MnJ5TFNiVDhuWGswMEF6ZDIyam1yV1lZUnQvdWlnK28yY3FhNGRDUUZZdlk5MlJWdDZpNDgvK2pxbEpYdGFudjBhVFNrVE1XY0QrcVZyb3NES25MSzNVa2p0bGFkVlBEelZsUW5UVWlDMXFydUhOSlVLLzkyL2Y0VXRWMkIzYlI4Sjc2aTZXYTJqS0dzbUZHM01kRnpOSlF6YWNaNXJRL0hVd3QyYndpMlZocVpjbVNlR3hkbXRTY2FPWTRab3pMRXB2OUMvc3o5SURNaEl6Vm1IQm5Ka2M5djJ1MUdkTkFuTU5VWG9xQ3VydlNxdThjUU1LMzJhNnp2Y1UwNU9WVlRsdEdNS3lCdk9VckNkSjhqRUVnYm5ibUxPUjRRQUdMc1dYd0pZVk5PVUlpTnY2VXF3WUwrUFJEbno5NGhLNVkrT0N4RmZIRGJEU3hCam1nN0ZoYnVSQmpCTVdFMDBpMFJ6VDJWNVRUV0ZYOXI3aDIxa3VmMDd1SXVOQi9MZUFyNnBaOEJiTHR3cnI5RGMwQUNkY2s4QmVoS0x0Q0puaC9vdHAwS1BPWVBkSnh2c2RzWjlrS3k2SlU0djVLWTA0M3V3Y3VGSWt5c2NKNEs3cW8xazUzb0VDaWxLaW5MdGNsUkdaZGxpVXdadGdpU2drVytkQkdHUnpxT0p1UGR2UHhFMTlidjYrLy9FbytwKzltajhrWDk3ZU9hZGd2ZXQ3QjZ0RVRaYktDTXdoblNZUnRlcjJxZG4wVUtBSS9wUGtoWldvTVorcjVzVkFMbjhHNUppeUYraklFeXVnQmZaNnhrSllSRkRFLzVDamJ2cVAxYjBXTkdBTW1HK2RzQk9CQUZxQ2V1c29WSFM0V0FVa1NWWGJaeW5lelRwekVYSUhQMEV2b2krWHBPc2dDVHM0eEdmSkNoanNGYVV6SnlnOEFNTzlwOEpWeTN5VUk2aURZNlh0VzZBNzdCNUZyTkFIWGZBSGs2bjlNUDVIM05Qekl6UThmLy83cWZmcDROK3JzWTZvb3BoWGNaQ2dWZStVZGRRQWpZR0E2QjRSTGpNNVk3QUVZb0VHUE5ubjlpc1FMUCt4d0ZyVzJ6UmpuYkZWcTNsVUxTWDBQSk9Yc2djY2tUTjRBTVdyR0dNUkZnb2N3bnZlTkI0L09TUnJ3QjdxaGJrdmIyNUttNEM1YkZJWEhQZ2tYY0ZWaHdqWTBKWUk4L1hEeFdSMWNJMUNyNENleHExRGRSNWcvVXU0dW14UURJQ1ltQ1VacXVKWHZlY0haNGRycFZ1SGE3VGN3YlFOZXV5OEExNy8rdk5mOTRITTh0Ly9SamZ0L2hyODliajUxREZ1dkhSTDFoSWVpTGxuTWwyekJRaEpNaWxxbnFQM0FBSDk0aXY5U3pyZEsrSUNvNmhuVGpjL3ZsZXloL0UrcC9uWlRhcmpkWmhlaDJPQjkrUUx1MFcrTWZuWmQzSWRYMlkwVk9JMVpHdnRDZjRTMjByVnFyQnl1cnZkdU0wSWNnVU1IdXhiS205Vk5mWkNvbXNiTGUwUTBIQ1hiMEpYVnBVN3QrQ2x6bzZpblhhOVBoem11UU9vN0xtRU5hTUtFeEM3ZGQ1eVc4ZzdGeWhlVTcrMXBOeU0xcGdIaC90ZnFXbDRjZDZaZWR3cS9iOXhkUWZjU29MTmVFM1Q1UWsrd3pVV1kxVkVlSjFqVGVERjdZL1Q3NkVLQ1Fkd3B2ODB0TVp4OFo2NXdNU3E3bk9Jd3pCNTZaV0hDaEpkV2E4Z0hGRUVLU3pDTXFJd3F3d01ZMDdveEkxNjM3c2M1ekFLS1h0TzlVL3pWazYwSWExWmFmNXpRaUFXK3V4WEZLSjJKa2lodytyQWlic3lTYktwWnZEdDV6WFUydisxdmZWMG13S1FXLzcyUkgyL2I3cmlqSU1NMEFsd0MxTUZiOHRHekY4Y1JDeTlMRG9ycEEvaXpoTk9TTTBDaEVtUHVqcDFHMkFuOHE1UUxmd2ZHRW02LzhQMzhrTVRibTNicDdqdGFYZnpNNXcxT0g1MUR1TkoyUHJKYTRDMXMxSWNkSmRCemxKWktiK3VUdnRFZ2ZzeW5sTU9mc2hjQTZqUGkrRi9rMGtxck9FMlliWHBTODZCYjVpODUxcHJSNjVaOGFiaHNSTjF4RHJVSUhiVERxWVo5eHFrbDBoT2JudU5QM2dVRGtYYkh1T1lGTjFpVFZzZTRkekNNTTRkTmZuSHZmTGJDT3RsV0hLa2JlMG04MGlobmdOYVF4U3NTVkp2WFNoRFEzcE56WUdNZ0hDSWFkMVR3MUhqLzNvZ1RHMzBSVklXOEhscGlJeUo5TG9iTUJnOEwyN1FXTUtuT1hiNzliT1kwUDRJZGE1cnJhOTJZN3VyeUwwZEhzVCttMHRrTld0ZHJVTHIrK1lMUjNvVUZCUzhiaklMRm5rNS9vTGpBUGpZdXNNMVhqUXRzKzhKdzk2S2dROWZxWndSZEN6dCtxMkMwL1JISE5SajltWUxSZWhhZUJWNFd6WURNK1RhaXNoVFM5WUU0ZFNSR1dSRk1iUWZibGtDMU5MeU1Wdk5oVDRoUUlRb1crZ3c0UUUrRmV1ZzVDTWRCTHJneGFtMlV3VFdVUFNXUzNCL0pJZ1NDUURCMGxvTUlxVXVUaENDelJUUmUrVWtpd0pBOE1hbHdJQTdlR3dKRHBJdUw3eG55dzd6R3ZkYk84eUNySWZDMW1nTGZ3Zm1jOE83SmR1a2F5cjY2TWE3YlRLQ0MzOGtqelptZ1lncVk2NmFnQ3pNQW8zcUsrOEtKUnJBQ0QrVkp2eWxOYXpLMUpqK0VCbzZpbUFFVHlncXpOSE94MjBvR29Jbll6ODlLWmU5Y2JKZThLVFpiK3VpKy9VNEp6QnJVQ2N4b0lqRHJmUHhsbk14ZnIvMEN4dlhkaStQZXZYZ1dVbmZmdlRDN2RhaCs0M2N2ekdzRWVJMEF0VHdDZkg3d3B6ei90aWVVcnhyNDZYOHVmYkMrTE1UQWxNQmFreWJuQkRHRmoxSTlSaE4weW5qYm1DNUpFNXAxeHkxbGpnM1pDWVE3c0J2czJ4cHAxWjRTejNGNUJNYkdwYTlsZWN0U3VDQmhzOGQwRFhJUEJibjd3c1J6N2VodzNQd3g4TFRpVWIydzRWdUYvQnlrQ3ZZazlIWVZyUFRRWCtoVVBrd0RQb2pTMGFwenFrYldob0Q5QmVXRWN3QXhKRmxobjVSNHVSWlNYRnVFdlc4YjNkajZGR2JGLzkzUnRUYXdubG9ETXZ5anRQbE1hL0I5ZG1TSjJWYXJja2toMXYyU01sc2toV2x2ZkV0Nmo3QUtjZTRYMnd2dTI1WFlwUWlVdTEvZmpkOS91TTFRSWwvdEFGcWljY091L1RrTkVsb2tTd0N4NEJrVytDMUtkUWwxS3dlZCtBdDNDVjlJT1QyeStlSGRrSmVQTi9mNEhGZUpYeVgrZzBvY2lHY1NraG15OHVqUGg3dkorSy9QRXptR2Z3TzhyZ2YrekVVNkZKNFpXaS9tTmZHOUovWkdVZzlkdVRiVEZUTEMxVGp0eTdtL3YwY3lMb1lUZk96NUhrRnpNRXM1V29rdnFSK2plemxQWTJHSFloUlU2alc5Ym5mSW9FcGpKTmpXRDhFTGpnTi9KY3dybHR1TXpUWFZkSElBM3pWMkF2aUdMMC8wc3JweUJHK2U4WTJWL3VVa20vSWdXcHYwTlV2OGRyV0pwWTBtbW1OcGs0Rm1EN1hSc096RVlMZXBOcHBxazU3bU9OcW9EOTBzRzdyQmpWM05HbVBOV0xPRzBGa01aWTl3cUFIVzRGM09RSnRNTldlTW5mdWFZMk5ORHlhMWU4MHJxVS9Sc0RaTGMyNjEwVmd0MHJiVW1FNjJBRWV2OWgvQzJxd2V0cHFhZFl2OWJ6VjcvRFRyOEQyYzRrQWJDUkdnRU1WZjJGc3VncHBZODllVGp6clY5aFNrL3R6enpSZHkxRmsyTEVUYmZaMzZRZzR1TXlKcSt5MENQbE1vMkRicFUrTENhNTc1cER4ejM2aWJxVytjWjc2Z3I2Ulc2SzJCeG0xZ2JBczVZelJBWXJIaEV1eU9JSXdwOHRMVGpGVFpRQXlBeDRETnhrQkljbVRiVVd3bUdQT3ltT2M0azNHRUhFODBDejhWclRkdDZEaU9QMHNTNjByU0o1SDBRSDkxa2o3OXU0bmZBNkUwUmhKMTJ1NXJ0aUNYcnVxdnlFSFhMQk41dDZlTkxLZ1JCQ1JhRlYxazFHNUJ5RjNrVUpGRXBrQklzcDh6eEg1REtGOFdjenpaazIraW1rTEV1NTUrVlpCWlNyaFJrSmNsUDVVcEwzMno3bkNtdkVsME9NQ2h0UG1WWVovTHNNTlhaOWpUdjlIM1BYQURwaWtjOUVJRlhUckFnVVdhdFFpOXBZOXFLK1lZU1Q5T2NHdlpmUjBDejFwT01SUm8va2cxaWI5QTM1S2d6VXBRdjVzdndCckx5Q2c3NjJ5UGxweEhDVzRMbHI5ZXIyOVdKQnplc0hnaExnTS9URGR3ZENUc3dMODFTMlRaRkIvZzNhUWJjVEEzNWcxcXkyVXgwWEZNamdWSVBFa21SMzZHREZTL1RObXliWXFCemhES2g0SjJsUjRyUnpDVk5MbnFjY2twcjNJbS82aEVSdU5UZ2d2WmJNVzNFbHJuU0pVV0J6dkpJSVRCbWkxZ1ptUzZMVUUxUkx5MUp6b0xsYTVIMFRsSHlDbHlKUGRWekF4dWdxalJrU095Y1o3elJsZEJXUGxFcFpVNzB1ZkpDVXNzMGtKUHBnY0NzYWNsYlVKRkcyRzRDaldZemhTalFTUmJvakRSUWQyZTVTVkJKbWFOTjN2VnZMT0Z4SWVCTUhTV0dRRzlRc0dWNUxMazB6Slo3MzNKNVVJd2VWSVc4UWtQdzY0dTFaTmNxcUg5eWk2Vm1VWE5GK1pTU2NZeFN4bStobFRYM3VjVHVjTG55YktjcW5MU1FYZkptbFN0ZXpHUUpZUGtob2prb3JoaHh3Zzg5VDJLNHNXRHJtRlZYajFvdGl2cXVmUGhMNTBjZk41U01GY0RyemtIQ1B6S1ljL2tNT3Q4SENZdWkzOXZqRzN2aXY4aGJVNytEdz09Jmx0Oy9kaWFncmFtJmd0OyZsdDsvbXhmaWxlJmd0OyI+PGRlZnM+PGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+PGZlR2F1c3NpYW5CbHVyIGluPSJTb3VyY2VBbHBoYSIgc3RkRGV2aWF0aW9uPSIxLjciIHJlc3VsdD0iYmx1ciIvPjxmZU9mZnNldCBpbj0iYmx1ciIgZHg9IjMiIGR5PSIzIiByZXN1bHQ9Im9mZnNldEJsdXIiLz48ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzNENDU3NCIgZmxvb2Qtb3BhY2l0eT0iMC40IiByZXN1bHQ9Im9mZnNldENvbG9yIi8+PGZlQ29tcG9zaXRlIGluPSJvZmZzZXRDb2xvciIgaW4yPSJvZmZzZXRCbHVyIiBvcGVyYXRvcj0iaW4iIHJlc3VsdD0ib2Zmc2V0Qmx1ciIvPjxmZUJsZW5kIGluPSJTb3VyY2VHcmFwaGljIiBpbjI9Im9mZnNldEJsdXIiLz48L2ZpbHRlcj48L2RlZnM+PGcgZmlsdGVyPSJ1cmwoI2Ryb3BTaGFkb3cpIj48cGF0aCBkPSJNIDUxNiAwIEwgNjY2IDAgTCA2NzYgMTAgTCA2NjYgMjAgTCA1MTYgMjAgTCA1MjYgMTAgWiIgZmlsbD0icmdiYSgyNTUsIDI1NSwgMjU1LCAxKSIgc3Ryb2tlPSIjOTk5OTk5IiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48c3dpdGNoPjxmb3JlaWduT2JqZWN0IHBvaW50ZXItZXZlbnRzPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiByZXF1aXJlZEZlYXR1cmVzPSJodHRwOi8vd3d3LnczLm9yZy9UUi9TVkcxMS9mZWF0dXJlI0V4dGVuc2liaWxpdHkiIHN0eWxlPSJvdmVyZmxvdzogdmlzaWJsZTsgdGV4dC1hbGlnbjogbGVmdDsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGNlbnRlcjsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgY2VudGVyOyB3aWR0aDogMTU4cHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogMTBweDsgbWFyZ2luLWxlZnQ6IDUxN3B4OyI+PGRpdiBkYXRhLWRyYXdpby1jb2xvcnM9ImNvbG9yOiByZ2JhKDAsIDAsIDAsIDEpOyAiIHN0eWxlPSJib3gtc2l6aW5nOiBib3JkZXItYm94OyBmb250LXNpemU6IDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IHdoaXRlLXNwYWNlOiBub3JtYWw7IG92ZXJmbG93LXdyYXA6IG5vcm1hbDsiPjxmb250IGNvbG9yPSIjOTk5OTk5Ij5pbml0X2RhZW1vbl9kb21haW48L2ZvbnQ+PC9kaXY+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0Pjx0ZXh0IHg9IjU5NiIgeT0iMTQiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJIZWx2ZXRpY2EiIGZvbnQtc2l6ZT0iMTJweCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+aW5pdF9kYWVtb25fZG9tYWluPC90ZXh0Pjwvc3dpdGNoPjwvZz48cGF0aCBkPSJNIDEzMjEgMTE1IEwgMTU1MSAxMTUiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiB0cmFuc2Zvcm09InJvdGF0ZSg5MCwxNDM2LDExNSkiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48c3dpdGNoPjxmb3JlaWduT2JqZWN0IHBvaW50ZXItZXZlbnRzPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiByZXF1aXJlZEZlYXR1cmVzPSJodHRwOi8vd3d3LnczLm9yZy9UUi9TVkcxMS9mZWF0dXJlI0V4dGVuc2liaWxpdHkiIHN0eWxlPSJvdmVyZmxvdzogdmlzaWJsZTsgdGV4dC1hbGlnbjogbGVmdDsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGZsZXgtc3RhcnQ7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGZsZXgtZW5kOyB3aWR0aDogMXB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDE1cHg7IG1hcmdpbi1sZWZ0OiAxNDQ0cHg7Ij48ZGl2IGRhdGEtZHJhd2lvLWNvbG9ycz0iY29sb3I6IHJnYmEoMCwgMCwgMCwgMSk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiByaWdodDsiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyI+PGZvbnQgY29sb3I9IiM5OTk5OTkiPmxta2TCoCDCoMKgPC9mb250PjwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48dGV4dCB4PSIxNDQ0IiB5PSIyNyIgZmlsbD0icmdiYSgwLCAwLCAwLCAxKSIgZm9udC1mYW1pbHk9IkhlbHZldGljYSIgZm9udC1zaXplPSIxMnB4IiB0ZXh0LWFuY2hvcj0iZW5kIj5sbWsuLi48L3RleHQ+PC9zd2l0Y2g+PC9nPjxwYXRoIGQ9Ik0gNjY2IDExMCBMIDY3NiAxMTUgTCA2NjYgMTIwIFoiIGZpbGw9InJnYmEoMjU1LCAyNTUsIDI1NSwgMSkiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5IiBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBjZW50ZXI7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGZsZXgtZW5kOyB3aWR0aDogMXB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDExNXB4OyBtYXJnaW4tbGVmdDogNjU0cHg7Ij48ZGl2IGRhdGEtZHJhd2lvLWNvbG9ycz0iY29sb3I6IHJnYmEoMCwgMCwgMCwgMSk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiByaWdodDsiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyI+PHByZSBzdHlsZT0idGV4dC1hbGlnbjogbGVmdCA7IGJvcmRlcjogMHB4IDsgbWFyZ2luLXRvcDogMHB4IDsgbWFyZ2luLWJvdHRvbTogMHB4Ij5kb21haW5fYXV0b190cmFucyhpbml0LCBoYWxfbnJmNTJfZGVmYXVsdF9leGVjLCBoYWxfbnJmNTJfZGVmYXVsdCk8L3ByZT48L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iNjU0IiB5PSIxMTkiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJIZWx2ZXRpY2EiIGZvbnQtc2l6ZT0iMTJweCIgdGV4dC1hbmNob3I9ImVuZCI+ZG9tYWluX2F1dG9fdHJhbnMoaW5pdCwgaGFsX25yZjUyX2RlZmF1bHRfZXhlYywgaGFsX25yZjUyX2RlZmF1bHQpPC90ZXh0Pjwvc3dpdGNoPjwvZz48cGF0aCBkPSJNIDcxNiAxNDQgTCA3MTYgMTcwIFEgNzE2IDE4MCA3MjYgMTgwIEwgNzU2IDE4MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjOTk5OTk5IiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJzdHJva2UiLz48ZWxsaXBzZSBjeD0iNzE2IiBjeT0iMTQxIiByeD0iMyIgcnk9IjMiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzk5OTk5OSIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxwYXRoIGQ9Ik0gNzU2IDE4MCBMIDc0OSAxNzYuNSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjOTk5OTk5IiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48cGF0aCBkPSJNIDcxNiAxNDQgTCA3MTYgOTAwIiBmaWxsPSJub25lIiBzdHJva2U9IiM5OTk5OTkiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9InN0cm9rZSIvPjxlbGxpcHNlIGN4PSI3MTYiIGN5PSIxNDEiIHJ4PSIzIiByeT0iMyIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjOTk5OTk5IiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PHBhdGggZD0iTSA3MTYgOTAwIEwgNzE5LjUgODkzIiBmaWxsPSJub25lIiBzdHJva2U9IiM5OTk5OTkiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxyZWN0IHg9IjcxNiIgeT0iMCIgd2lkdGg9IjM3MCIgaGVpZ2h0PSIxNDEiIGZpbGw9Im5vbmUiIHN0cm9rZT0ibm9uZSIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0wLjUgLTAuNSkiPjxzd2l0Y2g+PGZvcmVpZ25PYmplY3QgcG9pbnRlci1ldmVudHM9Im5vbmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHJlcXVpcmVkRmVhdHVyZXM9Imh0dHA6Ly93d3cudzMub3JnL1RSL1NWRzExL2ZlYXR1cmUjRXh0ZW5zaWJpbGl0eSIgc3R5bGU9Im92ZXJmbG93OiB2aXNpYmxlOyB0ZXh0LWFsaWduOiBsZWZ0OyI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiB1bnNhZmUgZmxleC1zdGFydDsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgZmxleC1zdGFydDsgd2lkdGg6IDM2OHB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDdweDsgbWFyZ2luLWxlZnQ6IDcxOHB4OyI+PGRpdiBkYXRhLWRyYXdpby1jb2xvcnM9ImNvbG9yOiByZ2JhKDAsIDAsIDAsIDEpOyBiYWNrZ3JvdW5kLWNvbG9yOiAjZmZmZmZmOyBib3JkZXItY29sb3I6ICM5OTk5OTk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiBsZWZ0OyI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiAmcXVvdDtDb3VyaWVyIE5ldyZxdW90OzsgY29sb3I6IHJnYigwLCAwLCAwKTsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSwgMjU1LCAyNTUpOyBib3JkZXI6IDFweCBzb2xpZCByZ2IoMTUzLCAxNTMsIDE1Myk7IHdoaXRlLXNwYWNlOiBub3JtYWw7IG92ZXJmbG93LXdyYXA6IG5vcm1hbDsiPjxwcmUgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6IHJnYigyNTUgLCAyNTUgLCAyNTUpIDsgZm9udC1mYW1pbHk6ICZxdW90O2NvbnNvbGFzJnF1b3Q7ICwgbW9ub3NwYWNlIDsgZm9udC1zaXplOiA4LjNwdCI+PGZvbnQgY29sb3I9IiM5OTAwNGQiPi8vIHN5c3RlbVxzZXBvbGljeVxwdWJsaWNcdGVfbWFjcm9zPGJyIC8+PC9mb250PiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyM8YnIgLz4jIGluaXRfZGFlbW9uX2RvbWFpbihkb21haW4pPGJyIC8+IyBTZXQgdXAgYSB0cmFuc2l0aW9uIGZyb20gaW5pdCB0byB0aGUgZGFlbW9uIGRvbWFpbjxiciAvPiMgdXBvbiBleGVjdXRpbmcgaXRzIGJpbmFyeS48YnIgLz48Zm9udCBjb2xvcj0iIzAwMDBmZiI+ZGVmaW5lPC9mb250PjxzcGFuIHN0eWxlPSJjb2xvcjogcmdiKDAgLCAwICwgMCkiPihgPC9zcGFuPjxmb250IGNvbG9yPSIjMDA5OTAwIj5pbml0X2RhZW1vbl9kb21haW48L2ZvbnQ+JywgYDxiciAvPjxmb250IGNvbG9yPSIjOTkwMDRkIj5kb21haW5fYXV0b190cmFuczwvZm9udD4oaW5pdCwgJDFfZXhlYywgJDEpPGJyIC8+PC9wcmU+PC9kaXY+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0Pjx0ZXh0IHg9IjcxOCIgeT0iMTkiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJDb3VyaWVyIE5ldyIgZm9udC1zaXplPSIxMnB4Ij4vLyBzeXN0ZW1cc2Vwb2xpY3lccHVibGljXHRlX21hY3Jvcy4uLjwvdGV4dD48L3N3aXRjaD48L2c+PHJlY3QgeD0iNzE2IiB5PSI5MDAiIHdpZHRoPSI0MCIgaGVpZ2h0PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJub25lIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5IiBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBmbGV4LXN0YXJ0OyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBmbGV4LXN0YXJ0OyB3aWR0aDogMzhweDsgaGVpZ2h0OiAxcHg7IHBhZGRpbmctdG9wOiA5MDdweDsgbWFyZ2luLWxlZnQ6IDcxOHB4OyI+PGRpdiBkYXRhLWRyYXdpby1jb2xvcnM9ImNvbG9yOiByZ2JhKDAsIDAsIDAsIDEpOyBiYWNrZ3JvdW5kLWNvbG9yOiAjZmZmZmZmOyBib3JkZXItY29sb3I6ICM5OTk5OTk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiBsZWZ0OyI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiAmcXVvdDtDb3VyaWVyIE5ldyZxdW90OzsgY29sb3I6IHJnYigwLCAwLCAwKTsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSwgMjU1LCAyNTUpOyBib3JkZXI6IDFweCBzb2xpZCByZ2IoMTUzLCAxNTMsIDE1Myk7IHdoaXRlLXNwYWNlOiBub3JtYWw7IG92ZXJmbG93LXdyYXA6IG5vcm1hbDsiPjxwcmUgc3R5bGU9ImNvbG9yOiByZ2IoMCAsIDAgLCAwKSA7IGZvbnQtc2l6ZTogOC4zcHQgOyBmb250LXN0eWxlOiBub3JtYWwgOyBmb250LXdlaWdodDogNDAwIDsgbGV0dGVyLXNwYWNpbmc6IG5vcm1hbCA7IHRleHQtYWxpZ246IGxlZnQgOyB0ZXh0LWluZGVudDogMHB4IDsgdGV4dC10cmFuc2Zvcm06IG5vbmUgOyB3b3JkLXNwYWNpbmc6IDBweCA7IGJhY2tncm91bmQtY29sb3I6IHJnYigyNTUgLCAyNTUgLCAyNTUpIDsgZm9udC1mYW1pbHk6ICZxdW90O2NvbnNvbGFzJnF1b3Q7ICwgbW9ub3NwYWNlIj4nKTwvcHJlPjwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48dGV4dCB4PSI3MTgiIHk9IjkxOSIgZmlsbD0icmdiYSgwLCAwLCAwLCAxKSIgZm9udC1mYW1pbHk9IkNvdXJpZXIgTmV3IiBmb250LXNpemU9IjEycHgiPicpPC90ZXh0Pjwvc3dpdGNoPjwvZz48cGF0aCBkPSJNIDc1NiAzMDMgTCA3NTYgMzg3LjUgUSA3NTYgMzk3LjUgNzY2IDM5Ny41IEwgNzk2IDM5Ny41IiBmaWxsPSJub25lIiBzdHJva2U9IiM5OTk5OTkiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9InN0cm9rZSIvPjxlbGxpcHNlIGN4PSI3NTYiIGN5PSIzMDAiIHJ4PSIzIiByeT0iMyIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjOTk5OTk5IiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PHBhdGggZD0iTSA3OTYgMzk3LjUgTCA3ODkgMzk0IiBmaWxsPSJub25lIiBzdHJva2U9IiM5OTk5OTkiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxwYXRoIGQ9Ik0gNzU2IDMwMyBMIDc1NiA4MjAiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0ic3Ryb2tlIi8+PGVsbGlwc2UgY3g9Ijc1NiIgY3k9IjMwMCIgcng9IjMiIHJ5PSIzIiBmaWxsPSJub25lIiBzdHJva2U9IiM5OTk5OTkiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48cGF0aCBkPSJNIDc1NiA4MjAgTCA3NTkuNSA4MTMiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PHJlY3QgeD0iNzU2IiB5PSIxNDAiIHdpZHRoPSIzODAiIGhlaWdodD0iMTYwIiBmaWxsPSJub25lIiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48c3dpdGNoPjxmb3JlaWduT2JqZWN0IHBvaW50ZXItZXZlbnRzPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiByZXF1aXJlZEZlYXR1cmVzPSJodHRwOi8vd3d3LnczLm9yZy9UUi9TVkcxMS9mZWF0dXJlI0V4dGVuc2liaWxpdHkiIHN0eWxlPSJvdmVyZmxvdzogdmlzaWJsZTsgdGV4dC1hbGlnbjogbGVmdDsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGZsZXgtc3RhcnQ7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGZsZXgtc3RhcnQ7IHdpZHRoOiAzNzhweDsgaGVpZ2h0OiAxcHg7IHBhZGRpbmctdG9wOiAxNDdweDsgbWFyZ2luLWxlZnQ6IDc1OHB4OyI+PGRpdiBkYXRhLWRyYXdpby1jb2xvcnM9ImNvbG9yOiByZ2JhKDAsIDAsIDAsIDEpOyBiYWNrZ3JvdW5kLWNvbG9yOiAjZmZmZmZmOyBib3JkZXItY29sb3I6ICM5OTk5OTk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiBsZWZ0OyI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiAmcXVvdDtDb3VyaWVyIE5ldyZxdW90OzsgY29sb3I6IHJnYigwLCAwLCAwKTsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSwgMjU1LCAyNTUpOyBib3JkZXI6IDFweCBzb2xpZCByZ2IoMTUzLCAxNTMsIDE1Myk7IHdoaXRlLXNwYWNlOiBub3JtYWw7IG92ZXJmbG93LXdyYXA6IG5vcm1hbDsiPjxwcmUgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6IHJnYigyNTUgLCAyNTUgLCAyNTUpIDsgZm9udC1mYW1pbHk6ICZxdW90O2NvbnNvbGFzJnF1b3Q7ICwgbW9ub3NwYWNlIDsgZm9udC1zaXplOiA4LjNwdCI+PGZvbnQgY29sb3I9IiM5OTAwNGQiPi8vIHN5c3RlbVxzZXBvbGljeVxwdWJsaWNcdGVfbWFjcm9zPGJyIC8+PC9mb250PiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyM8YnIgLz4jIGRvbWFpbl9hdXRvX3RyYW5zKG9sZGRvbWFpbiwgdHlwZSwgbmV3ZG9tYWluKTxiciAvPiMgQXV0b21hdGljYWxseSB0cmFuc2l0aW9uIGZyb20gb2xkZG9tYWluIHRvIG5ld2RvbWFpbjxiciAvPiMgdXBvbiBleGVjdXRpbmcgYSBmaWxlIGxhYmVsZWQgd2l0aCB0eXBlLjxiciAvPiM8YnIgLz48Zm9udCBjb2xvcj0iIzAwMDBmZiI+ZGVmaW5lPC9mb250PjxzcGFuIHN0eWxlPSJjb2xvcjogcmdiKDAgLCAwICwgMCkiPihgPC9zcGFuPjxmb250IGNvbG9yPSIjMDA5OTAwIj5kb21haW5fYXV0b190cmFuczwvZm9udD4nLCBgPGJyIC8+IyBBbGxvdyB0aGUgbmVjZXNzYXJ5IHBlcm1pc3Npb25zLjxiciAvPjxmb250IGNvbG9yPSIjOTkwMDRkIj5kb21haW5fdHJhbnM8L2ZvbnQ+KCQxLCQyLCQzKTxiciAvPjwvcHJlPjwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48dGV4dCB4PSI3NTgiIHk9IjE1OSIgZmlsbD0icmdiYSgwLCAwLCAwLCAxKSIgZm9udC1mYW1pbHk9IkNvdXJpZXIgTmV3IiBmb250LXNpemU9IjEycHgiPi8vIHN5c3RlbVxzZXBvbGljeVxwdWJsaWNcdGVfbWFjcm9zLi4uPC90ZXh0Pjwvc3dpdGNoPjwvZz48cmVjdCB4PSI3NTYiIHk9IjgyMCIgd2lkdGg9IjI4MCIgaGVpZ2h0PSI4MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJub25lIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5IiBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBmbGV4LXN0YXJ0OyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBmbGV4LXN0YXJ0OyB3aWR0aDogMjc4cHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogODI3cHg7IG1hcmdpbi1sZWZ0OiA3NThweDsiPjxkaXYgZGF0YS1kcmF3aW8tY29sb3JzPSJjb2xvcjogcmdiYSgwLCAwLCAwLCAxKTsgYmFja2dyb3VuZC1jb2xvcjogI2ZmZmZmZjsgYm9yZGVyLWNvbG9yOiAjOTk5OTk5OyAiIHN0eWxlPSJib3gtc2l6aW5nOiBib3JkZXItYm94OyBmb250LXNpemU6IDBweDsgdGV4dC1hbGlnbjogbGVmdDsiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogJnF1b3Q7Q291cmllciBOZXcmcXVvdDs7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IGJhY2tncm91bmQtY29sb3I6IHJnYigyNTUsIDI1NSwgMjU1KTsgYm9yZGVyOiAxcHggc29saWQgcmdiKDE1MywgMTUzLCAxNTMpOyB3aGl0ZS1zcGFjZTogbm9ybWFsOyBvdmVyZmxvdy13cmFwOiBub3JtYWw7Ij48cHJlIHN0eWxlPSJmb250LXNpemU6IDguM3B0IDsgZm9udC1zdHlsZTogbm9ybWFsIDsgZm9udC13ZWlnaHQ6IDQwMCA7IGxldHRlci1zcGFjaW5nOiBub3JtYWwgOyB0ZXh0LWFsaWduOiBsZWZ0IDsgdGV4dC1pbmRlbnQ6IDBweCA7IHRleHQtdHJhbnNmb3JtOiBub25lIDsgd29yZC1zcGFjaW5nOiAwcHggOyBiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMjU1ICwgMjU1ICwgMjU1KSA7IGZvbnQtZmFtaWx5OiAmcXVvdDtjb25zb2xhcyZxdW90OyAsIG1vbm9zcGFjZSI+IyBNYWtlIHRoZSB0cmFuc2l0aW9uIG9jY3VyIGJ5IGRlZmF1bHQuPGJyIC8+PGZvbnQgY29sb3I9IiMwMDAwZmYiPnR5cGVfdHJhbnNpdGlvbjwvZm9udD48c3BhbiBzdHlsZT0iY29sb3I6IHJnYigwICwgMCAsIDApIj4gJDEgJDI6cHJvY2VzcyAkMzs8YnIgLz4nKTwvc3Bhbj48L3ByZT48L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iNzU4IiB5PSI4MzkiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJDb3VyaWVyIE5ldyIgZm9udC1zaXplPSIxMnB4Ij4jIE1ha2UgdGhlIHRyYW5zaXRpb24gb2NjdXIgYnkgZGVmYXVsdC4uLi48L3RleHQ+PC9zd2l0Y2g+PC9nPjxwYXRoIGQ9Ik0gNjY2IDI3MCBMIDY3NiAyNzUgTCA2NjYgMjgwIFoiIGZpbGw9InJnYmEoMjU1LCAyNTUsIDI1NSwgMSkiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5IiBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBjZW50ZXI7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGZsZXgtZW5kOyB3aWR0aDogMXB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDI3NXB4OyBtYXJnaW4tbGVmdDogNjU0cHg7Ij48ZGl2IGRhdGEtZHJhd2lvLWNvbG9ycz0iY29sb3I6IHJnYmEoMCwgMCwgMCwgMSk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiByaWdodDsiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyI+PHByZSBzdHlsZT0idGV4dC1hbGlnbjogbGVmdCA7IGJvcmRlcjogMHB4IDsgbWFyZ2luLXRvcDogMHB4IDsgbWFyZ2luLWJvdHRvbTogMHB4Ij5kb21haW5fdHJhbnMoaW5pdCwgaGFsX25yZjUyX2RlZmF1bHRfZXhlYywgaGFsX25yZjUyX2RlZmF1bHQpPC9wcmU+PC9kaXY+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0Pjx0ZXh0IHg9IjY1NCIgeT0iMjc5IiBmaWxsPSJyZ2JhKDAsIDAsIDAsIDEpIiBmb250LWZhbWlseT0iSGVsdmV0aWNhIiBmb250LXNpemU9IjEycHgiIHRleHQtYW5jaG9yPSJlbmQiPmRvbWFpbl90cmFucyhpbml0LCBoYWxfbnJmNTJfZGVmYXVsdF9leGVjLCBoYWxfbnJmNTJfZGVmYXVsdCk8L3RleHQ+PC9zd2l0Y2g+PC9nPjxyZWN0IHg9Ijc5NiIgeT0iMzEwIiB3aWR0aD0iNDUwIiBoZWlnaHQ9IjM1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJub25lIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5IiBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBmbGV4LXN0YXJ0OyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBmbGV4LXN0YXJ0OyB3aWR0aDogNDQ4cHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogMzE3cHg7IG1hcmdpbi1sZWZ0OiA3OThweDsiPjxkaXYgZGF0YS1kcmF3aW8tY29sb3JzPSJjb2xvcjogcmdiYSgwLCAwLCAwLCAxKTsgYmFja2dyb3VuZC1jb2xvcjogI2ZmZmZmZjsgYm9yZGVyLWNvbG9yOiAjOTk5OTk5OyAiIHN0eWxlPSJib3gtc2l6aW5nOiBib3JkZXItYm94OyBmb250LXNpemU6IDBweDsgdGV4dC1hbGlnbjogbGVmdDsiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogJnF1b3Q7Q291cmllciBOZXcmcXVvdDs7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IGJhY2tncm91bmQtY29sb3I6IHJnYigyNTUsIDI1NSwgMjU1KTsgYm9yZGVyOiAxcHggc29saWQgcmdiKDE1MywgMTUzLCAxNTMpOyB3aGl0ZS1zcGFjZTogbm9ybWFsOyBvdmVyZmxvdy13cmFwOiBub3JtYWw7Ij48cHJlIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMjU1ICwgMjU1ICwgMjU1KSA7IGZvbnQtZmFtaWx5OiAmcXVvdDtjb25zb2xhcyZxdW90OyAsIG1vbm9zcGFjZSA7IGZvbnQtc2l6ZTogOC4zcHQiPjxmb250IGNvbG9yPSIjOTkwMDRkIj4vLyBzeXN0ZW1cc2Vwb2xpY3lccHVibGljXHRlX21hY3JvczxiciAvPjwvZm9udD4jIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjPGJyIC8+IyBkb21haW5fdHJhbnMob2xkZG9tYWluLCB0eXBlLCBuZXdkb21haW4pPGJyIC8+IyBBbGxvdyBhIHRyYW5zaXRpb24gZnJvbSBvbGRkb21haW4gdG8gbmV3ZG9tYWluPGJyIC8+IyB1cG9uIGV4ZWN1dGluZyBhIGZpbGUgbGFiZWxlZCB3aXRoIHR5cGUuPGJyIC8+IyBUaGlzIG9ubHkgYWxsb3dzIHRoZSB0cmFuc2l0aW9uOyBpdCBkb2VzIG5vdDxiciAvPiMgY2F1c2UgaXQgdG8gb2NjdXIgYXV0b21hdGljYWxseSAtIHVzZSBkb21haW5fYXV0b190cmFuczxiciAvPiMgaWYgdGhhdCBpcyB3aGF0IHlvdSB3YW50LjxiciAvPiM8YnIgLz48Zm9udCBjb2xvcj0iIzAwMDBmZiI+ZGVmaW5lPC9mb250PjxzcGFuIHN0eWxlPSJjb2xvcjogcmdiKDAgLCAwICwgMCkiPihgPC9zcGFuPjxmb250IGNvbG9yPSIjMDA5OTAwIj5kb21haW5fdHJhbnM8L2ZvbnQ+PHNwYW4gc3R5bGU9ImNvbG9yOiByZ2IoMCAsIDAgLCAwKSI+JywgYDxiciAvPiMgT2xkIGRvbWFpbiBtYXkgZXhlYyB0aGUgZmlsZSBhbmQgdHJhbnNpdGlvbiB0byB0aGUgbmV3IGRvbWFpbi48YnIgLz5hbGxvdyAkMSAkMjpmaWxlIHsgZ2V0YXR0ciBvcGVuIHJlYWQgZXhlY3V0ZSBtYXAgfTs8YnIgLz5hbGxvdyAkMSAkMzpwcm9jZXNzIHRyYW5zaXRpb247PGJyIC8+PGJyIC8+PGJyIC8+PGJyIC8+IyBOZXcgZG9tYWluIGlzIGVudGVyZWQgYnkgZXhlY3V0aW5nIHRoZSBmaWxlLjxiciAvPmFsbG93ICQzICQyOmZpbGUgeyBlbnRyeXBvaW50IG9wZW4gcmVhZCBleGVjdXRlIGdldGF0dHIgbWFwIH07PGJyIC8+PGJyIC8+PGJyIC8+PGJyIC8+IyBOZXcgZG9tYWluIGNhbiBzZW5kIFNJR0NITEQgdG8gaXRzIGNhbGxlci48YnIgLz5pZmVsc2UoJDEsIGBpbml0JywgYCcsIGBhbGxvdyAkMyAkMTpwcm9jZXNzIHNpZ2NobGQ7Jyk8L3NwYW4+PC9wcmU+PHByZSBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSAsIDI1NSAsIDI1NSkgOyBmb250LWZhbWlseTogJnF1b3Q7Y29uc29sYXMmcXVvdDsgLCBtb25vc3BhY2UgOyBmb250LXNpemU6IDguM3B0Ij48c3BhbiBzdHlsZT0iY29sb3I6IHJnYigwICwgMCAsIDApIj48YnIgLz48L3NwYW4+PC9wcmU+PHByZSBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSAsIDI1NSAsIDI1NSkgOyBmb250LWZhbWlseTogJnF1b3Q7Y29uc29sYXMmcXVvdDsgLCBtb25vc3BhY2UgOyBmb250LXNpemU6IDguM3B0Ij48c3BhbiBzdHlsZT0iY29sb3I6IHJnYigwICwgMCAsIDApIj48YnIgLz48L3NwYW4+PC9wcmU+PHByZSBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDI1NSAsIDI1NSAsIDI1NSkgOyBmb250LWZhbWlseTogJnF1b3Q7Y29uc29sYXMmcXVvdDsgLCBtb25vc3BhY2UgOyBmb250LXNpemU6IDguM3B0Ij48c3BhbiBzdHlsZT0iY29sb3I6IHJnYigwICwgMCAsIDApIj48YnIgLz4jIEVuYWJsZSBBVF9TRUNVUkUsIGkuZS4gbGliYyBzZWN1cmUgbW9kZS48YnIgLz5kb250YXVkaXQgJDEgJDM6cHJvY2VzcyBub2F0c2VjdXJlOzxiciAvPiMgWFhYIGRvbnRhdWRpdCBjYW5kaWRhdGUgYnV0IHJlcXVpcmVzIGZ1cnRoZXIgc3R1ZHkuPGJyIC8+YWxsb3cgJDEgJDM6cHJvY2VzcyB7IHNpZ2luaCBybGltaXRpbmggfTs8YnIgLz4nKTwvc3Bhbj48L3ByZT48L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iNzk4IiB5PSIzMjkiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJDb3VyaWVyIE5ldyIgZm9udC1zaXplPSIxMnB4Ij4vLyBzeXN0ZW1cc2Vwb2xpY3lccHVibGljXHRlX21hY3Jvcy4uLjwvdGV4dD48L3N3aXRjaD48L2c+PHBhdGggZD0iTSA2NjYgNDgwIEwgNjc2IDQ4NSBMIDY2NiA0OTAgWiIgZmlsbD0icmdiYSgyNTUsIDI1NSwgMjU1LCAxKSIgc3Ryb2tlPSIjOTk5OTk5IiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48c3dpdGNoPjxmb3JlaWduT2JqZWN0IHBvaW50ZXItZXZlbnRzPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiByZXF1aXJlZEZlYXR1cmVzPSJodHRwOi8vd3d3LnczLm9yZy9UUi9TVkcxMS9mZWF0dXJlI0V4dGVuc2liaWxpdHkiIHN0eWxlPSJvdmVyZmxvdzogdmlzaWJsZTsgdGV4dC1hbGlnbjogbGVmdDsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGNlbnRlcjsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgZmxleC1lbmQ7IHdpZHRoOiAxcHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogNDg1cHg7IG1hcmdpbi1sZWZ0OiA2NTRweDsiPjxkaXYgZGF0YS1kcmF3aW8tY29sb3JzPSJjb2xvcjogcmdiYSgwLCAwLCAwLCAxKTsgIiBzdHlsZT0iYm94LXNpemluZzogYm9yZGVyLWJveDsgZm9udC1zaXplOiAwcHg7IHRleHQtYWxpZ246IHJpZ2h0OyI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7Ij48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPi8vIOWFgeiuuOaXpyBkb21haW4g5Y+v5Lul5omn6KGM5oyH5a6a5paH5Lu277yM5bm25LiU5YWB6K645omn6KGM5penIGRvbWFpbiDovazlj5jkuLrmlrAgZG9tYWluIOeahOaTjeS9nDwvcHJlPjxwcmUgc3R5bGU9InRleHQtYWxpZ246IGxlZnQgOyBib3JkZXI6IDBweCA7IG1hcmdpbi10b3A6IDBweCA7IG1hcmdpbi1ib3R0b206IDBweCI+Ly8g5q2k5aSE5Li65YWB6K64IGluaXQg5Y+v5Lul5omn6KGMIGhhbF9ucmY1Ml9kZWZhdWx0X2V4ZWMg5paH5Lu277yM5bm25LiU5YWB6K64IGluaXQgZG9tYWluIOi9rOWPmOS4uiBoYWxfbnJmNTJfZGVmYXVsdCBkb21haW48L3ByZT48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPmFsbG93IGluaXQgaGFsX25yZjUyX2RlZmF1bHRfZXhlYzpmaWxlIHsgZ2V0YXR0ciBvcGVuIHJlYWQgZXhlY3V0ZSBtYXAgfTs8YnIgLz5hbGxvdyBpbml0IGhhbF9ucmY1Ml9kZWZhdWx0OnByb2Nlc3MgdHJhbnNpdGlvbjs8YnIgLz48L3ByZT48L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iNjU0IiB5PSI0ODkiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJIZWx2ZXRpY2EiIGZvbnQtc2l6ZT0iMTJweCIgdGV4dC1hbmNob3I9ImVuZCI+Ly8g5YWB6K645penIGRvbWFpbiDlj6/ku6XmiafooYzmjIflrprmlofku7bvvIzlubbkuJTlhYHorrjmiafooYzml6cgZG9tYWluIOi9rOWPmOS4uuaWsCBkb21haW4g55qE5pON5L2cLi4uPC90ZXh0Pjwvc3dpdGNoPjwvZz48cGF0aCBkPSJNIDY2NiA1NjAgTCA2NzYgNTY1IEwgNjY2IDU3MCBaIiBmaWxsPSJyZ2JhKDI1NSwgMjU1LCAyNTUsIDEpIiBzdHJva2U9IiM5OTk5OTkiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0wLjUgLTAuNSkiPjxzd2l0Y2g+PGZvcmVpZ25PYmplY3QgcG9pbnRlci1ldmVudHM9Im5vbmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHJlcXVpcmVkRmVhdHVyZXM9Imh0dHA6Ly93d3cudzMub3JnL1RSL1NWRzExL2ZlYXR1cmUjRXh0ZW5zaWJpbGl0eSIgc3R5bGU9Im92ZXJmbG93OiB2aXNpYmxlOyB0ZXh0LWFsaWduOiBsZWZ0OyI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiB1bnNhZmUgY2VudGVyOyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBmbGV4LWVuZDsgd2lkdGg6IDFweDsgaGVpZ2h0OiAxcHg7IHBhZGRpbmctdG9wOiA1NjVweDsgbWFyZ2luLWxlZnQ6IDY1NHB4OyI+PGRpdiBkYXRhLWRyYXdpby1jb2xvcnM9ImNvbG9yOiByZ2JhKDAsIDAsIDAsIDEpOyAiIHN0eWxlPSJib3gtc2l6aW5nOiBib3JkZXItYm94OyBmb250LXNpemU6IDBweDsgdGV4dC1hbGlnbjogcmlnaHQ7Ij48ZGl2IHN0eWxlPSJkaXNwbGF5OiBpbmxpbmUtYmxvY2s7IGZvbnQtc2l6ZTogMTJweDsgZm9udC1mYW1pbHk6IEhlbHZldGljYTsgY29sb3I6IHJnYigwLCAwLCAwKTsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsiPjxwcmUgc3R5bGU9InRleHQtYWxpZ246IGxlZnQgOyBib3JkZXI6IDBweCA7IG1hcmdpbi10b3A6IDBweCA7IG1hcmdpbi1ib3R0b206IDBweCI+Ly8g5pawIGRvbWFpbiDpnIDopoHpgJrov4fmiafooYzmjIflrprmlofku7bnmoTmlrnlvI/ov5vlhaU8L3ByZT48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPi8vIOatpOWkhOS4uumAmui/h+aJp+ihjCBoYWxfbnJmNTJfZGVmYXVsdF9leGVjIOaWh+S7tui9rOWPmOS4uiBoYWxfbnJmNTJfZGVmYXVsdCBkb21haW48L3ByZT48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPmFsbG93IGhhbF9ucmY1Ml9kZWZhdWx0IGhhbF9ucmY1Ml9kZWZhdWx0X2V4ZWM6ZmlsZSB7IGVudHJ5cG9pbnQgb3BlbiByZWFkIGV4ZWN1dGUgZ2V0YXR0ciBtYXAgfTs8YnIgLz48L3ByZT48L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iNjU0IiB5PSI1NjkiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJIZWx2ZXRpY2EiIGZvbnQtc2l6ZT0iMTJweCIgdGV4dC1hbmNob3I9ImVuZCI+Ly8g5pawIGRvbWFpbiDpnIDopoHpgJrov4fmiafooYzmjIflrprmlofku7bnmoTmlrnlvI/ov5vlhaUuLi48L3RleHQ+PC9zd2l0Y2g+PC9nPjxwYXRoIGQ9Ik0gNjY2IDYzMCBMIDY3NiA2MzUgTCA2NjYgNjQwIFoiIGZpbGw9InJnYmEoMjU1LCAyNTUsIDI1NSwgMSkiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5IiBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBjZW50ZXI7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGZsZXgtZW5kOyB3aWR0aDogMXB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDYzNXB4OyBtYXJnaW4tbGVmdDogNjU0cHg7Ij48ZGl2IGRhdGEtZHJhd2lvLWNvbG9ycz0iY29sb3I6IHJnYmEoMCwgMCwgMCwgMSk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiByaWdodDsiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyI+PHByZSBzdHlsZT0idGV4dC1hbGlnbjogbGVmdCA7IGJvcmRlcjogMHB4IDsgbWFyZ2luLXRvcDogMHB4IDsgbWFyZ2luLWJvdHRvbTogMHB4Ij4vLyDlhYHorrjmlrAgZG9tYWluIOWQkeWFtuiwg+eUqOiAheWPkemAgSBTSUdDSExEIOS/oeWPt+mHjzwvcHJlPjxwcmUgc3R5bGU9InRleHQtYWxpZ246IGxlZnQgOyBib3JkZXI6IDBweCA7IG1hcmdpbi10b3A6IDBweCA7IG1hcmdpbi1ib3R0b206IDBweCI+Ly8g5q2k5aSE5Li65YWB6K64IGhhbF9ucmY1Ml9kZWZhdWx0IOWQkSBpbml0IOWPkemAgSBzaWdjaGxkIOS/oeWPtzwvcHJlPjxwcmUgc3R5bGU9InRleHQtYWxpZ246IGxlZnQgOyBib3JkZXI6IDBweCA7IG1hcmdpbi10b3A6IDBweCA7IG1hcmdpbi1ib3R0b206IDBweCI+aWZlbHNlKGluaXQsIGBpbml0JywgYCcsIGBhbGxvdyBoYWxfbnJmNTJfZGVmYXVsdCBpbml0OnByb2Nlc3Mgc2lnY2hsZDsnKTxiciAvPjwvcHJlPjwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48dGV4dCB4PSI2NTQiIHk9IjYzOSIgZmlsbD0icmdiYSgwLCAwLCAwLCAxKSIgZm9udC1mYW1pbHk9IkhlbHZldGljYSIgZm9udC1zaXplPSIxMnB4IiB0ZXh0LWFuY2hvcj0iZW5kIj4vLyDlhYHorrjmlrAgZG9tYWluIOWQkeWFtuiwg+eUqOiAheWPkemAgSBTSUdDSExEIOS/oeWPt+mHjy4uLjwvdGV4dD48L3N3aXRjaD48L2c+PHBhdGggZD0iTSA2NjYgNzUwIEwgNjc2IDc1NSBMIDY2NiA3NjAgWiIgZmlsbD0icmdiYSgyNTUsIDI1NSwgMjU1LCAxKSIgc3Ryb2tlPSIjOTk5OTk5IiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48c3dpdGNoPjxmb3JlaWduT2JqZWN0IHBvaW50ZXItZXZlbnRzPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiByZXF1aXJlZEZlYXR1cmVzPSJodHRwOi8vd3d3LnczLm9yZy9UUi9TVkcxMS9mZWF0dXJlI0V4dGVuc2liaWxpdHkiIHN0eWxlPSJvdmVyZmxvdzogdmlzaWJsZTsgdGV4dC1hbGlnbjogbGVmdDsiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGNlbnRlcjsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgZmxleC1lbmQ7IHdpZHRoOiAxcHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogNzU1cHg7IG1hcmdpbi1sZWZ0OiA2NTRweDsiPjxkaXYgZGF0YS1kcmF3aW8tY29sb3JzPSJjb2xvcjogcmdiYSgwLCAwLCAwLCAxKTsgIiBzdHlsZT0iYm94LXNpemluZzogYm9yZGVyLWJveDsgZm9udC1zaXplOiAwcHg7IHRleHQtYWxpZ246IHJpZ2h0OyI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDEycHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiByZ2IoMCwgMCwgMCk7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7Ij48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPi8vIOS9v+iDvSBBVF9TRUNVUkXvvIzov5nkuKrot5/ov5vnqIvog73lipvnm7jlhbPvvIzlj6/ku6Xlj4LogIPvvJpodHRwczovL3d3dy5tYW43Lm9yZy9saW51eC9tYW4tcGFnZXMvbWFuMy9nZXRhdXh2YWwuMy5odG1sPC9wcmU+PHByZSBzdHlsZT0idGV4dC1hbGlnbjogbGVmdCA7IGJvcmRlcjogMHB4IDsgbWFyZ2luLXRvcDogMHB4IDsgbWFyZ2luLWJvdHRvbTogMHB4Ij4vLyDmraTlpITkuLrkuI3orrDlvZUgaW5pdCDorr/pl64gaGFsX25yZjUyX2RlZmF1bHQ6cHJvY2VzcyDml7bnmoQgbm9hdHNlY3VyZSDmk43kvZw8L3ByZT48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPmRvbnRhdWRpdCBpbml0IGhhbF9ucmY1Ml9kZWZhdWx0OnByb2Nlc3Mgbm9hdHNlY3VyZTs8L3ByZT48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPi8vIOWvueS6juS4iumdoui/neinhOeahOaTjeS9nO+8jOmcgOimgei/m+S4gOatpeWuoeaguO+8jDxmb250IGNvbG9yPSIjOTkwMDRkIj7ov5nmraXnmoTmtYHnqIvmiJHkuZ/kuI3lpKfmuIXmpZrvvIzlp5HkuJTlvZPov5nkuKTooYzmmK/miZPlvIAgQVRfU0VDVVJFIOeahOWKn+iDvTwvZm9udD48L3ByZT48cHJlIHN0eWxlPSJ0ZXh0LWFsaWduOiBsZWZ0IDsgYm9yZGVyOiAwcHggOyBtYXJnaW4tdG9wOiAwcHggOyBtYXJnaW4tYm90dG9tOiAwcHgiPmFsbG93IGluaXQgaGFsX25yZjUyX2RlZmF1bHQ6cHJvY2VzcyB7IHNpZ2luaCBybGltaXRpbmggfTs8YnIgLz48L3ByZT48L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PHRleHQgeD0iNjU0IiB5PSI3NTkiIGZpbGw9InJnYmEoMCwgMCwgMCwgMSkiIGZvbnQtZmFtaWx5PSJIZWx2ZXRpY2EiIGZvbnQtc2l6ZT0iMTJweCIgdGV4dC1hbmNob3I9ImVuZCI+Ly8g5L2/6IO9IEFUX1NFQ1VSRe+8jOi/meS4qui3n+i/m+eoi+iDveWKm+ebuOWFs++8jOWPr+S7peWPguiAg++8mmh0dHBzOi8vd3d3Lm1hbjcub3JnL2xpbnV4L21hbi1wYWdlcy9tYW4zL2dldGF1eHZhbC4zLmh0bWwuLi48L3RleHQ+PC9zd2l0Y2g+PC9nPjxwYXRoIGQ9Ik0gNjY2IDg1MCBMIDY3NiA4NTUgTCA2NjYgODYwIFoiIGZpbGw9InJnYmEoMjU1LCAyNTUsIDI1NSwgMSkiIHN0cm9rZT0iIzk5OTk5OSIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PHN3aXRjaD48Zm9yZWlnbk9iamVjdCBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgcmVxdWlyZWRGZWF0dXJlcz0iaHR0cDovL3d3dy53My5vcmcvVFIvU1ZHMTEvZmVhdHVyZSNFeHRlbnNpYmlsaXR5IiBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7Ij48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBjZW50ZXI7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGZsZXgtZW5kOyB3aWR0aDogMXB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDg1NXB4OyBtYXJnaW4tbGVmdDogNjU0cHg7Ij48ZGl2IGRhdGEtZHJhd2lvLWNvbG9ycz0iY29sb3I6IHJnYmEoMCwgMCwgMCwgMSk7ICIgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMHB4OyB0ZXh0LWFsaWduOiByaWdodDsiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxMnB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogcmdiKDAsIDAsIDApOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyI+PHByZSBzdHlsZT0idGV4dC1hbGlnbjogbGVmdCA7IGJvcmRlcjogMHB4IDsgbWFyZ2luLXRvcDogMHB4IDsgbWFyZ2luLWJvdHRvbTogMHB4Ij4vLyDmraPlvI/miafooYwgZG9tYWluIOi9rOWPmOeahOi/h+eoi++8jOS7jiBpbml0IOi9rOWIsCBoYWxfbnJmNTJfZGVmYXVsdDwvcHJlPjxwcmUgc3R5bGU9InRleHQtYWxpZ246IGxlZnQgOyBib3JkZXI6IDBweCA7IG1hcmdpbi10b3A6IDBweCA7IG1hcmdpbi1ib3R0b206IDBweCI+PGZvbnQgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6IHJnYigyNTUgLCAwICwgMTI4KSIgY29sb3I9IiNmZmZmZmYiPnR5cGVfdHJhbnNpdGlvbiBpbml0IGhhbF9ucmY1Ml9kZWZhdWx0X2V4ZWM6cHJvY2VzcyBoYWxfbnJmNTJfZGVmYXVsdDs8L2ZvbnQ+PGJyIC8+PC9wcmU+PC9kaXY+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0Pjx0ZXh0IHg9IjY1NCIgeT0iODU5IiBmaWxsPSJyZ2JhKDAsIDAsIDAsIDEpIiBmb250LWZhbWlseT0iSGVsdmV0aWNhIiBmb250LXNpemU9IjEycHgiIHRleHQtYW5jaG9yPSJlbmQiPi8vIOato+W8j+aJp+ihjCBkb21haW4g6L2s5Y+Y55qE6L+H56iL77yM5LuOIGluaXQg6L2s5YiwIGhhbF9ucmY1Ml9kZWZhdWx0Li4uPC90ZXh0Pjwvc3dpdGNoPjwvZz48L2c+PHN3aXRjaD48ZyByZXF1aXJlZEZlYXR1cmVzPSJodHRwOi8vd3d3LnczLm9yZy9UUi9TVkcxMS9mZWF0dXJlI0V4dGVuc2liaWxpdHkiLz48YSB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLC01KSIgeGxpbms6aHJlZj0iaHR0cHM6Ly93d3cuZGlhZ3JhbXMubmV0L2RvYy9mYXEvc3ZnLWV4cG9ydC10ZXh0LXByb2JsZW1zIiB0YXJnZXQ9Il9ibGFuayI+PHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMHB4IiB4PSI1MCUiIHk9IjEwMCUiPlZpZXdlciBkb2VzIG5vdCBzdXBwb3J0IGZ1bGwgU1ZHIDEuMTwvdGV4dD48L2E+PC9zd2l0Y2g+PC9zdmc+" style="cursor:pointer;max-width:100%;"onclick="(function(img){if(img.wnd!=null&&!img.wnd.closed){img.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&&evt.source==img.wnd){img.wnd.postMessage(decodeURIComponent(img.getAttribute('src')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);img.wnd=window.open('https://viewer.diagrams.net/?client=1&edit=_blank');}})(this);"/>
</pre>



Appendix
----------------------------------------------------------------------------------------------------

### 快速解决Android中的selinux权限问题
```
type=1400 audit(32.939:25): avc: denied { open } for pid=2592 comm="chmod" path="/dev/block/mmcblk0p25" dev="tmpfs" ino=6494 scontext=u:r:init_shell:s0 tcontext=u:object_r:block_device:s0 tclass=blk_file permissive=1
```
整理成如下表
```
denied { open }             u:r:init_shell:s0            u:object_r:block_device:s0       tclass=blk_file
             A              B                            C                                D
             B              C                            D                                A
```
变成allow规则如下
```
allow init_shell  block_device:blk_file open;
```



Reference
----------------------------------------------------------------------------------------------------
* https://www.cnblogs.com/shell812/p/6379321.html
* http://www.cnblogs.com/shell812/p/6379370.html
