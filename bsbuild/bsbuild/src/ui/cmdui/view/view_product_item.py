from src.core.context import Context
from src.core.constant import Constant
from src.ui.cmdui.view.view import View
from src.util.helper_log import Log

_ = (Log)


class ItemView(View):
    def __init__(self):
        View.__init__(self)
        return


class ConfigItemView(View):
    def __init__(self):
        View.__init__(self)
        self.mValue = None
        return

    def onDraw(self, stdscr, x=0, y=0, flag=Constant.FLAG_ON_DRAW_NONE):
        colorPair = Context.getColorPair(self.mColorKey)
        if flag == Constant.FLAG_ON_DRAW_SELECTED_ITEM:
            colorPair = Context.getColorPair(Constant.CURSES_ID_COLOR_SELECTED)

        stdscr.addstr(y, x, self._itemTitle(self.mTitle, self.mValue), colorPair)
        return

    def _itemTitle(self, configKey, configVal):
        if configVal is None:
            configVal = ''
        headStr = "choose %s" % configKey.replace("_", " ")
        formatStr = " " * (Constant.MENU_HEAD_CH_LENGTH - len(headStr))
        return '%s%s[%s]' % (headStr, formatStr, configVal)


class OptItemView(View):
    def __init__(self):
        return


class Empty_lineItemView(View):
    def __init__(self):
        return

    def onDraw(self, stdscr, x=0, y=0, flag=Constant.FLAG_ON_DRAW_NONE):
        return


class ActionItemView(View):
    def __init__(self):
        return


class InputItemView(View):
    def __init__(self):
        return
