#!/usr/bin/python
import sys, os
import linecache
import random
import time
import re
from subprocess import Popen, PIPE

# ------------------------ Constants ------------------------
SECTION_ADDED = 'added'
SECTION_REMOVED = 'removed'
SECTION_CHANGED = 'changed'
SECTION_UNREACHABLE_REVISION = 'unreachable_revision'

OP_FLAG_SKIP = '[skip]'
OP_FLAG_MERGED = '[merg]'
OP_FLAG_CONFLICTED = '[conf]'

MARK_PATCH_MINUS = '[-]'
MARK_PATCH_PLUS = '[+]'
# ------------------------ Global Fields ------------------------
gSourceDiffManifest = None


# ------------------------ classes ------------------------
class DiffManifestFile:
    def __init__(self, path, mode):
        self.file = open(path, mode)
        self.lines = []
        self.sections = {}

        self.startedSectionName = ''
        self.startedProjectName = ''
        pass

    def parse(self):
        self.lines = self.file.readlines()

        section = None
        project = None
        for n in range(0, len(self.lines)):
            l = self.lines[n]
            # parse sections in diffmanifests
            if "added projects : " in l:
                section = Section(SECTION_ADDED)
                self.sections[SECTION_ADDED] = section
                section.lineNo = n
                continue
            elif "removed projects : " in l:
                section = Section(SECTION_REMOVED)
                self.sections[SECTION_REMOVED] = section
                section.lineNo = n
                continue
            elif "changed projects : " in l:
                section = Section(SECTION_CHANGED)
                self.sections[SECTION_CHANGED] = section
                section.lineNo = n
                continue
            elif "projects with unreachable revisions : " in l:
                section = Section(SECTION_UNREACHABLE_REVISION)
                self.sections[SECTION_UNREACHABLE_REVISION] = section
                section.lineNo = n
                continue

            # filter empty lines
            if section is None:
                continue

            # parse projects in a section
            pos = 0
            if SECTION_ADDED in section.name:
                pos = l.find(" at revision ")
                if pos != -1:
                    project = Project()
                    project.path = l[:pos].strip()
                    project.lineNo = n
                    section.addProject(project)
                    continue
            elif SECTION_REMOVED in section.name:
                pos = l.find(" at revision ")
                if pos != -1:
                    project = Project()
                    project.path = l[:pos].strip()
                    project.lineNo = n
                    section.addProject(project)
                    continue
            elif SECTION_CHANGED in section.name:
                matchObj = re.match(r'(\[.*\])?\t(.*?) changed from (.*?) to ([a-zA-Z0-9_]*)(?:<(miui)>)?', l)
                if matchObj:
                    project = Project()
                    project.opflag = matchObj.group(1)
                    project.path = matchObj.group(2)
                    project.fromRevision = matchObj.group(3)
                    project.toRevision = matchObj.group(4)
                    project.groups = matchObj.group(5)
                    project.lineNo = n
                    section.addProject(project)
                    continue
            elif SECTION_UNREACHABLE_REVISION in section.name:
                matchObj = re.match(r'\t(.*) (.*) or (.*) not found', l)
                if matchObj:
                    project = Project()
                    project.path = matchObj.group(1)
                    project.lineNo = n
                    section.addProject(project)
                    continue

            # parse patches in a project
            matchObj = re.match(r'(\[.*\])?.*\t\t\[([+-])\] ([0-9a-fA-F].*)    (.*) \((.*)\) \<(.*)\>', l)
            if matchObj:
                patch = Patch()
                patch.opflag = matchObj.group(1)
                patch.plusminus = matchObj.group(2)
                if '-' in patch.plusminus:
                    patch.branch = project.fromRevision
                elif '+' in patch.plusminus:
                    patch.branch = project.toRevision
                patch.hash = matchObj.group(3)
                patch.title = matchObj.group(4)
                patch.time = matchObj.group(5)
                patch.author = matchObj.group(6)
                patch.lineNo = n
                project.addPatch(patch)
                continue
        # print (self.dump())

    def dump(self):
        dumpstr = ''
        # dumpstr += SECTION_ADDED + ':' + self.sections[SECTION_ADDED].name + '\n'
        # for p in self.sections[SECTION_ADDED].projects:
        #     dumpstr += p.path + '\n'

        # dumpstr += SECTION_REMOVED + ':' + self.sections[SECTION_REMOVED].name + '\n'
        # for p in self.sections[SECTION_REMOVED].projects:
        #     dumpstr += p.path + '\n'

        dumpstr += SECTION_CHANGED + ':' + self.sections[SECTION_CHANGED].name + '\n'
        for p in self.sections[SECTION_CHANGED].projects:
            if p.groups is not None and 'miui' in p.groups:
                dumpstr += "[%s] %s (:%d %s %d %s->%s)\n" % (p.groups, p.path, (p.lineNo + 1), p.opflag, len(p.patches), p.fromRevision, p.toRevision)
            # for pth in p.patches:
            #     dumpstr += "%s[%s] %s %s %s %s %s  :%d\n" % (pth.opflag, pth.plusminus, pth.branch, pth.hash, pth.title, pth.time, pth.author, pth.lineNo)

        # dumpstr += SECTION_UNREACHABLE_REVISION + ':' + self.sections[SECTION_UNREACHABLE_REVISION].name + '\n'
        # for p in self.sections[SECTION_UNREACHABLE_REVISION].projects:
        #     dumpstr += p.path + '\n'
        return dumpstr

    def autoPatch(self):
        root = os.getcwd()
        for p in self.sections[SECTION_CHANGED].projects:
            # if 'build/make' not in p.path:
            #     continue

            if p.opflag is not None and OP_FLAG_SKIP in p.opflag:
                p.setopflag(OP_FLAG_SKIP)
                continue

            # if p.groups is None or 'miui' not in p.groups:
            #     print ('skip non-miui proj', p.path)
            #     p.setopflag(OP_FLAG_SKIP)
            #     continue

            # change dir to project path
            os.chdir(os.path.join(root, p.path))
            print(os.getcwd())

            # git hard reset to fromRevision
            cmd = "git reset --hard remotes/shgit/%s" % p.fromRevision
            print (cmd)
            r = self.run_cmd(cmd)
            print (r)

            # loop pick [+] and bs patches from toRevsion
            patches = list(reversed(p.patches))
            for pth in patches:
                if '+' in pth.plusminus:
                    if 'blackshark.com' in pth.author or 'zeusis.com' in pth.author:
                        cmd = "git cherry-pick -x %s" % pth.hash
                        print cmd
                        r = self.run_cmd(cmd)
                        print (r)
                        if r[0] != 0:
                            cmd = "git cherry-pick --abort"
                            print cmd
                            r = self.run_cmd(cmd)
                            print (r)
                            pth.setopflag(OP_FLAG_CONFLICTED)
                        else:
                            pth.setopflag(OP_FLAG_MERGED)
                        continue

                pth.setopflag(OP_FLAG_SKIP)

    def getline(self, lineno):
        return self.lines[lineno]

    def edit(self, lineno, content):
        self.lines[lineno] = content

    def saveas(self, path):
        f = open(path, 'w+')
        f.writelines(self.lines)

    def skipPath(self, skip_paths):
        for p in self.sections[SECTION_CHANGED].projects:
            for sp in skip_paths:
                if sp in p.path:
                    p.setopflag(OP_FLAG_SKIP)

    def run_cmd(self, cmd):
        # Popen call wrapper.return (code, stdout, stderr)
        child = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = child.communicate()
        ret = child.wait()
        return (ret, out, err)


