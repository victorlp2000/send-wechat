#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  July 2, 2020
# By: Weiping Liu

import time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getMainInfo(driver, url):
    logger.info('loading: %s', url)
    driver.loadPage(url) # open the home page
    time.sleep(2)
    browser = driver.getBrowser()

    # 1. find main class
    main = browser.find_element_by_css_selector('div.main')

    # 2. from main class, find all 'basicteaser'
    selector = 'article.teaser'
    teasers = browser.find_elements_by_css_selector(selector)

    # 3. ignore ad, take articles
    print(len(teasers))
    articles = []
    for teaser in teasers:
        div = teaser.find_element_by_tag_name('div')
        # pick article, ignore ad
        basic = 'basicteaser'
        if div.get_attribute('class') != basic:
            continue
        articles.append(div)

    if len(articles) == 0:
        logger.warning('did not find aticles')
        return None

    mainInfo = getArticlesInfo(articles)
    if mainInfo == None:
        logger.warning('did not find link from the article list.')
        return None

    logger.info('%d articles', len(mainInfo))
    return mainInfo

def getArticlesInfo(articles):
    info = []
    for item in articles:
        headline = item.find_element_by_tag_name('h2')
        link = headline.find_element_by_tag_name('a')
        href = link.get_attribute('href')
        if href.startswith('https://m.dw.com/zh/'):
            info.append({'link': href, 'title':link.text})
    return info
