#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created at:  June 11, 2020
# By: Weiping Liu

import time, os
import logging
import shutil
from datetime import datetime

from nyt.nyt_lead_article import getLeadArticleInfo
from nyt.nyt_article import getPageImage
from util.copy_to_contacts import copyToContacts
from util.pid_man import PidMan
from helper.browser_driver import WebDriver
from helper.cmd_argv import getContacts
from helper.accessed import Accessed
from helper.my_logger import getMyLogger

class Settings(object):
    browser = 'Chrome'
    # we like to have 540px width of image
    # to get about 18 characters in a line, need to adjust devScale/zoom
    devScale = 1.5
    pageWidth = 540/devScale
    # zoom = 98.5
    headless = True
    configDir = None
    userAgent = 'Mobile'

file = 'nyt-opinion'

def main():
    logger.info('start %s', __file__)
    driver = WebDriver(Settings)
    pidMan = PidMan(file)
    pidMan.save(driver.getPIDs())
    contacts = getContacts()
    accessed = Accessed('accessed_nytimes.json')

    url = 'https://m.cn.nytimes.com/opinion'
    info = getLeadArticleInfo(driver, url)

    if info == None:
        logger.error('did not find article info.')
    elif not accessed.exists(info):
        driver.setWindowSize(Settings.pageWidth, 2000)
        imgInfo = info.copy()
        imgInfo['type'] = '纽约时报中文网: 观点与评论'
        imgInfo['fn'] = '/tmp/' + file + '.jpg'
        imageFile = getPageImage(driver, imgInfo)
        # save page to contact outbox
        if imageFile != None:
            fn = datetime.now().strftime('%Y%m%d-%H%M%S_' + file + '.jpg')
            copyToContacts(imageFile, fn, contacts)
            os.remove(imageFile)
            info['exec'] = __file__
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
