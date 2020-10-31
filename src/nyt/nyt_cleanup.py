#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def cleanupPage(driver):
    logger.info('cleaning content')

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
