"""
Built on Python 3.8.5
"""
import argparse
import urllib.request as urllib
from pathlib import Path
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


class TqdmUpTo(tqdm):
    def __init__(self, title):
        super(TqdmUpTo, self).__init__(desc=f"Downloading {title}", total=9e9, unit="B", unit_scale=True)
        self.n = 0

    def __call__(self, block, block_size, total_size=None):
        self.update_to(block, block_size, total_size)

    def update_to(self, block, block_size, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.update(block * block_size - self.n)
        self.n = block * block_size


parser = argparse.ArgumentParser(description="Download recordings from Blackboard Collaborate.")
parser.add_argument("url", metavar="URL", type=str, help="URL of the recording")
parser.add_argument("dest", metavar="DEST", type=str, nargs="?", default="./", help="Directory where to save recording")
parser.add_argument("--gui", dest="headless", action="store_false", default=True, help="Uses the GUI version of the browser; mostly for debug purposes")
parser.add_argument("--maxtime", dest="T", type=int, help="Maximum time allowed for the recording to load before a TimeoutError is thrown")
args = parser.parse_args()

# TODO: add support to other browsers
opts = webdriver.FirefoxOptions()
opts.headless = args.headless
driver = webdriver.Firefox(executable_path="./geckodriver_026", options=opts)
driver.get(args.url)
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

urllib.urlretrieve(video_src, outdir/f"{recording_title}.mp4", reporthook=TqdmUpTo(recording_title))
