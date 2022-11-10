import curses

from src.util.helper_key import Key


class Constant:
    APP_NAME = "bsbuild"
    APP_VERSION = "1.0.0"
    APP_DEBUG = False

    OS_WIN = "Windows"
    OS_LINUX = "Linux"
    OS_MAC = "Mac"

    CURSES_A_REVERSE = curses.A_REVERSE
    CURSES_A_BOLD = curses.A_BOLD
    CURSES_ID_COLOR_SELECTED = 11

    KEYCODE_BACKSPACE = Key.BACKSPACE
    KEYCODE_Q = Key.Q
    KEYCODE_ESC = Key.ESCAPE
    KEYCODE_ENTER = Key.ENTER

    DIR_PRODUCT_ASSET = "bsbuild/res/asset/"
    DIR_PRODUCT_CONFIG = "bsbuild/res/config/"
    DIR_PRODUCT_SCRIPT = "bsbuild/res/script/"
    DIR_TEMP = "out/.bsbuild"

    PATH_LOG = "out/.bsbuild/bsbuild.self.log"
    PATH_BSBUILD_INI = "bsbuild/res/bsbuild.ini"
    PATH_DEFAULT_COOKIES = "bsbuild/res/cookies/cookies.txt"
    PATH_COOKIES = "out/.bsbuild/cookies.txt"
    PATH_BUILD_SCRIPT = "out/.bsbuild/bsbuild.sh"

    MENU_HEAD_CH_LENGTH = 30

    SUFFIX_CONFIG_FILE_NAME = ".xml"
    SUFFIX_SCRIPT_FILE_NAME = ".sh"
    SUFFIX_RANGE = "_range"

    XML_TAG_PRODUCT_CONFIG = 'product-config'
    XML_TAG_OPT = 'opt'

    XML_ATTR_TITLE = 'title'
    XML_ATTR_MODULE = 'module'
    XML_ATTR_HANDLER = 'handler'
    XML_ATTR_TARGET = 'target'
    XML_ATTR_VALUE = 'value'
    XML_ATTR_COLOR_KEY = 'color-key'

    FLAG_ON_DRAW_NONE = 0
    FLAG_ON_DRAW_SELECTED_ITEM = 1

    NAME_WINDOW_WORKSPACE = 'workspace'
    NAME_WINDOW_SYSTEM_UI = 'systemui'

    KEY_SECTION_BUILD_CONFIG = "build_config"
    KEY_SECTION_COOKIES = "cookies"

    KEY_BUILD_PARAM_PRODUCT = "product"
    KEY_BUILD_PARAM_BUILD_SCRIPT_ENTRY = "build_script_entry"

    VAL_INVALID_POS = -1
    VAL_CONFIG_NA = "n/a"
    VAL_CONFIG_YES = "yes"
    VAL_CONFIG_NO = "no"

    def __init__(self): raise RuntimeError('Constant class Can not be instanted!')
