#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  October 4, 2020
# By: Weiping Liu

from datetime import datetime
import pytz
import urllib.parse

def insertHeader(browser):
    js = ''' let articleHeader = document.createElement('div');
    document.body.insertBefore(articleHeader, document.body.firstChild);
    return articleHeader;'''

    return browser.execute_script(js)

def getTimeNow(zone):
    # 'US/Pacific'
    # 'Asia/Shanghai'
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    return now.astimezone(pytz.timezone(zone)).strftime("%Y-%m-%d %H:%M:%S %Z")

def setArticleHeader(driver, config):
    browser = driver.getBrowser()
    header = insertHeader(browser)
    hSettings = config['article_img']
    html = '<div style="padding:10px;backGround:#666666;color:white;">'
    html += '<div style="text-align:center; padding: 6px;"><b>' + hSettings['h-title'] + '</b></div>'
    # html += '<br>' + getTimeNow('Asia/Shanghai')    # 'US/Pacific'
    html += getTimeNow('US/Pacific')    # 'US/Pacific'
    if 'meta' in config:
        if 'updated' in config['meta']:
            html += ' <span style="color:orange">--修改更新</span>'
        html += '<br>' + urllib.parse.unquote(config['meta']['url'])
    html += '</div>'
    html += '<div style="background-color:black;height:6px;margin:0px;padding:0px;border-width:0;"></div>'
    browser.execute_script("arguments[0].innerHTML = arguments[1]", header, html)
    if 'h-zoom' in hSettings:
        browser.execute_script("arguments[0].style.zoom = '" + str(hSettings['h-zoom']) + "%';", header)
