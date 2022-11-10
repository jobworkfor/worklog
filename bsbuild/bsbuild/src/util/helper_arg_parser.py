#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser


class ArgParserHelper(ArgumentParser):
    """
    WEB: https://docs.python.org/2/library/argparse.html#help
    SRC: https://github.com/python/cpython/blob/2.7/Lib/argparse.py
    """

    def __init__(self, usage="%prog [optinos]"):
        ArgumentParser.__init__(self, usage=usage)
        self.args = []
        self.unknownArgs = []
        return

    def getValue(self, dest):
        try:
            value = getattr(self.args, str(dest))
            return value
        except Exception as e:
            print(e)
            return None

    # @override
    def add_argument(self, *args, **kwargs):
        ArgumentParser.add_argument(self, *args, **kwargs)
        return

    # @override
    def parse_known_args(self, _args):
        (args, unknown) = ArgumentParser.parse_known_args(self, args=_args)
        self.args = args
        self.unknownArgs = unknown
        return (args, unknown)

    # @override
    def error(self, msg):
        if "no such option:" in msg:
            raise RuntimeError("11error: %s\n" % msg)
        else:
            raise RuntimeError("error: %s\n" % msg)


if __name__ == '__main__':
    """ DEMO """
    parser = ArgParserHelper()
    parser.add_argument("-t", "--tree", dest="tree", help="get id of a tree")
    parser.parse_known_args(['-t', '1234', '-u', 'abc'])
    print("args:", parser.args, "unknownArgs:", parser.unknownArgs)
    print("getvalue(\"tree\"):", parser.getValue("tree"))
