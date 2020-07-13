#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  May 18, 2020
# By: Weiping Liu

import os
from datetime import datetime
from urllib.parse import urlparse
import logging

from helper.browser_driver import WebDriver
from reuters.reuters_article import cleanPage as cleanReutersArticle
from nyt.nyt_article import cleanPage as cleanNYTimesArticle
from bbc.bbc_article import cleanPage as cleanBBCArticle
from dw.dw_article import cleanPage as cleanDWArticle
from ft.ft_article import cleanPage as cleanFTArticle
from voa.voa_article import cleanPage as cleanVOAArticle
from util.copy_to_contacts import copyToContacts
from helper.cmd_argv import getContacts
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

class Settings(object):
    browser = 'Firefox'     # to get full page image, have to use Firefox now
    pageWidth = 400
    headless = False
    userAgent = 'Mobile'

def main():
    logger.info('start %s', __file__)
    driver = WebDriver(Settings)
    driver.loadPage('file://' + os.path.abspath('./manual-bookmarks.html'))
    contacts = getContacts()
    imageFile = '/tmp/manual-pick.jpg'
    fn = None

    if os.path.isfile(imageFile):
        os.remove(imageFile)

    while True:
        select = getChoice(driver.driver)
        if select == '1':
            driver.setZoom(driver.zoom)
            driver.setWindowSize(driver.pageWidth)
            driver.scrollToTop()
            driver.scrollToBottom()

            url = driver.getCurrentUrl()
            if url.startswith('https://cn.reuters.com/article/'):
                cleanReutersArticle(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-reu.jpg')
            elif url.startswith('https://cn.nytimes.com/'):
                cleanNYTimesArticle(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-nyt.jpg')
            elif url.startswith('https://www.bbc.com/zhongwen/simp/'):
                cleanBBCArticle(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-nyt.jpg')
            elif url.startswith('https://m.dw.com/zh/'):
                cleanDWArticle(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-dw.jpg')
            elif url.startswith('https://m.ftchinese.com/'):
                cleanFTArticle(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-ft.jpg')
            elif url.startswith('https://www.voachinese.com'):
                cleanVOAArticle(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-voa.jpg')
            else:
                print ('no parser for the page.')

        elif select == '2':
            if fn == None:
                logger.warning('select 1 to get page cleaned.')
                continue
            logger.info('save page: %s', url)
            if driver.saveFullPageToJpg(imageFile) != None:
                copyToContacts(imageFile, fn, contacts)
        elif select == '0':
            logger.info('exit\n')
            break
    driver.close()

if __name__ == '__main__':
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn, logging.DEBUG)
    main()
