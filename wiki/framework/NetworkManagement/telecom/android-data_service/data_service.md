/'
![pic](neon-init_wifi_service.png)
'/

```
@startuml

autonumber
'hide footbox

title "Connectivity Service Network default interface"
legend top left
This diagram describes the initial process of wifi service
endlegend

actor System

box "system_server" #white
participant ConnectivityService
participant NetworkControllerImpl
participant MobileSignalController
participant BitSet
participant mCurrentState.isDefault #YellowGreen
end box

rnote right ConnectivityService:<&tag> D ConnectivityService: sendStickyBroadcast: action=android.net.conn.CONNECTIVITY_CHANGE

ConnectivityService->NetworkControllerImpl:mContext.sendStickyBroadcastAsUser\n(ConnectivityManager.CONNECTIVITY_ACTION)
NetworkControllerImpl->NetworkControllerImpl:onReceive()
activate NetworkControllerImpl
NetworkControllerImpl->NetworkControllerImpl:updateConnectivity()\nline:411
activate NetworkControllerImpl
NetworkControllerImpl->NetworkControllerImpl:pushConnectivityToSignals()\nline672
activate NetworkControllerImpl
NetworkControllerImpl -> MobileSignalController : updateConnectivity()
activate MobileSignalController

MobileSignalController ->BitSet:connectedTransports\n.get(mTransportType)
BitSet -> mCurrentState.isDefault:mCurrentState.isDefault=\nconnectedTransports.get(mTransportType);
note left
<&info> isDefault comes from the mTransportType bit of connectedTransports
and the connectedTransports equals mConnectedTransports of MobileSignalController
it depend on m<b>ConnectivityManager.getDefaultNetworkCapabilitiesForUser</b>(mCurrentUserId)
end note

MobileSignalController->MobileSignalController:notifyListenersIfNecessary()
NetworkControllerImpl<--MobileSignalController
deactivate MobileSignalController
deactivate NetworkControllerImpl








@enduml

```