settings#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  May 18, 2020
# By: Weiping Liu

import os, time
from datetime import datetime
from urllib.parse import urlparse
import logging

from helper.browser_driver import WebDriver
from reuters import reuters_article as reutersArticle
from nyt import nyt_article as nytArticle
from bbc import bbc_article as bbcArticle
from dw import dw_article as dwArticle
from ft import ft_article as ftArticle
from voa import voa_article as voaArticle
from util.copy_to_contacts import copyToContacts
from helper import cmd_argv as CmdArg
from helper.my_logger import getMyLogger

def menu():
    print('ENTER to TAB window')
    print(' 0. exit')
    print(' 1. cleanup page content')
    print(' 2. save page image to outbox')

def getChoice(browser, tab=0):
    while True:
        tabs = len(browser.window_handles)
        browser.switch_to_window(browser.window_handles[tab])
        menu()
        choice = input('input choice: ')
        if choice == '':
            tab += 1
            if tab >= tabs:
                tab = 0
        else:
            return choice

def getArticleSource(url)
    if url.startswith('https://cn.reuters.com/article/'):
        return 'reuters'
    elif url.startswith('https://cn.nytimes.com/'):
        return 'nyt'
    elif url.startswith('https://www.bbc.com/zhongwen/simp/'):
        return 'bbc'
    elif url.startswith('https://m.dw.com/zh/'):
        return 'dw'
    elif url.startswith('https://m.ftchinese.com/'):
        return 'ft'
    elif url.startswith('https://www.voachinese.com'):
        return 'voa'
    else:
        print ('no parser for the page.')
    return None

def getPageSettings(src, settings):
    if src == 'reuters':
        settings = reutersArticle.pageSettings(settings)
    elif src == 'nyt':
        settings = nytArticle.pageSettings(settings)
    elif src == 'bbc':
        settings = bbcArticle.pageSettings(settings)
    elif src == 'dw':
        settings = dwArticle.pageSettings(settings)
    elif src == 'ft':
        settings = ftArticle.pageSettings(settings)
    elif src == 'voa':
        settings = voaArticle.pageSettings(settings)
    else:
        print ('no parser for the page.')
    return settings

def getPageImage(driver, imgInfo):
    src = getArticleSource(driver)
    imgInfo['fn'] = '/tmp/manual-pick.jpg'
    if src == 'reuters':
        imgInfo['type'] = 'BBC News 中文: 文章选摘'
        imgInfo['zoomHeader'] = '85%'
        img = reutersArticle.getPageImage(driver)

    elif src == 'nyt':
        img = nytArticle.getPageImage(driver)

    elif src == 'bbc':
        img = bbcArticle.getPageImage(driver)

    elif src == 'dw':
        img = dwArticle.getPageImage(driver)

    elif src == 'ft':
        img = ftArticle.getPageImage(driver)

    elif src == 'voa':
        img = voaArticle.getPageImage(driver)

    else:
        print ('no parser for the page.')
    return fn

def cleanPage(driver):
    src = getArticleSource(driver)
    if src == 'reuters':
        reutersArticle.pageClean(driver)
        fn = datetime.now().strftime('%Y%m%d-%H%M%S-reu.jpg')
    elif src == 'nyt':
        nytArticle.pageClean(driver)
        fn = datetime.now().strftime('%Y%m%d-%H%M%S-nyt.jpg')
    elif src == 'bbc':
        bbcArticle.pageClean(driver)
        fn = datetime.now().strftime('%Y%m%d-%H%M%S-nyt.jpg')
    elif src == 'dw':
        dwArticle.pageClean(driver)
        fn = datetime.now().strftime('%Y%m%d-%H%M%S-dw.jpg')
    elif src == 'ft':
        ftArticle.pageClean(driver)
        fn = datetime.now().strftime('%Y%m%d-%H%M%S-ft.jpg')
    elif src == 'voa':
        voaArticle.pageClean(driver)
        fn = datetime.now().strftime('%Y%m%d-%H%M%S-voa.jpg')
    else:
        print ('no parser for the page.')
    return fn

class Settings(object):
    browser = 'Chrome'
    userAgent = 'Mobile'

def main():
    logger.info('start %s', __file__)
    contacts = CmdArg.getContacts()
    url = CmdArg.getUrl()
    if url == None or getArticleSource(url) == None:
        url = 'file://' + os.path.abspath('./manual-bookmarks.html')
        Settings.headless = False
    else:
        Settings.headless = True
    settings = getPageSetings(getArticleSource(url), Settings)

    driver = WebDriver(settings)
    driver.getBrowser().get(url)
    imageFile = '/tmp/manual-pick.jpg'
    fn = None

    if os.path.isfile(imageFile):
        os.remove(imageFile)

    if url.startswith('http'):
        fn = cleanPage(driver)
        if driver.saveFullPageToJpg(imageFile) != None:
            copyToContacts(imageFile, fn, contacts)
        driver.getBrowser().quit()
        return

    while True:
        select = getChoice(driver.driver)
        if select == '1':
            fn = cleanPage(driver)
        elif select == '2':
            if fn == None:
                logger.warning('select 1 to get page cleaned.')
                continue
            logger.info('save page: %s', url)
            if driver.saveFullPageToJpg(imageFile) != None:
                copyToContacts(imageFile, fn, contacts)

        elif select == '3':
            driver.setZoom(driver.zoom)
            driver.setWindowSize(driver.pageWidth)
            browser = driver.getBrowser()
            body = browser.find_element_by_tag_name('body')
            script = 'return window.getComputedStyle(arguments[0]).height;'
            h = browser.execute_script(script, body)
            print('computed height:', h)
            print('body size:', body.size)
            driver.scrollToTop()
            driver.scrollToBottom()

        elif select == '0':
            logger.info('exit\n')
            break
    driver.getBrowser().quit()

if __name__ == '__main__':
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn, logging.DEBUG)
    main()
