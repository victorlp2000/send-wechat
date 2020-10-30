#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 21, 2020
# By: Weiping Liu

import time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleInfo(driver):
    logger.info('looking for article')

    item = findTopStoryItem(driver)
    if item == None:
        return None

    # in the list, we only care the first item
    return getArticleInfo(item)

def findTopStoryItem(driver):
    # first 'div.item-inner' in 'div.items'
    selector = 'div.block-container.dark-green.has-side.side-right.all'
    items = driver.driver.find_elements_by_css_selector(selector)
    # items = driver.driver.find_elements_by_css_selector('div.items')
    logger.debug('%d of "div.items" found.', len(items))
    if len(items) == 0:
        logger.warning('did not find list items')

    item = items[0].find_element_by_css_selector('div.item-inner')
    logger.debug('%d inner items found', len(items))
    return item

def getArticleInfo(item):
    try:
        link = item.find_element_by_css_selector('a.item-headline-link')
        classes = link.get_attribute('class').split()
        for c in classes:
            if c == 'locked':
                return None

        return {'link': link.get_attribute('href'),
                'title':link.text}
    except:
        logger.warning('did not find link item')
        return None
