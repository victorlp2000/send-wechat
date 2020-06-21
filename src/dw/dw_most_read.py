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

    section = findMostReadSection(driver)
    if section == None:
        return None

    list = section.find_elements_by_css_selector('div.linkList.plain')
    if len(list) == 0:
        logger.warning('did not find aticle list.')
        return None

    # in the list, we only care the first item
    info = getArticleInfo(list[0])
    if info == None:
        logger.warning('did not find link from the article list.')
        return None

    logger.info('article: %s', info['title'])
    return info

def findMostReadSection(driver):
    # find the most-read-section in about 10 sections
    sections = driver.findElementsByCssSelector('h4.meta')
    logger.debug('found %d sections in the page.', len(sections))
    for section in sections:
        text = section.text
        logger.debug('section: %s', text)
        if text != '最多阅读':
            continue
        return section.find_element_by_xpath('..')
    logger.info('did not find most-read section')
    return None

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        return {'link': links[0].get_attribute('href'),
                'title':links[0].text}
    return None
