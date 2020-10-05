#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 15, 2020
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
    print(len(divs))
    for div in divs:
        classes = div.get_attribute('class')
        ss = classes.split()
        rm = False
        for s in ss:
            rm |= s.startswith('StickyContainer_')
            rm |= s.startswith('AdSlot_')
            rm |= s.startswith('RelatedArticles-container')
            rm |= s.startswith('ArticlePage-dianomi')
            rm |= s.startswith('SocialTools_')
            # rm |= s.startswith('RecircRibbon-container-')
        if rm:
            print(classes)
            browser.execute_script("arguments[0].style.display = 'none';", div)

    uls = browser.find_elements_by_tag_name('ul')
    for ul in uls:
        role = ul.get_attribute('role')
        if role == 'site-links':
            print(role)
            browser.execute_script("arguments[0].style.display = 'none';", ul)
