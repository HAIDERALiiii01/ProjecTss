# 💬 Quote Generator

<p align="center">
  <img src="https://media1.tenor.com/m/HPryfF_cllQAAAAC/fire-writing.gif" alt="Quote Generator" width="800"/>
</p>

> A random quote. Every 30 minutes. Whether you're ready or not. 🔔

---

## 🎯 What it does

A background motivational quote notifier. Run it once and it sends a random desktop notification every 30 minutes pulled from a handpicked collection of 100+ quotes. Logs every notification to a temp file so you know it's working.

---

## 📁 Files

| File | Description |
| --- | --- |
| `quote_generator.py` | 🚀 The entire tool — run this to start receiving quotes |

---

## ⚙️ How it works

1. **Start** — Script runs and immediately sends the first notification
2. **Wait** — Sleeps for 30 minutes
3. **Repeat** — Sends another random quote and loops forever
4. **Log** — Every notification is logged with a timestamp to `quote_log.txt` in your system's temp folder

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Quote_Generator"
```

### 2. Install dependencies
```bash
pip install plyer
```

### 3. Run the script
```bash
python quote_generator.py
```

Keep it running in the background and let the quotes come to you. 🧘

---

## 📦 Requirements
```bash
pip install plyer
```

---

## 📝 Notes

- The script runs indefinitely — keep the terminal open or run it as a background process
- Notifications appear as native desktop popups — works on Windows, macOS and Linux
- Logs are saved to `quote_log.txt` inside your system's temp folder (`%TEMP%` on Windows)
- Over 100 handpicked quotes covering discipline, mindset, faith and self-growth
- First notification fires instantly on launch — no waiting for the first 30 minutes

---

*"You didn't ask for it. But you needed it."*
