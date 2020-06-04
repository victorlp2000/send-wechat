#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, traceback
import time

import logging

import file_in_use

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

browser = 'Firefox'

from selenium.webdriver import Firefox
driver = Firefox()
driver.set_window_size(800, 1000)

def loginWechat():
    # webpage: WeChat微信网页版
    url = "https://wx.qq.com/"
    loginUrl = "https://web.wechat.com/"

    logger.info('start login...')
    driver.get(url)
    while (driver.current_url != loginUrl):
        time.sleep(5)
        logger.info('wait login to WeChat from phone...')
    logger.info('logged in.')
    return True

def getFriendInNavView(friend):
    try:
        # left-side navigation menu
        navView = driver.find_element_by_id('J_NavChatScrollBody')
        # <div ng-repeat="chatContact in chatList track by chatContact.UserName" class="ng-scope"...
        divs = navView.find_elements_by_css_selector('div.ng-scope')
        menuItem = 'chatContact in chatList track by chatContact.UserName'
        logger.debug('items: %d', len(divs))
        for div in divs:
            # ignore if it is not menu item
            if div.get_attribute('ng-repeat') != menuItem:
                continue
            nickname = div.find_element_by_css_selector('h3.nickname')
            logger.debug('nickname - %s', nickname.text)
            if nickname.text == friend:
                return div  # found the friend
        return None
    except:
        logger.warning('!! error in search friend in nav view')
        traceback.print_exc()
        return None

def getLastMsg(friend):
    div = getFriendInNavView(friend)
    if div is None:
        logger.info('the friend is not in nav view, searching...')
        # search friend
        if searchFriend(friend) is None:
            logger.info('did not find friend "%s"', friend)
            return ''
        div = getFriendInNavView(friend) # try again after search
    if div is None:
        logger.info('failed activate friend')
    try:
        msg = div.find_element_by_css_selector('p.msg.ng-scope')
        return msg.text
    except:
        # may not have any msg tag
        logger.info('did not find msg tag')
        return ''

def getCurrentFriend():
    chatArea = driver.find_element_by_id('chatArea')
    name = chatArea.find_element_by_tag_name('a')
    return name.text

# return True if the friend is found
def searchFriend(nickname):
    retry = 3
    try:
        while retry > 0:
            # enter search, check chat header
            search = driver.find_element_by_id('search_bar')
            textInput = search.find_element_by_tag_name('input')
            textInput.clear()
            textInput.send_keys(nickname)
            textInput.send_keys(Keys.ENTER)
            delay = 5
            while delay > 0:
                if getCurrentFriend() == nickname:
                    textInput.clear()
                    return nickname
                time.sleep(1)
                delay -= 1
            retry -= 1
        textInput.clear()
        logger.warning('!! did not find friend: %s', nickname)
        return None
    except:
        logger.warning('!! got exception in searchFriend()')
        return None

def activateFriend(friend):
    if getCurrentFriend() != friend:
        searchFriend(friend)
        if getCurrentFriend() != friend:
            return False
    return True

def uploadFile(filename):
    logger.info('uploading file...')
    element = driver.find_element_by_name("file")
    element.send_keys(filename)
    time.sleep(1)   # wait short time let uploading starts

    # this tag show up while uploading
    # <span class="status ng-scope" ng-if="chatContact.MMStatus == CONF.MSG_SEND_STATUS_SENDING">
    #   <i class="web_wechat_send web_wechat_send_w" ng-class="{'web_wechat_send_w': chatContact.UserName == currentUserName}"></i>
    # </span>
    uploading = True
    while uploading:
        status = driver.find_elements_by_css_selector('span.status.ng-scope')
        if len(status) == 0:
            uploading = False
        time.sleep(1)
    file_in_use.waitFile(filename, 5)   # double check
    return

def sendFilesToFriends(workingDir, friends):
    for name in friends:
        if activateFriend(name) is True:
            sendFilesToFriend(workingDir, name)


def sendFilesToFriend(workingDir, name):
    count = 0   # number of files sent
    folderPath = workingDir + '/outbox/' + name
    files = os.listdir(folderPath)
    for f in files:
        filePath = folderPath + '/' + f
        if os.path.isfile(filePath):
            uploadFile(filePath)
            # move to sent folder
            os.rename(filePath, workingDir + '/sent/' + f)
            count += 1
    return count

def sendReport(friend, msg):
    if activateFriend(friend) == False:
        return
    # enter msg to textarea
    editArea = driver.find_element_by_id('editArea')
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
    logger.info('%d folders in outbox', len(folders))
    return folders

def checkOutbox(workingDir):
    # send file to friend if there is file in outbox
    folders = getOutboxFolders(workingDir)
    if len(folders) > 0:
        n = sendFilesToFriends(workingDir, folders)
        to = 'File Transfer'
        msg = time.strftime('%Y-%m-%d %H:%M ') + str(folders)
        sendReport(to, msg)

def inputFace(n):
    editArea = driver.find_element_by_id('editArea')
    editArea.click()

    menu = driver.find_element_by_css_selector('a.web_wechat_face')
    menu.click()
    faces = driver.find_element_by_css_selector('div.qq_face')
    links = faces.find_elements_by_tag_name('a')
    if n+1 <= len(links):
        links[n].click()
        editArea.send_keys(Keys.ENTER)
        return True
    return False

def checkCmd():
    # response if receive any cmd from "File Transfer":
    friend = "File Transfer"
    cmd = getLastMsg(friend)
    if cmd == '?' or cmd == u'？':
        if activateFriend(friend) is False:
            logger.info('failed activate friend "%s"', friend)
            return
        inputFace(0)
        # sendReport(friend, ":)")

def main(workingDir):
    loginWechat()
    time.sleep(1)  # wait fully loaded,
                    # need to find a flag when it is ready
    timeoutOutbox = 1200
    timeout = timeoutOutbox
    while True:
        timeout += 1
        if timeout >= timeoutOutbox:
            timeout = 0
            checkOutbox(workingDir)
        checkCmd()
        time.sleep(1)

if (__name__ == '__main__'):
    logger = logging.getLogger('wechat')
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

    main(os.path.abspath('.'))
    driver.close()

# element = driver.find_element_by_name("file")
# element.send_keys("/home/pavel/Desktop/949IH3GNHAo.jpg")

# driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
