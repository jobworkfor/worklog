#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil


class SyncDecupledAppFolder():
    def main(self):
        from_dir = os.path.join("/home/bob.shen/work", "decoupled_apps")
        to_dir = os.path.join("/home/bob.shen/work/sm8250_rebase/miui/prebuilts", "decoupled_apps")

        skip_modules = [
            "xxx",
        ]

        alllist = os.listdir(from_dir)
        alllist.sort()

        count = 0;
        for f in alllist:
            if f in skip_modules:
                print("skip module %s" % f)
                continue

            t_dir = os.path.join(to_dir, f)
            if os.path.exists(t_dir):
                count += 1
                print(f)

                # remove all files except Android.mk in target folder
                for sub_f in os.listdir(t_dir):
                    if sub_f == "Android.mk":
                        continue
                    else:
                        print("    " + sub_f)
                        path = os.path.join(to_dir, f, sub_f)
                        if os.path.isdir(path):
                            shutil.rmtree(path)
                        elif os.path.isfile(path):
                            os.remove(path)

                # copy all files except Android.mk here from source folder
                s_dir = os.path.join(from_dir, f)
                for sub_f in os.listdir(s_dir):
                    if sub_f == "Android.mk":
                        continue
                    else:
                        s_path = os.path.join(from_dir, f, sub_f)
                        t_path = os.path.join(to_dir, f, sub_f)
                        print("cp %s %s" % (s_path, t_path))
                        if os.path.isdir(s_path):
                            shutil.copytree(s_path, t_path)
                        elif os.path.isfile(s_path):
                            shutil.copyfile(s_path, t_path)

        print(count)
