#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 16, 2020
# By: Weiping Liu

from PIL import Image
from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def convertToJpeg(fnPng, fnJpg=None):
    logger.debug('convert to jpg')
    if fnPng.endswith('.png'):
        if fnJpg == None:
            fnJpg = fnPng[:-4] + '.jpg'
        img = Image.open(fnPng).convert('RGB')
        img.save(fnJpg, 'JPEG')
        return fnJpg
    logger.warning('convert from wrong png: %s', fnPng)
    return fnPng

if __name__ == '__main__':
    import sys
    jpg = None
    if len(sys.argv) > 2:
        jpg = sys.argv[2]
    if len(sys.argv) > 1:
        print(convertToJpeg(sys.argv[1], jpg))
