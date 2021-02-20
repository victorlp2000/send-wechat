#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleUrl(driver):
    logger.info('looking for article')
    browser = driver.getBrowser()

    ols = browser.find_elements_by_tag_name('ol')
    if len(ols) == 0:
        logger.warning('did not find article url')
        return None

    lis = ols[0].find_elements_by_tag_name('li')
    if len(lis) == 0:
        logger.warning('did not find article url')
        return None

    links = lis[0].find_elements_by_tag_name('a')
    if len(links) > 0:
        return links[0].get_attribute('href')

    return None
