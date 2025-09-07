from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.billboard.com/charts/hot-100/2021-08-14/")

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.o-chart-results-list__item"))
)

# Select chart item blocks
items = driver.find_elements(By.CSS_SELECTOR, "li.o-chart-results-list__item")

with open("data.txt", "w", encoding="utf-8") as f:
    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, "h3").text.strip()
            artist = item.find_element(By.CSS_SELECTOR, "span.c-label").text.strip()
            if title and artist and title.lower() != "hot 100":
                f.write(f"{title} {artist}\n")
        except:
            continue
