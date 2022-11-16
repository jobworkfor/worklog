# Qualcomm Training Day 1

## SS

```
document: 80-NV772-2_A
```

### Hold Call
* "Trans id 1" 来区分call
空口log mask： 0x713A

### multi part call (page 29)


### USSD
* 3GPP TS 9.02

Check point
* USSD String
* 网络端没有注册服务 code 10
* 发送的值有问题 code 36

## SMS

```
document: 80-P2102-1_A
```

NAS层SMS

### SMS分层
1. 中继层(MM)
2. CM(protocol defined CallManager)

### 处理流程
Page 6
MT, MO类似

CP-DATA, CP-ACK, 
TWO Timers -- TC1(20s), TR1(40s)

* OTA Errors(page 9)

* keywords -- "wmsmsg.c"

* Memory Full issue: WMS_TP_CAUSE_.._FULL
log mask 0x713A


## PLMN/RAT Selection

```
document: 80-N9533-2 D
```

找网的两个方面
1. PLMN ID
2. RAT

manual and auto select

3GPP TS 23.122






























































































































































































