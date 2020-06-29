#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  June 9, 2020
# By: Weiping Liu

import os, time

class PidMan(object):
    def __init__(self, workingDir='.'):
        self.folder = workingDir + '/.pid'
        self.fn = None
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
        t = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        self.fn = self.folder + '/' + t + '.pid'

        # json_file.saveFile(self.fn, pids)
        f = open(self.fn, 'w')
        f.write(s)
        f.close()
        return self.fn

    def clean(self):
        if self.fn != None:
            os.remove(self.fn)
            self.fn = None
