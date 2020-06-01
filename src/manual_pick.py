#!/usr/bin/python
# -*- coding: utf-8 -*-

# this utility scans webpage at https://cn.reuters.com/theWire
# to get specific of article and clean the content, then save as image

# written for learning Selenium tools

# Created:  May 18, 2020
# By: Weiping Liu

import os
from datetime import datetime
from urllib.parse import urlparse
import logging

from selenium import webdriver

from reuters_article import ArticleReuters
from nytimes_article import ArticleNYTimes
from bbc_article import ArticleBBC
import json_file
import cmd_argv

driver = webdriver.Firefox()

workingDir = os.path.abspath('.')

driver.get('https://www.bbc.com/zhongwen/simp/chinese-news-52859095')

def main():
    contacts = cmd_argv.getContacts()
    while True:
        print ("\nSave current page as image? (y/n)")
        select = input('response:')
        if select == 'y' or select == 'Y':
            if driver.current_url.startswith('https://cn.reuters.com/article/'):
                page = ArticleReuters(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-reu.png')
            elif driver.current_url.startswith('https://cn.nytimes.com/'):
                page = ArticleNYTimes(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-nyt.png')
            elif driver.current_url.startswith('https://www.bbc.com/zhongwen/'):
                page = ArticleBBC(driver)
                fn = datetime.now().strftime('%Y%m%d-%H%M%S-bbc.png')
            else:
                page = None
                print ('no parser for the page.')

            if page != None:
                page.setPageSize(400, 600)
                page.disableSpecificElements()
                outboxDir = workingDir + '/outbox'
                for contact in contacts:
                    contactDir = outboxDir + '/' + contact
                    if not os.path.isdir(contactDir):
                        continue
                    imgFile = contactDir + '/' + fn
                    logger.info('Save "%s" to "%s".', fn, contact)
                    page.savePageAsImageFile(imgFile)

if __name__ == '__main__':
    logger = logging.getLogger('scan_nytimes')
    logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    main()
