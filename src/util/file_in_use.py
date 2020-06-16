#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import psutil
import time

def hasHandle(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass

    return False

# return if the file has no access
def waitFile(fpath, timeoutSeconds=0):
    while hasHandle(fpath):
        time.sleep(1)
        if timeoutSeconds == 0:
            break
        timeoutSeconds -= 1
    return timeoutSeconds       # 0 for timeout

if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print (fpath, hasHandle(fpath))
