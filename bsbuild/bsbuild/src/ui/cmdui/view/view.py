from src.core.context import Context
from src.core.constant import Constant


class View(object):
    def __init__(self):
        self.mTitle = None
        self.mTarget = None
        self.mValue = None
        self.mColorKey = 0
        return

    def setData(self, data):
        self.mTitle = data.mTitle
        self.mTarget = data.mTarget
        self.mValue = data.mValue
        self.mColorKey = data.mColorKey
        return

    def onDraw(self, stdscr, x=0, y=0, flag=Constant.FLAG_ON_DRAW_NONE):
        colorPair = Context.getColorPair(self.mColorKey)
        if flag == Constant.FLAG_ON_DRAW_SELECTED_ITEM:
            colorPair = Context.getColorPair(Constant.CURSES_ID_COLOR_SELECTED)

        stdscr.addstr(y, x, str(self.mTitle), colorPair)
        return

    def onKeyEvent(self, key):
        return False
