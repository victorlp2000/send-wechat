import time

def run(browser):
    for x in range(600, 1000, 50):
        browser.setWindowSize(x, x)
        time.sleep(1)
        t = browser.getWindowSize()
        if t['width'] != x or t['height'] != x:
            print('Failed at %d', x)

    for x in range(1000, 600, -50):
        browser.setWindowSize(x, x)
        time.sleep(1)
        t = browser.getWindowSize()
        if t['width'] != x or t['height'] != x:
            print('Failed at %d', x)
    print('get/set window size ... pass')
