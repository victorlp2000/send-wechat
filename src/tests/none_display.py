import os

def run(browser):
    cwd = os.getcwd()
    url = 'file://' + cwd + '/tests/my_page_1.html'
    browser.loadPage(url)

    selectors = ["p.fact5"]
    ids = ["item3", "item6"]

    input("press ENTER to remove colored lines")
    browser.noneDisplayByIds(ids)
    browser.noneDisplayByCSSSelectors(selectors)
