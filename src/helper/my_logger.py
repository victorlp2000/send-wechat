#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import logging
from logging.handlers import RotatingFileHandler

def getMyLogger(name=None, fn=None):
    logger = logging.getLogger('mylog')
    if fn != None:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # create console handler and set level to debug
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if fn.endswith('.py'):
            logfn = './logs/' + fn[:-3] + '.log'
        else:
            logfn = './logs/' + fn + '.log'
        handler = RotatingFileHandler(logfn, maxBytes=10000, backupCount=1)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
