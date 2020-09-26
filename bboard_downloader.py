"""
Built on Python 3.8.5
"""
import argparse
import urllib.request as urllib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


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
args = parser.parse_args()

# TODO: add support to other browsers
opts = webdriver.FirefoxOptions()
opts.headless = True
driver = webdriver.Firefox(executable_path="./geckodriver_026", options=opts)
driver.get(args.url)
try:
    recording_title = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "recording-name"))
    ).get_attribute("innerText").replace('/', '-')
    video_src = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "playback-video-playback-video_html5_api"))
    ).get_attribute("src")
finally:
    driver.quit()

outdir = Path(args.dest)
if not outdir.is_dir():
    raise FileNotFoundError(f"No such file or directory: {outdir}")

urllib.urlretrieve(video_src, outdir/f"{recording_title}.mp4", reporthook=TqdmUpTo(recording_title))
