import os, time
import urllib.parse

from helper.my_logger import getMyLogger

logger = getMyLogger(__name__)

def getTopNews(driver, url):
    logger.info('loading "%s"', url)
    driver.getBrowser().get(url)
    time.sleep(10)
    browser = driver.getBrowser()
    # p = '//*[@id="root"]/div/div/div/div[2]/div/div/article/div[1]/h3/a'
    p = '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[1]/article/div[2]/h3/a'
    headline = browser.find_element_by_xpath(p)
    P = '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[1]/article/p'
    subHead = browser.find_element_by_xpath(P)

    return {
        'head': headline.text,
        'link': urllib.parse.unquote(headline.get_attribute('href')),
        'body': [subHead.text]
        }
