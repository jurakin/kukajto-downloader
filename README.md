# KukajTo Downloader - get a direct url to a video or subtitle file

This program can find the direct url of a video or subtitle file from `film.kukaj.io` or `serial.kukaj.io`, which can be used for downloading the video or opening the vlc network stream.

## How to use

* Using precompiled code:
  - Donwload latest release.
  - `cd` into download directory.
  - Go to https://kukaj.io/ and find film or episode.
  - Run `kukajto-downloader.exe https://film.kukaj.io/matrix` with the url.
  - The results are in format `<url of video>,<url of subtitles if any>`


* Using source code:
  - Clone repository `git clone https://github.com/jurajhonsch/kukajto-downloader.git`
  - Install requirements (`selenium4`, `argparse`) `python3 -m pip install -r requirements.txt`
  - `cd` into download directory.
  - Go to https://kukaj.io/ and find film or episode.
  - Run `python3 kukajto-downloader.py https://film.kukaj.io/matrix` with the url.
  - The results are in format `<url of video>,<url of subtitles if any>`

## Examples

Get the direct url of a video and subtitle file (if any) of Matrix

`kukajto-downloader.exe https://film.kukaj.io/matrix`

Specify language (english) by copying the link from flag icon (make sure you are on streamtape source)

`kukajto-downloader.exe https://film.kukaj.io/matrix/1?lng=EN`

Specify language (english) and subtitle (english) by combinig the url params from flag icon and subtitle button (make sure you are on streamtape source)

`kukajto-downloader.exe https://film.kukaj.io/avatar/1?subs=1&lng=EN`

Get multiple urls of video and subtitle files (if any) at once.

`kukajto-downloader.exe https://film.kukaj.io/matrix/1?lng=EN https://film.kukaj.io/avatar/1?subs=1&lng=EN`

You can output the results to the file.

`kukajto-downloader.exe https://film.kukaj.io/matrix > output.txt`

Special arguments tothe `chromedriver`.

`kukajto-downloader.exe https://film.kukaj.io/matrix -a="start-maximized" -a="--disable-extensions"`

## TODO

- Support other sources (netu.tv, mixdrop.co)

## Disclaimer

FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY.

The information provided in or through this website is for educational and informational
purposes only and solely as a self-help tool for your own use.

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.

## License

This program is released under MIT License.

## Credits

In my project I used following icons:
 - [kukajto](https://kukaj.io) favicon 228x228 [icon](https://kukaj.io/img/icons/228x228.png)
 - [flaticon](https://flaticon.com) icons [download file icon](https://www.flaticon.com/free-icons/download-file)
