#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  May 24, 2020
# By: Weiping Liu

import os
import shutil
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def copyToContacts(image, fn, contacts):
    for contact in contacts:
        contactFolder = './outbox' + '/' + contact
        logger.debug('check folder: "%s"', contactFolder)
        if folderExists(contactFolder):
            logger.info('Save "%s" to "%s".', fn, contact)
            shutil.copyfile(image, contactFolder + '/' + fn)

def folderExists(folder):
    return os.path.isdir(folder)
