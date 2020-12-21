#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  May 18, 2020
# By: Weiping Liu

import os, sys, time, pytz
from datetime import datetime, timedelta
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
            item = {}
            item['title'] = m['title']
            if 'abstract' in m:
                item['abstract'] = m['abstract']
            news.append(item)
    if len(news) == 0:
        return None
    return { 'head': history['head'],
            'url': history['url'],
            'items': news }


def main(config):
    logger.info('start %s', __file__)

    # create news file in '/tmp'
    fn = datetime.now().strftime('标题新闻%Y-%m-%d') + '.html'
    tmpF = '/tmp/' + fn
    logger.info('tmp file: %s', fn)
    f = open(tmpF, 'w')

    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    s = now.astimezone(pytz.timezone('US/Pacific')).strftime('[%Y-%m-%d %H:%M %Z]')
    title = '新闻简报'
    f.write('<!DOCTYPE html><html>')
    f.write('<head><title>' + title + '</title></head><body>\n')
    f.write('<style>')
    f.write('div.head {font-weight:normal; font-size:large; color:#0000bb;}\n')
    f.write('span.weburl {font-style:italic;}\n')
    f.write('div.title {font-family:sans-serif; font-weight:normal;}\n')
    f.write('div.abstract {font-family:serif; font-size:small; color:#666666;}\n')
    f.write('ul {list-style-type:disc; padding-left:20px;}')
    f.write('li {margin-top:10px;}')
    f.write('div.dd1 {text-align:center; padding-top:20px; font-size:x-large}')
    f.write('div.dd2 {text-align:center; padding-bottom:20px; font-size:normal; color:#999999;}')
    f.write('</style>\n')

    f.write('<div class="dd1">' + title + '</div>\n')
    f.write('<div class="dd2">' + s + '</div>\n')
    # get start time from past 24 hours
    timeFrom = datetime.now() - timedelta(hours=24, minutes=0)

    data = False
    for history in config['history']:
        news = collectNews(history, timeFrom)
        if news != None:
            data = True
            f.write('<div class="head">' + news['head'])
            f.write('<span class="weburl">(' + news['url'] + ')</span></div>\n')
            f.write('<ul>\n')
            for t in news['items']:
                f.write('<li><div class="title">' + t['title'] + '</div>')
                if 'abstract' in t:
                    f.write('<div class="abstract">' + t['abstract'] + '</div>')
                f.write('</li>\n')
            f.write('</ul>')
    f.write('</body>')
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
        main(config)