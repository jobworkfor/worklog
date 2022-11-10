from src.ui.cmdui.page import Page
from src.ui.cmdui.view.view_edit_text import EditTextView


class TextInputPage(Page):
    def __init__(self):
        Page.__init__(self)
        self.mHandler = None
        self.mEditTextView = EditTextView()
        return

    def onCreate(self):
        self.mHandler = self.mData
        return

    def onCreateContentView(self):
        self.mEditTextView.setTitle(self.mHandler.mTitle)
        self.mEditTextView.setListener(self.mHandler)
        return self.mEditTextView
