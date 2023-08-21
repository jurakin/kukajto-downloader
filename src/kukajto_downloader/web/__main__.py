from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from ..wrapper import Kukaj

from .constants import ASSETS_DIR
from .constants import HOME_PAGE
import eel

video = ""
subtitles = ""


def create_driver():
    options = ChromeOptions()
    options.add_argument("--incognito")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(HOME_PAGE)

    return driver

driver = create_driver()

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
