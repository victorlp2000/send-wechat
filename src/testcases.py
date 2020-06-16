from browser_driver import WebDriver
from tests import window_size as tWindowSize
from tests import url_location as tLocation
from tests import zoom as tZoom
from tests import save_image as tSaveImg
from tests import none_display as tNoneDisplay

driver = WebDriver()
browser = driver.getBrowser()

# tWindowSize.run(driver)
# tLocation.run(driver)
# tZoom.run(driver)
# tSaveImg.run(driver)
tNoneDisplay.run(driver)
