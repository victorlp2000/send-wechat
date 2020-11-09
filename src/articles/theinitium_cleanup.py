import time
from helper.my_logger import getMyLogger
from selenium.webdriver.common.action_chains import ActionChains

logger = getMyLogger(__name__)

def cleanupPage(driver):
    logger.info('cleaning content')
    driver.scrollToBottom(1.5)
    browser = driver.getBrowser()

    actions = ActionChains(browser)

    # button = browser.find_element_by_xpath('//button[text()="關閉廣告"]')
    button = None
    timeout = 20
    while timeout > 0:
        time.sleep(2)
        try:
            button = browser.find_element_by_css_selector('button.c-ad__btn')
            attr = button.get_attribute('class')
            if not 'hidden' in attr.split(' '):
                break
            else:
                timeout -= 1
        except:
            pass
        print('wait...', timeout)
    # button = browser.find_element_by_id('cbb')
    # print(button)
    time.sleep(2)
    actions.move_by_offset(10, 10).click().perform()
    # input('wait')
    selectors = [
        'div.article__foot',
        'section.c-ad.u-section',
        'div.teads-inread.sm-screen',
        'div.content__foot',
        'section.c-global-footer__social.l-row',
        'section.c-global-footer__links.l-row'
    ]
    driver.noneDisplayByCSSSelectors(selectors)

    float = 'div.container-fluid'
    # header = browser.find_element_by_css_selector('header.u-font-sans')
    header = browser.find_element_by_id('header')
    browser.execute_script("arguments[0].style.position = 'relative';", header)

    nav = browser.find_element_by_css_selector('div.navigation.black')
    browser.execute_script("arguments[0].style.display = 'inline';", nav)

    footer = browser.find_element_by_css_selector('footer.c-global-footer')
    browser.execute_script("arguments[0].style.height = '170px';", footer)
