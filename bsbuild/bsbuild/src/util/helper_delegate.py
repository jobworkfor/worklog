from src.util.helper_arg_parser import ArgParserHelper
from src.util.helper_config import ConfigHelper
from src.util.helper_file_system import FileSystemHelper
from src.util.helper_string import StringHelper


class HelperDelegate(object):
    def __init__(self):
        self.mStringHelper = StringHelper()
        self.mFileSystemHelper = FileSystemHelper()
        pass

    def obtainArgparseHelper(self):
        return ArgparseHelper()

    def obtainConfigHelper(self, path):
        return ConfigHelper(path)

    def getFileSystemHelper(self):
        return self.mFileSystemHelper

    def getStringHelper(self):
        return self.mStringHelper
