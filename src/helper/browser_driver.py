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

def isSameStrArray(s1, s2):
    if s1 == None and s2 == None:
        return True
    if s1 == None or s2 == None:
        return False
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False
    return True

class WebDriver(object):
    def __init__(self, settings=None):
        # default settings
        self.browser = 'Firefox'
        self.headless = False
        self.zoom = None
        self.pageWidth = 400
        self.configDir = None
        self.workingDir = os.path.abspath('.')
        self.userAgent = None   # or 'Mobile'

        setDir = dir(settings)
        if 'browser' in setDir:
            self.browser = settings.browser
        if 'headless' in setDir:
            self.headless = settings.headless
        if 'zoom' in setDir:
            self.zoom = settings.zoom
        if 'pageWidth' in setDir:
            self.pageWidth = settings.pageWidth
        if 'userAgent' in setDir:
            self.userAgent = settings.userAgent
        if 'configDir' in setDir and settings.configDir != None:
            if os.path.isdir(settings.configDir):
                self.configDir = settings.configDir
            else:
                logger.warning('configDir: "%s" does not exist', settings.configDir)
        if 'workingDir' in setDir and settings.workingDir != None:
            if os.path.isdir(settings.workingDir):
                self.workingDir = os.path.abspath(settings.workingDir)
            else:
                logger.warning('workingDir: "%s" does not exist', settings.workingDir)

        self.driver = None

        # user agent string from here:
        #   https://deviceatlas.com/blog/list-of-user-agent-strings
        if self.browser == 'Chrome':
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            if self.userAgent == 'Mobile':
                # Samsung Galaxy S8
                ua = 'Chrome/60.0.3112.107 Mobile Safari/537.36'
                options.add_argument('user-agent=' + ua)
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
            if self.userAgent == 'Mobile':
                # Samsung Galaxy S8
                ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv)'
                profile = webdriver.FirefoxProfile()
                profile.set_preference('general.useragent.override', ua)
                options.profile = profile
            self.driver = webdriver.Firefox(
                        firefox_options=options,
                        executable_path='/usr/local/bin/geckodriver')
        else:
            print('did not specify browser')

    def getPIDs(self):
        import psutil
        pids = []
        if self.browser == 'Firefox':
            pid = self.driver.capabilities['moz:processID']
        elif self.browser == 'Chrome':
            pid = self.driver.service.process.pid

        pids.append(pid)
        ps = psutil.Process(pid)
        for p in ps.children(recursive=True):
            pids.append(p.pid)
        return pids

    def getBrowser(self):
        return self.driver

    def loadPage(self, url):
        self.driver.get(url)

    def getCurrentUrl(self):
        return self.driver.current_url

    def close(self):
        self.driver.quit()

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
            tag = selector[:selector.find('.')]
            sClass = selector[(selector.find('.') + 1):]
            sClass = sClass.split('.')
            sClass.sort()
            divs = ele.find_elements_by_css_selector(selector)
            for div in divs:
                eClass = div.get_attribute('class')
                eClass = eClass.split()
                eClass.sort()
                if len(eClass) != len(sClass) or not isSameStrArray(eClass, sClass):
                    logger.debug('ignore: %s\n   "%s" <>\n   "%s"', tag, sClass, eClass)
                    continue
                logger.debug('set:\n   "%s"', selector)
                ele.execute_script("arguments[0].style.display = 'none';", div)

    def noneDisplayByIds(self, ids, element=None):
        ele = self.driver
        if element != None:
            ele = element
        for id in ids:
            divs = ele.find_elements_by_id(id)
            for div in divs:
                ele.execute_script("arguments[0].style.display = 'none';", div)

    def noneDisplayElements(self, elements=[]):
        for e in elements:
            self.driver.execute_script("arguments[0].style.display = 'none';", e)

    def saveFullPageToPng(self, fn):
        self.setWindowSize(self.pageWidth)
        time.sleep(2)
        if self.browser == 'Chrome':
            logger.debug('save Chrome page to %s', fn)
            pageLength = self.scrollToBottom()  # get length
            time.sleep(2)
            if self.zoom != None:
                self.setZoom(self.zoom)
                pageLength *= self.zoom / 100
            self.setWindowSize(self.pageWidth, pageLength)
            self.scrollToTop()
            self.driver.save_screenshot(fn)
        elif self.browser == 'Firefox':
            logger.debug('save Firefox page to %s', fn)
            if self.zoom != None:
                self.setZoom(self.zoom)
            pageLength = self.scrollToBottom()
            time.sleep(2)
            self.setWindowSize(self.pageWidth, pageLength)
            self.scrollToTop()
            body = self.driver.find_element_by_tag_name('body')
            png = body.screenshot_as_png    # some image does not been load if do once
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
