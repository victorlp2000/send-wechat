#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  October 4, 2020
# By: Weiping Liu

class PageType(object):

    def __init__(self):
        """
            info = [
                name: website name, i.e. 'bbc'
                {
                    type: comments for the page structure
                    head: array of head tags
                    body: array of body tags
                }, ...
                ]
        """
        self.info = None
        self.fn = None

    def load(fn):
        data = json_file.readFile(self.fn)
        if isinstance(data, list):
            self.tags = data
            self.fn = fn

    def save(self, info, fn=None):
        if fn != None:
            self.fn = fn
        self.info = info
        json_file.saveFile(self.fn, self.info)

    def getChildrenTagNames(self, elem):
        tagName = []
        list = elem.find_elements_by_xpath('*')
        for t in list:
            tagName.append(t.tag_name)
        return tagName

    def getInfo(self, browser):
        info = {}
        info['head'] = getChildrenTagNames(browser.find_element_by_tag_name('head'))
        info['body'] = getChildrenTagNames(browser.find_element_by_tag_name('body'))
