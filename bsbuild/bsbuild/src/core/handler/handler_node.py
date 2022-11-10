from src.util.helper_log import Log
from src.util.helper_string import StringHelper

# from src.util.helper_string import StringHelper

_ = (Log)


class NodeHandler(object):
    def __init__(self):
        self.mTagName = None
        self.mTitle = None
        self.mModule = None
        self.mHandler = None
        self.mTarget = None
        self.mValue = None
        self.mColorKey = 0

        self.mLevel = 0
        self.mPage = None
        self.mView = None
        self.mParent = None
        self.mChildren = []
        return

    def setParenet(self, h):
        self.mParent = h
        return

    def init(self, *data):
        self.mTagName = data[0]
        self.mTitle = data[1]
        self.mModule = data[2]
        self.mHandler = data[3]
        self.mTarget = data[4]
        self.mValue = data[5]
        colorKey = 0
        colorKeyStr = data[6]
        if not StringHelper.isEmpty(colorKeyStr):
            colorKey = int(colorKeyStr)
        self.mColorKey = colorKey
        return

    def addChild(self, handler, pos=-1):
        if pos == -1:
            self.mChildren.append(handler)
        else:
            self.mChildren.insert(pos, handler)
        return

    def getChildCount(self):
        return len(self.mChildren)

    def getChild(self, pos):
        return self.mChildren[pos]

    def selectable(self):
        return True

    def getItemView(self):
        return None

    def onPageCreate(self, page):
        self.mPage = page
        return

    def onSelected(self):
        return

    def onKeyPressed(self, keycode):
        Log.i('onKeyPressed', keycode, self)
        return
