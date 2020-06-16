#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created at:  June 16, 2020
# By: Weiping Liu

import time, os
import logging
import shutil
from datetime import datetime

from nyt.nyt_lead_news import getLeadArticleInfo
from nyt.nyt_article import getPageImage
from util.copy_to_contacts import copyToContacts
from helper.browser_driver import WebDriver
from helper.cmd_argv import getContacts
from helper.last_access import LastAccess
from helper.check_new_article import isNewArticle
from helper.my_logger import getMyLogger

class Settings(object):
    browser = 'Chrome'
    zoom = 100
    pageWidth = 400     # about 20 c-chars in a line
    headless = True     # need to be True for Chrome taking full page image
    configDir = None

file = 'nyt-lead-news'

def main():
    logger.info('start %s', __file__)
    driver = WebDriver(Settings)
    contacts = getContacts()
    lastAccess = LastAccess('last_' + file + '.json')

    url = 'https://cn.nytimes.com/'
    info = getLeadArticleInfo(driver, url)

    if info and isNewArticle(info, lastAccess.load()):
        fn = '/tmp/' + file + '.jpg'
        imageFile = getPageImage(driver, info['link'], fn)
        # save page to contact outbox
        if imageFile != None:
            fn = datetime.now().strftime('%Y%m%d-%H%M%S_' + file + '.jpg')
            copyToContacts(imageFile, fn, contacts)
            os.remove(imageFile)
            lastAccess.save(info)
    logger.info('exit.\n')
    driver.close()

if __name__ == "__main__":
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)
    main()
