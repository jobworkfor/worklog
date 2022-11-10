#!/usr/bin/env python3
# _*_coding:utf-8_*_

import os
import re
import io

from src.util.file_system_helper import FileSystemHelper
from core.cmd.command import Command


class Logcat(Command):
    def init(self, args):
        self.locateDir = args[0]
        self.filename = args[1]
        self.startTime = ''
        self.endTime = ''

    def parse(self):
        if not str(self.filename).startswith("logcat"):
            return

        try:
            f = io.open(os.path.join(self.locateDir, self.filename), mode="r", encoding="utf-8")
            for n in range(0, 5):
                l = f.readline()
                # print("sl:", l)
                matchObj = re.match(r'^(.*)\.[\d]*( +[\d]+ +[\d]+ ).*', l)
                if matchObj:
                    self.startTime = matchObj.group(1)
                    # print("self.startTime:", self.startTime)
                    break
        except Exception as e:
            print("Error:", str(e))

        f = io.open(os.path.join(self.locateDir, self.filename), mode="r", encoding="utf-8")
        offset = 100  # 设置偏移量
        while offset < 20480:
            try:
                f.seek(0, os.SEEK_END)  # seek to end of file; f.seek(0, 2) is legal
                f.seek(f.tell() - offset, os.SEEK_SET)  # go backwards off bytes
                lines = f.readlines()  # 读取文件指针范围内所有行
            except Exception as e:
                print("Error:", str(e))

            # print("lines:", len(lines))
            if len(lines) >= 5:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                for n in range(1, 5):
                    j = (0 - n)
                    l = lines[j]
                    # print("el:", l)
                    matchObj = re.match(r'^(.*)\.[\d]*( +[\d]+ +[\d]+ ).*', l)
                    if matchObj:
                        self.endTime = matchObj.group(1)
                        # print("self.endTime:", self.endTime)
                        break
                break
            # double offset to read more bytes
            offset *= 2
        pass

    def rename(self):
        opath = os.path.join(self.locateDir, self.filename)

        tname = ""
        if self.escape(self.startTime) != '':
            tname += self.escape(self.startTime)

        if self.escape(self.endTime) != '':
            tname += "@" + self.escape(self.endTime)

        tname += "." + self.filename

        if self.endTime == '' and self.startTime == '':
            return

        tpath = os.path.join(self.locateDir, tname)
        print("-> %s" % tpath)
        Logcat.renamedFiles += 1
        os.rename(opath, tpath)
        pass

    def escape(self, str):
        return str.replace(':', '\'').replace('/', '!')

    def dump(self):
        print("done, renamed ", Logcat.renamedFiles, " files.")

    # ------------------------ program start ------------------------
    def main(argv):
        current_dir = os.getcwd()
        if len(argv) > 0:
            current_dir = argv[0]

        if FileSystemHelper.exist(current_dir):
            Logcat.renamedFiles = 0
            for f in os.listdir(current_dir):
                logcat = Logcat(current_dir, f)
                logcat.parse()
                logcat.rename()
            logcat.dump()
