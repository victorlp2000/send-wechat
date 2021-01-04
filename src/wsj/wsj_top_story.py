import os, time
import urllib.parse

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

# return 'url' of article link
def findArticleUrl(driver):
    logger.info('looking for article')
    browser = driver.getBrowser()

    articles = browser.find_elements_by_tag_name('article')
    a = articles[0].find_element_by_tag_name('a')

    return a.get_attribute('href')
