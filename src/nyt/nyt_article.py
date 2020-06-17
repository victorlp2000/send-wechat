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
    driver.scrollToBottom()
    time.sleep(3)   # for loading completely
    cleanPage(driver)

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
