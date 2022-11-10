#!/usr/bin/env python3
# _*_coding:utf-8_*_

import os
import time
import re

from core.cmd.command import Command


class Utc2time(Command):
    def file_name(file_dir):
        i = 0
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                matchObj = re.match(r'([\d].*-[\d].*-[\d].* [\d][\d]\'[\d][\d]\'[\d][\d]__)', file, re.M | re.I)
                if matchObj:
                    print("already had time info, skipped.")
                    continue

                matchObj = re.match(r'.*@([\d]*).*', file, re.M | re.I)
                if matchObj:
                    utc_timestamp = int(matchObj.group(1)) / 1000
                    timeStr = time.strftime("%Y-%m-%d %H'%M'%S", time.localtime(utc_timestamp))
                    os.rename(file, timeStr + "__" + file)
                    i += 1
        print("done, renamed ", i, " files.")

    def convert(self):
        file_name(os.getcwd())

        print("Will exit after 3 seconds...")
        time.sleep(3)
