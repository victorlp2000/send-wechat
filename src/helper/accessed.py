#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from datetime import datetime
import urllib.parse
from util import json_file

class Accessed(object):
    def __init__(self, fn):
        self.fn = fn
        self.maxInfo = 10
        self.info = []

    def refresh(self):
        data = json_file.readFile(self.fn)
        if isinstance(data, list):
            self.info = data

    def save(self, info):
        link = urllib.parse.unquote(info['link'])
        info['link'] = link
        info['time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.info.insert(0, info.copy())
        if len(self.info) > self.maxInfo:
            del self.info[-1]
        json_file.saveFile(self.fn, self.info)

    def exists(self, info):
        self.refresh()  # data may changed from outside
        link = urllib.parse.unquote(info['link'])
        for i in self.info:
            if i['link'] == link:
                return True
        return False
