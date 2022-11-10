# -*- coding: utf-8 -*-

import platform
import curses

from src.core.constant import Constant


class Context(object):
    _instance = None
    sOsName = platform.system()

    def __init__(self):
        self.mStdscr = None

        self.mApplication = None
        self.mAndroidRootDir = None
        self.mAppRootDir = None

        self.mHelperDelegate = None
        self.mContentManager = None
        self.mWindowManager = None
        self.mPageManager = None
        self.mHandlerManager = None

        self.mDatabase = None
        self.mProductConfigHandler = None

        raise RuntimeError('Singleton Object: Call instance() instead!')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance

    # color
    @classmethod
    def getColorPair(cls, i):
        style = curses.color_pair(i)
        if i == 1:
            style |= Constant.CURSES_A_BOLD
        return style

    def init(self, app, androidRootDir, appRootDir):
        self.mApplication = app
        self.mAndroidRootDir = androidRootDir
        self.mAppRootDir = appRootDir
        return

    def getApplication(self):
        return self.mApplication

    def getAndroidRootDir(self):
        return self.mAndroidRootDir

    def getAppRootDir(self):
        return self.mAppRootDir

    # --------- self.mStdscr ---------
    def getStdscr(self):
        return self.mStdscr

    def setStdscr(self, stdscr):
        self.mStdscr = stdscr

    # --------- self.mHelperDelegate ---------
    def getHelperDelegate(self):
        return self.mHelperDelegate

    def setHelperDelegate(self, hd):
        self.mHelperDelegate = hd

    # --------- self.mContentManager ---------
    def getContentManager(self):
        return self.mContentManager

    def setContentManager(self, cm):
        self.mContentManager = cm

    # --------- self.mWindowManager ---------
    def getWindowManager(self):
        return self.mWindowManager

    def setWindowManager(self, wm):
        self.mWindowManager = wm

    # --------- self.mPageManager ---------
    def getPageManager(self):
        return self.mPageManager

    def setPageManager(self, pm):
        self.mPageManager = pm

    # --------- self.mHandlerManager ---------
    def getHandlerManager(self):
        return self.mHandlerManager

    def setHandlerManager(self, hm):
        self.mHandlerManager = hm

    # --------- self.mDatabase ---------
    def getDatabase(self):
        return self.mDatabase

    def setDatabase(self, db):
        self.mDatabase = db

    # --------- self.mProductConfigHandler ---------
    def getProductConfigHandler(self):
        return self.mProductConfigHandler

    def setProductConfigHandler(self, pch):
        self.mProductConfigHandler = pch

    def startPage(self, page, win=None):
        self.mPageManager.startPage(page, win)
        return

    def exit(self, code=0):
        exit(code)


# static init
Context.instance()
