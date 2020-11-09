#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  Nov 8, 2020
# By: Weiping Liu

import time
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

# return
#   meta = {
#       link:
#       title:
#       live:
#       ...
#   }
def getArticleMeta(driver, url):
    logger.info('get article meta data')
    meta = {}
    browser = driver.getBrowser()

    if url == '':
        return meta

    browser.get(url)

    # url
    meta['url'] = browser.current_url

    # title
    xpath = '/html/body/div[4]/article/h1'
    element = browser.find_element_by_xpath(xpath)
    meta['title'] = element.text

    xpath = '/html/body/div[3]/section/ol/li[2]/a'
    element = browser.find_element_by_xpath(xpath)
    meta['category'] = element.text

    return meta
