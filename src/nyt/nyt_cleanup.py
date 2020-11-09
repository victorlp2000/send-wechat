#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def cleanupPage(driver, config):
    logger.info('cleaning content')
    driver.scrollToBottom()
    browser = driver.getBrowser()

    selectors = [
        "div.top_banner_ad",
        "div.setting-bar.row",
        "div.big_ad",
        "div.article-body-aside.col-lg-3",
        "div.container.article-footer",
        "nav.nav-footer.container",
        "div.download"
    ]
    for s in selectors:
        elements = browser.find_elements_by_css_selector(s)
        for e in elements:
            if 'debug' in config:
                print('none display:', e.tag_name, 'class:', e.get_attribute('class'))
            browser.execute_script("arguments[0].style.display = 'none';", e)

    ids = [
        "subscribe_cont",
        "subscribe_mobile_cont"
    ]
    # driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)
