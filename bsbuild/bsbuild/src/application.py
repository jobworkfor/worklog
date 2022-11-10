import curses
import os

from src.core.constant import Constant
from src.core.context import Context
from src.util.helper_delegate import HelperDelegate
from src.util.helper_log import Log
from src.core.manager.manager_content import ContentManager
from src.core.manager.manager_handler import HandlerManager
from src.core.manager.manager_page import PageManager
from src.core.manager.manager_window import WindowManager
from src.core.database.database import Database

_ = (Log)


class Application(object):
    def __init__(self):
        return

    def onCreate(self):
        helperDelegate = HelperDelegate()
        fsHelper = helperDelegate.getFileSystemHelper()

        appRootDir = os.environ.get('BS_BUILD_ROOT')
        androidRootDir = fsHelper.getAndroidCodebaseTopDir(appRootDir)
        # check temp dir, create if not existed.
        tmpDir = fsHelper.join(androidRootDir, Constant.DIR_TEMP)
        if not fsHelper.exists(tmpDir):
            fsHelper.mkdirs(tmpDir)

        Log.instance().init(fsHelper.join(androidRootDir, Constant.PATH_LOG))

        context = Context.instance()
        context.init(self, androidRootDir, appRootDir)
        context.setHelperDelegate(helperDelegate)
        context.setContentManager(ContentManager())
        context.setWindowManager(WindowManager())
        context.setPageManager(PageManager())
        context.setHandlerManager(HandlerManager())
        context.setDatabase(Database())

        Log.i("\n\n\n")

        # set delay of esc key as 25ms
        os.environ.setdefault('ESCDELAY', '25')
        # transfer control to curses
        curses.wrapper(self.onStart)
        return

    def onStart(self, stdscr):
        # from src.core.handler.handler_menu_config import MenuConfigHandler
        # src.core.handler.handler_menu_config.test_for_call()

        context = Context.instance()

        context.setStdscr(stdscr)

        context.getContentManager().systemReady()
        context.getHandlerManager().systemReady()
        context.getWindowManager().systemReady()
        context.getPageManager().systemReady()

        while (True):
            self._loop()
        return

    def _loop(self):
        context = Context.instance()

        # dispatch draw
        context.getWindowManager().dispatchDraw()

        # dispatch key event
        key = context.getStdscr().getch()
        context.getWindowManager().dispatchKeyEvent(key)
        return
