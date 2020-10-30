from urllib.parse import urlparse
import os

def run(browser):
    url = 'http://www.google.com'
    browser.getBrowser().get(url)
    u = browser.getBrowser().current_url
    p = urlparse(u)
    if p.netloc != urlparse(url).netloc:
        print('failed to "%s"', url)

    cwd = os.getcwd()
    url = 'file://' + cwd + '/tests/my_page_1.html'
    browser.getBrowser().get(url)
    u = browser.getBrowser().current_url
    if u != url:
        print('failed to "%s"', url)
    print('test url location ... pass')
