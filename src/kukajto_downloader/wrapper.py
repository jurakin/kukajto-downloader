from .scraper import Scraper

from .utils import urlparse

from .constants import KUKAJ_DOMAINS
from .constants import KUKFRAME_IFRAME
from .constants import NEEDSLEEP_IFRAME

from .exceptions import UnsupportedSiteError
from .exceptions import UnsupportedStructureError

from selenium.common.exceptions import NoSuchElementException


class Kukaj:
    def __init__(self, driver) -> None:
        self.driver = driver
    
    def _check_domain(self, url: str) -> None:
        if urlparse(url).netloc not in KUKAJ_DOMAINS:
            raise UnsupportedSiteError(f"the site domain must match one of ({', '.join(KUKAJ_DOMAINS)})")

    def _get_subtitles(self, needsleep_iframe) -> str:
        subs = needsleep_iframe.get_attribute("name")

        if subs.startswith("subs:"):
            subs = subs.split("subs:", 1)[1]

        return subs

    def _get_source(self, needsleep_iframe) -> str:
        return needsleep_iframe.get_attribute("src")
    
    def run(self):
        # switch to default body frame
        self.driver.switch_to.default_content()
        
        url = self.driver.execute_script("""return window.location.href;""")

        self._check_domain(url)

        try:
            iframe = self.driver.find_element(*KUKFRAME_IFRAME)
        except NoSuchElementException:
            raise UnsupportedStructureError("the structure of kukaj is not supported, please report an issue") from None
        self.driver.switch_to.frame(iframe)

        try:
            iframe = self.driver.find_element(*NEEDSLEEP_IFRAME)
        except NoSuchElementException:
            raise UnsupportedStructureError("the structure of kukaj is not supported, please report an issue") from None

        subs = self._get_subtitles(iframe)
        source = self._get_source(iframe)

        self.driver.switch_to.frame(iframe)

        video = Scraper(self.driver, source).scrape()

        self.driver.switch_to.default_content()

        return (video, subs)