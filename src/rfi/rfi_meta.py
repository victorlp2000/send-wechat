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
    header = browser.find_element_by_css_selector('article')
    title = header.find_element_by_tag_name('h1')
    meta['title'] = title.text

    # author
    author = header.find_element_by_css_selector('div.m-from-author')
    meta['author'] = author.text

    # degestbody > div:nth-child(8) > div.t-content.t-content--article > article > p
    abstract = header.find_element_by_css_selector('p.t-content__chapo')
    meta['abstract'] = abstract.text

    return meta
