#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created at:  May 24, 2020
# By: Weiping Liu

import time, os
import logging
import shutil
from datetime import datetime

from bbc.bbc_article import getPageImage
from bbc.bbc_most_read import getMostReadArticleInfo
from util.copy_to_contacts import copyToContacts
from util.pid_man import PidMan
from helper.browser_driver import WebDriver
from helper.cmd_argv import getContacts
from helper.accessed import Accessed
from helper.my_logger import getMyLogger

class Settings(object):
    browser = 'Chrome'
    # we like to have 540px width of image
    # to get about 18 characters in a line, need to scale or zoom
    # when use zoom, page length returned not exactly right, so we use devScale
    # instead. need to adjust these settings: devScale, zoom
    devScale = 1.8
    pageWidth = 540/devScale
    zoom = 98.5
    headless = True
    configDir = None
    userAgent = 'Mobile'

file = 'bbc-most-read'

def main():
    logger.info('start %s', __file__)
    driver = WebDriver(Settings)
    pidMan = PidMan(file)
    pidMan.save(driver.getPIDs())
    contacts = getContacts()
    accessed = Accessed('accessed_' + file + '.json')

    url = "https://www.bbc.com/zhongwen/simp"
    info = getMostReadArticleInfo(driver, url)

    if info == None:
        logger.error('did not find article info.')
    elif not accessed.exists(info):
        driver.setWindowSize(Settings.pageWidth, 2000)
        imgInfo = info.copy()
        imgInfo['type'] = 'BBC News 中文: 热读'
        imgInfo['fn'] = '/tmp/' + file + '.jpg'
        imageFile = getPageImage(driver, imgInfo)
        # save page to contact outbox
        if imageFile != None:
            fn = datetime.now().strftime('%Y%m%d-%H%M%S_' + file + '.jpg')
            copyToContacts(imageFile, fn, contacts)
            os.remove(imageFile)
            accessed.save(info)
    else:
        logger.info('old article')

    logger.info('exit.\n')
    pidMan.clean()
    driver.close()

if __name__ == "__main__":
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)
    main()
