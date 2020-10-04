#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time
from datetime import datetime

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn, type):
    logger.info('loading "%s"', url)
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)
    time.sleep(3)   # for loading completely
    cleanPage(driver)

    innerHTML = '<h2>' + type + ' ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    innerHTML += '<br>' + url + '</h2>'
    driver.insertTopDiv(innerHTML)

    return driver.saveFullPageToJpg(fn)

def cleanPage(driver):
    logger.info('cleaning content...')
    selectors = [
        'div.container.google-translate-container',
        'div.share--box',  # 分享
        'div.media-block.also-read',    # 请同时参阅
        'div.media-block-wrap',         # 相关内容
        'div.region',                   # VOA卫视最新视频, 中国, 台湾, 港澳
                                        # 最新美国相关报道
        'div.comments.comments--fb',    # 脸书论坛
    ]
    ids = [
        'comments', # 脸书论坛
        'youmaylike'    # 您可能感兴趣的内容
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)

    browser = driver.getBrowser()
    # make header stay at top
    header = browser.find_element_by_css_selector('div.hdr')
    browser.execute_script("arguments[0].style.position = 'relative';", header)
