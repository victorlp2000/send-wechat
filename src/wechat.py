#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, traceback
import time

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from util.file_in_use import waitFile
from helper.browser_driver import WebDriver
from helper.my_logger import getMyLogger

def loginWechat(driver):
    # webpage: WeChat微信网页版
    loginUrl = "https://wx.qq.com/"
    url = "https://web.wechat.com/"

    logger.info('start %s', loginUrl)
    driver.loadPage(loginUrl)
    while (driver.getCurrentUrl() != url):
        time.sleep(5)
        logger.info('wait login to WeChat from phone...')
    logger.info('logged in.')
    return True

def getFriendInNavView(driver, friend):
    # left-side navigation menu
    navView = driver.findElementById('J_NavChatScrollBody')
    if navView == None:
        logger.warning('did not find nav menu')
        return None
    # <div ng-repeat="chatContact in chatList track by chatContact.UserName" class="ng-scope"...
    divs = navView.find_elements_by_css_selector('div.ng-scope')
    menuItem = 'chatContact in chatList track by chatContact.UserName'
    logger.debug('items in nav menu: %d', len(divs))
    for div in divs:
        # ignore if it is not menu item
        if div.get_attribute('ng-repeat') != menuItem:
            continue
        nickname = div.find_element_by_css_selector('h3.nickname')
        logger.debug('nickname - %s', nickname.text)
        if nickname.text == friend:
            logger.debug('found fiend: "%s"', friend)
            return div  # found the friend
    logger.info('did not find "%s" in nav menu', friend)
    return None

def getLastMsg(driver, friend):
    div = getFriendInNavView(driver, friend)
    if div is None:
        # search friend
        if searchFriend(driver, friend) is None:
            return ''
        div = getFriendInNavView(driver, friend) # try again after search
    if div is None:
        return ''

    '''
    if there is msg, it should have following data:
        <p class="msg ng-scope" ng-if="chatContact.MMDigest">
            <span ng-bind-html="chatContact.MMDigest" class="ng-binding">谢谢</span>
    '''
    msgs = div.find_elements_by_css_selector('p.msg.ng-scope')
    if len(msgs) > 0:
        return msgs[0].text
    return ''

def getCurrentFriend(driver):
    chatArea = driver.findElementById('chatArea')
    if chatArea == None:
        return None
    name = chatArea.find_element_by_tag_name('a')
    return name.text

# return True if the friend is found
def searchFriend(driver, nickname):
    retry = 3
    while retry > 0:
        retry -= 1
        # enter search, check chat header
        search = driver.findElementById('search_bar')
        if search == None:
            continue
        textInput = search.find_element_by_tag_name('input')
        textInput.clear()
        textInput.send_keys(nickname)
        textInput.send_keys(Keys.ENTER)
        delay = 5
        while delay > 0:
            if getCurrentFriend(driver) == nickname:
                textInput.clear()
                return nickname
            time.sleep(1)
            delay -= 1
    textInput.clear()
    logger.warning('!! did not find friend: %s', nickname)
    return None

def activateFriend(driver, friend):
    if getCurrentFriend(driver) != friend:
        searchFriend(driver, friend)
        if getCurrentFriend(driver) != friend:
            logger.info('failed activate friend "%s"', friend)
            return False
    return True

def uploadFile(driver, filename):
    logger.info('uploading: %s', filename)
    element = driver.findElementByName('file')
    if element == None:
        return False

    element.send_keys(filename)
    time.sleep(1)   # wait short time let uploading starts

    # this tag show up while uploading
    # <span class="status ng-scope" ng-if="chatContact.MMStatus == CONF.MSG_SEND_STATUS_SENDING">
    #   <i class="web_wechat_send web_wechat_send_w" ng-class="{'web_wechat_send_w': chatContact.UserName == currentUserName}"></i>
    # </span>
    uploading = True
    while uploading:
        status = driver.findElementsByCssSelector('span.status.ng-scope')
        if len(status) == 0:
            uploading = False
        time.sleep(1)
    ns = waitFile(filename, 15)
    logger.info('file in use timeout: %d!', ns)
    return True

