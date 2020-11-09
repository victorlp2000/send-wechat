#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

# return
#   meta = {
#       link:
#       title:
#       live:
#       ...
#   }
def getArticleMeta(driver, url):
    meta = {}
    browser = driver.getBrowser()

    if url == '':
        return meta

    browser.get(url)

    # url
    meta['url'] = url

    if url.find('/live/') > 0:
        getLiveMeta(browser, meta)
    else:
        getMeta(browser, meta)
    return meta

def getMeta(browser, meta):
    xpath = '//*[@id="main-wrapper"]/div/div/div[1]/main'
    content = browser.find_element_by_xpath(xpath)

    # title
    xpath = '//*[@id="content"]'
    title = content.find_element_by_xpath(xpath)
    meta['title'] = title.text

    # author
    author = content.find_element_by_xpath('//div[2]/div/ul')
    meta['author'] = author.text
    return meta

def getLiveMeta(browser, meta):
    # title
    xpath = '//*[@id="lx-event-title"]'
    title = browser.find_element_by_xpath(xpath)
    meta['title'] = title.text

    # timePoints
    timePoints = getTimePoints(browser)
    if timePoints != None:
        meta['live'] = getTimePoints(browser)

    return meta

def getTimePoints(browser):
    items = None
    # if there is button '直播报道'
    buttons = browser.find_elements_by_tag_name('button')
    if len(buttons) == 0:
        return None
    for b in buttons:
        if b.text == '直播报道':
            items = []
            break
    if items == None:
        return None

    list = browser.find_elements_by_css_selector('ol.gs-u-m0.gs-u-p0.lx-stream__feed.qa-stream')
    if len(list) == 0:
        return None

    times = list[0].find_elements_by_tag_name('time')
    if len(times) == 0:
        return None
    items = []
    for i in times:
        t = i.find_element_by_css_selector('span.qa-post-auto-meta')
        items.append(t.text)
    return items