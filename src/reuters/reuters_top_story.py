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

    # find topStory section
    name = 'topStory'
    section = driver.findElementById(name)
    if section == None:
        logger.info('did not find "%s" section.', name)
        return None

    # find title link
    try:
        title = section.find_element_by_css_selector('h2.story-title')
        link = title.find_element_by_tag_name('a')
        info = {'link': link.get_attribute('href'),
                'title':link.text}
        logger.info('article: %s', info['title'])
        return info
    except:
        logger.warning('did not find top story')
        return None
