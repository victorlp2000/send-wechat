#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 21, 2020
# By: Weiping Liu

import urllib.parse

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def cleanupPage(driver):
    browser = driver.getBrowser()
    try:
        full = browser.find_element_by_link_text(u'全文')
        fullLink = full.get_attribute('href')
        logger.info('loading full "%s"', urllib.parse.unquote(fullLink))
        browser.get(fullLink)
    except:
        logger.error('did not find full page link.')
        pass

    logger.info('cleaning content')

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
        'nologincomment',
        'subscribe-now-container',
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)

    browser = driver.getBrowser()

    divs = browser.find_elements_by_tag_name('div')
    for div in divs:
        id = div.get_attribute('id')
        if id.startswith('google_ad'):
            driver.noneDisplayByIds([id])

    # 关于我们 加入我们 问题回馈 联系方式 合作伙伴 服务条款 广告业务 版权声明 最新动态
    footer = browser.find_elements_by_css_selector('div.footer-inner')
    if len(footer) > 0:
        links = footer[0].find_elements_by_tag_name('a')
        driver.noneDisplayElements(links)

    links = browser.find_elements_by_partial_link_text('读者评论')
    driver.noneDisplayElements(links)

    # make header stay at top
    header = browser.find_element_by_css_selector('div.o-nav')
    browser.execute_script("arguments[0].style.position = 'relative';", header)
