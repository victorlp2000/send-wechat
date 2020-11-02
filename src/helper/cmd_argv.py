#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import sys

from util import json_file

def getUrl():
    for argv in sys.argv:
        if argv.startswith('http'):
            return argv
    return None

def getDebug():
    for argv in sys.argv:
        if argv == 'debug':
            return True
    return False

# config file must be in config folder and starts with config_
def getConfig():
    for argv in sys.argv:
        if argv.startswith('config/config_'):
            return argv
    return None
