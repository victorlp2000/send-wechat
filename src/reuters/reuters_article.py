#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 15, 2020
# By: Weiping Liu

import os, time
from datetime import datetime
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn):
    logger.info('loading "%s"', url)
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)

    driver.scrollToBottom()     # make all content visible, then do clean
    time.sleep(3)               # elements may not show if not visible
    cleanPage(driver)

    innerHTML = '<center>' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</center>'
    innerHTML += url
    driver.insertTopDiv(innerHTML)

    return driver.saveFullPageToJpg(fn)

def cleanPage(driver):
    logger.info('cleaning content...')
    selectors = [
        # 广告
        'div.DPSlot_container.StandardArticleBody_dp-slot-inline.StandardArticleBody_inline-canvas',
        'div.DPSlot_container.StandardArticleBody_dp-slot-inline',
        'div.StandardArticleBody_dp-slot-inline',
        # 下一篇文章, 更多文章
        'div.RelatedCoverage_related-coverage-module.module.RelatedCoverage_recirc',
        # Paid promotional links, More from Reuters,
        'div.StandardArticleBody_dianomi-container.dianomi_context',
        # 移动应用 邮件订阅 Reuters Plus 广告选择 使用条款 隐私保护
        'div.Footer_links',
        'div.Footer_social',
        # 'div.Sticky_track.Leaderboard_sticky-container',
        # 'div.DPSlot_container.StandardArticleBody_dp-slot-inline.StandardArticleBody_inline-canvas',
        # 'div.DPSlot_container',
        # 'div.TrendingStories_container',
        # 'div.footer-container',
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    # ids = [
    # ]
    # driver.noneDisplayByIds(ids)

    # articleBody = driver.driver.find_element_by_css_selector('div.StandardArticleBody_body')
    # # convert links into <img>, so it get showing
    # links = articleBody.find_elements_by_tag_name('a')
    # for link in links:
    #     if link.text.startswith('tmsnrt.rs'):
    #         print(link.get_attribute('href'))
    #         iframe = '<iframe width="' + str(driver.pageWidth) + 'px" src=\"' + link.get_attribute('href') + '"></iframe>'
    #         driver.driver.execute_script('arguments[0].innerHTML=arguments[1]', link, iframe)
