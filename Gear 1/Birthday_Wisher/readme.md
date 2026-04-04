# 🎂 Birthday Wisher

<p align="center">
  <img src="https://media1.tenor.com/m/Dx5hXsY0xHkAAAAd/vivienne.gif" alt="Birthday" width="800"/>
</p>

> Never forget a birthday again. It sends the wishes — you take the credit. 🎉

---

## 🎯 What it does

Birthday Wisher automatically sends personalized birthday emails to your friends and family. Just add their details to a CSV file, run the script, and it handles the rest — picking a random letter template and sending it straight to their inbox.

---

## 📁 Files

| File | Description |
| --- | --- |
| `main.py` | 🚀 Entry point — run this to send birthday emails |
| `birthdays.csv` | List of people with their name, email, and birthday |
| `letter_templates/letter_1.txt` | Birthday letter template 1 |
| `letter_templates/letter_2.txt` | Birthday letter template 2 |
| `letter_templates/letter_3.txt` | Birthday letter template 3 |
| `letter_templates/letter_4.txt` | Birthday letter template 4 |
| `letter_templates/letter_5.txt` | Birthday letter template 5 |

---

## ⚙️ How it works

1. **Date Check** — The script gets today's date and compares it against every entry in `birthdays.csv`
2. **Match Found** — If today is someone's birthday, it picks a random letter from `letter_templates/`
3. **Personalization** — The `[NAME]` placeholder in the template is replaced with the person's actual name
4. **Email Sent** — The personalized message is sent to their email via Gmail SMTP

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Birthday_Wisher"
```

### 2. Install dependencies
```bash
pip install pandas
```

### 3. Configure your email

Open `main.py` and replace the placeholders:
```python
email = "your_email@gmail.com"
word = "your_app_password"
```

> ⚠️ Use a **Gmail App Password** — not your regular login password. Generate one from your Google Account → Security → 2-Step Verification → App Passwords.

### 4. Add birthdays

Fill in `birthdays.csv` with the following format:
```
name,email,year,month,day
John,john@example.com,2005,8,13
```

### 5. Run the script
```bash
python main.py
```

---

## ✉️ Letter Templates

Each template inside `letter_templates/` should contain `[NAME]` as a placeholder:
```
Dear [NAME],

Wishing you a wonderful birthday! 🎂
...
```

A random template (1–5) is picked each time a birthday is detected.

---

## 📦 Requirements
```
pandas
smtplib (built-in)
```

---

## 📝 Notes

- The script only sends emails when **today matches** someone's birthday — perfect for running daily via a scheduler
- Make sure your Gmail account has **2-Step Verification** enabled to generate an App Password
- You can customize all 5 letter templates however you like — just keep `[NAME]` in there

---

*"Wishes hit different when they arrive right at midnight." 🕛*
