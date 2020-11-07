#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created at:  June 11, 2020
# By: Weiping Liu

import time, os
import logging
from datetime import datetime
import importlib
import urllib.parse
from util.copy_to_contacts import copyToContacts
from util.pid_man import PidMan
from helper.browser_driver import WebDriver
from helper.history import History
from helper.my_logger import getMyLogger
from util import json_file as JsonUtil
from helper import cmd_argv as CmdArgv
from helper.set_article import setArticle

def getArticle(driver, url, imgInfo):
    unquote = urllib.parse.unquote(url)
    logger.info('loading %s', unquote)
    browser = driver.getBrowser()

    browser.get(url)

    if 'do_live' in imgInfo:
        module = importlib.import_module(imgInfo['do_live'])
        live = module.getTimePoints(driver)
        if live != None:
            imgInfo['live'] = live
            print(live)

    # cleanup the page
    if 'do_cleanup' in imgInfo:
        module = importlib.import_module(imgInfo['do_cleanup'])
        module.cleanupPage(driver)

    imgInfo['link'] = urllib.parse.unquote(browser.current_url)
    setArticle(driver, imgInfo)
    return

def findArticle(driver, url, configInfo):
    if not 'do_find' in configInfo:
        return {'link': url, 'title': 'article'}

    driver.getBrowser().get(config['main_url'])
    module = importlib.import_module(configInfo['do_find'])
    return module.findArticleInfo(driver)

def processPage(driver, config):
    # load hidtory for checking visited articles
    fn = 'history_' + config['name'] + '.json'
    history = History(fn)

    # load main page
    if not 'main_url' in config:
        logger.warning('did not find \'main_url\' in config')
        return

    # find article from webpage
    info = findArticle(driver, config['main_url'], config['article_info'])
    if info == None:  # found article
        logger.warning('did not find article.')
        return
    if info['title'] == '':
        logger.warning('did not get title')
        return
    logger.info('article: "%s"', info['title'])

    # check if the article has been visited
    if ('debug' not in config) and history.exists(info):
        logger.warning('old article')
        return

    # get article image
    imgInfo = {}
    imgInfo.update(config['article_img'])
    imgInfo.update(info)
    getArticle(driver, info['link'], imgInfo)

    if 'debug' in config:
        input('finished clenup...')

    if 'live' in imgInfo:
        info['live'] = imgInfo['live']
        if history.exists(info):
            return

    # get article image
    fn = '/tmp/' + config['name'] + '.jpg'
    img = driver.saveFullPageToJpg(fn)
    if img == None:
        logger.warning('failed to generate article image.')
        return

    # save page to outbox
    fn = datetime.now().strftime('%Y%m%d-%H%M%S_' + config['name'] + '.jpg')
    copyToContacts(img, fn, config['contacts'])
    os.remove(img)
    history.save(info)

def main(config):
    logger.info('=== start "%s"', config['name'])

    # start driver with website specific configurations
    driver = WebDriver(config['settings'])

    # keep process pid for kill in case of failed
    fn = config['name'] + '.pid'
    pidMan = PidMan(fn)
    pidMan.save(driver.getPIDs())

    processPage(driver, config)

    logger.info('exit.\n')
    pidMan.clean()
    driver.getBrowser().quit()

if __name__ == "__main__":
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)
    configFile = CmdArgv.getConfig()
    if configFile != None:
        config = JsonUtil.readFile(configFile)
        if CmdArgv.getDebug():
            config['debug'] = True
            config['settings']['headless'] = False
        main(config)
    else:
        logger.error('no config')
