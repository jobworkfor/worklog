import curses

from src.ui.cmdui.view.view import View
from src.core.context import Context
from src.core.constant import Constant
from src.util.helper_log import Log

_ = (Log)


class ListView(View):
    def __init__(self):
        self.mContext = Context.instance()
        self.mStdscr = self.mContext.getStdscr()

        self.mAdapter = None
        self.mListener = None

        self.mSelectedPos = 0
        return

    def setAdapter(self, adapter):
        self.mAdapter = adapter
        return

    def setListener(self, listener):
        self.mListener = listener
        return

    def setSelectedPos(self, pos):
        self.mSelectedPos = pos
        return

    def onDraw(self, stdscr, x=0, y=0, flag=Constant.FLAG_ON_DRAW_NONE):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        count = self.mAdapter.getCount()
        if count == 0:
            Log.i('ListView: no items to draw.')
            return

        for pos in range(count):
            if pos == self.mSelectedPos:
                self.mAdapter.getItemView(pos).onDraw(stdscr, y=pos, flag=Constant.FLAG_ON_DRAW_SELECTED_ITEM)
                continue
            self.mAdapter.getItemView(pos).onDraw(stdscr, y=pos)

        stdscr.refresh()
        return

    def onKeyEvent(self, key):
        handled = False
        if key == curses.KEY_UP:
            self._moveSelection(-1)
            handled = True
        elif key == curses.KEY_DOWN:
            self._moveSelection(1)
            handled = True
        elif key == Constant.KEYCODE_ENTER or key in [10, 13]:
            if self.mListener is not None:
                self.mListener.onItemChosen(self.mAdapter.getItem(self.mSelectedPos))
            handled = True
        if not handled:
            handled = self.mListener.onKeyEvent(key)
        return handled

    def _moveSelection(self, offset):
        length = self.mAdapter.getCount()
        lastPos = length - 1

        # loop is needed since skipping unfocusable items
        for i in range(length):
            self.mSelectedPos += offset
            if self.mSelectedPos < 0:
                self.mSelectedPos = lastPos
            elif self.mSelectedPos > lastPos:
                self.mSelectedPos = 0

            if self.mAdapter.selectable(self.mSelectedPos):
                break
        return
