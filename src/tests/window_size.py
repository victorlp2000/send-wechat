import time

def run(browser):
    for x in range(50, 1000, 50):
        browser.setWindowSize(x, x)
        time.sleep(1)
        t = browser.getWindowSize()
        if t['width'] != x or t['height'] != x:
            print('Failed (', t, t['width'], t['height'], ')')

    for x in range(1000, 50, -50):
        browser.setWindowSize(x, x)
        time.sleep(1)
        t = browser.getWindowSize()
        if t['width'] != x or t['height'] != x:
            print('Failed (', t, t['width'], t['height'], ')')
# Report:
# headless:False, Firefox minimum width 450, Chrome 508
# headless:True, Firefox minimum with 450, Chrome no limit
