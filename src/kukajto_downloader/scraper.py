from selenium.webdriver.common.by import By

from urllib.parse import urlparse

from .exceptions import UnsupportedSourceError
from .exceptions import UnsupportedStructureError


class ScraperTemplate:
    def _fix_scheme(self, url: str) -> str:
        if urlparse(url).scheme == "":
            url = "https:" + url

        return url


class StreamtapeScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self):
        video = self.driver.find_element(By.CSS_SELECTOR, "video#mainvideo")

        if not (url := video.get_attribute("src")):
            raise UnsupportedStructureError

        return self._fix_scheme(url)


class MixdropScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self) -> str:
        url = self.driver.execute_script("return MDCore.wurl")

        if not url:
            raise UnsupportedStructureError

        return self._fix_scheme(url)

class FilemoonScraper(ScraperTemplate):
    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self) -> str:
        url = self.driver.execute_script("return videop.hls.url")

        if not url:
            raise UnsupportedStructureError

        return self._fix_scheme(url)


class Scraper:
    SOURCES = {
        "streamtape.com": StreamtapeScraper,
        "mixdrop.co": MixdropScraper,
        "filemoon.sx": FilemoonScraper,
    }

    def __init__(self, driver) -> None:
        self.driver = driver
    
    def _get_domain(self, iframe):
        return urlparse(iframe.get_attribute("src")).netloc

    def get(self, iframe):
        domain = self._get_domain(iframe)

        self.driver.switch_to.frame(iframe)

        if domain not in self.SOURCES:
            raise UnsupportedSourceError from None
        
        scraper = self.SOURCES[domain](self.driver)
        
        video = scraper.get()

        return video
    
    def attach(self, domain, scraper):
        if not hasattr(scraper, "get"):
            raise ValueError("scraper must have get method")

        self.SOURCES[domain] = scraper
    
    def detach(self, domain):
        if domain in self.SOURCES:
            del self.SOURCES[domain]
