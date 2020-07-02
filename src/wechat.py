#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, traceback
import time
from PIL import Image

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from util.file_in_use import waitFile
from helper.browser_driver import WebDriver
from helper.my_logger import getMyLogger
from util.pid_man import PidMan

def getQRCode(driver):
    qrcode = driver.getBrowser().find_element_by_css_selector('div.qrcode')
    # once accepted, class become 'qrcode hide'
    if qrcode.get_attribute('class') == 'qrcode':
        img = qrcode.find_element_by_tag_name('img')
        png = img.screenshot_as_png
        return png
    return None

def showQRCode(qr):
    fn = '/tmp/qrcode.png'
    with open(fn, "wb") as file:
        file.write(qr)

    png = Image.open(fn)
    png.show()

def loginWechat(driver):
    # webpage: WeChat微信网页版
    loginUrl = "https://wx.qq.com/"
    url = "https://web.wechat.com/"

    logger.info('start %s', loginUrl)
    driver.loadPage(loginUrl)
    qr0 = getQRCode(driver)
    timeout = 10    # loop 10 times
    while (driver.getCurrentUrl() != url):
        if driver.headless:
            qr = getQRCode(driver)
            if qr != None and len(qr0) != len(qr):
                qr0 = qr    # qr image updated
                showQRCode(qr)
        logger.info('wait login to WeChat from phone...')
        print('\a')     # alerm sound
        time.sleep(3)
        timeout -= 1
        if timeout <= 0:
            return False
    logger.info('logged in.')
    return True

def getFriendFromNavView(driver, friend):
    # left-side navigation menu
    navView = driver.findElementById('J_NavChatScrollBody')
    if navView == None:
        logger.warning('browser was crashed?')
        return None
    # <div ng-repeat="chatContact in chatList track by chatContact.UserName" class="ng-scope"...
    divs = navView.find_elements_by_css_selector('div.ng-scope')
    menuItem = 'chatContact in chatList track by chatContact.UserName'
    names = []
    for div in divs:
        # ignore if it is not menu item
        if div.get_attribute('ng-repeat') != menuItem:
            continue
        nickname = div.find_element_by_css_selector('h3.nickname')
        names.append(nickname.text)
        if nickname.text == friend:
            logger.debug('found fiend: "%s"', friend)
            return div  # found the friend
    logger.info('did not find "%s" in nav menu', friend)
    logger.info(names)
    return None

def getLastMsg(driver, friend):
    div = getFriendFromNavView(driver, friend)
    if div is None:
        # search friend
        if searchFriend(driver, friend) is None:
            return ''
        div = getFriendFromNavView(driver, friend) # try again after search
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
    try:
        # enter search, check chat header
        search = driver.findElementById('search_bar')
        if search == None:
            return None
        textInput = search.find_element_by_tag_name('input')
        textInput.clear()
        textInput.send_keys(nickname)
        time.sleep(2)
        textInput.send_keys(Keys.ENTER)
        time.sleep(2)   # wait response after entering text
        delay = 5
        while delay > 0:
            if getCurrentFriend(driver) == nickname:
                textInput.clear()
                return nickname
            time.sleep(2)
            delay -= 1
        textInput.clear()
        logger.warning('!! did not find friend: %s', nickname)
    except:
        logger.error('!! error in searching friend "%s"', nickname)
        # traceback()
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
    ns = waitFile(filename, 30)
    logger.info('file in use timeout: %d!', ns)
    return True

def sendFilesToFriends(driver, friends):
    logger.debug('sendFilesToFriends...')
    count = 0   # number of files sent
    for name in friends:
        logger.info('send file(s) to "%s"', name)
        if activateFriend(driver, name) is False:
            logger.info('ignored to "%s"', name)
            continue
        folderPath = driver.workingDir + '/outbox/' + name
        files = os.listdir(folderPath)
        for f in files:
            filePath = folderPath + '/' + f
            if not os.path.isfile(filePath):
                continue
            if uploadFile(driver, filePath):
                # remove from the outbox folder
                os.remove(filePath)
                count += 1
        logger.info('sent %d file(s)', count)
    return count

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
    time.sleep(1)
    editArea.send_keys(Keys.ENTER)

# find any folder in outbox
# return the folder name if there is any file in side
# !! note the folder name encoding
def getOutboxFolders(workingDir):
    logger.debug('getOutboxFolders...')
    outboxPath = workingDir + '/outbox'
    folders = []
    outbox = os.listdir(outboxPath)
    for folderName in outbox:
        folderPath = outboxPath + '/' + folderName
        if not os.path.isdir(folderPath):
            continue
        if folderName.startswith('~'):  # folder for internal use
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
    logger.info('checking outbox...')
    # send file to friend if there is file in outbox
    folders = getOutboxFolders(driver.workingDir)
    if len(folders) > 0:
        if sendFilesToFriends(driver, folders) > 0:
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
        time.sleep(1)
        editArea.send_keys(Keys.ENTER)
        return True
    return False

def checkCmd(driver):
    logger.debug('checkCmd...')
    # response if receive any cmd from "File Transfer":
    friend = "File Transfer"
    cmd = getLastMsg(driver, friend)
    if not (cmd.startswith('?') or cmd.startswith(u'？')):
        return 0

    # process cmd
    logger.info('received cmd: %s', cmd)
    if cmd == '?' or cmd == u'？':
        if activateFriend(driver, friend) is False:
            return 0
        # sendReport(friend, ":)")
        inputFace(driver, 0)
    elif cmd == '?exit':    # exit wechat
        return -1
    return 0

class Settings(object):
    browser = 'Firefox'
    pageWidth = 800
    headless = True

def main():
    logger.info('start ... %s', __file__)
    driver = WebDriver(Settings)
    pidMan = PidMan('wechat', '.')
    pidMan.save(driver.getPIDs())
    driver.setWindowSize(driver.pageWidth, 800)
    if loginWechat(driver) == True:
        time.sleep(15)  # wait fully loaded,
                        # need to find a flag when it is ready
        timeoutOutbox = 12 * 5
        timeout = 0
        while True:
            timeout -= 1
            if timeout <= 0:
                checkOutbox(driver) # check image every timeout
                timeout = timeoutOutbox
                # pidMan.save(driver.getPIDs())
            # if checkCmd(driver) == -1:
            #     break
            time.sleep(5)
    pidMan.clean()
    driver.close()

if (__name__ == '__main__'):
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)
    main()
