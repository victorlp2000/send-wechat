#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created:  October 4, 2020
# By: Weiping Liu

class PageMeta(object):

    def __init__(self):
        """
            info = [
                {
                    type: comments for the page structure
                    url:
                    html: {
                        head: [array of head tags]
                        body: [array of body tags]
                    }
                },
                ...
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

    def getMeta(self, browser):
        info = {}
        html = {}
        html['head'] = self.getChildrenTagNames(browser.find_element_by_tag_name('head'))
        html['body'] = self.getChildrenTagNames(browser.find_element_by_tag_name('body'))
        url = browser.current_url
        info['url'] = url
        info['html'] = html
        print(info)
