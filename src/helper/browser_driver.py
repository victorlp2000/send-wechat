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
    def __init__(self, settings=None):
        # default settings
        self.browser = 'Firefox'
        self.headless = False
        self.zoom = None
        self.pageWidth = None
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
                # Mobile phone web browser
                ua = 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'
                logger.info('set userAgent: %s', ua)
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
        time.sleep(2)
        scrollHeight = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        viewHeight = self.driver.execute_script("return window.innerHeight")
        print('view height:', viewHeight)
        top = 0
        while top + viewHeight < scrollHeight:
            top += viewHeight
            print('top:', top, scrollHeight)
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight;")
            self.driver.execute_script("window.scrollTo(0, {0})".format(top))
            time.sleep(1)
            scrollHeight = self.driver.execute_script("return document.body.parentNode.scrollHeight")

        return scrollHeight

    def getPageLength(self):
        h1 = self.scrollToBottom()
        logger.info('scrollToBottom: %d', h1)
        h2 = self.driver.execute_script("return document.body.scrollHeight;")
        logger.info('body.scrollHeight: %d', h2)
        elem = self.driver.find_element_by_tag_name('body')
        h4 = self.driver.execute_script('return parseInt(window.getComputedStyle(arguments[0]).height);', elem)
        logger.info('computed height: %d', h4)
        h5 = elem.size['height']
        logger.info('element size height: %d', h4)
        return max(h1, h2, h4, h5)

    def scrollToTop(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def insertTopDiv(self, innerHTML):
        js = ''' let element = document.createElement('div');
        element.style.color = 'white'
        element.style.background = '#666666'
        document.body.insertBefore(element, document.body.firstChild);
        return element;'''
        element = self.driver.execute_script(js)

        hr = '<hr style="background-color:black;height:10px;border-width:0;">'
        self.driver.execute_script("arguments[0].innerHTML = arguments[1]", element, innerHTML + hr)

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

    # save for later debugging
    def saveFullPageToPng0(self, fn):
        driver = self.driver
        file = fn

        print("Starting chrome full page screenshot workaround ...")

        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))

            time.sleep(1)   # wait short time after scroll

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            # screenshot.show()

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            time.sleep(1)
            del screenshot
            # os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing chrome full page screenshot workaround...")
        return fn

    def saveFullPageToPng(self, fn):
        self.setWindowSize(self.pageWidth)
        if self.browser == 'Chrome':
            logger.info('save Chrome page to %s', fn)
            if self.zoom != None:
                self.setZoom(self.zoom)

            pageLength = self.getPageLength()  # get length
            # pageLength += 1000

            # if self.zoom != None:
                # pageLength *= self.zoom / 100
            # logger.info('zoom length: %d', pageLength)

            self.setWindowSize(self.pageWidth, pageLength)
            self.scrollToTop()

            wSize = self.getWindowSize()
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
            self.setWindowSize(pageWidth, pageLength + 1000)
            wSize = self.getWindowSize()
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
