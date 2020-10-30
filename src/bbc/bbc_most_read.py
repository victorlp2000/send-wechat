#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleInfo(driver):
    logger.info('looking for most read article')
    browser = driver.getBrowser()

    section = findMostReadSection(browser)
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
    return info

def findMostReadSection(browser):
    # find the most-read-section in about 10 sections
    sections = browser.find_elements_by_tag_name('section')
    logger.debug('found %d sections in the page.', len(sections))
    for section in sections:
        label = section.get_attribute('aria-labelledby')
        logger.debug('section in the page "%s"', label)
        if label == 'Most-Read':
            return section
    logger.warning('!! did not find "Most-Read" section.')
    return None

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        return {'link': links[0].get_attribute('href'),
                'title':links[0].text}
    return None
