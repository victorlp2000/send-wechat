#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def cleanupPage(driver):
    logger.info('cleaning content...')
    browser = driver.getBrowser()

    divs = browser.find_elements_by_tag_name('div')
    for div in divs:
        classes = div.get_attribute('class')
        ss = classes.split()
        rm = False
        for s in ss:
            rm |= (s == 'c-hlights')
            rm |= (s == 'article-share')
            rm |= (s == 'design-top-offset')
            rm |= (s == 'media-block-wrap')
            rm |= (s == 'google-translate-container')
        if rm:
            browser.execute_script("arguments[0].style.display = 'none';", div)

    selectors = [
    ]
    ids = [
        'foot-nav',
        'youmaylike'    # 您可能感兴趣的内容
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)
