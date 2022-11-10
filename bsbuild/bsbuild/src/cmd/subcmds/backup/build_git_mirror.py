#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import subprocess
import time
import sys

FNULL = open(os.devnull, 'w')


class Config:
    destDir = ''
    destHeadsName = ''
    forcePush = False
    # git symbolic-ref HEAD refs/heads/mybranch


class ShellCmd:
    runTimes = 0

    def __init__(self, cmd):
        self.stdoutLines = []
        self.cmd = cmd
        ShellCmd.runTimes += 1

    def execute(self):
        print ShellCmd.runTimes, "ShellCmd> ", self.cmd
        child = subprocess.Popen(self.cmd, shell=True, stderr=subprocess.STDOUT, close_fds=True)
        retcde = child.wait()
        if retcde != 0:
            print "FAILED:", self.cmd, "[$?=%s]" % retcde
        return retcde == 0

    def run(self):
        print ShellCmd.runTimes, "ShellCmd> ", self.cmd
        child = subprocess.Popen(self.cmd,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 close_fds=True)
        retcde = child.wait()
        self.stdoutLines = child.stdout.readlines()
        if retcde != 0:
            print "FAILED: " + self.cmd + "[" , retcde , "]"

        return retcde == 0

    def getStdout(self):
        return self.stdoutLines


def main():
    print sys.argv

    if len(sys.argv) < 3:
        print "ERROR FORMAT, example: python %s %s %s %s" % (
            sys.argv[0], "<TO_DIR>", "<HEADS_NAME>", "[force push]"
        )
        sys.exit(1)

    Config.destDir = sys.argv[1]
    if not os.path.exists(Config.destDir):
        print "." * 25, Config.destDir, "not exist", "." * 25
        return

    Config.destHeadsName = sys.argv[2]

    if len(sys.argv) > 3:
        Config.forcePush = sys.argv[3].lower() == "true"

    print  # ---------------------- start ----------------------

    # remote.grease.projectname=AndroidQ/platform/frameworks/base
    # get path in mirror repo
    git_name = ""
    path_in_mirror_repo = ""
    path_info = ""
    cmd = ShellCmd("git config  --get-regexp remote.*.projectname")
    if cmd.run():
        path_info = cmd.getStdout()[0].split()[1];
    else:
        path_info = raw_input("please input relative git mirror path in (%s/)：" % Config.destDir);

    path_info = os.path.split(path_info)
    path_in_mirror_repo = path_info[0]
    git_name = path_info[1] + ".git"
    if path_in_mirror_repo == "" or git_name == "":
        print "." * 25, "failed get mirror path info.", "." * 25
        return

    # mi@mi-PowerEdge-R630:~/code/mi9_q/frameworks/base$ mkdir -p /home/mi/mirror/mi9_mirror/AndroidQ/platform/frameworks/
    to_dir = Config.destDir + "/" + path_in_mirror_repo
    cmd = ShellCmd("mkdir -p " + to_dir)
    cmd.execute()

    # mi@mi-PowerEdge-R630:~/code/mi9_q/frameworks/base$ git init --bare /home/mi/mirror/mi9_mirror/AndroidQ/platform/frameworks/base.git
    dest_git_path = Config.destDir + "/" + path_in_mirror_repo + "/" + git_name
    if os.path.exists(dest_git_path):
        if not Config.forcePush:
            print "." * 25, dest_git_path, "inited already", "." * 25
            return
        else:
            print "*** force push ***", dest_git_path, Config.destHeadsName
    else:
        cmd = ShellCmd("git init --bare " + dest_git_path)
        cmd.execute()

    # check if shallow git
    # git rev-parse --is-shallow-repository
    cmd = ShellCmd("git rev-parse --is-shallow-repository")
    if cmd.run():
        if "true" == cmd.getStdout()[0].strip():
            cmd = ShellCmd("git rebase --root && git commit --amend --no-edit")
            cmd.execute()

    # mi@mi-PowerEdge-R630:~/code/mi9_q/frameworks/base$ git push -f /home/mi/mirror/mi9_mirror/AndroidQ/platform/frameworks/base.git refs/remotes/grease/*:refs/heads/*
    cmd = ShellCmd("git push -f " + dest_git_path + " HEAD:refs/heads/" + Config.destHeadsName)
    cmd.execute()

    print "-" * 25, "done", "-" * 25
    print


if __name__ == "__main__":
    main()