def sendFilesToFriends(driver, friends):
    for name in friends:
        logger.info('send file(s) to "%s"', name)
        if activateFriend(driver, name) is False:
            logger.info('ignored to "%s"', name)
            continue
        count = 0   # number of files sent
        folderPath = driver.workingDir + '/outbox/' + name
        files = os.listdir(folderPath)
        for f in files:
            filePath = folderPath + '/' + f
            if not os.path.isfile(filePath):
                continue
            if uploadFile(driver, filePath):
                # move to sent folder
                os.remove(filePath)
                count += 1
        logger.info('sent %d file(s)', count)
    return

def sendReport(driver, friend, msg):
    if activateFriend(driver, friend) == False:
        logger.info('could not send report.')
        return
    # enter msg to textarea
    editArea = driver.findElementById('editArea')
    if (editArea == None):
        logger.warning('!! did not find input area.')
        return

    editArea.send_keys(msg)
    editArea.send_keys(Keys.ENTER)

# find any folder in outbox
# return the folder name if there is any file in side
# !! note the folder name encoding
def getOutboxFolders(workingDir):
    outboxPath = workingDir + '/outbox'
    folders = []
    outbox = os.listdir(outboxPath)
    for folderName in outbox:
        folderPath = outboxPath + '/' + folderName
        if not os.path.isdir(folderPath):
            continue
        dirs = os.listdir(folderPath)
        files = False
        for f in dirs:
            filePath = folderPath + '/' + f
            if os.path.isfile(filePath):
                files = True
        if files:
            folders.append(folderName)
    if len(folders) > 0:
        logger.info('folders %s', folders)
    return folders

def checkOutbox(driver):
    logger.debug('checking outbox...')
    # send file to friend if there is file in outbox
    folders = getOutboxFolders(driver.workingDir)
    if len(folders) > 0:
        sendFilesToFriends(driver, folders)
        to = 'File Transfer'
        msg = time.strftime('%Y-%m-%d %H:%M ') + str(folders)
        sendReport(driver, to, msg)

def inputFace(driver, n):
    editArea = driver.findElementById('editArea')
    editArea.click()

    menu = driver.findElementsByCssSelector('a.web_wechat_face')
    if len(menu) <= 0:
        logger.warning('did not find stickers icon')
        return False
    menu[0].click()
    faces = driver.findElementsByCssSelector('div.qq_face')
    if len(faces) <= 0:
        logger.warning('could not open face menu')
        return False
    links = faces[0].find_elements_by_tag_name('a')
    if n+1 <= len(links):
        links[n].click()
        editArea.send_keys(Keys.ENTER)
        return True
    return False

def checkCmd(driver):
    # response if receive any cmd from "File Transfer":
    friend = "File Transfer"
    cmd = getLastMsg(driver, friend)
    if cmd == '?' or cmd == u'？':
        if activateFriend(driver, friend) is False:
            return
        inputFace(driver, 0)
        # sendReport(friend, ":)")

class Settings(object):
    browser = 'Firefox'
    pageWidth = 800
    headless = False

def main():
    logger.info('start ... %s', __file__)
    driver = WebDriver(Settings)
    driver.setWindowSize(driver.pageWidth, 800)
    loginWechat(driver)
    time.sleep(1)  # wait fully loaded,
                    # need to find a flag when it is ready
    timeoutOutbox = 60 * 10
    timeout = 0
    while True:
        timeout -= 1
        if timeout <= 0:
            checkOutbox(driver) # check image every timeout
            timeout = timeoutOutbox
        checkCmd(driver)    # check cmd every 1 second
        time.sleep(1)
    driver.close()

if (__name__ == '__main__'):
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)
    main()
