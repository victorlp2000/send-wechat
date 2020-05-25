#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

class Article(object):
    #
    def __init__(self, driver=None):
        self.driver = driver
        if driver == None:
            raise ValueError("driver need to be set in Article(driver).")

    def setPageSize(self, width=400, height=600):
        # scroll to bottom causes loading all visible objects
        self.driver.set_window_size(width, height)
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while match==False:
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
        # self.driver.execute_script("window.scrollTo(0, 0);")

    def disableElements(self, css_selectors):
        # set display:none for specified tag blocks
        for selector in css_selectors:
            divs = self.driver.find_elements_by_css_selector(selector)
            for div in divs:
                self.driver.execute_script("arguments[0].style.display = 'none';", div)

    def disableIds(self, ids):
        for id in ids:
            divs = self.driver.find_elements_by_id(id)
            for div in divs:
                self.driver.execute_script("arguments[0].style.display = 'none';", div)

    def savePageAsImageFile(self, fn):
        # save page to png file
        body = self.driver.find_element_by_tag_name('body')
        png = body.screenshot(fn)
