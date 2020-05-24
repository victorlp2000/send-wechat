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
from reuters_article import ArticleReuters

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from selenium.webdriver import Firefox
driver = Firefox(executable_path="/usr/local/bin/geckodriver")
from selenium.webdriver.support.ui import WebDriverWait

# getArticleList(lastAccess)
#   lastAccess = {href:"...", title:"..."}
#   get a list of elements, until max number or reach one in the log
#   return array of article-info
def getArticleList(lastAccess):
    # in case of not find the article lastAccess,
    # we don't want to load unlimited articles
    maxArticles = 30

    # <section class="module-content">
    #   <ul class="...">
    #     <li>
    #       ...
    #       <a href="/article/japan-covid-economy-recession-0518-idCNKBS22U07E?il=0">焦点：新冠疫情将日本经济拖入衰退 但最糟糕时期还未到来</a>
    #     </li>
    #   </ul>
    #   ...
    #   <div class="more-load">LOAD MORE</div>
    #   ...
    # </section>
    loop = True
    while loop:
        articles = []   # for return
        sections = driver.find_elements_by_css_selector('section.module-content')
        if len(sections) != 1:
            logger.warninig('!! should have only 1 module-content section, got %d', len(sections))
            break

        elements = sections[0].find_elements_by_tag_name('li')

        for e in elements:
            info = getArticleInfo(e)
            if lastAccess != None:
                if info['href'] == lastAccess['href'] or info['title'] == lastAccess['title']:
                    loop = False
                    break
            articles.append(info)

        if len(articles) >= maxArticles:
            break

        load = sections[0].find_elements_by_css_selector('div.more-load')
        if len(load) == 1:
            logger.info('load more ...%d', len(articles))
            load[0].click()
            # wait loading ...
            counter = 0
            while counter < 20:
                n = sections[0].find_elements_by_tag_name('li')
                if len(n) > len(elements):
                    break
                counter += 1
                time.sleep(1)

    return articles

# getArticleInfo(element)
#   extract href and link text from element
#   return {href: '', title: ''}
def getArticleInfo(element):
    link = element.find_elements_by_tag_name('a')
    if len(link) == 1:
        return {
            'href': link[0].get_attribute('href'),
            'title': link[0].text
        }
    return None

# pickArticle(articles)
#   filter link title to pick expected article
#   return article = {info, title} or None
#
def pickArticle(articles):
    # start process articles from older ones
    for article in reversed(articles):
        if article['title'].startswith(u'焦点：'):
            return article
    return None

def getContacts():
    # default contacts
    contacts = ['File Transfer']
    if len(sys.argv) > 1:
        tmp = json_file.readFile(sys.argv[1])
        if type(tmp) is list:
            contacts = tmp
    return contacts

def getLastAccess(lastAccessFile):
    last = json_file.readFile(lastAccessFile)
    return last

def loadArticle(url):
    driver.get(url)
    page = ArticleReuters(driver)
    page.setPageSize(400, 600)
    page.disableSpecificElements()
    return page

def main():
    contacts = getContacts()
    lastAccess = getLastAccess(lastAccessFile)
    fnFormat = '%Y%m%d-%H%M%S-reu.png'
    outboxDir = workingDir + outbox

    # set window size minimum
    driver.set_window_size(200, 600)

    articles = getArticleList(lastAccess)
    article = pickArticle(articles)
    if article != None:
        logger.info('Found article %s.', article['title'])
        page = loadArticle(article['href'])

        for contact in contacts:
            imgDir = outboxDir + '/' + contact
            logger.info('Save page image to %s.', imgDir)
            page.savePageImageToFolder(imgDir)

    json_file.saveFile(lastAccessFile, article)

    driver.close()

# webpage: 路透中文网
baseUrl = "https://cn.reuters.com"
driver.get(baseUrl + '/theWire')

workingDir = os.path.abspath('.')
lastAccessFile = workingDir + '/last-access-reuters.json'
outbox = '/outbox'

if __name__ == "__main__":
    # usage:
    #   $ python scan_reuters_the_wire [contactsFilename]

    logger = logging.getLogger('scan_reuters')
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
