#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created at:  June 21, 2020
# By: Weiping Liu

import time, os
import logging
import shutil
from datetime import datetime

from ft.ft_top_story import getTopStoryInfo
from ft.ft_article import getPageImage
from util.copy_to_contacts import copyToContacts
from helper.browser_driver import WebDriver
from helper.cmd_argv import getContacts
from helper.accessed import Accessed
from helper.my_logger import getMyLogger

class Settings(object):
    browser = 'Firefox'
    zoom = 100      # about 20 c-chars in a line
    pageWidth = 360
    headless = True     # need to be True, or Chrome does not take full page image
    configDir = None

file = 'ft-top-story'

def main():
    logger.info('start %s', __file__)
    driver = WebDriver(Settings)
    contacts = getContacts()
    accessed = Accessed('accessed_ft.json')

    url = "https://m.ftchinese.com/"
    info = getTopStoryInfo(driver, url)

    if info and not accessed.exists(info):
        fn = '/tmp/' + file + '.jpg'
        imageFile = getPageImage(driver, info['link'], fn)
        # save page to contact outbox
        if imageFile != None:
            fn = datetime.now().strftime('%Y%m%d-%H%M%S_' + file + '.jpg')
            copyToContacts(imageFile, fn, contacts)
            os.remove(imageFile)
            info['exec'] = __file__
            accessed.save(info)
    logger.info('exit.\n')
    driver.close()

if __name__ == "__main__":
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)
    main()
