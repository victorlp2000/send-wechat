#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  May 18, 2020
# By: Weiping Liu

import os, time
from datetime import datetime
from urllib.parse import urlparse
import logging

from helper.browser_driver import WebDriver
from helper.my_logger import getMyLogger

from bbc.bbc_article import cleanPage

class Settings(object):
    browser = 'Chrome'     # to get full page image, have to use Firefox now
    pageWidth = 540
    # zoom = 100
    headless = False
    # userAgent = 'Mobile'

def getChildrenTagNames(driver, elem):
    tagName = []
    head = driver.getBrowser().find_element_by_tag_name('head')
    list = elem.find_elements_by_xpath('*')
    for t in list:
        tagName.append(t.tag_name)
    return tagName

def main():
    logger.info('start %s', __file__)
    driver = WebDriver(Settings)
    url = 'https://www.bbc.com/zhongwen/simp/world-54407333'
    # url = 'https://www.voachinese.com/a/trump-to-return-to-white-house-20201005/5609783.html'
    # url = 'https://cn.reuters.com/article/us-trump-covid-stock-investors-1005-idCNKBS26Q0FD'
    driver.loadPage(url)
    driver.setWindowSize(Settings.pageWidth)
    # test this function
    cleanPage(driver)

    input('wait... close')

    driver.close()

if __name__ == '__main__':
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn, logging.DEBUG)
    main()
