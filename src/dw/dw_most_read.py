#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import time
import urllib.parse

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getMostReadArticleInfo(driver, url):
    logger.info('loading: %s', urllib.parse.unquote(url))
    driver.loadPage(url) # open the home page
    browser = driver.getBrowser()

    selector = 'div.articlelinks.articlelinks--numbered'
    divs = browser.find_elements_by_css_selector(selector)
    # verify...
    for div in divs:
        h2 = div.find_element_by_tag_name('h2')
        if h2.text != '最多阅读':
            continue
        list = div.find_elements_by_tag_name('li')
        info = getArticleInfo(list[0])
        if info == None:
            logger.warning('did not find link from the article list.')
            return None
        logger.info('article: %s', info['title'])
        return info
    return None

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        return {'link': links[0].get_attribute('href'),
                'title':links[0].text}
    return None
