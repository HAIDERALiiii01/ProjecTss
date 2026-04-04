# 🎬 Top 100 Movies — Empire

<p align="center">
  <img src="https://media1.tenor.com/m/zDZRlH-tT1sAAAAC/despicable-me-minions.gif" alt="Top 100 Movies" width="800"/>
</p>

> Scrape Empire's 100 greatest movies of all time and save them to a file. 🍿

---

## 🎯 What it does

Scrapes Empire magazine's list of the 100 best movies of all time from their website and saves them in order to a text file — from rank 1 down to 100.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 The entire scraper — run this to get the list |
| `Maaaal.txt` | Output file where the top 100 movies are saved |

---

## ⚙️ How it works

1. **Fetch** — Sends a request to Empire's best movies page
2. **Parse** — BeautifulSoup extracts all `<h2>` tags containing movie titles
3. **Reverse** — The list is reversed so rank 1 appears first
4. **Save** — All 100 movies are written to `Maaaal.txt` line by line

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Web_Scraping/Top_100_Movies"
```

### 2. Install dependencies
```bash
pip install requests beautifulsoup4
```

### 3. Run the scraper
```bash
python main.py
```

Open `Maaaal.txt` to see the full list. 🎬

---

## 📦 Requirements
```bash
pip install requests beautifulsoup4
```

---

## 📝 Notes

- Requires an active internet connection to scrape the page
- If Empire updates their website structure, the CSS selectors in `main.py` may need adjusting
- The output file is overwritten every time the script runs
- Results are ordered from rank 1 to 100

---

*"100 movies. No excuses for a bad movie night."*
