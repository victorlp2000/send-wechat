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
    selector = 'div.teaserContentWrap'
    divs = driver.getBrowser().find_elements_by_css_selector(selector)
    if len(divs) == 0:
        logger.warning('did not find aticle div: "%s"', selector)
        return None

    info = getArticleInfo(divs[0])
    if info == None:
        logger.warning('did not find link from the article list.')
        return None

    logger.info('article: %s', info['title'])
    return info

def getArticleInfo(item):
    links = item.find_elements_by_tag_name('a')
    if len(links) > 0:
        title = links[0].find_elements_by_tag_name('h2')
        return {'link': links[0].get_attribute('href'),
                'title':title[0].text}
    return None
