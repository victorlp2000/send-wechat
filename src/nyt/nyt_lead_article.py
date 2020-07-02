#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 10, 2020
# By: Weiping Liu

import time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getLeadArticleInfo(driver, url):
    logger.info('loading: %s', url)
    driver.loadPage(url) # open the home page
    time.sleep(1)
    browser = driver.getBrowser()

    list = getArticleList(browser)
    if len(list) == 0:
        logger.warning('did not find item in list')
        return None
    info = getArticleInfo(list[0])
    if info == None:
        return None

    logger.info('article: %s', info['title'])
    return info

def getArticleList(browser):
    selector = 'ol.article-list'
    try:
        ol = browser.find_element_by_css_selector(selector)
    except:
        logger.warning('did not find "%s"', selector)
        return []

    list = ol.find_elements_by_tag_name('li')
    return list

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        h2 = links[0].find_element_by_tag_name('h2')
        return {'link': links[0].get_attribute('href'),
                'title':h2.text}
    logger.warning('did not find article link.')
    return None
