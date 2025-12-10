from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Swebsite:

    def __init__(self, url):
        
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )

        self.title = driver.find_element(By.TAG_NAME, "title").get_attribute("innerText")
        self.text = driver.execute_script("return document.body.innerText;").strip()

        with open("data.txt", "w", encoding="utf-8") as f:
            f.write(f"Page Title: {self.title}\n\n")
            f.write("=" * 80 + "\n")
            f.write(f"{self.text}")
            f.write("\n" + "=" * 8 + "\n")
            print("Page content saved successfully to data.txt!")
            print("\n" * 20)

        driver.quit()

