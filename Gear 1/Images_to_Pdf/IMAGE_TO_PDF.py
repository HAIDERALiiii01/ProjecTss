import img2pdf

# List of image file paths
images = ["your_image.extension"]

with open("output.pdf", "wb") as f:
    f.write(img2pdf.convert(images))
