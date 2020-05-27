#!/usr/bin/python
# -*- coding: utf-8 -*-

# this utility scans webpage at https://cn.reuters.com/theWire
# to get specific of article and then save as image

# Created:  May 24, 2020
# By: Weiping Liu

import time
from datetime import datetime
import json
import os.path
import sys
import logging

import json_file
import cmd_argv
from bbc_article import ArticleBBC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from selenium.webdriver import Firefox
driver = Firefox(executable_path="/usr/local/bin/geckodriver")
from selenium.webdriver.support.ui import WebDriverWait

# getArticleList(lastAccess)
#   lastAccess = {title:"..."}
#   get a list of elements, until max number or reach one in the log
#   return array of article-info
def getArticleList(lastAccess):
    articles = []   # for return
    selector = 'section.MostReadSection-sc-58u5qv-1.ilJrAv'
    sections = driver.find_elements_by_css_selector(selector)
    if len(sections) != 1:
        logger.warning('!! got more than one selector "%s"', selector)
        return articles
    selector = 'ol.GridComponent-nf79gm-0.gjgzxV.OneColumnGrid-sc-1ofyujo-0.TwoColumnGrid-sc-1ofyujo-1.boiGsE'
    ol = sections[0].find_elements_by_css_selector(selector)
    if len(ol) != 1:
        logger.warninig('!! got more than one selector "%s"', selector)
        return articles
    list = ol[0].find_elements_by_tag_name('li')
    logger.debug('found %d items.', len(list))
    for e in list:
        if appendArticle(articles, e, lastAccess):
            break
    return articles

# return True if the item last accessed
def appendArticle(articles, element, lastAccess):
    info = getArticleInfo(element)
    if info == None:
        logger.warning('! did not find article info.')
        return False
    if lastAccess != None and info != None:
        if info['title'] == lastAccess['title']:
            logger.debug('last accessed article')
            return True
    articles.append(info)
    return False

# getArticleInfo(element)
#   extract href and link text from element
#   return {href: '', title: ''}
def getArticleInfo(element):
    links = element.find_elements_by_tag_name('a')
    if len(links) != 0:
        return {
            'href': links[0].get_attribute('href'),
            'title': links[0].text
        }
    else:
        logger.warning('!! did not find link')
    return None

# pickArticle(articles, lastAccess)
#   filter link title to pick expected article
#   return article = {info, title} or None
#
def pickArticle(articles, lastAccess):
    for article in articles:
        return article
    return None

def getLastAccess(lastAccessFile):
    last = json_file.readFile(lastAccessFile)
    return last

def loadArticle(url):
    driver.get(url)
    page = ArticleBBC(driver)
    page.setPageSize(400, 600)
    page.disableSpecificElements()
    return page

def main():
    contacts = cmd_argv.getContacts()
    lastAccess = getLastAccess(lastAccessFile)

    articles = getArticleList(lastAccess)
    article = pickArticle(articles, lastAccess)
    if article != None:
        logger.info('Found article "%s".', article['title'])
        page = loadArticle(article['href'])
        fn = datetime.now().strftime('%Y%m%d-%H%M%S_bbc-most-read.png')
        outboxDir = workingDir + '/outbox'
        for contact in contacts:
            contactDir = outboxDir + '/' + contact
            if not os.path.isdir(contactDir):
                continue
            imgFile = contactDir + '/' + fn
            logger.info('Save "%s" to "%s".', fn, contact)
            page.savePageAsImageFile(imgFile)
        last = {'title': article['title']}
        json_file.saveFile(lastAccessFile, last)
    driver.close()

# webpage: 纽约时报中文网 - 简报
# set window size minimum
driver.set_window_size(400, 600)
baseUrl = "https://www.bbc.com"
driver.get(baseUrl + '/zhongwen/simp')

workingDir = os.path.abspath('.')
lastAccessFile = workingDir + '/last_bbc-most-read.json'

if __name__ == "__main__":
    # usage:
    #   $ python scan_reuters_the_wire [contactsFilename]
    logger = logging.getLogger('scan_bbc')
    logger.setLevel(logging.DEBUG)
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
