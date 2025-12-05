import pandas as pd
import numpy as np
from playwright.sync_api import sync_playwright, Playwright
import re
import time

pw = sync_playwright().start()

chrome = pw.chromium.launch(headless=False, args=["--no-sandbox", "--disable-gpu", "--disable-software-rasterizer"],)

page = chrome.new_page()

page.goto('https://genius.com/artists/Taylor-swift/songs')

page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

def scroll_to_bottom(page):
    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

for i in range(300):
    scroll_to_bottom(page)
    time.sleep(np.random.uniform(.1, 1, 1)[0])

songs = page.locator('.ListItem__Container-sc-7c353cfe-0 a')

data = []
count = songs.count()

for i in range(count):
    el = songs.nth(i)
    link = el.get_attribute("href")
    title = el.locator("h3").inner_text()
    data.append({"song_name": title, "link": link})

lyricsdf = pd.DataFrame(data)
print(lyricsdf)

lyricsdf.to_csv("/Users/cherisa/Documents/ND/Fall/Unstructured Data Analytics/final_project/final_files/ts_songs_link1.csv", index=False)

page.close()
chrome.close()
pw.stop()