import requests
from bs4 import BeautifulSoup

url = "https://www.empireonline.com/movies/features/best-movies-2/"
response = requests.get(url).text
soup = BeautifulSoup(response, "html.parser")

h2_tags = soup.find_all("h2")
content = []

for tag in h2_tags:
    strong = tag.find("strong") # type: ignore
    if strong:
        content.append(strong.text) # type: ignore

movies = content[::-1]

with open("Maaaal.txt", "w", encoding="utf-8") as f:
    for movie in movies:
        write = f.write(f"{movie}\n")    
    
