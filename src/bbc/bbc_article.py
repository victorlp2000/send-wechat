#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time
from datetime import datetime

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn, type):
    logger.info('loading "%s"', url)
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)
    time.sleep(3)   # for loading completely
    cleanPage(driver)

    innerHTML = type + ' ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    innerHTML += '<br>' + url
    driver.insertTopDiv(innerHTML)

    return driver.saveFullPageToJpg(fn)

def cleanPage(driver):
    logger.info('cleaning content...')
    selectors = [
        'div.bbccom_slot.mpu-ad.bbccom_standard_slot.bbccom_visible',
        # 'ul.story-body__unordered-list',
        'div.share__back-to-top.ghost-column',
        'div.column--secondary',
        'div.navigation--footer',
        'div.story-more',
        'div.tags-container',
        'div.share.share--lightweight.show.ghost-column'
    ]
    ids = [
        'bbccom_leaderboard_1_2_3_4',
        'bbccom_mpu_1_2',
        'core-navigation',
        'orb-aside',
        'comp-small-promo-group',
        'pulse-container'
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)

    browser = driver.getBrowser()

    list = browser.find_elements_by_tag_name('ul')
    for ul in list:
        a = ul.find_elements_by_tag_name('a')
        li = ul.find_elements_by_tag_name('li')
        if len(li) == len(a):
            browser.execute_script("arguments[0].style.display = 'none';", ul)

    # 请告知您认可接受Cookies
    header = browser.find_element_by_tag_name('header')
    wrapper = header.find_element_by_tag_name('div')
    browser.execute_script("arguments[0].style.display = 'none';", wrapper)

    # <section class="AdContainer-..."
    sections = browser.find_elements_by_tag_name('section')
    for section in sections:
        e2e = section.get_attribute('data-e2e')
        if e2e == 'advertisement' or e2e == 'related-content-heading' or e2e == 'top-stories-heading' or e2e == 'features-analysis-heading' or e2e == 'most-read':
            browser.execute_script("arguments[0].style.display = 'none';", section)
