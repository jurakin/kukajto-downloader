from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from ..wrapper import Kukaj

from .dialogs import ask_file_save_location
from .utils import download_file
from .constants import ASSETS_DIR
from .constants import HOME_PAGE
from .constants import VIDEO_SUFFIX
from .constants import SUBS_SUFFIX
import eel

video = ""
subtitles = ""


def create_driver():
    options = ChromeOptions()
    options.add_argument("--incognito")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(HOME_PAGE)

    return driver

driver = create_driver()

user_agent = driver.execute_script("return window.navigator.userAgent")

kukaj = Kukaj(driver)

eel.init(ASSETS_DIR)

@eel.expose
def analyze():
    global video, subtitles

    result = kukaj.get()
    
    video = result.video
    subtitles = result.subtitles
    
    return video, subtitles

def main():
    try:
        eel.start("index.html", size=(480, 640))
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        driver.quit()


if __name__ == "__main__":
   main()