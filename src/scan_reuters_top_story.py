#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created at:  June 11, 2020
# By: Weiping Liu

import time, os
import logging
import shutil
from datetime import datetime

from reuters.reuters_top_story import getTopStoryInfo
from reuters.reuters_article import getPageImage
from util.copy_to_contacts import copyToContacts
from util.pid_man import PidMan
from helper.browser_driver import WebDriver
from helper.cmd_argv import getContacts
from helper.accessed import Accessed
from helper.my_logger import getMyLogger

class Settings(object):
    browser = 'Firefox'
    pageWidth = 450
    headless = True     # need to be True, or Chrome does not take full page image
    configDir = None

file = 'reuters-top-story'

def main():
    logger.info('start %s', __file__)
    driver = WebDriver(Settings)
    pidMan = PidMan(file)
    pidMan.save(driver.getPIDs())
    contacts = getContacts()
    accessed = Accessed('accessed_reuters.json')

    url = "https://cn.reuters.com/"
    info = getTopStoryInfo(driver, url)

    if info == None:
        logger.error('did not find article info.')
    elif not accessed.exists(info):
        fn = '/tmp/' + file + '.jpg'
        imageFile = getPageImage(driver, info['link'], fn)
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
