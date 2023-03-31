<img src="./favicon.png" width="100px" alt="KukajTo Downloader"/>

# KukajTo Downloader - get a direct url to a video or subtitle file

This program can find the direct url of a video or subtitle file from [kukaj.to](https://kukaj.io/), that can be opened in the [VLC media player](https://www.videolan.org/vlc/).

## Installation

- [Google Chrome](https://www.google.com/chrome/) (a reasonable version) must be installed in order **to use web gui of the downloader**.
- Windows
  - Install precompiled [latest setup from releases](https://github.com/jurakin/kukajto-downloader/releases/latest)
- Python and cmd use
  - Install from pip package `pip install kukajto-downloader`

## How to use

- Run the program or type `kukajto-downloader`
- Select the video and click `Analyze`
- Open VLC, then navigate to `Media`→`Open Network Stream` or press <kbd>Ctrl</kbd>+<kbd>N</kbd>
- Paste video url into `Please enter a network URL` input

- For those who want to add subtitles

  - Check `Show more options`
  - Check `Play another media`
  - Paste subtitles into `Extra media` input

- Click `Play`

## Supported sources

Kukajto is currently using following source:

| Shortcut | Domain         | Support | Play\* | Format |
| -------- | -------------- | ------- | ------ | ------ |
| TAP      | streamtape.com | ✅      | ✅     | mp4    |
| MIX      | mixdrop.co     | ✅      | ✅     | mp4    |
| MON      | filemoon.sx    | ✅      | ✅     | m3u8   |
| DOD      | -              | -       | -      | -      |
| NET      | -              | -       | -      | -      |

\*Can be analyzed without playing video first.

## Preview

![preview](./preview.gif)

## Using in code

You can use the library in your code:

```python
from selenium import webdriver

from kukajto_downloader import Kukaj

driver = webdriver.Chrome()

# mixdrop source, english, czech subtitles
driver.get("https://film.kukaj.io/matrix/1?subs=0&lng=EN")

# analyze kukaj site
result = Kukaj(driver).get()

# prints the url of video and subtitles
print(result.video)
print(result.subtitles)

driver.quit()
```

Custom scraper can be created too. This is an example how `MixdropScraper` is implemented:

```python
from selenium import webdriver

from src.kukajto_downloader import Kukaj
from src.kukajto_downloader import Scraper, UnsupportedStructureError

driver = webdriver.Chrome()

class MixdropScraper:
    """
    Scraper class must have following methods:
        __init__
            Arguments:
                driver - selenium webdriver instance
        get
            Method that extracts url from the source

            Arguments:
                iframe - selenium iframe object of source

            Returns:
                url - An url that will be displayed

    """
    def __init__(self, driver) -> None:
        self.driver = driver

    def get(self) -> str: # required method
        url = self.driver.execute_script("return MDCore.wurl")

        if not url:
            raise UnsupportedStructureError

        return url

# mixdrop source, english, czech subtitles
driver.get("https://film.kukaj.io/matrix/3?subs=0&lng=EN")

# create scraper instance
scraper = Scraper(driver)

# attach new scraper
scraper.attach("mixdrop.co", MixdropScraper)

# analyze kukaj site
result = Kukaj(driver).get(scraper)

# prints the url of video and subtitles
print(result.video)
```

## Disclaimer

FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY.

The information provided in or through this website is for educational and informational
purposes only and solely as a self-help tool for your own use.

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.

## License

This program is released under MIT License.

## Credits

In my project I used following icons from other sources:

- [kukajto](https://kukaj.io) favicon 228x228 [icon](https://kukaj.io/img/icons/228x228.png)
- [flaticon](https://flaticon.com) icons [download file icon](https://www.flaticon.com/free-icons/download-file)
