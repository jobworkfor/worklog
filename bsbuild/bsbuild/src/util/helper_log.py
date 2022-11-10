import logging

from src.core.constant import Constant


class Log(object):
    _sInstance = None
    sLogger = None

    @classmethod
    def instance(cls):
        if cls._sInstance is None:
            cls._sInstance = cls.__new__(cls)
            # Put any initialization here.
        return cls._sInstance

    @staticmethod
    def i(*msgs):
        Log._sInstance._info(Log.mergeStr(msgs))
        return

    @staticmethod
    def d(*msgs):
        if not Constant.APP_DEBUG:
            return
        Log._sInstance._debug(Log.mergeStr(msgs))
        return

    @staticmethod
    def w(*msgs):
        Log._sInstance._warning(Log.mergeStr(msgs))
        return

    @staticmethod
    def e(*msgs):
        Log._sInstance._error(Log.mergeStr(msgs))
        return

    @staticmethod
    def critical(*msgs):
        Log._sInstance._critical(Log.mergeStr(msgs))
        return

    @staticmethod
    def mergeStr(*strs):
        if 1 == len(strs[0]):
            return strs[0][0]
        result = ""
        for s in strs[0]:
            result += str(s) + ' '
        return result

    def __init__(self):
        raise RuntimeError('Singleton Object: Call instance() instead!')

    def init(self, logPath):
        Log.sLogger = logging.getLogger(__file__)
        hdlr = logging.FileHandler(logPath)
        hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        Log.sLogger.addHandler(hdlr)
        Log.sLogger.setLevel(logging.DEBUG)
        return

    def _info(self, msgText):
        Log.sLogger.info(msgText)
        return

    def _debug(self, msgText):
        Log.sLogger.debug(msgText)
        return

    def _warning(self, msgText):
        Log.sLogger.warning(msgText)
        return

    def _error(self, msgText):
        Log.sLogger.error(msgText)
        return

    def _critical(self, msgText):
        Log.sLogger.critical(msgText)
        return


# static init
Log.instance()
