#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn):
    logger.info('loading "%s"', url)
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)
    time.sleep(3)   # for loading completely
    cleanPage(driver)
    return driver.saveFullPageToJpg(fn)

def cleanPage(driver):
    logger.info('cleaning content...')
    selectors = [
        'div.share--box',  # 分享
        'div.media-block-wrap', # 相关内容, VOA卫视最新视频, 最新美国相关报道, 您可能感兴趣的内容
        'div.comments.comments--fb', # 脸书论坛
    ]
    ids = [
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)
