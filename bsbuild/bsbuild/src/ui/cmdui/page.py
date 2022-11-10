from src.core.context import Context
from src.util.helper_log import Log


class Page(object):
    def __init__(self):
        self.mView = None
        self.mWindow = None
        self.mData = None
        return

    def create(self, win):
        self.onCreate()
        self.mWindow = win
        self.mView = self.onCreateContentView()
        self.mWindow.setView(self.mView)
        return

    def resume(self):
        self.onResume()
        self.mWindow.setView(self.mView)
        return

    def finish(self):
        Context.instance().getPageManager().finish(self)
        return

    def setData(self, data):
        self.mData = data
        return

    def onCreate(self):
        Log.d("Page onCreate()", self)
        return

    def onResume(self):
        Log.d("Page onResume()", self)
        return

    def onCreateContentView(self):
        Log.d("Page onCreateContentView()", self)
        return

    def onFinished(self):
        Log.d("Page onFinished()", self)
        return
