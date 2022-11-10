from src.util.helper_log import Log

from src.core.database.dao_product import ProductDAO

_ = (Log)


class Database(object):
    def __init__(self):
        self.mProductDAO = ProductDAO()
        return

    def loadData(self, path):
        self.mProductDAO.load(path)
        # Context.instance().getDatabase().getMenuDao().dump()
        return

    def getProductDao(self):
        return self.mProductDAO
