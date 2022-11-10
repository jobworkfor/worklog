from src.util.helper_log import Log

from src.core.constant import Constant
from src.core.context import Context
from src.core.i_manager import IManager

from src.ui.cmdui.page_main import MainPage
from src.ui.cmdui.page_system_ui import SystemUiPage

_ = (Log)


class PageManager(IManager):
    class PageStack(object):
        def __init__(self):
            self.mPageList = []
            pass

        def push(self, page):
            self.mPageList.append(page)
            pass

        def pop(self, page):
            self.mPageList.remove(page)
            pass

        def top(self):
            return self.mPageList[-1]

    def __init__(self):
        self.mContext = Context.instance()
        self.mPageStack = PageManager.PageStack()
        self.mWindowManager = None
        self.mWorkspaceWindow = None
        self.mSystemUiWindow = None
        pass

    def systemReady(self):
        context = self.mContext

        self.mWindowManager = context.getWindowManager()
        # create windows for workspace and systemui
        self.mWorkspaceWindow = self.mWindowManager.getWindow(Constant.NAME_WINDOW_WORKSPACE, 0)
        self.mSystemUiWindow = self.mWindowManager.getWindow(Constant.NAME_WINDOW_SYSTEM_UI, 1000)

        # start systemui page
        context.startPage(SystemUiPage(), self.mSystemUiWindow)

        # start main page
        context.startPage(MainPage())
        pass

    def startPage(self, page, win=None):
        if page is None:
            Log.e("startPage(), page is None.")
            return

        if win is None:
            win = self.mWorkspaceWindow

        Log.i("PageManager.startPage():", page)
        page.create(win)

        self.mPageStack.push(page)
        pass

    def finish(self, page):
        self.mPageStack.pop(page)
        page.onFinished()

        page = self.mPageStack.top()
        page.resume()
        pass
