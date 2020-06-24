#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 21, 2020
# By: Weiping Liu

import os, time
import urllib.parse

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn):
    logger.info('loading "%s"', urllib.parse.unquote(url))
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)
    try:
        # if there is <a href="/story/001088254?adchannelID=&amp;full=y">全文</a>
        full = driver.getBrowser().find_element_by_link_text(u'全文')
        fullLink = full.get_attribute('href')
        logger.info('loading full "%s"', urllib.parse.unquote(fullLink))
        driver.loadPage(fullLink)
    except:
        pass
    driver.scrollToBottom()
    time.sleep(3)   # for loading completely
    cleanPage(driver)

    return driver.saveFullPageToJpg(fn)

def cleanPage(driver):
    logger.info('cleaning content...')
    selectors = [
        'div.story-action',     # left-side action menu
        'div.side-container',   # right-side column
        'div.o-ads.in-article-advert',  # ads
        'div.promo-box-container',   # promotion box
        'div.subscription-promo-container.show-image-in-mobile.noneSubscriber',
        'div.o-ads.o-ads--center',
        'div.o-ads__outer'
    ]
    ids = [
        'nologincomment'
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)

    browser = driver.driver
    footer = browser.find_elements_by_css_selector('div.footer-inner')
    if len(footer) > 0:
        links = footer[0].find_elements_by_tag_name('a')
        driver.noneDisplayElements(links)

    links = browser.find_elements_by_partial_link_text('读者评论')
    driver.noneDisplayElements(links)
