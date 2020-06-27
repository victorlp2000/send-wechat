from helper.browser_driver import WebDriver
from tests import window_size as tWindowSize
from tests import url_location as tLocation
from tests import zoom as tZoom
from tests import save_image as tSaveImg
from tests import none_display as tNoneDisplay
from tests import browser_pid as tGetPID

class Settings(object):
    browser = 'Firefox'
    zoom = 100      # about 20 c-chars in a line
    pageWidth = 200
    headless = False     # need to be True, or Chrome does not take full page image
    configDir = None

driver = WebDriver(Settings)
browser = driver.getBrowser()

# tWindowSize.run(driver)
# tLocation.run(driver)
# tZoom.run(driver)
# tSaveImg.run(driver)
# tNoneDisplay.run(driver)
tGetPIDs.run(driver)
# browser.quit()
