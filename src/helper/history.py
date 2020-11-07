#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from datetime import datetime
import urllib.parse
from util import json_file
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

class History(object):
    def __init__(self, fn):
        self.fn = fn
        self.maxInfo = 40
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

    def liveTimeout(self, i, info):
        last = datetime.strptime(i['time'], '%Y-%m-%d %H:%M')
        now = datetime.now()
        seconds = (now - last).seconds
        Hour = 60
        if (seconds / 60) < (3 * Hour):
            logger.info('less than interval time for live article.')
            return True
        if len(i['live']) > 0 and len(info['live']) > 0:
            if i['live'][0] == info['live'][0]:
                logger.info('no new update for live article')
                return True

        info['updated'] = True
        return False

    def exists(self, info):
        self.refresh()  # data may changed from outside
        link = urllib.parse.unquote(info['link'])
        for i in self.info:
            if i['title'] == info['title']:
                if 'live' in info:
                    return self.liveTimeout(i, info)
                return True
            if i['link'] == link:
                info['updated'] = True
                return False
        return False
