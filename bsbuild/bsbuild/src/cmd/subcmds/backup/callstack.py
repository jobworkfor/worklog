#!/usr/bin/python
import sys, os
import linecache
import random
import time
import re
from subprocess import Popen, PIPE

# ------------------------ Constants ------------------------
PARAM_FILE_NAME = 'callstack_txt'

# ------------------------ Global Fields ------------------------
gCallStackParser = None


# ------------------------ classes ------------------------
class CallStackParser:
    def __init__(self, path, mode):
        self.file = open(path, mode)
        self.lines = []
        self.callStacks = []
        self.uniqueStacks = []
        pass

    def parse(self):
        self.lines = self.file.readlines()
        stack = None
        mark = ''
        for n in range(0, len(self.lines)):
            l = self.lines[n]
            matchObj = re.match(r'.*bob_log_tag:...(.)($|...)(.*)', l)
            if matchObj:
                mark = matchObj.group(1)
                if '_' in mark:
                    stack = CallStack()
                    self.callStacks.append(stack)
                    pass
                elif '|' in mark:
                    stack.addItem(matchObj.group(3).strip())
                    pass
                elif '@' in mark:
                    pass

        for s in self.callStacks:
            if len(self.uniqueStacks) == 0:
                self.uniqueStacks.append(s)
                continue

            uniStack = s
            for us in self.uniqueStacks:
                if us.equals(s):
                    uniStack = None
                    break
                else:
                    # print 'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'
                    # for i in us.callitems:
                    #     print i
                    # print '-' * 40
                    # for i in s.callitems:
                    #     print i
                    # print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                    # line = input()
                    pass
            if uniStack is not None:
                self.uniqueStacks.append(uniStack)
            pass

    def printStacks(self):
        idx = 0
        for s in self.uniqueStacks:
            for i in s.callitems:
                idx += 1
                print  i
            print ' '

        print 'len', len(self.uniqueStacks), len(self.callStacks)
        pass


class CallStack:
    def __init__(self):
        self.callitems = []

    def addItem(self, item):
        self.callitems.append(item)

    def equals(self, stack):
        if len(self.callitems) != len(stack.callitems):
            return False

        for n in range(0, len(self.callitems)):
            if self.callitems[n] in stack.callitems[n]:
                continue
            else:
                # print '->', n, self.callitems[n], '<@>', stack.callitems[n]
                return False
        return True


# ------------------------ program start ------------------------
def main():
    gCallStackParser = CallStackParser(PARAM_FILE_NAME, 'r+');
    gCallStackParser.parse()
    gCallStackParser.printStacks()


if __name__ == '__main__':
    main()
