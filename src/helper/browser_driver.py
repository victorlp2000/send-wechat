#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import time, os
import shutil
from PIL import Image
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
    def __init__(self, settings):
        # default settings
        self.browser = 'Firefox'
        self.headless = False
        self.zoom = None
        self.devScale = 1
        self.pageWidth = None
        self.configDir = None
        self.workingDir = os.path.abspath('.')
        self.userAgent = None   # or 'Mobile'

        if 'browser' in settings:
            self.browser = settings['browser']
        if 'headless' in settings:
            self.headless = settings['headless']
        if 'zoom' in settings:
            self.zoom = settings['zoom']
        if 'devScale' in settings:
            self.devScale = settings['devScale']
        if 'pageWidth' in settings:
            self.pageWidth = settings['pageWidth'] / self.devScale
        if 'userAgent' in settings:
            self.userAgent = settings['userAgent']
        if 'configDir' in settings and settings['configDir'] != None:
            if os.path.isdir(settings['configDir']):
                self.configDir = settings['configDir']
            else:
                logger.warning('configDir: "%s" does not exist', settings['configDir'])
        if 'workingDir' in settings and settings['workingDir'] != None:
            if os.path.isdir(settings['workingDir']):
                self.workingDir = os.path.abspath(settings['workingDir'])
            else:
                logger.warning('workingDir: "%s" does not exist', settings['workingDir'])

        self.driver = None

        # user agent string from here:
        #   https://deviceatlas.com/blog/list-of-user-agent-strings
        if self.browser == 'Chrome':
            options = webdriver.ChromeOptions()
            if self.devScale:
                options.add_argument('--force-device-scale-factor=' + str(self.devScale))
            if self.headless:
                options.add_argument('--headless')
            if self.userAgent == 'Mobile':
                # Mobile phone web browser
                ua = 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'
                logger.debug('set userAgent: %s', ua)
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
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.zoom.full', False)
            # profile.set_preference('browser.zoom.siteSpecific', False)
            # profile.set_preference('layout.css.devPixelsPerPx', '2.0')
            # profile.set_preference('font.minimum-size.zh-CN', 20)
            # profile.set_preference('font.size.monospace.zh-CN', 16)
            # profile.set_preference('browser.display.auto_quality_min_font_size', 40)
            if self.headless:
                options.set_headless()
            if self.userAgent == 'Mobile':
                # Samsung Galaxy S8
                ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv)'
                logger.info('set userAgent: %s', ua)
                profile.set_preference('general.useragent.override', ua)
            options.profile = profile
            self.driver = webdriver.Firefox(
                        firefox_options=options,
                        executable_path='/usr/local/bin/geckodriver')
        else:
            logger.error('!! did not specify browser')

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

    # ubuntu min window width: 508
    def setWindowSize(self, width, height=None):
        if width is None or height is None:
            wsize = self.driver.get_window_size()
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
        scrollHeight = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        viewHeight = self.driver.execute_script("return window.innerHeight")
        top = 0
        while top + viewHeight < scrollHeight:
            top += viewHeight
            logger.debug('scrolling: %d', top)
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight;")
            self.driver.execute_script("window.scrollTo(0, {0})".format(top))
            time.sleep(2)
            scrollHeight = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        return scrollHeight

    def getPageLength(self):
        h1 = self.scrollToBottom()
        logger.debug('scrollToBottom: %d', h1)
        h2 = self.driver.execute_script("return document.body.scrollHeight;")
        logger.debug('body.scrollHeight: %d', h2)
        elem = self.driver.find_element_by_tag_name('body')
        h4 = self.driver.execute_script('return parseInt(window.getComputedStyle(arguments[0]).height);', elem)
        logger.debug('computed height: %d', h4)
        h5 = elem.size['height']
        logger.debug('element size height: %d', h4)
        return max(h1, h2, h4, h5)

    def scrollToTop(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

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
        body = self.driver.find_element_by_tag_name('html')
        self.driver.execute_script("arguments[0].style.overflow = 'hidden';", body)

        self.setWindowSize(self.pageWidth, 1080)
        if self.browser == 'Chrome':
            logger.debug('save Chrome page to %s', fn)
            if self.zoom != None:
                self.setZoom(self.zoom)

            pageLength = self.getPageLength()  # get length

            # if self.zoom != None:
                # pageLength *= self.zoom / 100
            # logger.info('zoom length: %d', pageLength)

            self.setWindowSize(self.pageWidth, pageLength)
            self.scrollToTop()

            wSize = self.driver.get_window_size()
            logger.warning('page size set: %d, %d', wSize['width'], wSize['height'])

            time.sleep(5)
            self.driver.get_screenshot_as_file(fn)
            # self.driver.save_screenshot(fn)
        elif self.browser == 'Firefox':
            logger.info('save Firefox page to %s', fn)
            time.sleep(5)
            pageLength = self.getPageLength()
            pageWidth = self.pageWidth
            logger.warning('page size: %d, %d', pageWidth, pageLength)
            if self.zoom != None:
                self.setZoom(self.zoom)
                pageLength *= self.zoom / 100
                pageWidth *= self.zoom / 100
            logger.warning('page size: %d, %d', pageWidth, pageLength)
            self.setWindowSize(pageWidth, pageLength + 1500)
            wSize = self.driver.get_window_size()
            logger.warning('page size set: %d, %d', wSize['width'], wSize['height'])
            time.sleep(5)
            self.driver.get_screenshot_as_file(fn)
        else:
            logger.error('unknown browser: "%s"', self.browser)

        if os.path.exists(fn) and os.path.getsize(fn) > 0:
            return fn
        logger.debug(' save failed.')
        return None

    def saveFullPageToJpg(self, fn):
        logger.debug('save to %s', fn)
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
