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
    cleanPage(driver)

    return driver.saveFullPageToJpg(fn)

def nonDisplayElements(browser, elements):
    for e in elements:
        browser.execute_script("arguments[0].style.display = 'none';", e)

def cleanPage(driver):
    logger.info('cleaning content...')
    browser = driver.getBrowser()
    # make header position fixed
    header = browser.find_element_by_tag_name('header')
    browser.execute_script("arguments[0].style.position = 'absolute';", header)

    # <div id="DW_M_Articles_Leaderboard-label" class="advertisement advertisement--leaderboard advertisement--detail" style="display: block;">
    # <div id="DW_M_Articles_Rectangle-1-label" class="advertisement advertisement--rectangle advertisement--detail" style="display: block;"
    selectors = [
        'div.advertisement__advertisement', # 广告
        'div.followus',   # 关注我们
        'section.offset_border',    #
        'section.relatedsubjects',  # 主题
        # div class="feedbackteaser feedbackteaser--linkelement"
        'div.feedbackteaser.feedbackteaser--linkelement',   # 意见反馈
        'section.rutscheteaser__wrap',  # 相关内容
        'ul.footer__sectionlist',
        'div.footer__meta',
        'div.cookie.cookie--visible',
    ]
    driver.noneDisplayByCSSSelectors(selectors)
