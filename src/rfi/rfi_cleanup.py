#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import time
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def closePopup(div):
    print('close popup')
    div.find_element_by_tag_name('a').click()
    return

def cleanupPage(driver):
    logger.info('cleaning content')
    browser = driver.getBrowser()

    check = 10
    while check > 0:
        print(check)
        div = browser.find_elements_by_css_selector('div.didomi-popup-view')
        if len(div) > 0:
            closePopup(div[0])
            break
        check -= 1
        time.sleep(1)

    # header position at top
    body = browser.find_element_by_tag_name('body')
    browser.execute_script("arguments[0].style.padding = '0px';", body)
    header = browser.find_element_by_tag_name('header')
    browser.execute_script("arguments[0].style.position = 'relative';", header)

    selectors = [
        'div.tms-ad',
        'div.m-block-ad',
        'div.t-content__tags',
        'div.t-content__related',
        'div.t-content__list-content',
    ]
    for selector in selectors:
        divs = browser.find_elements_by_css_selector(selector)
        for div in divs:
            browser.execute_script("arguments[0].style.display = 'none';", div)
