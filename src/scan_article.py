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
from helper.set_article import setArticleHeader

def saveArticleScreenShot(driver, config):
    # get screenshot image
    fn = '/tmp/' + config['name'] + '.jpg'
    img = driver.saveFullPageToJpg(fn)
    if img == None:
        logger.warning('failed to generate article image.')
        return

    # save page to outbox
    fn = config['meta']['file']
    if 'contacts' in config:
        copyToContacts(img, fn, config['contacts'])
    else:
        toFile = './outbox/' + fn
        logger.info('generated file: %s', toFile)
        import shutil
        shutil.copyfile(img, toFile)
    os.remove(img)

# get ready article page for taking screenshot
#   1. clean up content
#   2. set header info
def nomalizeArticle(driver, config):
    # cleanup the page
    if not 'article_img'in config:
        logger.warning('did not see article_img in config')
        return

    if 'm_cleanup' in config['article_img']:
        module = importlib.import_module(config['article_img']['m_cleanup'])
        module.cleanupPage(driver, config)
    else:
        logger.warning('did not see m_cleanup in config')

    # set header info
    setArticleHeader(driver, config)

#   1. load the article page
#   2. extract meta info:
#       link, title, author, ...
def getArticleMeta(driver, url, config):
    if 'article_info' in config:
        if 'm_getArticleMeta' in config['article_info']:
            module = importlib.import_module(config['article_info']['m_getArticleMeta'])
            meta = module.getArticleMeta(driver, url)
            return meta
        else:
            logger.warning('did not see m_getArticleMeta in config')
    # caller supposed the page is loaded
    driver.getBrowser().get(url)
    return {'url': url}

# get article url from:
#   1. command line
#   2. config
#   3. main_url page
def findArticleUrl(driver, config):
    # try to get from command line
    url = CmdArgv.getUrl()
    if url != None:
        return url

    if not 'main_url' in config:
        logger.warning('did not see main_url in config')
        return None

    # if m_find function does not set, use main_url
    if not 'article_info' in config:
        logger.warning('did not see article_info in config')
        return config['main_url']

    if not 'm_findArticleUrl' in config['article_info']:
        logger.warning('did not see m_find in article_info')
        return config['main_url']

    url = config['main_url']
    if url == '':
        logger.warning('did not set main url')
        return None

    logger.info('loading main url')
    driver.getBrowser().get(config['main_url'])

    module = importlib.import_module(config['article_info']['m_findArticleUrl'])
    return module.findArticleUrl(driver)

def processPage(driver, config):
    # load hidtory for checking visited articles
    fn = 'history_' + config['name'] + '.json'
    history = History(fn)

    # find specific article url
    url = findArticleUrl(driver, config)
    if url == None:
        return
    logger.info('url: "%s"', urllib.parse.unquote(url))

    # get article meta data
    meta = getArticleMeta(driver, url, config)
    if not ('url' in meta):
        logger.info(meta)
        logger.warning('did not find article url or title')
        return

    # check if the article has been visited
    if history.exists(meta):
        logger.warning('visited article')
        return

    if 'debug' in config:
        print(meta)
        input('finished meta...')

    # cleanup the article page
    config['meta'] = meta
    nomalizeArticle(driver, config)

    if 'debug' in config:
        input('finished clenup...')

    if len(config['contacts']) > 0:
        meta['file'] = datetime.now().strftime('%Y%m%d-%H%M%S_' + config['name'] + '.jpg')
        saveArticleScreenShot(driver, config)

    history.save(meta)

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
