# Blackboard Recording Downloader

CLI tool to download recordings from Blackboard Collaborate.

## Usage 

```console
foo@bar:~$ python3 bboard_downloader.py -h
usage: bboard_downloader.py [-h] [--browser {chrome,firefox}] [--executable_path EXECUTABLE_PATH] [--maxtime T] [--gui] URL [DEST]

Download recordings from Blackboard Collaborate.

positional arguments:
  URL                   URL of the recording
  DEST                  Directory where to save recording; default is current directory

optional arguments:
  -h, --help            show this help message and exit
  --browser {chrome,firefox}
                        Browser to be used to download the recording; currently supported options are Google Chrome and Mozilla Firefox; default is Chrome
  --executable_path EXECUTABLE_PATH
                        Path to webdriver executable; default is './chromedriver' for Chrome and './geckodriver' for Firefox
  --maxtime T           Maximum time allowed for the recording to load before a TimeoutError is thrown
  --gui                 Uses the GUI version of the browser; mostly for debug purposes

```