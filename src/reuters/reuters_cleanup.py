#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 15, 2020
# By: Weiping Liu

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def cleanupPage(driver):
    logger.info('cleaning content')
    browser = driver.getBrowser()

    divs = browser.find_elements_by_tag_name('div')
    for div in divs:
        classes = div.get_attribute('class')
        ss = classes.split()
        rm = False
        for s in ss:
            rm |= s.startswith('StickyContainer_')
            rm |= s.startswith('AdSlot_')
            rm |= s.startswith('RelatedArticles-container')
            rm |= s.startswith('ArticlePage-dianomi')
            rm |= s.startswith('SocialTools_')
            # rm |= s.startswith('RecircRibbon-container-')
        if rm:
            browser.execute_script("arguments[0].style.display = 'none';", div)

    uls = browser.find_elements_by_tag_name('ul')
    for ul in uls:
        role = ul.get_attribute('role')
        if role == 'site-links':
            browser.execute_script("arguments[0].style.display = 'none';", ul)
