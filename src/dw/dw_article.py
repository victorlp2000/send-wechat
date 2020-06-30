#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time
import urllib.parse

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn):
    logger.info('loading "%s"', urllib.parse.unquote(url))
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)
    driver.scrollToBottom()
    time.sleep(3)   # for loading completely
    browser = driver.getBrowser()
    cleanPage(browser)

    return driver.saveFullPageToJpg(fn)

def nonDisplayElements(browser, elements):
    for e in elements:
        browser.execute_script("arguments[0].style.display = 'none';", e)

def cleanPage(browser):
    logger.info('cleaning content...')
    divs = browser.find_elements_by_tag_name('div')
    for div in divs:
        prop = div.get_attribute('itemprop')
        if prop == 'articleBody':
            # remove 'div', 'section'
            elements = div.find_elements_by_tag_name('div')
            nonDisplayElements(browser, elements)
            elements = div.find_elements_by_tag_name('section')
            nonDisplayElements(browser, elements)

    footer = browser.find_element_by_tag_name('footer')
    sections = footer.find_elements_by_tag_name('section')
    for s in sections:
        prop = s.get_attribute('itemprop')
        if prop != 'copyrightHolder':
            nonDisplayElements(browser, [s])

    follow = browser.find_element_by_css_selector('div.followus')
    nonDisplayElements(browser, [follow])

    cookie = browser.find_element_by_css_selector('div.cookie__wrap')
    nonDisplayElements(browser, [cookie])
