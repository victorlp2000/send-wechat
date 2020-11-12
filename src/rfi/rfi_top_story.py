#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleUrl(driver):
    logger.info('looking for article')
    browser = driver.getBrowser()

    selector = 'div.m-item-list-article.m-item-list-article--main-article'
    div = browser.find_element_by_css_selector(selector)
    a = div.find_element_by_tag_name('a')
    return a.get_attribute('href')
