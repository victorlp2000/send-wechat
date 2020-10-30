#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time

from helper.my_logger import getMyLogger
from helper.set_article import setArticle

logger = getMyLogger(__name__)

def cleanupPage(driver):
    logger.info('cleaning content...')
    browser = driver.getBrowser()

    navs = browser.find_elements_by_tag_name('nav')
    for nav in navs:
        role = nav.get_attribute('role')
        if role == 'navigation':
            print(role)
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

    # <section class="AdContainer-..."
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
