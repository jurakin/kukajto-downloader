# KukajTo Downloader - get a direct url to a video or subtitle file

This program can find the direct url of a video or subtitle file from `film.kukaj.io` or `serial.kukaj.io`, which can be used for downloading the video or opening the vlc network stream.

## How to use

- Install pip package `pip install git+https://github.com/jurakin/kukajto-downloader`
- Run `kukajto-downloader`
- Select the video
- Click `Analyze`
- Download, copy video url or play preview

## Supported sources

The downloader currently supports following sources:

- [x] TAP
- [x] MIX
- [ ] NET
- [ ] MON
- [ ] DOD

## Using in code

You can use the library in your code:

```python
from selenium import webdriver

from kukajto_downloader import Kukaj

driver = webdriver.Chrome()

# mixdrop source, english, czech subtitles
driver.get("https://film.kukaj.io/matrix/1?subs=0&lng=EN")

video, subs = Kukaj(driver).run()

print(video)
print(subs)

driver.quit()
```

## Preview

![preview](./preview.gif)

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
