from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .scraper import Scraper
from .utils import urlparse

from .constants import KUKAJ_DOMAINS
from .exceptions import UnsupportedSiteError
from .exceptions import UnsupportedStructureError

from collections import namedtuple

KukajResult = namedtuple("KukajResult", ("video", "subtitles"))

class Kukaj:
    def __init__(self, driver) -> None:
        self.driver = driver
    
    def _check_domain(self, url: str) -> None:
        if urlparse(url).netloc not in KUKAJ_DOMAINS:
            raise UnsupportedSiteError

    def _get_subtitles(self, needsleep_iframe) -> str:
        subs = needsleep_iframe.get_attribute("name")

        if subs.startswith("subs:"):
            subs = subs.split("subs:", 1)[1]

        return subs
    
    def get(self, scraper=None):
        if scraper is None: scraper = Scraper(self.driver)

        # switch to default body frame
        self.driver.switch_to.default_content()
        
        url = self.driver.execute_script("""return window.location.href;""")

        self._check_domain(url)

        try:
            iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe#kukframe")
        except NoSuchElementException:
            raise UnsupportedStructureError from None
        self.driver.switch_to.frame(iframe)

        try:
            iframe = self.driver.find_element(By.CSS_SELECTOR, "div#needsleep iframe")
        except NoSuchElementException:
            raise UnsupportedStructureError from None

        subs = self._get_subtitles(iframe)

        video = scraper.get(iframe)

        self.driver.switch_to.default_content()

        return KukajResult(video, subs)