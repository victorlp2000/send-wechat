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
    xpath = '//*[@id="__next"]/div/div[3]/div[2]/div/div/h1'
    title = browser.find_element_by_xpath(xpath)
    meta['title'] = title.text

    # abstract
    xpath = '//*[@id="__next"]/div/div[4]/div[1]/article/div[1]/p[1]'
    abstract = browser.find_element_by_xpath(xpath)
    meta['abstract'] = abstract.text
    
    # author
    xpath = '//*[@id="__next"]/div/div[4]/div[1]/article/div[1]/div[1]/p/span'
    author = browser.find_element_by_xpath(xpath)
    meta['author'] = author.text

    return meta
