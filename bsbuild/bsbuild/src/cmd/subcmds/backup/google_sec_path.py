#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import argparse

from core.cmd.command import Command

BANNER_STR = "google_sec_path.py ver 0.1"

bundle = {
    "patch_dir": "",
    "debug": "",
}


class GoogleSecPath(Command):
    def parse_arg(argv):
        parser = argparse.ArgumentParser(description=BANNER_STR)
        parser.add_argument("patch_dir", nargs='?', help="specify your patch root directory.")
        parser.add_argument('--debug', action='store_true')

        args = parser.parse_args(argv)
        bundle["patch_dir"] = args.patch_dir
        bundle["debug"] = args.debug

    def main():
        if len(sys.argv) <= 1:
            parse_arg(["--help"])
            exit(0)

        parse_arg(sys.argv[1:])

        debug = bundle["debug"]

        if not os.path.isdir(bundle["patch_dir"]):
            print("invalid patch_dir directory!")
            exit(0)

        patch_dir = sys.argv[1]
        print('================================')
        print(BANNER_STR)
        print('================================', '\n')

        count = 0;
        cur_dir = os.getcwd()
        patches = []

        for parent, dirnames, filenames in os.walk(patch_dir):
            tmp = []
            for filename in filenames:
                if (filename.endswith(".patch")):
                    count += 1
                    tmp.append(os.path.join(parent, filename))
            tmp.sort()
            patches.extend(tmp)

        i = 0
        length = len(patches)
        unpatched = []
        for p in patches:
            i += 1
            git_dir = os.path.dirname(p).replace(patch_dir + 'platform/', '')
            if not os.path.isdir(git_dir):
                print(i, "*** skiping invalid patch: ", p)
                unpatched.append(p)
                continue

            patch_path = os.path.join(cur_dir, p)
            print('[' + str(i) + '/' + str(length) + ']', patch_path)

            os.chdir(git_dir)
            os.system("git am " + patch_path)
            os.system("git status")

            os.chdir(cur_dir)

            text = sys.stdin.readline().strip()

        print("\n\nunpatched file(s) are:")
        for u in unpatched:
            print(u)
