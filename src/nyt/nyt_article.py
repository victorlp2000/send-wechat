#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time

from helper.my_logger import getMyLogger
from helper.set_article import setArticle

logger = getMyLogger(__name__)

def getPageImage(driver, info):
    logger.info('loading "%s"', str(info))
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(info['link'])
    time.sleep(3)   # for loading completely

    cleanPage(driver, info)

    return driver.saveFullPageToJpg(info['fn'])

def cleanPage(driver, info=None):
    logger.info('cleaning content...')
    if info != None:
        setArticle(driver, info)

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
