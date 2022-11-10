from src.core.constant import Constant
from src.ui.cmdui.page import Page
from src.ui.cmdui.view.i_listener_view import IListViewListener
from src.ui.cmdui.view.adapter_view import ListViewAdapter
from src.ui.cmdui.view.view_list import ListView

from src.util.helper_log import Log

_ = (Log)


class ItemListPage(Page, IListViewListener):
    class SelfAdapter(ListViewAdapter):
        def __init__(self):
            ListViewAdapter.__init__(self)
            self.mHandler = None
            self.mCount = 0
            return

        def setData(self, data):
            self.mHandler = data
            return

        def getCount(self):
            return self.mHandler.getChildCount()

        def getItem(self, pos):
            return self.mHandler.getChild(pos)

        def selectable(self, pos):
            return self.getItem(pos).selectable()

        def getItemView(self, pos):
            return self.getItem(pos).getItemView()

    def __init__(self):
        Page.__init__(self)
        self.mHandler = None
        self.mAdapter = None
        self.mSelectedPos = 0
        return

    def setSelectedPos(self, pos):
        self.mSelectedPos = pos
        return

    def onCreate(self):
        self.mHandler = self.mData
        self.mHandler.onPageCreate(self)

        self.mAdapter = ItemListPage.SelfAdapter()
        self.mAdapter.setData(self.mHandler)
        return

    def onCreateContentView(self):
        self.mListView = ListView()
        self.mListView.setListener(self)
        self.mListView.setSelectedPos(self.mSelectedPos)

        self.mListView.setAdapter(self.mAdapter)
        return self.mListView

    def onKeyEvent(self, key):
        if key == Constant.KEYCODE_Q or key == Constant.KEYCODE_ESC:
            self.finish()
        return False

    def onItemChosen(self, item):
        item.onKeyPressed(Constant.KEYCODE_ENTER)
        return
