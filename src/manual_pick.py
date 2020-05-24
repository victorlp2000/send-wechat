#!/usr/bin/python
# -*- coding: utf-8 -*-

# this utility scans webpage at https://cn.reuters.com/theWire
# to get specific of article and clean the content, then save as image

# written for learning Selenium tools

# Created:  May 18, 2020
# By: Weiping Liu

import os
from urllib.parse import urlparse
from selenium import webdriver

from reuters_article import ArticleReuters
import json_file

driver = webdriver.Firefox()

workingDir = os.path.abspath('.')

def getContactName(contactFile):
    contact = None
    if contactFile != None and os.path.exists(contactFile):
        contact = json_file.readFile(contactFile)
    if contact != None:
        contactName = contact['name']
    else:
        contactName = 'File Transfer'
    print ('contact name:', contactName)
    return contactName

driver.get('https://cn.reuters.com/article/health-coronavirus-markets-outlook-0522-idCNKBS22Y14S?il=0')

def main(contactFile):
    contact = getContactName(contactFile)
    imgDir = workingDir + '/outbox/' + contact

    if not os.path.exists(imgDir):
        os.mkdir(imgDir)

    while True:
        print ("\nSave current page as image? (y/n)")
        select = input('response:')
        if select == 'y' or select == 'Y':
            if driver.current_url.startswith('https://cn.reuters.com/article/'):
                page = ArticleReuters(driver)
                page.setPageSize(400, 600)
                page.disableSpecificElements()
                page.savePageImageToFolder(imgDir)
            else:
                print ('no parser for the page.')

if __name__ == '__main__':
    import sys
    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    main(arg)
