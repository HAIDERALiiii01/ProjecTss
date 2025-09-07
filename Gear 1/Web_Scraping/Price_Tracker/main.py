import requests
from bs4 import BeautifulSoup

url = "https://www.khazanay.pk/collections/men-sneakers-shoes/products/nike-blazer-mid-77-s-747853?variant=44524717441219"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

tag = soup.find("ins")
if tag is not None:
    price = tag.find(class_="money").get_text() # type: ignore
    money = int(price.replace("Rs.", "").replace(",", "").strip())


    if money < 5000:
        print("Budget m h jootay....chotayy")
    else:
        print("Paisay nhi h")
else:
    print("Price tag not found")
