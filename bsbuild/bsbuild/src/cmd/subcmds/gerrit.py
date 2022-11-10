#!/usr/bin/env python
# coding:utf-8

import re

from src.util.helper_log import Log
from src.context import Context
from src.core.cmd.command import Command

_ = (Log)


class Gerrit(Command):
    ANDROID_CODE_FLAG_PATH = 'bionic'
    KEY_PROJECT = 'project'
    KEY_NUMBER = 'number'
    KEY_CURRENT_PATCHSET = 'currentPatchSet'

    def __init__(self):
        self.mContext = Context.instance();
        self.mHelperDelegate = self.mContext.getHelperDelegate()
        usage = "usage: Gerrit [options] arg1 arg2"
        self.mArgParser = self.mHelperDelegate.newArgParserHelper(usage=usage)
        self.mArgs = []

        self.mFsHelper = self.mHelperDelegate.getFileSystemHelper()
        self.mGerritGitNamePrefixLen = 0
        return

    def init(self):
        self.mArgParser.add_argument("-b", "--branch", dest="branch", help="what remote branch want to push")
        self.mArgParser.add_argument("-r", "--reviewer", dest="reviewer", help="reivew email address", default="")
        self.mArgParser.add_argument("-d", "--drafts", dest="drafts", action="store_true", help="push to gerrit as drafts", default=False)
        self.mArgParser.add_argument("-m", "--merge", dest="mergeUriList", nargs='+', help="urls for merging")
        self.mArgParser.add_argument("-t", "--type", dest="type", choices=['commit', 'merge'], help="action type", default="commit")
        return

    def execute(self, args):
        (args, unknown) = self.mArgParser.parse_known_args(args)
        type = self.mArgParser.getValue("type")
        branch = self.mArgParser.getValue("branch")
        reviewer = self.mArgParser.getValue("reviewer").strip()
        drafts = self.mArgParser.getValue("drafts")
        mergeUriList = self.mArgParser.getValue("mergeUriList")

        if type == 'commit':
            self._commitPath(branch, reviewer, drafts)
        elif type == 'merge':
            self._mergePatch(mergeUriList);
        return 0

    def _commitPath(self, branch, reviewer, drafts):
        context = self.mContext
        fsHelper = self.mFsHelper
        terminal = context.getTerminal()

        # get push hosts from git remote -v
        remotePushServerList = []

        def onStdoutListener(line):
            nonlocal remotePushServerList

            parten = re.compile('.*\t(.*) \(push\)')
            m = parten.match(line)
            if m:
                remotePushServerList.append(m.groups()[0])
            return

        cmd = 'git remote -v'
        ret = terminal.runCmd(cmd, stdoutListner=onStdoutListener)
        if ret != 0:
            Log.e("Failed to run", cmd)
            return None

        remote = remotePushServerList[0]

        # check if remote hosts more than one, let user choose one if it's true
        serverNum = len(remotePushServerList)
        if serverNum > 1:
            for i in range(0, serverNum):
                Log.v("[%2s]" % i, remotePushServerList[i])
            Log.v("which remote you want? please input [%s - %s] or exit? " % (1, serverNum))
            choice = input()
            try:
                index = int(choice)
            except ValueError as e:
                Log.e("exit", e)
                return 1

            remote = remotePushServerList[index]
            Log.v("your choice remote [%s]" % (remote))

        # try get branch info
        if branch is None:
            logNum = 5
            hasCommit = False
            branchList = []
            for i in range(0, 9):
                cmd = 'git log -n %d --pretty=%%d' % logNum

                def onStdoutListener(line):
                    nonlocal branch
                    nonlocal hasCommit
                    nonlocal branchList

                    if len(line) > 0:
                        if not hasCommit and '(HEAD)' == line.strip():
                            hasCommit = True
                            return

                        if not hasCommit:
                            return

                        branchListStr = line[1:-1]
                        if ',' in branchListStr:
                            branchList = branchListStr.split(',')
                        else:
                            branchList.append(branchListStr)
                    return

                ret = terminal.runCmd(cmd, stdoutListner=onStdoutListener)
                if ret != 0:
                    Log.e("Failed to run", cmd)
                    return None
                if not hasCommit:
                    Log.w("Has no commit yet.")
                    return
                if len(branchList) > 0:
                    branch = branchList[0]
                    break
                logNum *= 2

            brNum = len(branchList)
            if brNum > 1:
                for i in range(1, brNum + 1):
                    Log.v("[%2s]" % i, branchList[i - 1].strip())
                Log.v("which branch you want?")
                choice = input()
                try:
                    index = int(choice) - 1
                except ValueError as e:
                    Log.e("exit", e)
                    return 1

                branch = branchList[index]
                Log.v("your choice branch [%s]" % (branch))

        if branch is None:
            Log.e('Failed: Can not find branch info')
            return

        if '/' in branch:
            list = branch.split('/')
            branch = list.pop()

        if drafts:
            cmd = "git push %s HEAD:refs/drafts/%s --no-thin" % (remote, branch)

        if reviewer:
            cmd += "%%r=%s" % (reviewer)

        cmd = "git push %s HEAD:refs/for/%s --no-thin" % (remote, branch)
        ret = terminal.runCmd(cmd, stdoutListner=onStdoutListener)
        if ret != 0:
            Log.e("Failed to run", cmd)
            return None
        return

    def _mergePatch(self, uriList):
        context = self.mContext
        fsHelper = self.mFsHelper

        # get result of repo list
        repoListDict = self._getRepoListDict(context)
        if repoListDict is None:
            return

        # get host name and ssh port
        (host, port) = self._getHost(context)
        if host is None:
            return

        # set self.mGerritGitNamePrefixLen
        self.mGerritGitNamePrefixLen = self._getGerritGitNamePrefixLen(context, host, port, repoListDict)
        Log.d("Gerrit git name prefix length:", self.mGerritGitNamePrefixLen)

        sucess = 0
        failedUris = []
        # process each uri
        for uri in uriList:
            Log.d("processing uri:", uri)
            failedUris.append(uri)

            while uri.endswith('\/'):
                uri = uri[:-1]

            # parse change number
            # https://gerrit-review.googlesource.com/Documentation/intro-user.html
            # A change ref has the format refs/changes/X/Y/Z where X is the last two digits of the change number,
            # Y is the entire change number, and Z is the patch set. For example, if the change number is 263270,
            # the ref would be refs/changes/70/263270/2 for the second patch set.
            changeNo = self._getChangeNumbers(uri)
            if changeNo == -1:
                Log.e('can not parse uri:', uri)
                continue

            # get project of this uri
            fetchCmdList = self._getFetchInfo(context, host, port, changeNo, repoListDict)
            if fetchCmdList is None:
                Log.e("can not get fetch cmd")
                continue

            # pick patch, continue if any error
            try:
                for cmd in fetchCmdList:
                    ret = context.getTerminal().runCmd(cmd)
                    if ret != 0:
                        Log.e("Failed to run", cmd)
                        raise Exception()
            except Exception:
                continue

            failedUris.pop()
            sucess += 1

        failedNumber = len(uriList) - sucess
        Log.v('Sucess: %d, Failed: %d' % (sucess, failedNumber))
        if failedNumber > 0:
            Log.e("Failed:")
            for uri in failedUris:
                Log.e("   ", uri)
        return

    def _getRepoListDict(self, context):
        dict = {}
        resultOk = False

        def onStdoutListener(line):
            nonlocal dict
            nonlocal resultOk
            kv = line.split(':')
            gitName = kv[1].strip()
            path = kv[0].strip()
            if Gerrit.ANDROID_CODE_FLAG_PATH == path:
                resultOk = True
                # we need get gitName of ANDROID_CODE_FLAG_PATH to decide self.mGerritGitNamePrefixLen
                dict[Gerrit.ANDROID_CODE_FLAG_PATH] = gitName
            dict[gitName] = path
            return

        cmd = 'repo list'
        ret = context.getTerminal().runCmd(cmd, stdoutListner=onStdoutListener)
        if ret != 0 or not resultOk:
            Log.e("Failed to run", cmd)
            return None
        return dict

    def _getHost(self, context):
        host = None
        port = -1

        def onStdoutListener(line):
            nonlocal host
            nonlocal port
            parten = re.compile('.*ssh:\/\/(.*):(\d*)\/.* \(push\)')
            m = parten.match(line)
            if m:
                host = m.groups()[0]
                port = m.groups()[1]
            return

        cmd = 'git -C .repo/manifests remote -v'
        ret = context.getTerminal().runCmd(cmd, stdoutListner=onStdoutListener)
        if ret != 0:
            Log.e("Failed to run", cmd)
            return (None, -1)
        return (host, port)

    def _getGerritGitNamePrefixLen(self, context, host, port, repoListDict):
        gerritGitName = None

        def onStdoutListener(line):
            nonlocal gerritGitName
            gerritGitName = line.strip()
            return

        cmd = 'ssh -p %s %s gerrit ls-projects -n 1 --match /%s' % (port, host, Gerrit.ANDROID_CODE_FLAG_PATH)
        ret = context.getTerminal().runCmd(cmd, stdoutListner=onStdoutListener)
        if ret != 0:
            Log.e("Failed to run", cmd)
            return 0

        repoListGitName = repoListDict[Gerrit.ANDROID_CODE_FLAG_PATH]
        prefix = gerritGitName[:-len(repoListGitName)]
        return len(prefix)

    def _getChangeNumbers(self, uri):
        changeNo = None
        parten = re.compile('http:\/\/(.*)\/(.*)')
        m = parten.match(uri)
        if m:
            changeNo = m.groups()[1]
        return changeNo

    def _getFetchInfo(self, context, host, port, changeNo, repoListDict):
        cmdList = []
        gitPath = None
        patchSet = None
        project = None

        def onStdoutListener(line):
            nonlocal project
            nonlocal patchSet

            parten = re.compile('project: (.*)')
            m = parten.match(line)
            if m:
                project = m.groups()[0]
                return

            parten = re.compile('number: (\d*)')
            m = parten.match(line)
            if m:
                patchSet = m.groups()[0]
                return
            return

        cmd = 'ssh -p %s %s gerrit query --current-patch-set %s' % (port, host, changeNo)
        ret = context.getTerminal().runCmd(cmd, stdoutListner=onStdoutListener)
        if ret != 0:
            Log.e("Failed to run", cmd)
            return None

        key = project[self.mGerritGitNamePrefixLen:]
        gitPath = repoListDict[key]
        cmdList.append("git -C %s fetch ssh://%s:%s/%s refs/changes/%s/%s/%s" % (gitPath, host, port, project, changeNo[-2:], changeNo, patchSet))
        cmdList.append("git -C %s cherry-pick FETCH_HEAD" % (gitPath))
        return cmdList
