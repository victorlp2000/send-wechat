#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getTopStoryInfo(driver, url):
    logger.info('loading: %s', url)
    driver.loadPage(url) # open the home page
    time.sleep(2)
    section = findTopStorySection(driver)
    if section == None:
        return None

    list = section.find_elements_by_tag_name('li')
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

def findTopStorySection(driver):
    # find the section in sections
    name = 'Top-stories'
    sections = driver.findElementsByTagName('section')
    logger.debug('found %d sections in the page.', len(sections))
    for section in sections:
        label = section.get_attribute('aria-labelledby')
        logger.debug('section in the page "%s"', label)
        if label == name:
            return section
    logger.warning('!! did not find "%s" section.', name)
    return None

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        return {'link': links[0].get_attribute('href'),
                'title':links[0].text}
    return None
