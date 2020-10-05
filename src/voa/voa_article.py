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
            print(classes)
            browser.execute_script("arguments[0].style.display = 'none';", div)

    uls = browser.find_elements_by_tag_name('ul')
    print('uls:', len(uls))
    for ul in uls:
        classes = ul.get_attribute('class')
        ss = classes.split()
        rm = False
        for s in ss:
            rm |= (s == 'follow')
        if rm:
            print(classes)
            browser.execute_script("arguments[0].style.display = 'none';", ul)

    selectors = [
    ]
    ids = [
        'youmaylike'    # 您可能感兴趣的内容
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)

    # browser = driver.getBrowser()
    # # make header stay at top
    # header = browser.find_element_by_css_selector('div.hdr')
    # browser.execute_script("arguments[0].style.position = 'relative';", header)
