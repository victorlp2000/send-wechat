#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getTimePoints(driver):
    browser = driver.getBrowser()
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
