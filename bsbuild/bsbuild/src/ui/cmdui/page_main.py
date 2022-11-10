from src.core.constant import Constant
from src.core.context import Context
from src.core.i_content_observer import IContentObserver
from src.ui.cmdui.page import Page
from src.ui.cmdui.view.view_list import ListView
from src.ui.cmdui.view.adapter_view import ListViewAdapter
from src.ui.cmdui.view.i_listener_view import IListViewListener
from src.util.helper_log import Log

_ = (Log)


class MainPage(Page, IContentObserver, IListViewListener):
    class MainAdapter(ListViewAdapter):
        def __init__(self):
            ListViewAdapter.__init__(self)
            self.mHandlerManager = Context.instance().getHandlerManager()

            self.mProductHandler = None
            self.mCount = 0
            return

        def setData(self, data):
            self.mProductHandler = data
            return

        def getCount(self):
            return self.mProductHandler.getChildCount()

        def getItem(self, pos):
            return self.mProductHandler.getChild(pos)

        def selectable(self, pos):
            return self.getItem(pos).selectable()

        def getItemView(self, pos):
            return self.getItem(pos).getItemView()

    def __init__(self):
        Page.__init__(self)
        self.mListView = None
        self.mAdapter = None
        self.mProductHandler = None
        self.mHandlerManager = None
        return

    def onCreate(self):
        context = Context.instance()
        context.getContentManager().registerContentObserver(self)

        self.mHandlerManager = context.getHandlerManager()

        self.mProductHandler = self.mHandlerManager.getProductHandler()
        self.mProductHandler.onPageCreate(self)
        self.mAdapter = MainPage.MainAdapter()
        self.mAdapter.setData(self.mProductHandler)
        return

    def onCreateContentView(self):
        self.mListView = ListView()
        self.mListView.setListener(self)

        self.mListView.setAdapter(self.mAdapter)
        return self.mListView

    def onFinished(self):
        Context.instance().getContentManager().unregisterContentObserver(self)
        return

    def onContentChanged(self):
        self.mProductHandler = self.mHandlerManager.getProductHandler()
        self.mAdapter.setData(self.mProductHandler)
        return

    def onKeyEvent(self, key):
        if key == Constant.KEYCODE_Q or key == Constant.KEYCODE_ESC:
            Context.instance().exit(1)
        return True

    def onItemChosen(self, item):
        item.onKeyPressed(Constant.KEYCODE_ENTER)
        return
