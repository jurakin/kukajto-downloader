from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from urllib.parse import urljoin
import logging, argparse

parser = argparse.ArgumentParser(
    prog="kukajto-downloader",
    description="This program can find the direct url of a video or subtitle file from film.kukaj.io or serial.kukaj.io, which can be used for downloading the video or opening the vlc network stream.",
    epilog="Examples:\n  \
kukajto-downloader https://film.kukaj.io/matrix\n  \
kukajto-downloader https://film.kukaj.io/matrix https://film.kukaj.io/matrix\n  \
kukajto-downloader https://film.kukaj.io/matrix -a='start-maximized' -a='--disable-extensions'\n",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

parser.add_argument(
    "url",
    type=str,
    nargs="+",
    help="url of video page (https://film.kukaj.io/matrix)",
)
parser.add_argument(
    "-a",
    "--add-argument",
    type=str,
    default=[],
    metavar="ARGUMENT",
    nargs="+",
    action="append",
    help="options passed to chromedriver",
)
parser.add_argument(
    "-d", "--driverpath", type=str, default=None, help="custom path to the chromedriver"
)
parser.add_argument(
    "-s",
    "--separator",
    type=str,
    default=",",
    help="separate video and subtitle files' url (comma by default)",
)
parser.add_argument("-q", "--quiet", action="store_true", help="quiet mode")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose mode")

args = parser.parse_args()

level = logging.WARN
if args.quiet:
    level = logging.ERROR
elif args.verbose:
    level = logging.DEBUG

logging.basicConfig(format="%(levelname)s : %(message)s", level=level)

if args.driverpath:
    service = Service(args.driverpath)
else:
    service = Service()

options = Options()

for arg in args.add_argument:
    options.add_argument(arg[0])

driver = webdriver.Chrome(options=options, service=service)

for url in args.url:
    try:
        logging.info(f"processing url {url}")
        driver.get(url)

        element = driver.find_element(By.XPATH, """//*[@id="shost"]/option[.="TAP"]""")
        # check for streamtape source is selected
        if element and not element.get_attribute("selected"):
            logging.warning("using streamtape source")

            tape_source = element.get_attribute("data-href")
            url = urljoin(url, tape_source)
            driver.get(url)

        # find kukframe iframe
        element = driver.find_element(By.XPATH, """//*[@id="kukframe"]""")
        # check result
        assert element, """element //*[@id="kukframe"] not found"""
        # select iframe
        driver.switch_to.frame(element)

        # find needsleep iframe
        try:
            element = driver.find_element(By.XPATH, """//*[@id="needsleep"]/iframe""")
        except NoSuchElementException:
            input("please accept captcha and then press enter")
            element = driver.find_element(By.XPATH, """//*[@id="needsleep"]/iframe""")

        # check result
        assert element, """element //*[@id="needsleep"]/iframe not found"""

        # get subtitles and extract url part after "subs:" prefix if any
        if (subs := element.get_attribute("name")).startswith("subs:"):
            subs = subs.split("subs:", 1)[1]
        else:
            subs = ""

        # select iframe
        driver.switch_to.frame(element)

        # find mainvideo element
        element = driver.find_element(By.XPATH, """//*[@id="mainvideo"]""")
        # check result
        assert element, """element //*[@id="mainvideo"] not found"""

        if not (video := element.get_attribute("src")):
            logging.error("video not found")
            video = ""

        print(video, subs, sep=args.separator)
    except:
        logging.exception(f"error on {url} url")

driver.close()

logging.info("closing bye")
