#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn):
    logger.info('loading "%s"', url)
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)
    time.sleep(3)   # for loading completely
    cleanPage(driver)
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
    '''
    <section>
        <div id="pulse-container" class="pulse-banner orb-banner-wrapper">
            <div class="orb-banner b-g-p b-r b-f">
                <div class="orb-banner-inner">
                    <h2 class="orb-banner-title">请您自我介绍</h2>
                    <div class="orb-banner-content">
                        <p>我们长期致力于网站的改进，您的意见很重要</p>
                        <p class="pulse-question">您能用几分钟告诉我们您对这个网站的看法吗?</p>
                    </div>
                    <ul class="orb-banner-options">
                        <li><a href="{{pulseaccepthref}}" id="pulse-accept">能</a></li>
                        <li><button type="button" id="pulse-reject">不能</button></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    '''
    unordered = 'ul.story-body__unordered-list'
    list = driver.findElementsByCssSelector(unordered)
    browser = driver.getBrowser()
    for ul in list:
        a = ul.find_elements_by_tag_name('a')
        li = ul.find_elements_by_tag_name('li')
        if len(li) == len(a):
            browser.execute_script("arguments[0].style.display = 'none';", ul)
