#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  Jan 4, 2021
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

# return
#   meta = {
#       ...
#   }
def getArticleMeta(driver, url):
    logger.info('get article meta data')
    meta = {}
    browser = driver.getBrowser()

    if url == '':
        logger.warning('no url for article.')
        return meta

    browser.get(url)

    # url
    meta['url'] = url
    getMeta(browser, meta)
    return meta

def getMeta(browser, meta):
    # title
    selector = 'div.wsj-article-headline-wrap'
    header = browser.find_element_by_css_selector(selector)
    meta['title'] = header.find_element_by_tag_name('h1').text
    meta['abstract'] = header.find_element_by_tag_name('h2').text
    return meta
