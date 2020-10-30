import os
import time

def run(browser):
    cwd = os.getcwd()
    url = 'file://' + cwd + '/tests/my_page_1.html'
    browser.getBrowser().get(url)

    for x in range(80, 121, 20):
        browser.setZoom(x)
        # time.sleep(2)
        fn = 'test-' + str(x) + '.png'
        print('save as', fn)
        browser.savePageImage(fn)
