import os
import time

def run(browser):
    cwd = os.getcwd()
    url = 'file://' + cwd + '/tests/my_page_1.html'
    browser.loadPage(url)

    browser.setWindowSize(500, 500)
    for x in range(60, 160, 20):
        browser.setZoom(x)
        time.sleep(5)
        h = browser.getPageLength()
        print("zoom", x, "length", h)
