#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleInfo(driver):
    logger.info('looking for article')
    browser = driver.getBrowser()
    selector = 'div.basicteaser__wrap'
    divs = browser.find_elements_by_css_selector(selector)
    if len(divs) == 0:
        logger.warning('did not find aticle div: "%s"', selector)
        return None

    info = getArticleInfo(divs[0])
    if info == None:
        logger.warning('did not find link from the article list.')
        return None
    return info

def getArticleInfo(item):
    headline = item.find_element_by_tag_name('h2')
    link = headline.find_element_by_tag_name('a')
    return {'link': link.get_attribute('href'),
            'title':link.text}
