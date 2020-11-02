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

def setHeader(browser, info):
    header = insertHeader(browser)
    if 'zoom' in info:
        browser.execute_script("arguments[0].style.zoom = '" + str(info['zoom']) + "%';", header)
    html = '<div style="padding:10px;backGround:#666666;color:white;">'
    html += '<div style="text-align:center; padding: 6px;"><b>' + info['title'] + '</b></div>'
    # html += '<br>' + getTimeNow('Asia/Shanghai')    # 'US/Pacific'
    html += getTimeNow('US/Pacific')    # 'US/Pacific'
    if 'updated' in info:
        html += ' <span style="color:orange">--修改更新</span>'
    html += '<br>' + urllib.parse.unquote(info['link'])
    html += '</div>'
    html += '<div style="background-color:black;height:6px;margin:0px;padding:0px;border-width:0;"></div>'
    browser.execute_script("arguments[0].innerHTML = arguments[1]", header, html)

def setArticle(driver, info):
    browser = driver.getBrowser()
    setHeader(browser, info)
