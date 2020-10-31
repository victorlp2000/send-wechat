#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

# find 'most-read' article from the current page
# return {link, title} or None
def findArticleInfo(driver):
    logger.info('looking for article')
    browser = driver.getBrowser()

    h2s = browser.find_elements_by_tag_name('h2')
    for h2 in h2s:
        if h2.text != '最多阅读':
            continue
        a = h2.find_element_by_xpath('../ol/li[1]/h3/a')
        link =  a.get_attribute('href')
        title = a.text
        if link and title:
            return {'link': link, 'title': title}
    logger.info('did not find article')
    return None
