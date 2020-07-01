#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time

class PidMan(object):
    def __init__(self, fid, workingDir=None):
        if workingDir == None:
            self.folder = './.pid'
        else:
            self.folder = workingDir

        self.fn = None
        self.fid = fid
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

    def save(self, pids):
        # convert array to string
        s = ' '.join(map(str, pids)) + '\n'

        # only keep the last saved pids
        if self.fn != None:
            self.clean()

        # generate filename
        # t = time.time()
        # self.fn = self.folder + '/' + str(t) + '.pid'
        t = time.strftime("%Y%m%d-%H%M%S-", time.localtime())
        self.fn = self.folder + '/' + t + self.fid + '.pid'

        # json_file.saveFile(self.fn, pids)
        f = open(self.fn, 'w')
        f.write(s)
        f.close()
        return self.fn

    def clean(self):
        if self.fn != None:
            os.remove(self.fn)
            self.fn = None
