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

# select browser
# browser = 'Chrome'
browser = 'Firefox'

if (browser == 'Chrome'):
    from selenium.webdriver import Chrome
    driver = Chrome()
elif (browser == 'Firefox'):
    from selenium.webdriver import Firefox
    driver = Firefox()
# from selenium.webdriver.support.ui import WebDriverWait
#
driver.set_window_size(800, 1000)

# driver.manage().window().setSize(new Dimension(1024,768));
#driver.close()

def loginWechat():
    # webpage: WeChat微信网页版
    url = "https://wx.qq.com/"
    loginUrl = "https://web.wechat.com/"

    if (driver.current_url != url):
        driver.get(url)
    while (driver.current_url != loginUrl):
        time.sleep(5)
        logger.info('wait login to WeChat from phone...')
    logger.info('logged in.')
    return True

# whenever the list changes,
# need to call this function to get new user list
def updateUserList(list):
    userList = []
    divs = list.find_elements_by_tag_name('div')
    for item in divs:
        if item.get_attribute('ng-repeat') != None:
            userList.append(item)
    return userList

# active user is the one whos class include 'active'
def getActiveUser(users):
    active = None
    for item in users:
        div = item.find_element_by_tag_name('div')
        attr = div.get_attribute('class')
        if ('active' in attr.split()):
            active = item
            break
    return active

def getNickName(user):
    nickname = user.find_element_by_css_selector('h3.nickname')
    if (nickname != None):
        return nickname.text
    return ''

def getDataUserName(user):
    div = user.find_element_by_tag_name('div')
    attr = div.get_attribute('data-username')
    return attr

# to top
#   click the first user
#   get active user
#   press UP
#   check active user is the same (at top)
def goTop(list):
    userList = updateUserList(list)
    if (len(userList) == 0):
        logger.warning('!! did not find user in the list, something wrong.')
        return

    # click the first user
    userList[0].click()
    time.sleep(WAIT_KEY_ACTION_TIME)
    activeUser = getActiveUser(updateUserList(list))
    if (activeUser == None):
        logger.warning('!! the clicked user does not go active.')
        return

    body = driver.find_element_by_tag_name('body')
    while (True):
        body.send_keys(Keys.UP)
        time.sleep(WAIT_KEY_ACTION_TIME)
        newActive = getActiveUser(updateUserList(list))
        if (newActive == None):
            logger.warning('!! UP key does not active new user in the list.')
            return
        if (getDataUserName(activeUser) == getDataUserName(newActive)):
            break   # got top
        activeUser = newActive
    return activeUser

def getContact(nickname):
    if (nickname == None or nickname == ''):
        return None

    list = driver.find_element_by_id('J_NavChatScrollBody')

    current = goTop(list)
    if (current == None):
        return None

    name = getNickName(current)
    if (name == nickname):
        return current
    body = driver.find_element_by_tag_name('body')

    # press DOWN, get one by one
    while (True):
        body.send_keys(Keys.DOWN)
        time.sleep(WAIT_KEY_ACTION_TIME)
        newActive = getActiveUser(updateUserList(list))
        if (newActive == None):
            logger.warning('!! UP key does not active new user in the list.')
            return None
        name = getNickName(newActive)
        if (name == nickname):
            return newActive
        if (getDataUserName(current) == getDataUserName(newActive)):
            break   # got bottom
        current = newActive
    logger.warning('!! did not find contact: %s', nickname)
    return None

# send a list of msgs to the contact
def sendTextMessage(contact, msgs):
    # click user to get focus
    contact.click()

    # enter msg to textarea
    editArea = driver.find_element_by_id('editArea')
    if (editArea == None):
        logger.warning('!! did not find input area.')
        return

    for line in msgs:
        editArea.send_keys(line)
        editArea.send_keys(Keys.CONTROL + Keys.ENTER)

    # press send button
    sendButton = driver.find_element_by_css_selector('a.btn.btn_send')
    sendButton.click()
    return

def uploadFile(filename):
    element = driver.find_element_by_name("file")
    element.send_keys(filename)
    time.sleep(3)   # wait short time let uploading starts
    # this tag show up while uploading
    # <span class="status ng-scope" ng-if="chatContact.MMStatus == CONF.MSG_SEND_STATUS_SENDING">
    #   <i class="web_wechat_send web_wechat_send_w" ng-class="{'web_wechat_send_w': chatContact.UserName == currentUserName}"></i>
    # </span>
    file_in_use.waitFile(filename)
    return

def sendFilesToContact(workingDir, folderName):
    # folder name is used as contact
    # nickName = unicode(folderName, 'utf8')
    contact = getContact(folderName)
    if (contact == None):
        return

    count = 0   # number of files sent
    folderPath = workingDir + '/outbox/' + folderName
    files = os.listdir(folderPath)
    for f in files:
        filePath = folderPath + '/' + f
        if os.path.isfile(filePath):
            uploadFile(filePath)
            logger.info('Sent %s to %s".', f, folderName)
            # move to sent folder
            os.rename(filePath, workingDir + '/sent/' + f)
            count += 1
    return count

# find any folder in outbox
# return the folder name if there is any file in side
# !! note the folder name encoding
def checkOutboxFolder(workingDir):
    outboxPath = workingDir + '/outbox'
    outbox = os.listdir(outboxPath)
    for folderName in outbox:
        folderPath = outboxPath + '/' + folderName
        if not os.path.isdir(folderPath):
            continue
        folders = os.listdir(folderPath)
        for f in folders:
            filePath = folderPath + '/' + f
            if os.path.isfile(filePath):
                return folderName
    return None

def main(workingDir):
    loginWechat()
    time.sleep(15)  # wait fully loaded,
                    # need to find a flag when it is ready
    while True:
        folder = checkOutboxFolder(workingDir)
        if folder != None:
            n = sendFilesToContact(workingDir, folder)
        time.sleep(600)  # wait ten minutes

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
