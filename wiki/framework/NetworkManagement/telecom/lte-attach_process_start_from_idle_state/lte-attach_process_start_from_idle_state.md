# LTE手机初始空闲接入流程 

![overview](res/lte-attach_process_start_from_idle_state-overview.jpg)


1. UE根据优先级顺序自主选择PLMN

 UE AS（Access Stratum）初始小区查寻（测量小区的信号强度，将可用的PLMN标识上报给NAS，从SIB1中读取了所有PLMN，并且它向UE NAS（Non Access Stratum）报告，UE NAS将根据这种被预定义的优先级来选择其中的一个。

2. 频率选择

 如果UE能保存上次关机时的频点信息，则开机后可能会先在上次驻留的小区上尝试驻留；如果没有先验信息，则很可能要全频段搜索，发现信号较强的频点，再去尝试驻留。

3. 小区搜索（获得PCI和下行同步）

 在上一步确定的中心频点周围收PSS（primary synchronization signal）和SSS（secondary synchronization signal），这两个信号和系统带宽没有限制，可以直接检测并接收到，据此可以得到小区ID。

4. 获取系统消息

 完成小区搜索需要接收SIB，即UE接收承载在PDSCH上的BCCH信息。

5. 小区选择

 Cell selection主要是为了选择一个合适的cell并将该手机驻扎到该小区中。

6. 初始附着（PLMN注册）

 手机完成PLMN和Cell选择后，会发起位置注册流程（location registration），将手机的位置报告给移动网络。