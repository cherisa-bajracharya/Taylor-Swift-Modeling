import pandas as pd
import numpy as np
from playwright.sync_api import sync_playwright
import re
import time

pw = sync_playwright().start()

chrome = pw.chromium.launch(headless=False, args=["--no-sandbox", "--disable-gpu", "--disable-software-rasterizer"],)

page = chrome.new_page()

page.goto('https://www.discogs.com/artist/1124645-Taylor-Swift?srsltid=AfmBOopvo-xhBkd1-xg3RZqGElU9XPKbymXsIg4dAH7rqqrkA-y5m7W-')

albums = page.locator('.releases_mxLkA .title_K9_iv a[href*="-Taylor-Swift-"]')
count = albums.count()

get_link = [albums.nth(x).get_attribute('href') for x in range(count)]  # Removed [0]
print(get_link)
all_links = [f"https://www.discogs.com{x}" for x in get_link]

song_list = []
for i in all_links[:20]:
    page.goto(i)
    time.sleep(np.random.uniform(.1, 1, 1)[0])
    album_name = page.locator('h1').first.text_content()
    date = page.locator('.table_c5ftk .link_wXY7O').first.text_content()
    print(album_name)

    
    songs_loc = page.locator('.main_cQEFk .trackTitleNoArtist_VUgUr')
    song_count = songs_loc.count()
    
    for s in range(song_count):
        song_text = songs_loc.nth(s).text_content()
        song_list.append({"album_name": album_name, "song": song_text, "track_number": s + 1})
    
album_songs = pd.DataFrame(song_list)
album_songs.to_csv('/Users/cherisa/Documents/ND/Fall/Unstructured Data Analytics/final_project/final_files/albums.csv', index=False)

page.close()
chrome.close()
pw.stop()