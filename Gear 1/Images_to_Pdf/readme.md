# 🖼️ Images to PDF

<p align="center">
  <img src="https://media1.tenor.com/m/-LHzJmfwj2kAAAAC/spongebob-too-easy.gif" alt="Images to PDF" width="800"/>
</p>

> Drop your images in. Get a PDF out. That's it. 📄

---

## 🎯 What it does

A minimal Python script that converts one or multiple image files into a single PDF. No extra software, no online tools — just run the script and your images are merged into a clean PDF instantly.

---

## 📁 Files

| File | Description |
| --- | --- |
| `IMAGE_TO_PDF.py` | 🚀 The entire tool — run this to convert images |

---

## ⚙️ How it works

1. **List your images** — Add your image file paths to the `images` list in the script
2. **Run the script** — It converts and combines them in order
3. **Output** — A file called `output.pdf` is created in the same directory

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 1/Images_to_pdf"
```

### 2. Install dependencies
```bash
pip install img2pdf
```

### 3. Add your images

Open `IMAGE_TO_PDF.py` and update the images list:
```python
images = ["image1.jpg", "image2.png", "image3.jpeg"]
```

### 4. Run the script
```bash
python IMAGE_TO_PDF.py
```

Your `output.pdf` will appear in the same folder. 🎉

---

## 📦 Requirements
```bash
pip install img2pdf
```

---

## 📝 Notes

- Supports `.jpg`, `.jpeg`, `.png`, and most common image formats
- Images are added to the PDF in the order they appear in the list
- Output is always saved as `output.pdf` — rename it as needed
- Make sure image paths are correct — use full paths if images are in a different folder

---

*"Screenshots se PDF — jugaar at its finest. 📎"*
