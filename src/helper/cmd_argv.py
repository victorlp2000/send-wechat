#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import sys

from util import json_file

def getContacts():
    # default contacts
    contacts = ['test']
    if len(sys.argv) > 1:
        tmp = json_file.readFile(sys.argv[1])
        if type(tmp) is list:
            contacts = tmp
    return contacts
