#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleUrl(driver):
    logger.info('looking for article')

    browser = driver.getBrowser()
    # find topStory section
    topStory = browser.find_element_by_css_selector('div.topStory')
    if topStory == None:
        logger.warning('did not find topStory.')
        return None

    # find title link
    try:
        link = topStory.find_element_by_tag_name('a')
        return link.get_attribute('href')

    except:
        logger.warning('did not find top story')
        return None
