import time

import selenium.webdriver as webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()

gmail_button = '.gb_W'


SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

def scrape_website_without_proxy(website):
    print("launching chrome browser")

    chrome_driver_path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("page was loaded")

        html = driver.find_element(By.CSS_SELECTOR, gmail_button).text
        print(html)

        driver.find_element(By.CSS_SELECTOR, '[name="q"]').send_keys('yes')
        driver.find_element(By.CSS_SELECTOR, '[name="q"]').send_keys(Keys.ENTER)
        driver.save_screenshot('screenshoot.png')

        time.sleep(2)




    finally:
        driver.quit()

scrape_website_without_proxy('https://google.com')