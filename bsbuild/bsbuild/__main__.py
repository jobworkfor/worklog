#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PYTHONDONTWRITEBYTECODE=1 python __main__.py

import sys

from src.application import Application

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    Application().onCreate()
