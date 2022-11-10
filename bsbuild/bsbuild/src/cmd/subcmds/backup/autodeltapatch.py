#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
import linecache
import random
import time
import re
import xml.sax
from subprocess import Popen, PIPE

# ------------------------ Constants ------------------------
PARAM_MANIFEST_PATH = 'SM8250_Q_DEV_BSUI_20190923_2019_11_05__20_57_42.xml'
PARAM_TARGET_MANIFEST_PATH = '.repo/manifests/blackshark/SM8250_Q_DEV_BSUI_20190923.xml'
PARAM_REPORT_PATCH_PREFIX = 'delta_patch_report_'


# ------------------------ classes ------------------------
class AutoDeltaPatcher:
    def __init__(self):
        self.reportLines = []

        self.projs = []
        self.targetProjs = []
        self.deltaProjs = []

    def parse(self):
        # parse original manifest
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = OManifestXmlHandler(self.projs)
        parser.setContentHandler(handler)
        parser.parse(PARAM_MANIFEST_PATH)
        print ("found %d projs in projs" % len(self.projs))
        # i = 0
        # for p in self.projs:
        #     i += 1
        #     print i, p.path, p.upstream
        # print '*' * 100
        # parse target manifest
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = ManifestXmlHandler(self.targetProjs)
        parser.setContentHandler(handler)
        parser.parse(PARAM_TARGET_MANIFEST_PATH)
        print ("found %d projs in target projs" % len(self.targetProjs))
        # i = 0
        # for p in self.targetProjs:
        #     i += 1
        #     print i, p.path, p.upstream
        # print '*' * 100

    def confirmDeltaPatch(self):
        root = os.getcwd()
        for p in self.projs:
            dest_dir = os.path.join(root, p.path)
            if not os.path.exists(dest_dir):
                print ('     skip(%s) missed dir: %s - %s' % (p.upstream, p.path, p.upstream))
                continue

            for tp in self.targetProjs:
                if p.path == tp.path:
                    if tp.upstream == 'sm8250_q_r00640.1_miui_20191102' or tp.upstream != p.upstream:
                        # print "-->", p.path, p.upstream
                        self.deltaProjs.append(p)
                    break

        print '-----', len(self.deltaProjs)

        dProjs = []
        for p in self.deltaProjs:
            print p.path
            dest_dir = os.path.join(root, p.path)
            os.chdir(dest_dir)
            cmd = 'git log --oneline %s...shgit/%s' % (p.revision, p.upstream)
            r = self.run_cmd(cmd)
            patchLines = r[1].split('\n')
            print '***', len(patchLines)
            if len(patchLines) > 1:
                dProjs.append(p)
                print 'append proj', p.path
                continue
            os.chdir(root)

        self.deltaProjs = dProjs
        print '-----', len(self.deltaProjs)

        dProjs = []
        for p in self.deltaProjs:
            # if 'frameworks/compile/mclinker' != p.path:
            #     continue
            print p.path
            dest_dir = os.path.join(root, p.path)
            os.chdir(dest_dir)
            cmd = 'git fetch shgit %s' % p.upstream
            r = self.run_cmd(cmd)

            cmd = 'git l -5 shgit/%s' % p.upstream
            r = self.run_cmd(cmd)
            print r[1]
            if 'blackshark.com' in r[1] or 'zeusis.com' in r[1]:
                dProjs.append(p)
                print 'append proj', p.path
                continue

            os.chdir(root)

        self.deltaProjs = dProjs
        print '-----', len(self.deltaProjs)

        # return
        print '*' * 100

        i = 0
        for p in self.deltaProjs:
            tp = None
            for _p in self.targetProjs:
                if p.path == _p.path:
                    tp = _p
                    break

            # if 'miui/frameworks/base' != p.path:
            #     continue
            i += 1
            print i, p.path, p.upstream

            dest_dir = os.path.join(root, p.path)
            os.chdir(dest_dir)

            cmd = 'git fetch shgit %s' % p.upstream
            r = self.run_cmd(cmd)
            print r

            cmd = 'git --no-pager lg --all --pretty=format:\'%%H %%s (%%ad) <%%ae> %%d\' --abbrev-commit --date=local -30 %s' % p.revision
            r = self.run_cmd(cmd)
            print '== %s ==' % tp.upstream
            patchLines = r[1].split('\n')
            for l in patchLines:
                print l

            print '\n\n'
            os.chdir(root)

        # os.chdir(dest_dir)
        # print os.getcwd()
        #

        #
        # cmd = 'git --no-pager lg --pretty=format:\'%%H %%s (%%ad) <%%ae> %%d\' --abbrev-commit --date=local %s..shgit/%s' % (p.revision, p.upstream)
        # r = self.run_cmd(cmd)
        # patchLines = r[1].split('\n')
        # for l in patchLines:
        #     matchObj = re.match(r'\* (.*?) (.*?) (\(.*\)) (\<.*\>) (.*)', l)
        #     if matchObj:
        #         patch = Patch()
        #         patch.hash = matchObj.group(1)
        #         patch.title = matchObj.group(2)
        #         patch.date = matchObj.group(3)
        #         patch.email = matchObj.group(4)
        #         p.addPatch(patch)
        #
        # os.chdir(root)

    def run_cmd(self, cmd):
        print '$', cmd
        # Popen call wrapper.return (code, stdout, stderr)
        child = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = child.communicate()
        ret = child.wait()
        return (ret, out, err)


class OManifestXmlHandler(xml.sax.ContentHandler):
    def __init__(self, projs):
        self.projs = projs

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "project":
            p = Project()
            self.projs.append(p)
            names = attributes.getNames()
            if u'groups' in names:
                p.groups = attributes.getValue(u'groups')
            else:
                p.groups = u'all'
            p.name = attributes.getValue(u'name')

            if u'path' in names:
                p.path = attributes.getValue(u'path')
            else:
                p.path = p.name

            if u'revision' in names:
                p.revision = attributes.getValue(u'revision')

            if u'upstream' in names:
                p.upstream = attributes.getValue(u'upstream')


class ManifestXmlHandler(xml.sax.ContentHandler):
    def __init__(self, projs):
        self.projs = projs
        self.defRevision = ''

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "project":
            # <project groups="miuigit" name="device/qcom/sepolicy" path="device/qcom/sepolicy" revision="sm8250_q_r00640.1_miui_20191102"/>
            p = Project()
            self.projs.append(p)
            names = attributes.getNames()
            if u'groups' in names:
                p.groups = attributes.getValue(u'groups')
            else:
                p.groups = u'all'

            p.name = attributes.getValue(u'name')

            if u'path' in names:
                p.path = attributes.getValue(u'path')
            else:
                p.path = p.name

            if u'revision' in names:
                p.upstream = attributes.getValue(u'revision')
            else:
                p.upstream = self.defRevision

        elif tag == 'default':
            # <default remote="shgit" revision="sm8250_q_dev_20190906" sync-c="true" sync-j="4"/>
            self.defRevision = attributes.getValue(u'revision')


class Project:
    def __init__(self):
        self.lineNo = 0
        self.groups = ''
        self.name = ''
        self.path = ''
        self.revision = ''
        self.upstream = ''
        self.patches = []

    def addPatch(self, patch):
        self.patches.append(patch)


class Patch:
    def __init__(self):
        self.hash = ''
        self.date = ''
        self.title = ''
        self.email = ''
        self.stat = ''


# ------------------------ program start ------------------------
def main():
    patcher = AutoDeltaPatcher();
    patcher.parse()
    patcher.confirmDeltaPatch()


if __name__ == '__main__':
    main()
