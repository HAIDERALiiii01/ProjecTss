# 🔐 Cipher

<p align="center">
  <img src="https://media1.tenor.com/m/kAVw_yBARkMAAAAd/message-destruct.gif" alt="Cipher" width="800"/>
</p>

> Encrypt it. Decrypt it. Keep your secrets secret. 🕵️

---

## 🎯 What it does

A terminal-based Caesar Cipher tool that encrypts and decrypts messages using a shift-based alphabet rotation. Type your message, choose a shift number, and get your encoded or decoded text instantly.

---

## 📁 Files

| File | Description |
| --- | --- |
| `CIPHER.py` | 🚀 The entire tool — run this to encode or decode |

---

## ⚙️ How it works

1. **Choose** — Select `encode` to encrypt or `decode` to decrypt
2. **Message** — Type the message you want to process
3. **Shift** — Enter a shift number (how many letters to rotate by)
4. **Result** — Your encrypted or decrypted message is printed instantly
5. **Repeat** — Option to run again without restarting the script

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Cipher"
```

### 2. Run the program
```bash
python CIPHER.py
```

No dependencies. No setup. Just Python. 🐍

---

## 🎮 How to use

- Type `encode` → enter your message and shift → get encrypted text
- Type `decode` → enter the encrypted message and same shift → get original text back
- Non-alphabet characters (spaces, numbers, symbols) are kept as-is
- Shift wraps around automatically — shift of 27 = shift of 1

---

## 📝 Notes

- No external libraries required — pure Python
- Only works with **lowercase letters** — input is auto-lowercased
- The same shift number used to encode must be used to decode
- Based on the classic **Caesar Cipher** algorithm

---

*"If they can't read it, it never happened. 🔏"*
