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
    if meta == None:
        return None
    news = []
    lastUrl = ''
    for m in meta:
        if lastUrl == m['url']:
            continue
        lastUrl = m['url']
        title = m['title']
        dt = datetime.strptime(m['time'], '%Y-%m-%d %H:%M')
        if dt >= timeFrom:
            item = {}
            item['title'] = m['title']
            if 'abstract' in m:
                item['abstract'] = m['abstract']
            news.append(item)
    logger.info('news in <%s>: %d', history['fn'], len(news))
    if len(news) == 0:
        return None
    return { 'name': history['name'],
            'url': history['url'],
            'items': news }


def main(config):
    logger.info('start %s', __file__)

    head = '今日新闻'
    # create news file in '/tmp'
    fn = head + datetime.now().strftime('%Y-%m-%d') + '.html'
    tmpF = '/tmp/' + fn
    logger.info('generating file: %s', tmpF)
    f = open(tmpF, 'w')

    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = now.astimezone(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M %Z')
    f.write('<!DOCTYPE html>\n<html>\n')
    f.write('<head>\n <title>' + head + '</title>\n <meta charset="utf-8"/>\n')
    f.write(' <style>\n')
    f.write('  div.head {text-align:center; padding-top:1em; font-weight:bold; font-size:2em;}\n')
    f.write('  div.time {text-align:center; padding-bottom:1em; font-size:1em; color:#999999;}\n')
    f.write('  img.logo {float:left; height:3em;margin:0.2em;}\n')
    f.write('  div.src-name {display:table-row; font-weight:normal; font-size:1.4em; color:#0000bb;}\n')
    f.write('  div.src-url {display:table-row; font-style:italic; font-size:0.8em; color:#9999ee;}\n')
    f.write('  div.article {font-family:sans-serif; font-weight:normal;}\n')
    f.write('  div.abstract {font-family:serif; font-size:0.7em; color:#777777;}\n')
    f.write('  ul {list-style-type:disc; padding-left:2em;}\n')
    f.write('  li {margin-bottom:2em;}\n')
    f.write('  div.ending {display:block; text-align:center;height:0.2em; background-color:#999999; margin:6em;}\n')
    f.write(' </style>\n')
    f.write('</head>\n')

    f.write('<body style="margin:1em; font-size:0.2in">\n')
    f.write(' <div class="head">' + head + '</div>\n')
    f.write(' <div class="time">' + now + '</div>\n')

    # get start time from past 24 hours
    timeFrom = datetime.now() - timedelta(hours=24, minutes=0)

    news = None
    for history in config['history']:
        if not history['active']:
            continue
        news = collectNews(history, timeFrom)
        if news != None:
            f.write(' <div style="display:flow-root; font-size:1em;">\n')
            with open('./outbox/' + history['logo'], 'r') as flogo:
                f.write(flogo.read())
                pass
            f.write('  <div class="src-name">' + news['name'] + '</div>\n')
            f.write('  <div class="src-url">(' + news['url'] + ')</div>\n')
            f.write(' </div>\n')
            f.write(' <hr style="border-width:0px; margin:0.2em; height:0.1em; background-color:#0000bb;"/>\n')
            f.write(' <ul>\n')
            for t in news['items']:
                f.write('  <li>\n   <div class="article">' + t['title'] + '</div>\n')
                if 'abstract' in t:
                    f.write('   <div class="abstract">' + t['abstract'] + '</div>\n')
                f.write('  </li>\n')
            f.write(' </ul>\n')
    f.write(' <div class="ending"></div>\n')
    f.write('</body>\n</html>')
    f.close()

    # copy generated file to contacts
    logger.info('save to contacts %s', config['contacts'])
    copyToContacts(tmpF, fn, config['contacts'])

    return

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
