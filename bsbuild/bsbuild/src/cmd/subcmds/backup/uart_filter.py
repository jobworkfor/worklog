#!/usr/bin/python
# -*-coding: utf-8 -*-

'''
pyserial 实现串口log过滤
-----------------------
经常遇到下位机平台大量输出log，导致快速刷屏，看不清自己所关注的信息
写了一个脚本，可以设置white list 和black list，根据关键字，实现过滤log，清爽屏幕的功能

说明：
    1. 是否过滤，在def filter_policy(white_list = None,black_list=None,line=None)定义，默认的逻辑是，所有白名单里面的log，都输出，在黑名单中但是不在白名单中的log不输出，既不在白名单，也不在黑名单中的log默认输出
    2. 需要根据下位机实际情况配置com 口，波特率等信息，可以查看code 注释config 位置
'''

import serial
import serial.tools.list_ports
import threading
import binascii
import time
from datetime import datetime

# config
baunRate = 115200
is_exit = False
data_bytes = bytearray()

# 列出所有当前的com口
port_list = list(serial.tools.list_ports.comports())
port_list_name = []


class SerialPort:
    def __init__(self, port, buand):
        self.port = serial.Serial(port, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.close()

    def send_data(self):
        # 此处可以发送命令，暂未实现
        self.port.write("hello")

    def read_data(self):
        global is_exit
        global data_bytes
        while not is_exit:
            count = self.port.inWaiting()
            if count > 0:
                rec_str = self.port.read(count)
                data_bytes = data_bytes + rec_str
                # print("receive:",rec_str.decode())


def show_all_com():
    if len(port_list) <= 0:
        print("the serial port can't find!")
    else:
        for itms in port_list:
            port_list_name.append(itms.device)


def filter_policy(white_list=None, black_list=None, line=None):
    if line == None:
        return False

    if not white_list == None:
        for each in white_list:
            if each in line:
                return True

    if not black_list == None:
        for each in black_list:
            if each in line:
                return False
    # default return True
    return True


if __name__ == '__main__':
    print("1.list all com")
    show_all_com()
    print(port_list_name)

    print("2.open ", port_list_name[0])
    # config other com , eg: serialPort_r = "COM5"
    serialPort_r = port_list_name[0]
    mSerial_r = SerialPort(serialPort_r, baunRate)

    print("3.start thread: read from thread")
    t2 = threading.Thread(target=mSerial_r.read_data)
    t2.setDaemon(True)
    t2.start()

    print("6.init white list and black list")
    # config your filter key words, eg: b_list.append("hello")"
    b_list = []
    b_list.append("app")

    w_list = []
    w_list.append("bt")

    i = 0
    # 标记一行字符的起始索引值
    line_head = 0
    while not is_exit:
        data_len = len(data_bytes)
        line = []
        while (i < data_len - 1):
            # print(data_bytes[i])
            if (data_bytes[i] == 0x0a):
                # 换行
                line = data_bytes[line_head:i].decode()
                line_head = i + 1
                if filter_policy(white_list=w_list, black_list=b_list, line=line):
                    print(line)
            i += 1
