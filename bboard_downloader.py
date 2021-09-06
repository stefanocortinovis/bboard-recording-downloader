import argparse
import os
from pathlib import Path
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


def is_unauthorized(driver):
    unauthorized = False
    try:
        element = driver.find_element_by_xpath("//h1[@class='recording-failure-title full-page-title ng-scope ng-binding']")
        if element.get_attribute("analytics-id") == "recording.failure.unauthorized.title":
            unauthorized = True
    finally:
        return unauthorized


parser = argparse.ArgumentParser(description="Download recordings from Blackboard Collaborate. It requires either Chrome or Firefox to be installed and the associated webdriver to be in the current working directory or at a location specified through the executable_path argument.")
parser.add_argument("dest", metavar="DEST", type=str, nargs="?", default=os.getcwd(), help="Directory where to save recording; default is current directory")
parser.add_argument("url", metavar="URL", type=str, nargs="?", default=None, help="URL of the recording")
parser.add_argument("--browser", dest="browser", type=str, choices=["chrome", "firefox"], default="chrome", help="Browser to be used to download the recording; currently supported options are Google Chrome and Mozilla Firefox; default is Chrome")
parser.add_argument("--executable_path", dest="executable_path", type=str, default="default", help="Path to webdriver executable; default is './chromedriver' for Chrome and './geckodriver' for Firefox")
parser.add_argument("--maxtime", dest="T", type=int, default=10, help="Maximum time in seconds allowed for the recording to load before a TimeoutError is thrown; default is 10s")
parser.add_argument("--gui", dest="headless", action="store_false", default=True, help="Uses the GUI version of the browser; mostly for debug purposes")
args = parser.parse_args()

url = input("Paste the recording URL: ") if args.url is None else args.url
if args.browser.lower() == "chrome":
    opts = webdriver.ChromeOptions()
    opts.headless = args.headless
    if args.executable_path == "default":
        args.executable_path = "./chromedriver"
    driver = webdriver.Chrome(executable_path=args.executable_path, options=opts)
elif args.browser.lower() == "firefox":
    opts = webdriver.FirefoxOptions()
    opts.headless = args.headless
    if args.executable_path == "default":
        args.executable_path = "./geckodriver"
    driver = webdriver.Firefox(executable_path=args.executable_path, options=opts)
else:
    raise ValueError("The only currently supported browsers are Google Chrome and Mozilla Firefox")
driver.get(url)
try:
    recording_title = WebDriverWait(driver, args.T).until(
        EC.presence_of_element_located((By.ID, "recording-name"))
    ).get_attribute("innerText").replace("/", "-")
    video_src = driver.find_element_by_id("playback-video-playback-video_html5_api").get_attribute("src")
except TimeoutException:
    if is_unauthorized(driver):
        raise WebDriverException("Unauthorized request: the recording URL is likely to have expired")
    else:
        raise TimeoutException("Can't seem to find the video at the specified URL; try to manually increase the maximum waiting time or run the command with --gui for graphical debugging")
finally:
    driver.quit()

outdir = Path(args.dest)
if not outdir.is_dir():
    raise FileNotFoundError(f"No such file or directory: {outdir}")

response = requests.get(video_src, stream=True) # stream allows to iterate over response
total_size_in_bytes= int(response.headers.get('content-length', 0))
block_size = 1024 #1 Kibibyte
progress_bar = tqdm(desc=f"Downloading {recording_title}", total=total_size_in_bytes, unit='iB', unit_scale=True)
with open(outdir/f"{recording_title}.mp4", 'wb') as f:
    for chunk in response.iter_content(block_size):
        progress_bar.update(len(chunk))
        f.write(chunk)
progress_bar.close()
