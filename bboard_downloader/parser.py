import argparse
import os


parser = argparse.ArgumentParser(description="Download recordings from Blackboard Collaborate. It requires either Chrome or Firefox to be installed and the associated webdriver to be in the current working directory or at a location specified through the executable_path argument.")
parser.add_argument("dest", metavar="DEST", type=str, nargs="?", default=os.getcwd(), help="Directory where to save recording; default is current directory")
parser.add_argument("url", metavar="URL", type=str, nargs="?", default=None, help="URL of the recording; if not provided, the user will be asked to paste it into the terminal once the program starts")
parser.add_argument("--browser", dest="browser", type=str, choices=["chrome", "firefox"], default="chrome", help="Browser to be used to download the recording; currently supported options are Google Chrome and Mozilla Firefox; default is Chrome")
parser.add_argument("--executable_path", dest="executable_path", type=str, default="default", help="Path to webdriver executable; default is './chromedriver' for Chrome and './geckodriver' for Firefox")
parser.add_argument("--maxtime", dest="T", type=int, default=10, help="Maximum time in seconds allowed for the recording to load before a TimeoutError is thrown; default is 10s")
parser.add_argument("--gui", dest="headless", action="store_false", default=True, help="Uses the GUI version of the browser; mostly for debug purposes")
parser.add_argument("--course", dest="course", type=str, default="default", help="Code of the course to which the recording belongs; it is used, together with the recording date, to generate the video filename")
