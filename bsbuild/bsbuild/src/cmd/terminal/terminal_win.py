import os

from src.core.cmd.terminal.abstrace_terminal import AbsTerminal


class WinTerminal(AbsTerminal):
    def __init__(self):
        return

    def runCmd(self, cmdStr):
        print("> " + cmdStr)
        os.system(cmdStr)
