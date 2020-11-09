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

    # tcateory / title
    articleHeader = browser.find_element_by_css_selector('div.article-header')
    header = articleHeader.find_element_by_tag_name('header')
    category = header.find_element_by_tag_name('small')
    title = header.find_element_by_tag_name('h1')
    meta['title'] = title.text
    meta['category'] = category.text

    # author
    author = articleHeader.find_element_by_tag_name('address')
    meta['author'] = author.text

    return meta
