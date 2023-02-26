from . import Kukaj
from .utils import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import argparse

parser = argparse.ArgumentParser(
    prog="kukajto-downloader",
    description="This program can find the direct url of a video or subtitle file from film.kukaj.io or serial.kukaj.io, which can be used for downloading the video or opening the vlc network stream.",
    epilog="Examples:\n  \
kukajto-downloader https://film.kukaj.io/matrix\n  \
kukajto-downloader https://film.kukaj.io/matrix https://film.kukaj.io/matrix\n  \
kukajto-downloader https://film.kukaj.io/matrix -a='start-maximized' -a='--disable-extensions'\n",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

parser.add_argument("url", nargs="+", help="url of video page (https://film.kukaj.io/matrix)")

parser.add_argument("-a", "--add-argument", default=[], metavar="ARGUMENT", nargs="+", action="append", help="options passed to chromedriver")

parser.add_argument("-o", "--output",         default=None,  help="put the output into a file")
parser.add_argument("-e", "--no-encode",      default=False, help="do not encode url", action="store_true")
parser.add_argument("-i", "--ignore-captcha", default=False, help="ignore captcha prompt", action="store_true")
parser.add_argument("-l", "--no-headless",                   help="turn off headless mode", action="store_true")
parser.add_argument("-d", "--driverpath",     default=None,  help="custom path to the chromedriver")
parser.add_argument("-s", "--separator",      default=",",   help="separate video and subtitle files' url (comma by default)")

args = parser.parse_args()


if args.driverpath:
    service = Service(args.driverpath)
else:
    service = Service(ChromeDriverManager(path=r".").install())

options = webdriver.ChromeOptions()
for arg in args.add_argument:
    options.add_argument(arg[0])
if not args.no_headless:
    options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

file = None
if args.output: file = open(args.output, "w")

for url in args.url:

    try:
        video, subs = Kukaj(driver, url)
    except:
        if not args.ignore_captcha:
            input("Answer captcha, then press enter ...")
            
            video, subs = Kukaj(driver, url)
    
    if not args.no_encode:
        # do not encode : and /
        video = quote(video, safe="/:")
        subs = quote(subs, safe="/:")
    
    data = video + args.separator + subs
    
    if file:
        file.write(data + "\n")
    else:
        print(data)

if file: file.close()

driver.quit()