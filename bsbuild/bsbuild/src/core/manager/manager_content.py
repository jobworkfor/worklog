from src.core.constant import Constant
from src.core.context import Context
from src.core.i_manager import IManager

from src.util.helper_string import StringHelper
from src.util.helper_log import Log

_ = (Log)


class ContentManager(IManager):
    def __init__(self):
        self.mObservers = []
        self.mContext = Context.instance()
        self.mCurrentProduct = None

        self.mCookiesDict = {}  # {'product':'kaiser', ...}
        self.mSupportProductList = []  # ['kaiser', 'penrose']
        return

    def systemReady(self):
        context = self.mContext
        fsHelper = context.getHelperDelegate().getFileSystemHelper()
        self.mFsHelper = fsHelper

        # init support products
        self._loadSupportProducts()

        # load cookies and product XML
        self.loadProductData()
        return

    def loadProductData(self):
        context = self.mContext
        fsHelper = self.mFsHelper

        # load default cookies
        self._loadCookies(Constant.PATH_DEFAULT_COOKIES)
        # overlay current user cookies
        self._loadCookies(Constant.PATH_COOKIES)

        # init self.mCurrentProduct
        self.mCurrentProduct = self._tryGetCurrentProduct()

        configXMLName = self.mCurrentProduct + Constant.SUFFIX_CONFIG_FILE_NAME
        configXMLPath = fsHelper.join(context.getAppRootDir(), Constant.DIR_PRODUCT_ASSET, configXMLName)
        context.getDatabase().loadData(configXMLPath)

        # copy porduct.sh to build dir
        self._loadBuildScript()
        return

    def registerContentObserver(self, listener):
        self.mObservers.append(listener)
        return

    def unregisterContentObserver(self, listener):
        self.mObservers.remove(listener)
        return

    def notifyContentChanged(self):
        for l in self.mObservers:
            l.onContentChanged()
        return

    def getCurrentProduct(self):
        return self.mCurrentProduct

    def getCookiesDict(self):
        return self.mCookiesDict

    def getSupportProductList(self):
        return self.mSupportProductList

    def saveCookies(self):
        productDao = Context.instance().getDatabase().getProductDao()

        fsHelper = self.mFsHelper
        cookiesPath = fsHelper.join(self.mContext.getAndroidRootDir(), Constant.PATH_COOKIES)
        cfgHelper = self.mContext.getHelperDelegate().obtainConfigHelper(cookiesPath)

        cfgHelper.save(Constant.KEY_SECTION_COOKIES, productDao.getProductConfigDict())
        return

    def _loadSupportProducts(self):
        fsHelper = self.mFsHelper
        productConfigDir = fsHelper.join(self.mContext.getAppRootDir(), Constant.DIR_PRODUCT_ASSET)
        configFiles = fsHelper.searchFile(productConfigDir, r".+\%s$" % Constant.SUFFIX_CONFIG_FILE_NAME)

        # init self.mProductConfigDict["products"]
        section = Constant.KEY_SECTION_BUILD_CONFIG
        valList = []
        for cf in configFiles:
            configProductName = fsHelper.fileName(cf)
            valList.append(configProductName.rstrip(Constant.SUFFIX_CONFIG_FILE_NAME))
        valList.sort()

        self.mSupportProductList = valList
        return

    def _loadCookies(self, path):
        fsHelper = self.mFsHelper
        defCookiesPath = fsHelper.join(self.mContext.getAndroidRootDir(), path)
        if fsHelper.exists(defCookiesPath):
            configHelper = self.mContext.getHelperDelegate().obtainConfigHelper(defCookiesPath)
            config = configHelper.items(Constant.KEY_SECTION_COOKIES)
            if config is not None:
                for t in config:
                    self.mCookiesDict[t[0]] = t[1]
        return

    def _tryGetCurrentProduct(self):
        cookiesProduct = None
        if Constant.KEY_BUILD_PARAM_PRODUCT in self.mCookiesDict:
            product = self.mCookiesDict[Constant.KEY_BUILD_PARAM_PRODUCT]
            if not StringHelper.isEmpty(product):
                cookiesProduct = product

        currentProduct = cookiesProduct
        if currentProduct is None:
            currentProduct = self.mSupportProductList[0]

        return currentProduct

    def _loadBuildScript(self):
        context = Context.instance()
        fsHelper = context.getHelperDelegate().getFileSystemHelper()

        scriptName = self.mCurrentProduct + Constant.SUFFIX_SCRIPT_FILE_NAME
        sourceScriptPath = fsHelper.join(context.getAppRootDir(), Constant.DIR_PRODUCT_ASSET, scriptName)
        targetScriptPath = fsHelper.join(context.getAndroidRootDir(), Constant.PATH_BUILD_SCRIPT)

        Log.i("COPY BUILD SCRIPT:", sourceScriptPath, targetScriptPath)
        fsHelper.cp(sourceScriptPath, targetScriptPath, True)
        return
