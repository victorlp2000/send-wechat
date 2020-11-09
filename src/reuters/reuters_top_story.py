#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleUrl(driver):
    logger.info('looking for article')

    # find topStory section
    name = 'topStory'
    section = driver.getBrowser().find_element_by_id(name)
    if section == None:
        logger.warning('did not find "%s" section.', name)
        return None

    # find title link
    try:
        title = section.find_element_by_css_selector('h2.story-title')
        link = title.find_element_by_tag_name('a')
        return link.get_attribute('href')

    except:
        logger.warning('did not find top story')
        return None
