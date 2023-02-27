from selenium.webdriver.common.by import By

from .utils import urlparse

from .exceptions import UnsupportedSourceError
from .exceptions import UnsupportedStructureError

from .constants import STREAMTAPE_SOURCE, MIXDROP_SOURCE


class ScraperTemplate:
    def __init__(self, driver) -> None:
        self.driver = driver

    def _fixurl(self, url: str) -> str:
        if urlparse(url).scheme == "":
            url = "https:" + url

        return url

    def scrape(self) -> str:
        url = self._geturl()

        url = self._fixurl(url)

        return url


class StreamtapeScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        super().__init__(driver)

    def _geturl(self):
        video = self.driver.find_element(By.CSS_SELECTOR, "video#mainvideo")

        if not (url := video.get_attribute("src")):
            raise UnsupportedStructureError("the structure of kukaj is not supported, please report an issue")

        return url


class MixdropScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        super().__init__(driver)

    def _geturl(self) -> str:
        url = self.driver.execute_script("return MDCore.wurl")

        if not url:
            raise UnsupportedStructureError("the structure of kukaj is not supported, please report an issue")

        return url


class Scraper:
    SOURCES = {
        STREAMTAPE_SOURCE: StreamtapeScraper,
        MIXDROP_SOURCE: MixdropScraper,
    }

    def __init__(self, driver, source) -> None:
        self.driver = driver
        self.source = source

    def scrape(self):
        domain = urlparse(self.source).netloc

        try:
            scraper = self.SOURCES[domain](self.driver)
        except KeyError:
            raise UnsupportedSourceError("the source is not currently supported, use other source please") from None

        video = scraper.scrape()

        return video
