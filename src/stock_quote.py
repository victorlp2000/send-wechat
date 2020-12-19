#!/usr/bin/python
# -*- coding: utf-8 -*-

# Created at:  June 11, 2020
# By: Weiping Liu

import time, os
from helper.browser_driver import WebDriver


def getQuote(browser, symbol):
    url = 'https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch'
    xpath = '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]'
    browser.get(url)
    div = browser.find_element_by_xpath(xpath)
    return div.text

def findSymbol(s):
    start = s.find('(')
    end = s.find(')', start)
    return s[start+1:end]

def main(config):
    driver = WebDriver(config['settings'])
    browser = driver.getBrowser()
    symbol = [
        # 'Chesapeake Energy Corporation (CHK)',
        'Chesapeake Energy Corporation (CHKAQ)',
        'Morgan Stanley Insight Fund Class A (CPOAX)',
        'Dropbox, Inc. (DBX)',
        # 'Denbury Resources Inc. (DNR)',
        # 'Fidelity Four-in-One Index Fund (FFNOX)',
        'The Home Depot, Inc. (HD)',
        # 'JD.com, Inc. (JD)',
        # 'Luckin Coffee Inc. (LK)',
        'Lowe\'s Companies, Inc. (LOW)',
        'NIO Limited (NIO)',
        'NVIDIA Corporation (NVDA)',
        'PG&E Corporation (PCG)',
        'Roku, Inc. (ROKU)',
        'Sparrow Growth Fund Class A (SGFFX)',
        'Virgin Galactic Holdings, Inc. (SPCE)',
        'Talend S.A. (TLND)',
        'Weatherford International plc (WFTLF)',
        'Weatherford International plc (WFTUF)',
    ]

    for s in symbol:
        code = findSymbol(s)
        quote = getQuote(browser, code)
        print(code, quote)
    browser.quit()

if __name__ == "__main__":
    config = {
      "settings": {
        "browser": "Chrome",
        "headless": False,
      }
    }
    main(config)
