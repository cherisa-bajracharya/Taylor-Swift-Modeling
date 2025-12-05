import pandas as pd
import numpy as np
from playwright.sync_api import sync_playwright
import time

df = pd.read_csv("ts_songs_link1.csv")

pw = sync_playwright().start()
chrome = pw.chromium.launch(headless=False, args=["--no-sandbox", "--disable-gpu", "--disable-software-rasterizer"],)
page = chrome.new_page()

lyrics_list = []

for idx, row in df.iterrows():
    url = row['link']

    page.goto(url, wait_until="domcontentloaded", timeout=120000)

    lyric_blocks = page.locator('div[data-lyrics-container="true"]')

    lyrics = ""
    for i in range(lyric_blocks.count()):
        lyrics += lyric_blocks.nth(i).inner_text() + "\n"

    lyrics_list.append({
        "song_name": row["song_name"],
        "link": url,
        "lyrics": lyrics.strip()
    })

    time.sleep(np.random.uniform(.3, 1, 1)[0])  

lyrics_df = pd.DataFrame(lyrics_list)
lyrics_df.to_csv('ts_tw_lyrics1.csv', index=False)

page.close()
chrome.close()
pw.stop()