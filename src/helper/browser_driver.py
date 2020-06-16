#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import time, os
import shutil

from selenium import webdriver
from helper.my_logger import getMyLogger
from util.png2jpg import convertToJpeg

logger = getMyLogger(__name__)

class WebDriver(object):
    def __init__(self, settings=None):
        # default settings
        self.browser = 'Chrome'
        self.headless = True
        self.zoom = 100
        self.pageWidth = 400
        self.configDir = None
        self.workingDir = os.path.abspath('.')

        setDir = dir(settings)
        if 'browser' in setDir:
            self.browser = settings.browser
        if 'headless' in setDir:
            self.headless = settings.headless
        if 'zoom' in setDir:
            self.zoom = settings.zoom
        if 'pageWidth' in setDir:
            self.pageWidth = settings.pageWidth
        if 'configDir' in setDir:
            self.configDir = settings.configDir
        if 'workingDir' in setDir:
            self.workingDir = os.path.abspath(settings.workingDir)

        self.driver = None

        if self.browser == 'Chrome':
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            if self.configDir is not None:
                # config data will be changed a lot at run time
                # we'd like to keep user's config data clean
                # use copy in /tmp folder
                dst = '/tmp/ChromeConfig'
                shutil.rmtree(dst, ignore_errors=True)
                shutil.copytree(configDir, dst)

                options.add_argument("--user-data-dir=" + dst)

            self.driver = webdriver.Chrome(
                        chrome_options=options,
                        executable_path='/usr/local/bin/chromedriver')
        elif self.browser == 'Firefox':
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.set_headless()
            self.driver = webdriver.Firefox(
                        firefox_options=options,
                        executable_path='/usr/local/bin/geckodriver')
        else:
            print('did not specify browser')

    def getBrowser(self):
        return self.driver

    def loadPage(self, url):
        self.driver.get(url)

    def getCurrentUrl(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()

    def getWindowSize(self):
        return self.driver.get_window_size()

    # ubuntu min window width: 508
    def setWindowSize(self, width, height=None):
        if width is None or height is None:
            wsize = self.getWindowSize()
        if width is None:
            width = wsize['width']
        if height is None:
            height = wsize['height']

        # scroll to bottom causes loading all visible objects
        self.driver.set_window_size(width, height)

    def setZoom(self, zoom):
        if zoom is not None:
            if self.browser == 'Chrome':
                self.driver.execute_script("document.body.style.zoom='" + str(zoom) + "%'")
            else:
                self.driver.execute_script("document.body.style.transform = 'scale(" + str(zoom/100) + ")'")
                self.driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

    # !!! Firefox does not work right??
    def scrollToBottom(self):
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while match==False:
            lastCount = lenOfPage
            # time.sleep(1)
            lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
        # time.sleep(1)
        return lenOfPage

    def scrollToTop(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def findElementsByCssSelector(self, css_selectors):
        return self.driver.find_elements_by_css_selector(css_selectors)

    def findElementsByTagName(self, tag):
        return self.driver.find_elements_by_tag_name(tag)

    def findElementByName(self, name):
        try:
            element = self.driver.find_element_by_name(name)
            return element
        except:
            logger.error('did not find element with name: "%s"', name)
            return None

    def findElementById(self, id):
        try:
            element = self.driver.find_element_by_id(id)
            return element
        except:
            logger.error('did not find element with id: "%s"', id)
            return None

    def noneDisplayByCSSSelectors(self, css_selectors, element=None):
        ele = self.driver
        if element != None:
            ele = element
        # set display:none for specified tag blocks
        for selector in css_selectors:
            divs = ele.find_elements_by_css_selector(selector)
            for div in divs:
                ele.execute_script("arguments[0].style.display = 'none';", div)

    def noneDisplayByIds(self, ids, element=None):
        ele = self.driver
        if element != None:
            ele = element
        for id in ids:
            divs = ele.find_elements_by_id(id)
            for div in divs:
                ele.execute_script("arguments[0].style.display = 'none';", div)

    def saveFullPageToPng(self, fn):
        self.setZoom(self.zoom)
        pageLength = self.scrollToBottom()
        time.sleep(2)
        self.scrollToTop()
        if self.browser == 'Chrome':
            logger.debug('save Chrome page to %s', fn)
            pageLength *= self.zoom / 100
            self.setWindowSize(self.pageWidth, pageLength)
            # for headless browser
            self.driver.save_screenshot(fn)
        elif self.browser == 'Firefox':
            logger.debug('save Firefox page to %s', fn)
            self.setWindowSize(self.pageWidth, pageLength)
            body = self.driver.find_element_by_tag_name('body')
            png = body.screenshot_as_png
            with open(fn, "wb") as file:
                file.write(png)
        else:
            logger.error('unknown browser: "%s"', self.browser)

        if os.path.exists(fn) and os.path.getsize(fn) > 0:
            return fn
        logger.debug(' save failed.')
        return None

    def saveFullPageToJpg(self, fn):
        logger.info('save to %s', fn)
        imgf = self.saveFullPageToPng(fn + '.png')
        logger.debug('tmp file %s', imgf)
        if imgf != None:
            r = convertToJpeg(imgf, fn)
            os.remove(imgf)
            logger.debug('return file %s', r)
            return r
        return None

if __name__ == '__main__':
    pass
