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
    innerHTML = '<div style="padding:10px;backGround:#666666;color:white;">'
    innerHTML += '<center><b>' + info['type'] + '</b></center>'
    # innerHTML += '<br>' + getTimeNow('Asia/Shanghai')    # 'US/Pacific'
    innerHTML += '<br>' + getTimeNow('US/Pacific')    # 'US/Pacific'
    if info['updated']:
        innerHTML += ' <b>更新</b>'
    innerHTML += '<br>' + urllib.parse.unquote(info['link'])
    innerHTML += '</div>'
    innerHTML += '<hr style="background-color:black;height:6px;margin:0px;padding:0px;border-width:0;">'
    browser.execute_script("arguments[0].innerHTML = arguments[1]", header, innerHTML)

def removeScrollbar(browser):
    body = browser.find_element_by_tag_name('body')
    browser.execute_script("arguments[0].style.overflow = 'hidden';", body)

def setArticle(driver, info):
    browser = driver.getBrowser()
    setHeader(browser, info)
    removeScrollbar(browser)
