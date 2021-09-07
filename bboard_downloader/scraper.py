import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

HEADERS = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'} # http://www.useragentstring.com/index.php?id=19858

def get_driver(browser, executable_path, headless):
    if browser == 'chrome':
        opts = webdriver.ChromeOptions()
        opts.headless = headless
        driver = webdriver.Chrome(executable_path=executable_path, options=opts)
    elif browser == 'firefox':
        opts = webdriver.FirefoxOptions()
        opts.headless = headless
        driver = webdriver.Firefox(executable_path=executable_path, options=opts)
    else:
        raise ValueError("The only currently supported browsers are Google Chrome and Mozilla Firefox")
    return driver

def is_unauthorized(driver):
    unauthorized = False
    try:
        element = driver.find_element_by_xpath("//h1[@class='recording-failure-title full-page-title ng-scope ng-binding']")
        if element.get_attribute("analytics-id") == "recording.failure.unauthorized.title":
            unauthorized = True
    finally:
        return unauthorized

def get_video_src(driver, url, T):
    driver.get(url)
    try:
        recording_title = WebDriverWait(driver, T).until(
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
    return recording_title, video_src

def download_video(video_src, outdir, recording_title=''):
    response = requests.get(video_src, headers=HEADERS, stream=True) # stream allows to iterate over response
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(desc=f"Downloading {recording_title}", total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(outdir/f"{recording_title}.mp4", 'wb') as f:
        for chunk in response.iter_content(block_size):
            progress_bar.update(len(chunk))
            f.write(chunk)
    progress_bar.close()
