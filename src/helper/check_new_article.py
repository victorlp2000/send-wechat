#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def isNewArticle(info, last):
    if info == None or last == None:
        return True

    # title may slitely change, need to improve
    if info['title'] != last['title']:
        return True

    logger.warning('old article.')
    return False
