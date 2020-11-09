#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def cleanupPage(driver, config):
    logger.info('cleaning content')
    driver.scrollToBottom()
    browser = driver.getBrowser()

    # 返回页首
    divs = browser.find_elements_by_css_selector('div.lx-commentary__top-link')
    for div in divs:
        browser.execute_script("arguments[0].style.display = 'none';", div)
    # 分类
    divs = browser.find_elements_by_id('core-navigation')
    for div in divs:
        buttons = div.find_elements_by_tag_name('button')
        for btn in buttons:
            browser.execute_script("arguments[0].style.display = 'none';", btn)

    navs = browser.find_elements_by_tag_name('nav')
    for nav in navs:
        role = nav.get_attribute('role')
        if role == 'navigation':
            logger.debug('role: %s', role)
            browser.execute_script("arguments[0].style.display = 'none';", nav)

    # links in line
    uls = browser.find_elements_by_tag_name('ul')
    for ul in uls:
        a = ul.find_elements_by_tag_name('a')
        li = ul.find_elements_by_tag_name('li')
        if len(li) == len(a):
            browser.execute_script("arguments[0].style.display = 'none';", ul)

    # 请告知您认可接受Cookies
    header = browser.find_element_by_tag_name('header')
    wrapper = header.find_element_by_tag_name('div')
    browser.execute_script("arguments[0].style.display = 'none';", wrapper)

    # <section class="AdContainer-"
    sections = browser.find_elements_by_tag_name('section')
    data = [
        'advertisement',
        'related-content-heading',  # 更多相关内容
        'top-stories-heading',      # 头条新闻
        'features-analysis-heading',    # 特别推荐
        'most-read',                # 热读
    ]
    for section in sections:
        e2e = section.get_attribute('data-e2e')
        if e2e in data:
            browser.execute_script("arguments[0].style.display = 'none';", section)
