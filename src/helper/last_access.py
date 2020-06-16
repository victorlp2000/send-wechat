#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from util import json_file

class LastAccess(object):
    def __init__(self, fn):
        self.fn = fn

    # read from json file , return data
    def load(self):
        data = json_file.readFile(self.fn)
        return data

    def save(self, data):
        json_file.saveFile(self.fn, data)
