# 💰 Price Tracker

<p align="center">
  <img src="https://media1.tenor.com/m/Gq5wfrkgezMAAAAC/price-cost-so-much.gif" alt="Price Tracker" width="800"/>
</p>

> Set your budget. Run the script. Buy when the price is right. 🛒

---

## 🎯 What it does

Scrapes the price of a product from a website and checks if it falls within your budget. With a small extension, it can email you automatically when the price drops below your target — so you never miss a deal.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 The entire tracker — run this to check the price |

---

## ⚙️ How it works

1. **Scrape** — Sends a request to the product URL and parses the page with BeautifulSoup
2. **Extract** — Finds the price tag and cleans it into a plain integer
3. **Compare** — Checks if the price is under your set budget
4. **Alert** — Prints whether the product is within budget or not

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Web_Scraping/Price_Tracker"
```

### 2. Install dependencies
```bash
pip install requests beautifulsoup4
```

### 3. Set your product and budget

Open `main.py` and replace the URL with your desired product:
```python
url = "your_product_url_here"
```

Then set your budget threshold:
```python
if money < 5000:  # Change 5000 to your budget
```

### 4. Run the script
```bash
python main.py
```

---

## 📧 Optional — Email yourself when price drops

To get notified automatically, add this to `main.py` using `smtplib`:
```python
import smtplib

def send_email(price):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user="your_email@gmail.com", password="your_app_password")
        connection.sendmail(
            from_addr="your_email@gmail.com",
            to_addrs="your_email@gmail.com",
            msg=f"Subject: Price Alert!\n\nThe price has dropped to Rs.{price}. Go grab it!"
        )

if money < 5000:
    send_email(money)
```

> Use a **Gmail App Password** — not your regular login password. Generate one from Google Account → Security → 2-Step Verification → App Passwords.

---

## 📦 Requirements
```bash
pip install requests beautifulsoup4
```

---

## 📝 Notes

- The script is currently set to a Nike sneaker on khazanay.pk — swap the URL for any product you want to track
- Price scraping depends on the website's HTML structure — the price tag selector may need adjusting for different sites
- Run this on a schedule (e.g. Windows Task Scheduler or a cron job) to check prices automatically every day

---

*"Patience is a virtue. So is a good deal."*
