#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  July 2, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleInfo(driver):
    browser = driver.getBrowser()

    content = browser.find_element_by_id('content')
    ul = content.find_element_by_tag_name('ul')
    li = ul.find_element_by_tag_name('li')

    # in the list, we only care the first item
    info = getArticleInfo(li)
    if info == None:
        logger.warning('did not find link from the article list.')
        return None
    return info

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        return {'link': links[0].get_attribute('href'),
                'title':links[0].get_attribute('title')}
    return None
