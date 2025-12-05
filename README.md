# README


## Lyrical Topic Modeling (Taylor’s Version)

# Project Overview

This project analyzes Taylor Swift’s song lyrics, identifies recurring
themes and emotional vibes across her discography, and groups songs
based on these vibes. The workflow includes web scraping, data cleaning,
topic modeling with LDA, sentiment analysis, and an interactive
Streamlit dashboard for visualization.

# Main App Link

- [Lyrical Topic Modeling (Taylor’s
  Version)](https://cherisa-bajracharya-taylor-swift-modeling-app-cjfhck.streamlit.app/)

# Reference Links

- [Taylor Swift on
  Genius](https://genius.com/artists/Taylor-swift/songs)  
- [Taylor Swift Discography on
  Discogs](https://www.discogs.com/artist/1124645-Taylor-Swift?srsltid=AfmBOopvo-xhBkd1-xg3RZqGElU9XPKbymXsIg4dAH7rqqrkA-y5m7W-)

# Project Structure

**pw_get_links.py** - Scrapes song links from Genius  
- Uses Playwright to navigate and scroll through Taylor Swift’s song
catalog.  
- Extracts song titles and URLs.  
- Saves data to CSV (`ts_songs_link1.csv`).

**pw_get_lyrics.py** - Scrapes lyrics from individual song pages  
- Iterates through links in `ts_songs_link1.csv`.  
- Fetches complete lyrics, song name, and page URL.  
- Saves lyrics data to CSV (`ts_tw_lyrics1.csv`).

**scrape_album.py** - Scrapes album names and tracklists from Discogs  
- Iterates through each album page.  
- Collects album names, release dates, and track listings.  
- Saves album metadata to CSV (`albums.csv`) for later merging.

**data_cleaning.qmd** - Data wrangling, cleaning, and merging  
- Cleans and preprocesses scraped lyrics.  
- Merges lyrics with album data using fuzzy matching.  
- Saves the final dataset to CSV (`final_dataset.csv`).

**topic_modeling.qmd** - Topic analysis and sentiment scoring  
- Preprocesses and cleans lyrics for modeling.  
- Performs topic modeling using LDA (11 topics).  
- Conducts sentiment analysis using Hugging Face transformers.  
- Interprets and names topics.

**streamlit_app.py** - Interactive dashboard  
- Visualizes topic distributions.  
- Explores songs by topic.  
- Displays sentiment analysis results.  
- Allows interactive filtering and exploration.

# Running the Project

**Data Collection**

1.  Get song links from Genius:  

``` {bash}
python pw_get_links.py
```

2.  Get lyrics for each song:

``` {bash}
python pw_get_lyrics.py
```

3.  Get album data from Discogs:

``` {bash}
python scrape_album.py
```

**Data Analysis**

4.  Run data cleaning and merging:

``` {bash}
quarto render data_cleaning.qmd
```

5.  Perform topic modeling and sentiment analysis:

``` {bash}
quarto render topic_modeling.qmd
```

**Visualizing**

6.  Run the Streamlit app:

``` {bash}
python streamlit_app.py
```

    Or run via terminal:

``` {bash}
python3 -m streamlit run app.py
```

# Topics Overview

| Topic | Name | Example Keywords |
|----|----|----|
| 0 | Honey and Daylight | york, hold, lights, feel, time, rains, floor, waitin, babe, called |
| 1 | My Heart in Your Palms | red, girl, wanna, gotta, lost, night, blue, lucky, walk, boy |
| 2 | Ghosts of You | baby, bad, blood, grow, feel, smile, time, fly, belong, wanna |
| 3 | Rain or Shine | live, time, wait, list, white, afraid, follow, god, wild, style |
| 4 | Unapologetically ME! | gonna, shake, hate, break, play, fake, baby, friends, mind, nice |
| 5 | Beginning’s Butterflies | stay, time, woods, trouble, mad, daylight, remember, finally, hard, wanna |
| 6 | Hearts on the Edge | love, beautiful, time, life, leave, loved, hands, bad, dancin, dark |
| 7 | POV | remember, night, talk, starlight, forget, dreams, day, hair, lips, karma |
| 8 | Echoes of Betrayal | dress, car, story, dance, night, tonight, happy, summer, town, gonna |

# Analysis & Reflection

## Pros

- **High clustering accuracy:** Topic modeling successfully grouped over
  70% of songs into meaningful themes, showing strong signal despite
  messy, inconsistent lyric sources.  
- **Efficient workflow for large text corpora:** The pipeline handled
  hundreds of songs, scraping, cleaning, vectorizing, modeling, and
  visualizing without major performance issues.  
- **Clear insights into lyrical patterns:** The analysis highlighted
  recurring emotional and thematic motifs across Taylor Swift’s
  discography, useful for fan engagement, music marketing, or academic
  analysis.  
- **Strong foundation for future applications:** The project functions
  as a prototype that could easily evolve into a public-facing lyric
  explorer, a fan analytics tool, or a marketing insights dashboard.  
- **Scalable structure:** The modular pipeline (scraping → cleaning →
  NLP → Streamlit) can easily be adapted to analyze any artist,
  soundtrack, or large lyric dataset.

## Cons & Challenges

- **Excessive and messy scraped data:** Genius.com listed over 1,700
  Taylor Swift–related songs—including features, production credits, and
  songs where she was mentioned—while she has only around 300 official
  releases. Cleaning and filtering this down to her actual discography
  was tedious and error-prone.
- **Dataset Joining Issues:** Even after extensive cleaning, a low
  similarity threshold (10%) had to be used when merging datasets by
  `song_name`. Some duplicates may have been incorrectly included or
  excluded.
- **Sentiment Analysis Limitations:** The 511-character limit of the
  transformer model fails to capture nuance, emotional shifts, sarcasm,
  and poetic structure in Taylor Swift’s lyrics. Examples include
  *Happiness* (a sad song) and *It’s Actually Romantic* (a diss track
  written ironically).
- **Topic Modeling Constraints:** LDA treats words independently, which
  overlooks lyrical context and complexity. Some songs were misclustered
  or oversimplified (e.g., *Is It Over Now?* and *Lover* in the same
  “Honey and Daylight” cluster).

## Streamlit App Reflection

The Streamlit app acted as an effective analytics prototype, giving
users an interactive way to explore lyrics, topics, and sentiment. While
the current version is geared toward data interpretation rather than
general user experience, it provides a strong foundation for future
development.

- The app could evolve into a mood- or theme-based music browsing tool
  with album-inspired color palettes.  
- Integrating music playback directly within the interface would greatly
  enhance user engagement.  
- Streamlit’s simplicity made development smooth and allowed fast
  iteration—useful for prototyping real-world applications.  
- Two versions could be created:
  - **Fan-facing app:** focused on aesthetics, mood, color themes, and
    song exploration  
  - **Marketing/analytics app:** incorporating sales data, streaming
    performance, and musical characteristics to identify patterns behind
    successful tracks

## Notes

- **Web Scraping Ethics:** All scraping adhered to the terms of service
  of Genius.com and Discogs.com, using only publicly accessible pages.
- **Rate Limiting:** Random delays were added to prevent excessive
  server requests.
- **Data Accuracy:** Lyric variations across platforms may introduce
  minor inconsistencies.
- **Topic Interpretation:** LDA topics require human interpretation, as
  the model clusters based on word patterns rather than meaning.

## Suggestions & Next Steps

- **Improve Sentiment Analysis:** Split lyrics into segments and
  aggregate results to capture full emotional progression.
- **Upgrade Topic Modeling:** Combine LDA with semantic embeddings
  (e.g., Sentence-BERT) for context-aware clustering.
- **Enhance the Streamlit App:**
  - Add color themes or album-based visuals  
  - Integrate music playback or playlist features  
  - Develop separate versions for fan engagement vs. marketing
    analytics  
- **Add Storytelling Elements:** Highlight interesting patterns, lyrical
  motifs, or surprises in the dashboard to engage users.
