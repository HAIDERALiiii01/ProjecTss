# 🎵 Spotify Playlist Maker

<p align="center">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjQ2dHZrZnB2Z3E5cGsyOGl0MXI3ZnJkeGUwOTR4YjYyYmk5d3JhNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/guNXesWtLfqOfnWwmx/giphy.gif" alt="Spotify Playlist Maker" width="800"/>
</p>

> Scrape the Billboard Hot 100. Turn it into a Spotify playlist. Automatically. 🎧

---

## 🎯 What it does

A two-part automation tool. First it scrapes the Billboard Hot 100 chart for any date using Selenium, then it creates a private Spotify playlist from those songs using the Spotipy API — complete with a custom cover image.

---

## 📁 Files

| File | Description |
| --- | --- |
| `scrapping.py` | 🕸️ Scrapes Billboard Hot 100 and saves songs to `data.txt` |
| `main.py` | 🚀 Creates the Spotify playlist and adds all scraped songs |
| `data.txt` | Scraped song titles and artists — input for `main.py` |
| `uri.txt` | Auto-generated file storing Spotify URIs of added songs |
| `2021.jpeg` | Cover image uploaded to the created playlist |

---

## ⚙️ How it works

1. **Scrape** — `scrapping.py` opens a chart source in Chrome and extracts song titles and artists into `data.txt`
2. **Create** — `main.py` creates a new private Spotify playlist using the Spotipy API
3. **Cover** — The playlist cover image is uploaded from `2021.jpeg`
4. **Search** — Each song from `data.txt` is searched on Spotify
5. **Add** — Found tracks are added to the playlist one by one
6. **Save** — All Spotify URIs are saved to `uri.txt` for reference

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Web_Scraping/Spotify_Playlist"
```

### 2. Install dependencies
```bash
pip install spotipy selenium webdriver-manager
```

### 3. Set up Spotify credentials

Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create an app. Then open `main.py` and fill in:
```python
client_id = "your_spotify_client_id"
client_secret = "your_spotify_client_secret"
redirect_url = "https://example.com/callback"
```

> Make sure `https://example.com/callback` is added as a Redirect URI in your Spotify app settings.

### 4. Get your song list

> ⚠️ **Billboard Hot 100 is now behind a paywall** — the chart page requires a paid Billboard subscription to access. Here are two free alternatives to get a song list:

**Option A — Wikipedia**
Wikipedia hosts archived Billboard Hot 100 charts for free. For example:
```
https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2021
```
Update the URL and CSS selectors in `scrapping.py` to match Wikipedia's table structure.

**Option B — Manual**
Simply open `data.txt` and type your songs manually in this format:
```
Song Title Artist Name
Levitating Dua Lipa
Blinding Lights The Weeknd
```

### 5. Run the scraper (if using Option A)
```bash
python scrapping.py
```

### 6. Create the playlist
```bash
python main.py
```

A browser window will open asking you to log in to Spotify and authorize the app. After that, the playlist is created automatically.

---

## 📦 Requirements
```bash
pip install spotipy selenium webdriver-manager
```

---

## 📝 Notes

- ChromeDriver is installed automatically via `webdriver-manager` — no manual setup needed
- The playlist is created as **private** by default — change `public=False` to `True` in `main.py` if needed
- Songs not found on Spotify are skipped and logged with ❌ in the terminal
- Replace `2021.jpeg` with any image you want as the playlist cover
- Change the playlist name inside `main.py` to match your chosen year or theme

---

*"Every year had a soundtrack. Now yours has a playlist."*
