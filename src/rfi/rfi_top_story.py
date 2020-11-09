#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def findArticleUrl(driver):
    logger.info('looking for article')
    browser = driver.getBrowser()

    xpath = '/html/body/div[2]/div[3]/section[1]/div/div[1]/div[1]/div/a'
    a = browser.find_element_by_xpath(xpath)
    return a.get_attribute('href')
