#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os
import json
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

# read utf8 json defaultContact
# convert to unicode for the return object
def readFile(filename):
    logger.info('loading %s ...', filename)
    if os.path.isfile(filename):
        with open(filename) as infile:
            return json.load(infile)
    return None

# save unicode data into file
# need to be converted into utf8
def saveFile(filename, dictObj):
    with open(filename, 'w') as outfile:
        str = json.dumps(dictObj,
                         indent=2,
                         ensure_ascii=False)
        outfile.write(str)

if __name__ == '__main__':
    d = readFile('./tests/test-encoding0.json')
    if type(d) is dict:
        print (d)
        saveFile('./test-encoding1.json', d)

    d = readFile('./tests/test-array.json')
    if type(d) is list:
        print (d)
