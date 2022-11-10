from src.core.context import Context
from src.core.i_manager import IManager
from src.util.helper_log import Log

_ = (Log)


class HandlerManager(IManager):
    def __init__(self):
        self.mProductHandler = None
        self.mPendingActions = []
        return

    def systemReady(self):
        context = Context.instance()
        contentManager = context.getContentManager()
        self.loadProductHandler()
        return

    def getProductHandler(self):
        return self.mProductHandler

    def loadProductHandler(self):
        context = Context.instance()
        contentManager = context.getContentManager()
        productDao = context.getDatabase().getProductDao()
        product = contentManager.getCurrentProduct()

        self.mProductHandler = productDao.createProductHandlerFromXML()
        Log.i('-------- dump mProductHandler --------')
        self._dumpProductHandler(self.mProductHandler, 0)
        Log.i('------------------------------')

        # set default product to build config
        productConfigHandler = productDao.getProductConfigHandler()
        key = productConfigHandler.mTarget
        val = product
        productDao.setProductConfigParam(key, val)

        # set cookies to build config
        cookiesDict = contentManager.getCookiesDict()
        for key in cookiesDict:
            productDao.setProductConfigParam(key, cookiesDict[key])
        Log.i("-------- dump mProductConfigDict --------")
        Log.i(productDao.mProductConfigDict)
        Log.i('------------------------------')
        return

    def _dumpProductHandler(self, h, lv):
        Log.i(' ' * 4 * lv, h.mTagName, h.mTitle, h.mModule, h.mHandler, h.mTarget, h.mValue, h.mColorKey)
        for ch in h.mChildren:
            self._dumpProductHandler(ch, lv + 1)
        return
