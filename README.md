# Blackboard Recording Downloader

CLI tool to download recordings from Blackboard Collaborate. This is an unofficial tool in no way associated with Blackboard Inc. and is provided without any kind of warranty.

## Setup and Requirements

This tool was briefly tested on Linux and Windows, but it should work also on OSX. It was built on Python 3.8.5 and it requires the libraries `requests`, `selenium` and `tqdm`. The tool may be installed locally as follows:

```console
git clone https://github.com/scortino/bboard-recording-downloader.git
cd bboard-recording-downloader
python setup.py install
```

The browsers currently supported are Google Chrome and Mozilla Firefox. In addition to the preferred browser being installed, the user is required to download the associated webdriver (i.e. [`chromedriver`](https://chromedriver.chromium.org/) for Chrome or [`geckodriver`](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0) for Firefox). The executable should be placed in the same directory as the `bboard_downloader.py` file. Alternatively, the user may specify the location of the webdriver using the `--executable_path` option as described below. 

Important note: unfortunately, the latest version of `geckodriver` (v0.27.0) has [issues](https://github.com/mozilla/geckodriver/issues/1756) with the current version of `selenium` (3.141.0) and Firefox (v81.0). Until these issues are resolved, I recommend dowloading `geckodriver` v0.26.0.

## Summary Usage 

```console
foo@bar:~$ bboard -h
usage: bboard_downloader.py [-h] [--browser {chrome,firefox}] [--executable_path EXECUTABLE_PATH] [--maxtime T] [--gui] [DEST] [URL]

Download recordings from Blackboard Collaborate. It requires either Chrome or Firefox to be installed and the associated webdriver to be in the current working directory or at a location specified through the executable_path argument.

positional arguments:
  DEST                  Directory where to save recording; default is current directory
  URL                   URL of the recording; if not provided, the user will be asked to paste it into the terminal once the program starts

optional arguments:
  -h, --help            show this help message and exit
  --browser {chrome,firefox}
                        Browser to be used to download the recording; currently supported options are Google Chrome and Mozilla Firefox; default is Chrome
  --executable_path EXECUTABLE_PATH
                        Path to webdriver executable; default is './chromedriver' for Chrome and './geckodriver' for Firefox
  --maxtime T           Maximum time in seconds allowed for the recording to load before a TimeoutError is thrown; default is 10s
  --gui                 Uses the GUI version of the browser; mostly for debug purposes

```
