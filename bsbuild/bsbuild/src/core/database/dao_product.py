import xml.dom.minidom

from src.core.constant import Constant
from src.core.context import Context
from src.core.handler.handler_node_product import ProductOptNodeHandler
from src.util.helper_string import StringHelper
from src.util.helper_log import Log

_ = (Log)


class ProductDAO(object):
    def __init__(self):
        self.mXmlPath = None
        self.mRootNode = None
        self.mModulePath = None

        self.mProductConfigHandler = None
        self.mProductConfigDict = {}
        return

    def load(self, xmlPath):
        print('start main()')
        self.mXmlPath = xmlPath
        DOMTree = xml.dom.minidom.parse(xmlPath)
        self.mRootNode = DOMTree.documentElement
        print("Root element : %s" % self.mRootNode)
        return

    def createProductHandlerFromXML(self):
        rootNode = self.mRootNode

        productHandler = self._tryCreateHandlerFromNode(rootNode, None)
        self._fillHandlerWithNode(productHandler, rootNode)
        Log.d('root handler', productHandler)

        # collect all nodes and build a tree of handlers
        self._traversalNode(rootNode, productHandler, 0)

        # add options for product config node
        self._addOptionsForProductConfigNode(productHandler)

        return productHandler

    def setProductConfigParam(self, key, val):
        self.mProductConfigDict[key] = val
        return

    def getProductConfigParam(self, key):
        if key in self.mProductConfigDict:
            return self.mProductConfigDict[key]
        return None

    def getProductConfigDict(self):
        return self.mProductConfigDict

    def getProductConfigHandler(self):
        return self.mProductConfigHandler

    def _tryCreateHandlerFromNode(self, n, parentHandler):
        handlerClassName = None

        # get create handler needed info from root node
        tagName = n.tagName
        modulePath = n.getAttribute(Constant.XML_ATTR_MODULE)
        if self.mModulePath is None:
            if StringHelper.isEmpty(modulePath):
                Log.e('Failed: XML root tag must have valid module attribuilt')
                return
            self.mModulePath = modulePath
        else:
            if StringHelper.isEmpty(modulePath):
                modulePath = self.mModulePath

        handlerAttr = n.getAttribute(Constant.XML_ATTR_HANDLER)
        className = self._getHandlerClassName(tagName)
        if not StringHelper.isEmpty(handlerAttr):
            className = handlerAttr
        handlerClassName = className

        Log.d('_tryCreateHandlerFromNode class path', self.mModulePath, handlerClassName)
        mod = __import__(self.mModulePath, globals(), locals(), ['%s' % handlerClassName])
        handler = getattr(mod, handlerClassName)()
        handler.setParenet(parentHandler)
        return handler

    def _fillHandlerWithNode(self, handler, n):
        handler.init(
            n.tagName,
            n.getAttribute(Constant.XML_ATTR_TITLE),
            n.getAttribute(Constant.XML_ATTR_MODULE),
            n.getAttribute(Constant.XML_ATTR_HANDLER),
            n.getAttribute(Constant.XML_ATTR_TARGET),
            n.getAttribute(Constant.XML_ATTR_VALUE),
            n.getAttribute(Constant.XML_ATTR_COLOR_KEY),
        )
        return

    def _traversalNode(self, n, h, lv):
        h.mLevel = lv
        # Log.i(' ' * 4 * lv, h.mTagName, h.mTitle, h.mModule, h.mHandler, h.mTarget, h.mValue, h.mColorKey)
        for cn in n.childNodes:
            if cn.nodeType == xml.dom.Node.ELEMENT_NODE:
                childHandler = self._tryCreateHandlerFromNode(cn, h)
                self._fillHandlerWithNode(childHandler, cn)
                h.addChild(childHandler)
                self._traversalNode(cn, childHandler, lv + 1)
        return

    def _addOptionsForProductConfigNode(self, productHandler):
        productConfigHandler = None
        for ch in productHandler.mChildren:
            if Constant.XML_TAG_PRODUCT_CONFIG == ch.mTagName:
                productConfigHandler = ch
                break
        self.mProductConfigHandler = productConfigHandler

        supportProductList = Context.instance().getContentManager().getSupportProductList()
        for p in supportProductList:
            optHandler = ProductOptNodeHandler()
            optHandler.init(
                Constant.XML_TAG_OPT,  # tagName
                p,  # XML_ATTR_TITLE
                '',  # XML_ATTR_MODULE
                '',  # XML_ATTR_HANDLER
                self.mProductConfigHandler.mTarget,  # XML_ATTR_TARGET
                p,  # XML_ATTR_VALUE
                '0',  # XML_ATTR_COLOR_KEY
            )
            productConfigHandler.addChild(optHandler)
        return

    def _getHandlerClassName(self, name):
        if StringHelper.isEmpty(name):
            return None
        clsn = name.replace("-", "_");
        clsn = "%sNodeHandler" % clsn.capitalize()
        return clsn