class Section:
    def __init__(self, name):
        self.name = name
        # operation flag at the start of line.
        # support flags:[skip] [merged] [conflictss]
        self.opflag = ''
        # parsed as this obj in diffmanifestsSourceFile
        self.lineNo = 0
        self.projects = []
        self.name = name
        pass

    def addProject(self, proj):
        self.projects.append(proj)

    def setopflag(self, flag):
        global gSourceDiffManifest
        if self.opflag is not None and flag in self.opflag:
            pass
        else:
            content = flag + gSourceDiffManifest.getline(self.lineNo)
            gSourceDiffManifest.edit(self.lineNo, content)
        self.opflag = flag
        for p in self.projects:
            p.setopflag(flag)


class Project:
    def __init__(self):
        self.path = ''
        self.opflag = ''
        self.lineNo = 0
        self.type = 0
        self.atRevision = ''
        self.fromRevision = ''
        self.toRevision = ''
        self.groups = ''
        self.patches = []
        pass

    def addPatch(self, patch):
        self.patches.append(patch)

    def setopflag(self, flag):
        global gSourceDiffManifest
        if self.opflag is not None and flag in self.opflag:
            pass
        else:
            content = flag + gSourceDiffManifest.getline(self.lineNo)
            gSourceDiffManifest.edit(self.lineNo, content)
        self.opflag = flag
        for p in self.patches:
            p.setopflag(flag)


class Patch:
    def __init__(self):
        self.opflag = ''
        self.lineNo = 0
        self.plusminus = ''
        self.branch = ''
        self.hash = ''
        self.title = ''
        self.time = ''
        self.author = ''
        pass

    def setopflag(self, flag):
        global gSourceDiffManifest
        if self.opflag is not None and flag in self.opflag:
            pass
        else:
            content = flag + gSourceDiffManifest.getline(self.lineNo)
            gSourceDiffManifest.edit(self.lineNo, content)
        self.opflag = flag


# ------------------------ program start ------------------------
def main():
    global gSourceDiffManifest
    gSourceDiffManifest = DiffManifestFile('diffmanifests_delta_patch_2019_10_30__23_02_32.txt', 'r+');
    gSourceDiffManifest.parse()

    gSourceDiffManifest.skipPath([
        # r'bootable/bootloader/edk2',
    ])

    root = os.getcwd()
    gSourceDiffManifest.autoPatch()
    os.chdir(root)

    # after all done, save all changes for checking manually
    nowStr = time.strftime('%Y_%m_%d__%H_%M_%S', time.localtime(time.time()))
    gSourceDiffManifest.saveas('diffmanifests_gen_delta_patch_%s.txt' % nowStr)


if __name__ == '__main__':
    main()
