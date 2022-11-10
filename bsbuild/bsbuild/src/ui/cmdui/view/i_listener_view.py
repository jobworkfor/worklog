class IListViewListener:
    def onKeyEvent(self, key): raise RuntimeError

    def onItemChosen(self, item): raise RuntimeError


class ITextInputListener:
    def onKeyEvent(self, key): raise RuntimeError

    def onTextChanged(self, text): raise RuntimeError
