#!/usr/bin/python
# -*- coding: utf-8 -*-


class StringHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def styleString(string, mode='default', fore='white', back=''):
        """
        format：\033[显示方式;前景色;背景色m
        explanation:

        foreground       background        color
        ---------------------------------------
          30                40              black
          31                41              red
          32                42              green
          33                43              yellow
          34                44              blue
          35                45              purple
          36                46              cyan
          37                47              white

        显示方式           意义
        -------------------------
           0             default
           1             highlight
           4             underline
           5             blink
           7             invert
           8             invisible

        eg.
        \033[1;31;40m    <!--1-highlight 31-foreground: red  40-background: black-->
        \033[0m          <!--use default, namely remove all styles-->]]]
        """
        style_data = {
            'fore':
                {  # foreground
                    'black': 30,  # black
                    'red': 31,  # red
                    'green': 32,  # green
                    'yellow': 33,  # yellow
                    'blue': 34,  # blue
                    'purple': 35,  # fuchsia
                    'cyan': 36,  # ultramarine
                    'white': 37,  # white
                },

            'back':
                {  # background
                    'black': 40,  # black
                    'red': 41,  # red
                    'green': 42,  # green
                    'yellow': 43,  # yellow
                    'blue': 44,  # blue
                    'purple': 45,  # purple
                    'cyan': 46,  # cyan
                    'white': 47,  # white
                },

            'mode':
                {  # mode
                    'default': 0,  # default
                    'bold': 1,  # highlight
                    'udline': 4,  # underline
                    'blink': 5,  # blink
                    'invert': 7,  # invert
                    'hide': 8,  # invisible
                },

            'default':
                {
                    'end': 0,
                    'end1': 1,
                },
        }

        mode = '%s' % style_data['mode'][mode] if style_data['mode'].has_key(mode) else ''
        fore = '%s' % style_data['fore'][fore] if style_data['fore'].has_key(fore) else ''
        back = '%s' % style_data['back'][back] if style_data['back'].has_key(back) else ''
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        end = '\033[%sm' % style_data['default']['end'] if style else ''
        return '%s%s%s' % (style, string, end)

    @staticmethod
    def substring(content, startStr, endStr, fromIndex=0):
        """
        str = '0123456789'
        print str[0:3]      # get characters from the first to the third character
        print str[:]        # keep all characters
        print str[6:]       # get characters from the 7th to the end
        print str[:-3]      # get characters form start to the third last character
        print str[2]        # get the third character
        print str[-1]       # get the last one character
        print str[::-1]     # create a string which is reverse to the original
        print str[-3:-1]    # get characters from the last third to the last one character
        print str[-3:]      # get characters from the last third to the end
        print str[:-5:-3]   # get characters from the last fifth to the last third, and reverse them
        """
        start_idx = content.index(startStr, fromIndex)
        if start_idx >= 0:
            start_idx += len(startStr)
        end_idx = content.index(endStr, start_idx)
        return content[start_idx:end_idx]

    @staticmethod
    def isEmpty(str):
        if str is not None and len(str) > 0:
            return False
        return True


if __name__ == '__main__':
    '''
    Entrance for testing this helper.
    '''
    print(StringHelper.styleString('default'))
    print('')

    print("test display mode")
    print(StringHelper.styleString('highlight', mode='bold'))
    print(StringHelper.styleString('underline', mode='udline'))
    print(StringHelper.styleString('blink', mode='blink'))
    print(StringHelper.styleString('invert', mode='invert'))
    print(StringHelper.styleString('invisible', mode='hide'))
    print('')

    print("test foreground")
    print(StringHelper.styleString('black', fore='black'))
    print(StringHelper.styleString('red', fore='red'))
    print(StringHelper.styleString('green', fore='green'))
    print(StringHelper.styleString('yellow', fore='yellow'))
    print(StringHelper.styleString('blue', fore='blue'))
    print(StringHelper.styleString('purple', fore='purple'))
    print(StringHelper.styleString('cyan', fore='cyan'))
    print(StringHelper.styleString('white', fore='white'))
    print('')

    print("test background")
    print(StringHelper.styleString('black', back='black'))
    print(StringHelper.styleString('red', back='red'))
    print(StringHelper.styleString('green', back='green'))
    print(StringHelper.styleString('yellow', back='yellow'))
    print(StringHelper.styleString('blue', back='blue'))
    print(StringHelper.styleString('purple', back='purple'))
    print(StringHelper.styleString('cyan', back='cyan'))
    print(StringHelper.styleString('white', back='white'))
    print('')
