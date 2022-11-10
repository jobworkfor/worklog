from src.core.handler.handler_node import NodeHandler
from src.core.constant import Constant
from src.core.context import Context

from src.ui.cmdui.page_item_list import ItemListPage
from src.ui.cmdui.page_text_input import TextInputPage
from src.ui.cmdui.view.view_product_item import ConfigItemView
from src.ui.cmdui.view.view_product_item import ItemView
from src.ui.cmdui.view.view_product_item import OptItemView
from src.ui.cmdui.view.view_product_item import Empty_lineItemView
from src.ui.cmdui.view.view_product_item import ActionItemView
from src.ui.cmdui.view.view_product_item import InputItemView
from src.ui.cmdui.view.i_listener_view import ITextInputListener

from src.util.helper_string import StringHelper
from src.util.helper_log import Log

_ = (Log)


class ProductNodeHandler(NodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def onPageCreate(self, page):
        NodeHandler.onPageCreate(self, page)
        for ch in self.mChildren:
            ch.onPageCreate(self)
        return


class ConfigNodeHandler(NodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def onPageCreate(self, page):
        NodeHandler.onPageCreate(self, page)
        for ch in self.mChildren:
            ch.onPageCreate(page)
        return

    def getItemView(self):
        productDao = Context.instance().getDatabase().getProductDao()
        self.mValue = productDao.getProductConfigParam(self.mTarget)

        view = ConfigItemView()
        view.setData(self)
        return view

    def onKeyPressed(self, keycode):
        page = ItemListPage()
        page.setData(self)

        for pos in range(self.getChildCount()):
            if self.mValue == self.getChild(pos).mValue:
                page.setSelectedPos(pos)
                break

        Context.instance().startPage(page)
        return


class Product_configNodeHandler(ConfigNodeHandler):
    def __init__(self):
        ConfigNodeHandler.__init__(self)
        return


class OptNodeHandler(NodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def init(self, *data):
        NodeHandler.init(self, *data)
        if StringHelper.isEmpty(self.mTitle):
            self.mTitle = self.mValue
        if StringHelper.isEmpty(self.mTarget):
            self.mTarget = self.mParent.mTarget
        return

    def getItemView(self):
        view = OptItemView()
        view.setData(self)
        return view

    def onKeyPressed(self, keycode):
        productDao = Context.instance().getDatabase().getProductDao()
        productDao.setProductConfigParam(self.mTarget, self.mValue)

        Context.instance().getContentManager().saveCookies()

        self.mPage.finish()
        return


class ProductOptNodeHandler(OptNodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def onKeyPressed(self, keycode):
        productDao = Context.instance().getDatabase().getProductDao()
        productDao.setProductConfigParam(self.mTarget, self.mValue)

        contentManager = Context.instance().getContentManager()
        contentManager.saveCookies()

        handlerManager = Context.instance().getHandlerManager()
        if self.mValue != contentManager.getCurrentProduct():
            contentManager.loadProductData()
            handlerManager.loadProductHandler()

        contentManager.notifyContentChanged()

        self.mPage.finish()
        return


class ItemNodeHandler(NodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def getItemView(self):
        view = ItemView()
        view.setData(self)
        return view

    def onKeyPressed(self, keycode):
        page = ItemListPage()
        page.setData(self)

        Context.instance().startPage(page)
        return


class Empty_lineNodeHandler(NodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def selectable(self):
        return False

    def getItemView(self):
        return Empty_lineItemView()


class ActionNodeHandler(NodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def init(self, *data):
        NodeHandler.init(self, *data)
        if StringHelper.isEmpty(self.mTitle):
            self.mTitle = self.mValue
        return

    def getItemView(self):
        view = ActionItemView()
        view.setData(self)
        return view

    def onKeyPressed(self, keycode):
        context = Context.instance()
        productDao = context.getDatabase().getProductDao()
        Log.i('self.mTarget', self.mTarget)
        productDao.setProductConfigParam(Constant.KEY_BUILD_PARAM_BUILD_SCRIPT_ENTRY, self.mTarget)
        context.getContentManager().saveCookies()
        context.exit()
        return


class LastBuildActionNodeHandler(ActionNodeHandler):
    def __init__(self):
        NodeHandler.__init__(self)
        return

    def onKeyPressed(self, keycode):
        Context.instance().exit()
        return


class InputNodeHandler(NodeHandler, ITextInputListener):
    def __init__(self):
        NodeHandler.__init__(self)
        self.mPage = None
        return

    def getItemView(self):
        view = InputItemView()
        view.setData(self)
        return view

    def onKeyPressed(self, keycode):
        page = TextInputPage()
        page.setData(self)
        self.mPage = page

        Context.instance().startPage(page)
        return

    def onKeyEvent(self, key):
        if key == Constant.KEYCODE_ESC:
            self.mPage.finish()
        return

    def onTextChanged(self, text):
        context = Context.instance()
        productDao = context.getDatabase().getProductDao()
        cmd = self.mTarget + ' ' + text

        productDao.setProductConfigParam(Constant.KEY_BUILD_PARAM_BUILD_SCRIPT_ENTRY, cmd)
        context.getContentManager().saveCookies()
        context.exit()
        return
