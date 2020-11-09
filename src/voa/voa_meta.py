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
    title = browser.find_element_by_css_selector('h1.title.pg-title')
    meta['title'] = title.text

    # author
    headMeta = browser.find_elements_by_tag_name('meta')
    for m in headMeta:
        if m.get_attribute('name') == 'Author':
            meta['author'] = m.get_attribute('content')
            break

    return meta
