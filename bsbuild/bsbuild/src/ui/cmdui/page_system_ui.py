from src.util.helper_log import Log

from src.core.constant import Constant

from src.ui.cmdui.page import Page
from src.ui.cmdui.view.view import View

_ = (Log)


class SystemUiPage(Page):
    class SystemUiView(View):
        def __init__(self):
            return

        def onDraw(self, stdscr):
            cursor_x = 0
            cursor_y = 0
            height, width = stdscr.getmaxyx()
            statusbarstr = "{} ver:{}".format(Constant.APP_NAME, Constant.APP_VERSION)
            stdscr.addstr(height - 1, 0, statusbarstr, Constant.CURSES_A_REVERSE)
            stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1), Constant.CURSES_A_REVERSE)
            stdscr.refresh()
            return

    def __init__(self):
        return

    def onCreate(self):
        return

    def onCreateContentView(self):
        return SystemUiPage.SystemUiView()

    def onFinished(self):
        return
