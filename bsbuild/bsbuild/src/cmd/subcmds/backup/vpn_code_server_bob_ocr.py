#!/usr/bin/python3
# coding:utf-8
import socket
import os
import base64
import time
import datetime
import pytesseract
from PIL import Image

from multiprocessing import Process

CFG_PORT = 8000
CFG_USR_NAME = 'p-shensibo'
CFG_PASSWORD = 'Aawhatever8'
CFG_ADB_SNO = '6a6b3891'


def getFileAccessTime(path):
    """getFileAccessTime return ms"""
    return os.path.getatime(path)


def getDynamicCode(screencap_path):
    img = Image.open(screencap_path).convert('L')
    rect = (186, 1336, 888, 1450)
    img = img.crop(rect)
    pixels = img.load()

    width = img.size[0]
    height = img.size[1]
    for x in range(width):
        for y in range(height):
            if (x > 90 and x < 125) \
                    or (x > 210 and x < 245) \
                    or (x > 337 and x < 380) \
                    or (x > 460 and x < 500) \
                    or (x > 580 and x < 620) \
                    :
                pixels[x, y] = 255
                continue

            if pixels[x, y] == 255:
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255
    # img = img.resize((width >> 2, height >> 2), Image.ANTIALIAS)
    code = pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    print("code", code)
    return code


def tryCaptureScreenCap(screencap_path):
    timestamp = time.time()
    fileAccessTime = getFileAccessTime(screencap_path)
    if timestamp - fileAccessTime < 3:
        print("skip capture again in", (timestamp - fileAccessTime), "s")
        return

    try:
        os.system("adb -s %s shell screencap -p /sdcard/screencap.png" % (CFG_ADB_SNO))
        os.system("adb -s %s pull /sdcard/screencap.png %s" % (CFG_ADB_SNO, screencap_path))
    except:
        print('error')
    return


def handle_client(client_socket, screencap_path):
    """
    处理客户端请求
    """
    request_data = client_socket.recv(1024)
    # print("request data:", request_data)
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"

    tryCaptureScreenCap(screencap_path)

    with open(screencap_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        imageData = base64_data.decode()

    # data_uri = open('/home/baseline/bin/screencap.png', 'rb').read().encode('base64').replace('\n', '')
    dynCode = getDynamicCode(screencap_path)
    response_body = '''
    <html lang="zh-CN">
    <head>
    <meta charset="utf-8">
    <title>VPN/0.1</title>
    </head>
    <body>
    <h1>VPN Dynamic Code:</h1>
    <pre> 
    user name: {0}
    password : {1}{2}
    </pre>
    <img height=450px src="data:image/png;base64,{3}" />
    <pre>
    更新内容：
    2021年8月18日：支持OCR识别动态码（OCR powered by tesseract-ocr-w64-setup-v5.0.0-alpha.20210811）
    </pre>
    </body>
    </html>
    '''.format(CFG_USR_NAME, CFG_PASSWORD, dynCode, imageData)

    response = response_start_line + response_headers + "\r\n" + response_body

    # 向客户端返回响应数据
    client_socket.send(bytes(response, "utf-8"))

    # 关闭客户端连接
    client_socket.close()


if __name__ == "__main__":
    workspace_dir = os.path.split(os.path.realpath(__file__))[0]
    screencap_path = os.path.join(workspace_dir, "screencap_%s.png" % CFG_USR_NAME)
    screencap_path = "D:\\20210818\\screencap_p-shensibo.png"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", CFG_PORT))
    server_socket.listen(128)
    print("Server Started :%d" % CFG_PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s] connected %s." % (client_address[0], client_address[1], server_socket))
        # handle_client(client_socket, screencap_path)
        handle_client_process = Process(target=handle_client, args=(client_socket, screencap_path))
        handle_client_process.start()
        client_socket.close()
