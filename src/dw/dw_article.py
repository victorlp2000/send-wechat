#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getPageImage(driver, url, fn):
    logger.info('loading "%s"', url)
    driver.setWindowSize(driver.pageWidth)
    driver.loadPage(url)
    driver.scrollToBottom()
    time.sleep(3)   # for loading completely
    cleanPage(driver)

    return driver.saveFullPageToJpg(fn)

def cleanPage(driver):
    logger.info('cleaning content...')
    selectors = [
        'div.adsContainer',     # 广告
        'div.col1.dim',         # right-side column
        'div.col3.relatedContent',  # 相关内容
        'div.cookie__wrap',     # ...我们使用Cookies
        'div.col1',
        'ul.smallList',
        'div.linkList.intern'   # DW.COM ...
    ]
    ids = [
        'topMetaLang',  # Chinese (Traditional) 繁
        'navMeta',      #
        'navMain',      # 在线报导 多媒体中心 德语天地
        'sharing-bar',
    ]
    driver.noneDisplayByCSSSelectors(selectors)
    driver.noneDisplayByIds(ids)

    browser = driver.driver
    pWidth = driver.pageWidth-20

    # in footerSection, keep copyright, remove others
    footer = browser.find_element_by_id('footerBody')
    uls = footer.find_elements_by_tag_name('ul')
    for ul in uls:
        browser.execute_script("arguments[0].style.display = 'none';", ul)

    # adjust hard-coded width to or width
    content = driver.findElementsByCssSelector('div.col3')[0]
    browser = driver.driver
    setStyleWidth(browser, [content], pWidth)

    imgs = content.find_elements_by_tag_name('img')
    setStyleWidth(browser, imgs, pWidth-20) # smaller for images

    ps = content.find_elements_by_tag_name('p')
    setStyleWidth(browser, ps, pWidth)

    # if there is picBox, make it 2/3 width of page width
    # <div class="picBox medium">
    #   <a class="overlayLink init" href="#" link="/overlay/image/...">
    #     <img itemprop="image" src="/image/52050944_404.jpg" title="Huawei 5G"">
    #     </a>
    #   <p>美国方面一再对德国引入5G通讯时使用华为的技术产品提出警告</p>
    #   </div>
    picBox = browser.find_elements_by_css_selector('div.picBox.medium')
    if len(picBox) > 0:
        w = int(pWidth * 2 / 3)
        setStyleWidth(browser, [picBox[0]], w)
        imgs = picBox[0].find_elements_by_tag_name('img')
        setStyleWidth(browser, imgs, w)
        ps = picBox[0].find_elements_by_tag_name('p')
        setStyleWidth(browser, ps, w)

    # div.col3.right is a video, make it smaller
    right = browser.find_elements_by_css_selector('div.col3.right')
    if len(right) > 0:
        setStyleWidth(browser, [right[0]], pWidth)
        divs = right[0].find_elements_by_css_selector('div')
        setStyleWidth(browser, divs, pWidth)

    # remove minHeight
    navContainer = browser.find_element_by_id('navContainer')
    browser.execute_script('arguments[0].style.minHeight="0px";', navContainer)
    # browser.execute_script('arguments[0].style.removeProperty("min-height");', navContainer)

def setStyleWidth(browser, elements, width):
    for e in elements:
        browser.execute_script('arguments[0].style.width="' + str(width) + 'px";', e)
