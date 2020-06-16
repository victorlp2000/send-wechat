#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 10, 2020
# By: Weiping Liu

import time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getLeadArticleInfo(driver, url):
    logger.info('loading: %s', url)
    driver.loadPage(url) # open the home page
    time.sleep(1)
    # <div id="sectionLeadPackage">
    #   ...
    # </div>
    div = driver.findElementById('sectionLeadPackage')
    if div == None:
        return None

    info = getArticleInfo(div)
    if info == None:
        return None

    logger.info('article: %s', info['title'])
    return info

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        return {'link': links[0].get_attribute('href'),
                'title':links[0].text}
    logger.warning('did not find article link.')
    return None
