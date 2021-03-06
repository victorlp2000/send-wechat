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
from helper import crontab
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
    driver.getBrowser().get(loginUrl)
    qr0 = getQRCode(driver)
    timeout = 15    # loop 10 times
    while (driver.getBrowser().current_url != url):
        if driver.headless:
            qr = getQRCode(driver)
            if qr != None and len(qr0) != len(qr):
                qr0 = qr    # qr image updated
                showQRCode(qr)
        logger.info('wait login to WeChat from phone')
        print('\a')     # alerm sound
        time.sleep(3)
        timeout -= 1
        if timeout <= 0:
            return False
    logger.info('logged in.')
    return True

def getFriendFromNavView(driver, friend):
    # left-side navigation menu
    navView = driver.driver.find_element_by_id('J_NavChatScrollBody')
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
    logger.warning('did not find "%s" in nav menu', friend)
    logger.info(names)
    return None

def getCurrentFriend(driver):
    chatArea = driver.driver.find_element_by_id('chatArea')
    if chatArea == None:
        return None
    name = chatArea.find_element_by_tag_name('a')
    return name.text

# return True if the friend is found
def searchFriend(driver, nickname):
    try:
        # enter search, check chat header
        search = driver.driver.find_element_by_id('search_bar')
        if search == None:
            return None
        textInput = search.find_element_by_tag_name('input')
        textInput.clear()
        time.sleep(2)
        textInput.send_keys(nickname)
        time.sleep(2)
        textInput.send_keys(Keys.ENTER)
        time.sleep(3)   # wait response after entering text
        delay = 5
        while delay > 0:
            if getCurrentFriend(driver) == nickname:
                textInput.clear()
                return nickname
            time.sleep(2)
            delay -= 1
        textInput.clear()
        time.sleep(2)
        logger.warning('!! did not find friend: %s', nickname)
    except:
        logger.error('!! error in searching friend "%s"', nickname)
        driver.saveFullPageToJpg('error-wechat.jpg')
        # traceback()
    return None

def activateFriend(driver, friend):
    if getCurrentFriend(driver) != friend:
        searchFriend(driver, friend)
        if getCurrentFriend(driver) != friend:
            logger.warning('failed activate friend "%s"', friend)
            return False
    return True

def uploadFile(driver, filename):
    logger.info('uploading: %s', filename)
    element = driver.driver.find_element_by_name('file')
    if element == None:
        return False

    element.send_keys(filename)
    time.sleep(5)   # wait short time let uploading starts

    # this tag show up while uploading
    # <span class="status ng-scope" ng-if="chatContact.MMStatus == CONF.MSG_SEND_STATUS_SENDING">
    #   <i class="web_wechat_send web_wechat_send_w" ng-class="{'web_wechat_send_w': chatContact.UserName == currentUserName}"></i>
    # </span>
    waitUploading = 80  # no more than 8 min, or next scanning come
    while waitUploading > 0:
        status = driver.driver.find_elements_by_css_selector('span.status.ng-scope')
        if len(status) == 0:
            break
        logger.info('waiting for uploading finish')
        time.sleep(6)
        waitUploading -= 1

    ns = waitFile(filename, 60)
    logger.info('file in use timeout: %d!', ns)
    return True

def sendFilesToFriends(driver, friends):
    logger.debug('sendFilesToFriends')
    count = 0   # number of files sent
    report = ''
    for name in friends:
        logger.info('send file(s) to "%s"', name)
        if activateFriend(driver, name) is False:
            logger.info('ignored to "%s"', name)
            continue
        folderPath = driver.workingDir + '/outbox/' + name
        files = os.listdir(folderPath)
        if report != '':
            report += '\n'
        report += 'To ' + name + ': '
        for f in files:
            filePath = folderPath + '/' + f
            if not os.path.isfile(filePath):
                continue
            # move to sent folder, then upload,
            # back to original location if sent failed
            tmp = '/tmp/' + f
            os.rename(filePath, tmp)
            if uploadFile(driver, tmp):
                count += 1
                report += f + ' '
            else:
                logger.warning('failed to send file %s', filePath)
                os.rename(tmp, filePath)
    return report

def sendReport(driver, friend, msg):
    if activateFriend(driver, friend) == False:
        logger.warning('could not send report.')
        return
    # enter msg to textarea
    editArea = driver.driver.find_element_by_id('editArea')
    if (editArea == None):
        logger.warning('!! did not find input area.')
        return
    logger.info(msg)
    msg.replace('\n', ' ')
    editArea.send_keys(msg)
    time.sleep(2)
    editArea.send_keys(Keys.ENTER)
    time.sleep(2)

# find any folder in outbox
# return the folder name if there is any file in side
# !! note the folder name encoding
def getOutboxFolders(workingDir):
    logger.debug('getOutboxFolders')
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
    logger.info('check Outbox')
    # send file to friend if there is file in outbox
    folders = getOutboxFolders(driver.workingDir)
    if len(folders) > 0:
        report = sendFilesToFriends(driver, folders)
        to = 'File Transfer'
        sendReport(driver, to, report)

def main():
    logger.info('start "%s"', __file__)
    settings = {
        'browser': 'Chrome',
        'pageWidth': 800,
        'headless': False
    }
    driver = WebDriver(settings)
    pidMan = PidMan('wechat', '.')
    pidMan.save(driver.getPIDs())
    driver.setWindowSize(driver.pageWidth, 800)
    if loginWechat(driver) == True:
        time.sleep(15)  # wait fully loaded,
                        # need to find a flag when it is ready
        delayMin = 5
        while True:
            driver.saveFullPageToJpg('wechat.jpg')
            checkOutbox(driver)
            cmd = crontab.getCrontabSetting('scan_websites.sh')
            if cmd != None:
                logger.debug('crontab: "%s..."', cmd[:40])
                t = time.localtime()
                s = cmd.split()
                waitTime = crontab.nextMatchSeconds(t, s)
                logger.info('next check at %d:%02d plus %d min', waitTime[1], waitTime[2], delayMin)
                # delay 5 min for scanning webpages finish
                delay = waitTime[0] + (delayMin * 60)
                time.sleep(delay)
            else:
                time.sleep(delayMin * 60)
    pidMan.clean()
    driver.getBrowser().quit()

if (__name__ == '__main__'):
    fn = os.path.basename(__file__)
    logger = getMyLogger(None, fn)
    main()
