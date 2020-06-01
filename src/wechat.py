#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time

import logging

import file_in_use

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

# after functional key or mouse click, need to wait until page finish action
WAIT_KEY_ACTION_TIME = 0.1

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

# return True if the friend is found
def getFriend(nickname):
    logger.info('switch to "%s"...', nickname)
    retry = 3
    while retry > 0:
        # enter search, check chat header
        search = driver.find_element_by_id('search_bar')
        textInput = search.find_element_by_tag_name('input')
        textInput.clear()
        textInput.send_keys(nickname)
        textInput.send_keys(Keys.ENTER)
        delay = 5
        while delay > 0:
            chatArea = driver.find_element_by_id('chatArea')
            name = chatArea.find_element_by_tag_name('a')
            if name.text == nickname:
                textInput.clear()
                return nickname
            time.sleep(1)
            delay -= 1
        retry -= 1
    textInput.clear()
    logger.warning('!! did not find friend: %s', nickname)
    return None

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
        friend = getFriend(name)
        if friend != None:
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
    friend = getFriend(friend)
    if friend == None:
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
        for f in dirs:
            filePath = folderPath + '/' + f
            if os.path.isfile(filePath):
                folders.append(folderName)
    logger.info('%d folders in outbox', len(folders))
    return folders

def main(workingDir):
    loginWechat()
    time.sleep(15)  # wait fully loaded,
                    # need to find a flag when it is ready
    while True:
        folders = getOutboxFolders(workingDir)
        if len(folders) > 0:
            n = sendFilesToFriends(workingDir, folders)

        to = 'File Transfer'
        msg = time.strftime('%Y-%m-%d %H:%M ') + str(folders)
        sendReport(to, msg)

        time.sleep(1800)  # wait seconds

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
