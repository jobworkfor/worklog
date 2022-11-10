import curses

from src.util.helper_log import Log
from src.core.context import Context
from src.core.i_manager import IManager

_ = (Log)


class Window(object):
    def __init__(self, name, zIdx):
        self.mName = name
        self.mZIndex = zIdx
        self.mView = None
        return

    def setView(self, view):
        self.mView = view
        return

    def drawView(self):
        if self.mView is None: return
        self.mView.onDraw(Context.instance().getStdscr())
        return

    def sendKeyEvent(self, key):
        if self.mView is None: return
        return self.mView.onKeyEvent(key)


class WindowManager(IManager):
    def __init__(self):
        self.mWindowList = []
        return

    def systemReady(self):
        # turn off cursor blinking
        curses.curs_set(0)

        # color scheme for selected row
        # curses.init_pair(pair_number, fg, bg)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_WHITE)
        return

    def getWindow(self, name, zIndex):
        window = Window(name, zIndex)
        length = len(self.mWindowList)
        if length == 0:
            self.mWindowList.append(window)
        else:
            pos = 0
            for i in range(0, length):
                if zIndex > self.mWindowList[i].mZIndex:
                    pos = i + 1
                else:
                    break
            self.mWindowList.insert(pos, window)
        return window

    def dispatchDraw(self):
        length = len(self.mWindowList)
        for i in range(length):
            window = self.mWindowList[i]
            window.drawView()
        return

    def dispatchKeyEvent(self, key):
        length = len(self.mWindowList)
        for i in range(length):
            window = self.mWindowList[i]
            if window.sendKeyEvent(key):
                break
        return
