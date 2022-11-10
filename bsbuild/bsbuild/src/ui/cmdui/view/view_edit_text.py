from curses.textpad import rectangle

from src.ui.cmdui.view.view import View
from src.core.context import Context
from src.core.constant import Constant
from src.util.helper_log import Log

_ = (Log)


class EditTextView(View):
    def __init__(self):
        self.mContext = Context.instance()
        self.mStdscr = self.mContext.getStdscr()

        self.mListener = None

        self.mTitle = None
        self.mRectHeight = 1
        self.mTextChList = list("")
        return

    def setListener(self, listener):
        self.mListener = listener
        return

    def setTitle(self, title):
        self.mTitle = title
        return

    def onDraw(self, stdscr, x=0, y=0, flag=Constant.FLAG_ON_DRAW_NONE):
        height, width = stdscr.getmaxyx()

        stdscr.clear()

        x = 0
        y = 0
        # print message
        stdscr.addstr(y, 0, self.mTitle)

        # draw input box
        y += 1
        rectangle(stdscr, y, 0, 1 + self.mRectHeight + 1, width - 1)

        # print text in input box
        y += 1
        x = 1
        stdscr.addstr(y, x, "".join(self.mTextChList))

        # skip box bottom line
        y += 1

        stdscr.refresh()
        return

    def onKeyEvent(self, key):
        handled = True
        if key == Constant.KEYCODE_ENTER or key in [10, 13]:
            self.mListener.onTextChanged("".join(self.mTextChList))
        elif key == Constant.KEYCODE_ESC:
            self.mListener.onKeyEvent(key)
        elif key > 0 and key <= 256:
            if key == Constant.KEYCODE_BACKSPACE:
                if len(self.mTextChList) > 0:
                    self.mTextChList.pop()
            else:
                self.mFocusPos = Constant.VAL_INVALID_POS
                ch = chr(key)
                self.mTextChList.append(ch)
                if len(self.mTextChList) > 256:
                    self.mTextChList.pop()

        return handled
