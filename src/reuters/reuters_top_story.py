#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleInfo(driver):
    logger.info('looking for article')

    # find topStory section
    name = 'topStory'
    section = driver.getBrowser().find_element_by_id(name)
    if section == None:
        logger.info('did not find "%s" section.', name)
        return None

    # find title link
    try:
        title = section.find_element_by_css_selector('h2.story-title')
        link = title.find_element_by_tag_name('a')
        info = {'link': link.get_attribute('href'),
                'title':link.text}
        return info
    except:
        logger.warning('did not find top story')
        return None
