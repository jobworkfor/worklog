#!/usr/bin/env python
# _*_coding:utf-8_*_

import os
import time
import re

from core.cmd.command import Command


class Tombstone(Command):
    def __init__(self):
        return

    def init(self, args):
        self.locateDir = args[0]
        self.filename = args[1]
        self.timestamp = args[2]
        self.pid = ''
        self.pname = ''
        self.signal = ''

    def parse(self):
        file = open(os.path.join(self.locateDir, self.filename), 'rb')
        lines = file.readlines()
        for n in range(0, min(30, len(lines))):
            try:
                l = lines[n]
                matchObj = re.match(r'Timestamp: (.*)\+', l)
                if matchObj:
                    self.timestamp = matchObj.group(1)
                    continue
                matchObj = re.match(r'^pid: (.*?),.*>>> (.*) <<<', l)
                if matchObj:
                    self.pid = matchObj.group(1)
                    self.pname = matchObj.group(2)
                    continue

                matchObj = re.match(r'^signal (.*?) ', l)
                if matchObj:
                    self.signal = matchObj.group(1)
                    continue
            except Exception as e:
                print("Error:", n, self.filename)
        pass

    def rename(self):
        opath = os.path.join(self.locateDir, self.filename)
        # tombstone_00 2019-11-08 13'02'21_sig35_com.pingan.lifecircle@4472
        tname = ""
        if self.escape(self.timestamp) != '':
            tname += self.escape(self.timestamp)

        if self.escape(self.signal) != '':
            tname += "sig" + self.escape(self.signal)

        if self.escape(self.pname) != '':
            tname += self.escape(self.pname)

        if self.escape(self.pid) != '':
            tname += "@" + self.escape(self.pid)

        tname += "." + self.filename
        # tname = "%s %s_sig%s_%s@%s" % (self.filename, self.escape(self.timestamp), self.signal, self.escape(self.pname), self.pid)
        tpath = os.path.join(self.locateDir, tname)
        print("-> %s" % tpath)
        os.rename(opath, tpath)
        pass

    def escape(self, str):
        return str.replace(':', '\'').replace('/', '!')

    # ------------------------ program start ------------------------
    def main():
        current_dir = os.getcwd()
        i = 0
        ts = 0
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                matchObj = re.match(r'.*?([0-9]*)\..*', str(file))
                if matchObj:
                    if matchObj.group(1) == '':
                        continue
                    else:
                        ts = matchObj.group(1)
                        ts = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(ts) / 1000))

                tombstone = Tombstone(current_dir, file, ts)
                tombstone.parse()
                tombstone.rename()
                i += 1

        print("done, renamed ", i, " files.")

# if __name__ == '__main__':
#     main()
#     print("Will exit after 3 seconds...")
#     time.sleep(5)
