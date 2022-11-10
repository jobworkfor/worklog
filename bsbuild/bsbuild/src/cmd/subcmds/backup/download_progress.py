#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import requests
import sys


class DownloadProgress():
    def main(self):
        link = "http://repo.pt.miui.com/content/repositories/releases/com/xiaomi/midrop_global/1.28.24/midrop_global-1.28.24-universal.apk"
        file_name = "midrop_global-1.28.24-universal.apk"
        with open(file_name, "wb") as f:
            print("Downloading %s" % file_name)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        return
