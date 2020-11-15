#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  May 18, 2020
# By: Weiping Liu

import os, sys, time
from datetime import datetime
from helper import cmd_argv as CmdArg
from helper.my_logger import getMyLogger
from util import json_file
from util.copy_to_contacts import copyToContacts

def collectNews(history, timeFrom):
    logger.info('processing %s', history['fn'])
    meta = json_file.readFile(history['fn'])
    news = []
    for m in meta:
        title = m['title']
        dt = datetime.strptime(m['time'], '%Y-%m-%d %H:%M')
        if dt > timeFrom:
            news.append(title)
    if len(news) == 0:
        return None
    return { 'head': history['head'],
            'url': history['url'],
            'title': news }


def main(config):
    logger.info('start %s', __file__)
    # get start tiem from config
    timeFrom = datetime.strptime(config['time'], '%Y-%m-%d %H:%M')

    # create news file in '/tmp'
    fn = datetime.now().strftime('标题新闻%Y-%m-%d') + '.txt'
    tmpF = '/tmp/' + fn
    logger.info('tmp file: %s', fn)
    f = open(tmpF, 'w')
    f.write(config['time'] + '\n')
    data = False
    for history in config['history']:
        news = collectNews(history, timeFrom)
        if news != None:
            data = True
            f.write('\n' + news['head'])
            f.write('\n(' + news['url'] + ')\n')
            for t in news['title']:
                f.write('- ' + t + '\n')
    f.close()

    # copy generated file to contacts
    if data:
        copyToContacts(tmpF, fn, config['contacts'])

    return data

if __name__ == '__main__':
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)

    if len(sys.argv) < 2:
        print('need config file')
    else:
        cfgFile = sys.argv[1]
        logger.info('run collect with: %s', cfgFile)
        config = json_file.readFile(cfgFile)
        # print(config)
        if main(config):
            config['time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            json_file.saveFile(cfgFile, config)
