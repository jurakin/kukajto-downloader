from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from kukajto_downloader.wrapper import Kukaj

from kukajto_downloader.web.dialogs import ask_file_save_location
from kukajto_downloader.web.utils import download_file
from kukajto_downloader.web.constants import ASSETS_DIR
from kukajto_downloader.web.constants import HOME_PAGE
from kukajto_downloader.web.constants import VIDEO_SUFFIX
from kukajto_downloader.web.constants import SUBS_SUFFIX
import eel

options = ChromeOptions()
options.add_argument("--incognito")

service = Service(ChromeDriverManager(path=r".").install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(HOME_PAGE)

user_agent = "Mozilla/5.0"
user_agent = driver.execute_script("""return window.navigator.userAgent;""")

data = {
    "video": "",
    "subs": "",
}

eel.init(ASSETS_DIR)


@eel.expose
def analyze():
    video, subs = Kukaj(driver).run()
    
    data["video"] = video
    data["subs"] = subs
    
    return video, subs

@eel.expose
def download_video():
    if not data["video"]: raise RuntimeError("no video analyzed")

    if not (path := ask_file_save_location(title="select video path")): return False

    with open(path if path.endswith(VIDEO_SUFFIX) else path + VIDEO_SUFFIX, "wb") as video_file:
        download_file(data["video"], video_file, headers={"User-Agent": user_agent}, update=lambda percent: eel.updateVideoDownloadBar(percent))

    return True
    

@eel.expose
def download_subs():
    if not data["subs"]: raise RuntimeError("no subs analyzed")

    if not (path := ask_file_save_location(title="select subs path")): return False

    with open(path if path.endswith(SUBS_SUFFIX) else path + SUBS_SUFFIX, "wb") as subs_file:
        download_file(data["subs"], subs_file, headers={"User-Agent": user_agent}, update=lambda percent: eel.updateSubsDownloadBar(percent))
    
    return True


def main():
    try:
        eel.start("index.html", size=(480, 640))
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        driver.quit()


if __name__ == "__main__":
   main()