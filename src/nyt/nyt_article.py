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
    driver.scrollToBottom()
    time.sleep(3)   # for loading completely
    cleanPage(driver)

    innerHTML = type + ' ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    innerHTML += '<br>' + url
    driver.insertTopDiv(innerHTML)

    return driver.saveFullPageToJpg(fn)

def cleanPage(driver):
    logger.info('cleaning content...')
    selectors = [
        "div.top_banner_ad",
        "div.setting-bar.row",
        "div.big_ad",
        "div.article-body-aside.col-lg-3",
        "div.container.article-footer",
        "nav.nav-footer.container",
        "div.download"
    ]
    ids = [
        "subscribe_cont",
        "subscribe_mobile_cont"
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)
