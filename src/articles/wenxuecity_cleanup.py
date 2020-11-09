import time
from helper.my_logger import getMyLogger
from selenium.webdriver.common.action_chains import ActionChains

logger = getMyLogger(__name__)

def cleanupPage(driver):
    logger.info('cleaning content')
    driver.scrollToBottom(1.5)
    browser = driver.getBrowser()

    actions = ActionChains(browser)

    # button = browser.find_element_by_id('cbb')
    selectors = [
        'h2.comment-title',
        'div.comments',
        'div.ad_center'
    ]
    for selector in selectors:
        elements = browser.find_elements_by_css_selector(selector)
        for element in elements:
            browser.execute_script("arguments[0].style.display = 'none';", element)

    sponsor = browser.find_element_by_tag_name('amp-embed')
    browser.execute_script("arguments[0].style.display = 'none';", sponsor)

    header = browser.find_element_by_tag_name('header')
    browser.execute_script("arguments[0].style.position = 'relative';", header)
