#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import time
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def closePopup(div):
    buttons = div.find_elements_by_tag_name('button')
    for button in buttons:
        if button.get_attribute('id') == 'didomi-notice-agree-button':
            logger.info('closed popup button')
            button.click()
    return

def cleanupPage(driver, config):
    logger.info('cleaning content')
    driver.scrollToBottom(1.5)
    browser = driver.getBrowser()

    check = 10
    while check > 0:
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

    # overwrite existing ::before style, as it covers the header info
    js = '''
        var myStyle = document.createElement('style');
        var myCss = '.o-header .o-header__inner .o-header__inner__background::before {height:0px;}';
        myStyle.innerHTML = myCss;
        document.body.insertBefore(myStyle, arguments[0]);
        '''
    oHeader = browser.find_element_by_css_selector('div.o-header')
    browser.execute_script(js, oHeader)

    div = oHeader.find_element_by_css_selector('div.o-site-nav-wrapper')
    browser.execute_script("arguments[0].style.display = 'none';", div)

    selectors = [
        'div.tms-ad',
        'div.m-block-ad',
        'div.t-content__tags',
        'div.t-content__related',
        'div.t-content__list-content',
        'div.o-self-promo'
    ]
    for selector in selectors:
        divs = browser.find_elements_by_css_selector(selector)
        for div in divs:
            browser.execute_script("arguments[0].style.display = 'none';", div)
